"""
WLAN5 namespace module
"""
from ._base import Namespace, GetMethod, PostMethod, Parameter, regexp


class WLAN5(Namespace):
    """
    WLAN5 API namespace definition
    """
    __namespace__ = 'wlan5'
    get_client_list = GetMethod('getClientList')
    get_info = GetMethod('getInfo')
    set_channel = PostMethod('setChannel', parameters=[
        Parameter('channel', regexp('auto|36|40|44|48|52|56|60|64|100|104|108|112|116|132|136|140'))
    ])
    set_wl0_enc = PostMethod('setWl0Enc', parameters=[
        Parameter('enc', regexp('OPEN|WPA-PSK|WPA2-PSK|WPA-WPA2-PSK'))
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
        Parameter('mode', regexp('11n|11ac|auto'))
    ])
