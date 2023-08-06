"""
DSL namespace module
"""
from ._base import Namespace, GetMethod


class DSL(Namespace):
    """
    DSL API namespace definition
    """
    __namespace__ = 'dsl'
    get_info = GetMethod('getInfo')
