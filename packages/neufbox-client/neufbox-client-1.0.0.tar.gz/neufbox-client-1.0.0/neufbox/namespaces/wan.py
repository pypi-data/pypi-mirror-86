"""
WAN namespace module
"""
from ._base import Namespace, GetMethod


class WAN(Namespace):
    """
    WAN API namespace definition
    """
    __namespace__ = 'wan'
    get_info = GetMethod('getInfo')
