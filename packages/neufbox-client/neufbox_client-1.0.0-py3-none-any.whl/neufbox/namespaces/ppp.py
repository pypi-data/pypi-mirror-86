"""
PPP namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter


class PPP(Namespace):
    """
    PPP API namespace definition
    """
    __namespace__ = 'ppp'
    get_credentials = GetMethod('getCredentials')
    get_info = GetMethod('getInfo')
    set_credentials = PostMethod('setCredentials', parameters=[
        Parameter('login'),
        Parameter('password')
    ])
