"""
Neufbox Client root module
"""
import pkg_resources
from .client import Client, ClientError
from .auth import username_password


__all__ = ['Client', 'ClientError', 'username_password']
__version__ = pkg_resources.get_distribution('neufbox-client').version
