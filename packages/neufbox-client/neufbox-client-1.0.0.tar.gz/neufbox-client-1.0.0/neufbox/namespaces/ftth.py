"""
FTTH namespace module
"""
from ._base import Namespace, GetMethod


class FTTH(Namespace):
    """
    FTTH API namespace definition
    """
    __namespace__ = 'ftth'
    get_info = GetMethod('getInfo')
