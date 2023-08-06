"""
SMB namespace module
"""
from ._base import Namespace, GetMethod


class SMB(Namespace):
    """
    SMB API namespace definition
    """
    __namespace__ = 'smb'
    get_info = GetMethod('getInfo')
