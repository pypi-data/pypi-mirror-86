"""
Backup3g namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter, regexp


class Backup3g(Namespace):
    """
    Backup3g API namespace definition
    """
    __namespace__ = 'backup3g'
    force_data_link = PostMethod('forceDataLink', parameters=[
        Parameter('mode', regexp('on|off|auto'))
    ])
    force_voip_link = PostMethod('forceVoipLink', parameters=[
        Parameter('mode', regexp('on|off'))
    ])
    get_pin_code = GetMethod('getPinCode')
    set_pin_code = PostMethod('setPinCode', parameters=[
        Parameter('pincode', regexp('[0-9]{4,8}'))
    ])
