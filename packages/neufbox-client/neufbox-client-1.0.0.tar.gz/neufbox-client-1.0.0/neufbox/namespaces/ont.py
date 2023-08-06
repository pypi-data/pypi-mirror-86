"""
ONT namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter


class ONT(Namespace):
    """
    ONT API namespace definition
    """
    __namespace__ = 'ont'
    get_info = GetMethod('getInfo')
    sync = PostMethod('sync')
    push = PostMethod('push', parameters=[
        Parameter('name'),
        Parameter('value'),
        Parameter('force', mandatory=False)
    ])
    pull = GetMethod('pull')
