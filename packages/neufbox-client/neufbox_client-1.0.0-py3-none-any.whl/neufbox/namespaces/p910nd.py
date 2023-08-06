"""
P910ND namespace module
"""
from ._base import Namespace, GetMethod


class P910ND(Namespace):
    """
    P910ND API namespace definition
    """
    __namespace__ = 'p910nd'
    get_info = GetMethod('getInfo')
