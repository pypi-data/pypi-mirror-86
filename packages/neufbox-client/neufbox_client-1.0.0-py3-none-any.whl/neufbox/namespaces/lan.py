"""
LAN namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter, ip_address


class LAN(Namespace):
    """
    LAN API namespace definition
    """
    __namespace__ = 'lan'
    add_dns_host = PostMethod('addDnsHost', parameters=[
        Parameter('ip', ip_address),
        Parameter('name')
    ])
    delete_dns_host = PostMethod('deleteDnsHost', parameters=[
        Parameter('ip', ip_address),
        Parameter('name')
    ])
    get_dns_host_list = GetMethod('getDnsHostList')
    get_hosts_list = GetMethod('getHostsList')
    get_info = GetMethod('getInfo')
