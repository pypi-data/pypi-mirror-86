"""
VoIP namespace module
"""
from ._base import Namespace, GetMethod, PostMethod


class VoIP(Namespace):
    """
    VoIP API namespace definition
    """
    __namespace__ = 'voip'
    get_call_history_list = GetMethod('getCallhistoryList')
    get_info = GetMethod('getInfo')
    restart = PostMethod('restart')
    start = PostMethod('start')
    stop = PostMethod('stop')
