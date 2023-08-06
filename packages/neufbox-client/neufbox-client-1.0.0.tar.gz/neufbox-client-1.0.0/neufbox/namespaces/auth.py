"""
Auth namespace module
"""
from ._base import Namespace, GetMethod, Parameter


class Auth(Namespace):
    """
    Auth API namespace definition
    """
    __namespace__ = 'auth'
    get_token = GetMethod('getToken')
    check_token = GetMethod('checkToken', parameters=[
        Parameter('token'),
        Parameter('hash')
    ])
