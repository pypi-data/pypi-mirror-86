"""
Firewall namespace module
"""
from ._base import Namespace, GetMethod, PostMethod


class Firewall(Namespace):
    """
    Firewall API namespace definition
    """
    __namespace__ = 'firewall'
    enable_smtp_filter = PostMethod('enableSmtpFilter')
    disable_smtp_filter = PostMethod('disableSmtpFilter')
    get_info = GetMethod('getInfo')
