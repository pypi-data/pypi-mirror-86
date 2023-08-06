"""
DDNS namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter, regexp


class DDNS(Namespace):
    """
    DDNS API namespace definition
    """
    __namespace__ = 'ddns'
    disable = PostMethod('disable')
    enable = PostMethod('enable')
    force_update = PostMethod('forceUpdate')
    get_info = GetMethod('getInfo')
    set_service = PostMethod('setService', parameters=[
        Parameter('service', regexp('dyndns|no-ip|ovh|dyndnsit|changeip|sitelutions')),
        Parameter('username'),
        Parameter('password'),
        Parameter('hostname')
    ])
