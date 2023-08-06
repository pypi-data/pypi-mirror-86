"""
Namespace base module
"""
from abc import ABC
import ipaddress
from functools import partial
import re


class Namespace(ABC):
    """
    API namespace definition. Should be subclassed to define concrete namespaces
    """
    __namespace__ = ''

    def __init__(self, client):
        self.client = client

    @classmethod
    def binding(cls):
        """Returns a descriptor that creates the namespace instance when the property is accessed"""
        return _Binding(cls)


class Method(ABC):
    """
    Abstract API method definition
    """

    _client_method = ''

    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = {
            param.name: param
            for param in (parameters or [])
        }

    def _call(self, namespace, **parameters):
        parameters_values = self._validate_parameters(parameters)
        qualified_name = f'{namespace.__namespace__}.{self.name}'
        client_method = getattr(namespace.client, self._client_method)
        return client_method(qualified_name, **parameters_values)

    def _validate_parameters(self, parameters):
        values = {}

        # check that the parameters values are valid
        for name, value in parameters.items():
            param = self.parameters.get(name)
            if param is None:
                raise TypeError(f'Unexpected parameter {name}')
            values[name] = param.validate(value)

        # check that all the mandatory parameters are present
        for param in self.parameters.values():
            if param.mandatory and not param.name in values:
                raise TypeError(f'Missing parameter {param.name}')

        return values

    def __get__(self, namespace, objtype = None):
        return partial(self._call, namespace)


class GetMethod(Method):
    """API GET method definition"""

    _client_method = 'get'


class PostMethod(Method):
    """API POST method definition"""

    _client_method = 'post'


class Parameter:
    """Parameter of a Method"""

    def __init__(self, name, validate=str, mandatory=True):
        self.name = name
        self.validate = validate
        self.mandatory = mandatory


def regexp(expr):
    """Validate that the value match the provided regexp"""
    regex = re.compile(f'^({expr})$')
    def validate(value):
        value = str(value)
        if not regex.match(value):
            raise ValueError(f'{value} is not a valid value for this parameter')
        return value
    return validate


def ip_address(value):
    """Validate that the value is an IP address"""
    value = str(value)
    ipaddress.ip_address(value)
    return value


class _Binding:
    """
    Creates a Namespace instance when the associated property is accessed on the Client instance
    """
    def __init__(self, namespace_factory):
        self.namespace_factory = namespace_factory

    def __get__(self, client, client_type=None):
        return self.namespace_factory(client)
