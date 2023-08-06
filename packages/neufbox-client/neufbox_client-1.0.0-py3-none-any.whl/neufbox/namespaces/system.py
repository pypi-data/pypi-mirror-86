"""
System namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter, regexp


class System(Namespace):
    """
    System API namespace definition
    """
    __namespace__ = 'system'
    get_info = GetMethod('getInfo')
    get_if_list = GetMethod('getIfList')
    get_wpa_key = GetMethod('getWpaKey')
    reboot = PostMethod('reboot')
    set_net_mode = PostMethod('setNetMode', parameters=[
        Parameter('mode', regexp('router|bridge'))
    ])
    set_ref_client = PostMethod('setRefClient', parameters=[
        Parameter('refclient')
    ])
