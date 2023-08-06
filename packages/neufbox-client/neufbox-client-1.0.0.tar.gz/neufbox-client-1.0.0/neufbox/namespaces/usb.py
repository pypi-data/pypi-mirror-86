"""
USB namespace module
"""
from ._base import Namespace, GetMethod


class USB(Namespace):
    """
    USB API namespace definition
    """
    __namespace__ = 'usb'
    get_info = GetMethod('getInfo')
