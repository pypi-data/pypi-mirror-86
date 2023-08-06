"""
WLAN namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter, regexp


class WLAN(Namespace):
    """
    WLAN API namespace definition
    """
    __namespace__ = 'wlan'
    enable = PostMethod('enable')
    disable = PostMethod('disable')
    get_client_list = GetMethod('getClientList')
    get_info = GetMethod('getInfo')
    get_scan_list = GetMethod('getScanList')
    set_channel = PostMethod('setChannel', parameters=[
        Parameter('channel', regexp('[1-9]|1[0-3]'))
    ])
    set_wl0_enc = PostMethod('setWl0Enc', parameters=[
        Parameter('enc', regexp('OPEN|WEP|WPA-PSK|WPA2-PSK|WPA-WPA2-PSK'))
    ])
    set_wl0_enc_type = PostMethod('setWl0Enctype', parameters=[
        Parameter('enctype', regexp('tkip|aes|tkipaes'))
    ])
    set_wl0_key_type = PostMethod('setWl0Keytype', parameters=[
        Parameter('keytype', regexp('ascii|hexa'))
    ])
    set_wl0_ssid = PostMethod('setWl0Ssid', parameters=[
        Parameter('ssid')
    ])
    set_wl0_wep_key = PostMethod('setWl0Wepkey', parameters=[
        Parameter('wepkey')
    ])
    set_wl0_wpa_key = PostMethod('setWl0Wpakey', parameters=[
        Parameter('wpakey')
    ])
    set_wlan_mode = PostMethod('setWlanMode', parameters=[
        Parameter('mode', regexp('11n|11ng|11g|11b|auto'))  # depend on the box hardware
    ])
    start = PostMethod('start')
    stop = PostMethod('stop')
    restart = PostMethod('restart')
