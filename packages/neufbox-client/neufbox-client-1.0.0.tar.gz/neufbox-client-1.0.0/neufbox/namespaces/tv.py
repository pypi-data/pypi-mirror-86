"""
TV namespace module
"""
from ._base import Namespace, GetMethod


class TV(Namespace):
    """
    TV API namespace definition
    """
    __namespace__ = 'tv'
    get_info = GetMethod('getInfo')
