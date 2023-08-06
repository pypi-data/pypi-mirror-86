"""
Client module
"""
import hashlib
import hmac
import requests
import xmltodict

from .namespaces import Auth, Backup3g, DDNS, DSL, Firewall, FTTH, Guest, Hotspot, \
    LAN, ONT, P910ND, PPP, SMB, System, TV, USB, VoIP, WAN, WLAN, WLAN5


class ClientError(Exception):
    """Neufbox API Error"""

    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


class Client:
    """Neufbox API client"""

    # namespaces
    auth = Auth.binding()
    backup3g = Backup3g.binding()
    ddns = DDNS.binding()
    dsl = DSL.binding()
    firewall = Firewall.binding()
    ftth = FTTH.binding()
    guest = Guest.binding()
    hotspot = Hotspot.binding()
    lan = LAN.binding()
    ont = ONT.binding()
    p910nd = P910ND.binding()
    ppp = PPP.binding()
    smb = SMB.binding()
    system = System.binding()
    tv = TV.binding()
    usb = USB.binding()
    voip = VoIP.binding()
    wan = WAN.binding()
    wlan = WLAN.binding()
    wlan5 = WLAN5.binding()

    def __init__(self, hostname):
        self.hostname = hostname
        self._session = requests.Session()
        self._token = None

    @property
    def api_url(self):
        """Return the API url"""
        return f'http://{self.hostname}/api/1.0'

    def login(self, auth_callback):
        """Login: this creates an authentication token that can be used to access
        the private methods. An authentication callback should be provided: it will
        be called with the requested authentication method (passwd / button / all),
        and should return either a username/password tuple (for password authentication),
        or None (for push-button authentication), after the user has taken action."""
        # ask for a token
        msg = self.auth.get_token()
        token = msg['token']
        method = msg['method']

        # prompt for username/password or wait until button pushed
        credentials = auth_callback(method)

        # compute hashed password if password provided
        hash_value = None
        if credentials:
            username, password = credentials
            username_hash = self._compute_hash(token, username)
            password_hash = self._compute_hash(token, password)
            hash_value = username_hash + password_hash

        # check authentication, which makes the token eventually valid
        result = self.auth.check_token(token=token, hash=hash_value)
        self._token = result['token']

    def logout(self):
        """Logout: forget the current token"""
        self._token = None

    def _method_params(self, method):
        params = {'method': method}
        if self._token:
            params['token'] = self._token
        return params

    def get(self, method, **parameters):
        """Perform a GET request with a fully qualified method name"""
        params = self._method_params(method)
        params.update(parameters)
        response = self._session.get(self.api_url, params=params)
        return self._process_response(response, method.endswith('List'))

    def post(self, method, **parameters):
        """Perform a POST request with a fully qualified method name"""
        params = self._method_params(method)
        response = self._session.post(self.api_url, params=params, data=parameters)
        return self._process_response(response)

    @staticmethod
    def _compute_hash(token, value):
        """Compute a password hash for a given token"""
        token_bytes = token.encode('ascii')
        value_bytes = value.encode('ascii')
        value_hash_bytes = hashlib.sha256(value_bytes).hexdigest().encode('ascii')
        return hmac.new(token_bytes, value_hash_bytes, hashlib.sha256).hexdigest()

    @staticmethod
    def _process_response(response, return_list=False):
        """Process the API response"""
        response.raise_for_status()

        data = xmltodict.parse(
            response.text,
            dict_constructor=dict,
            attr_prefix='',
            postprocessor=_value_postprocessor
        )['rsp']

        status = data.pop('stat')
        data.pop('version', None)
        if status == 'ok':
            # get the value of the remaining key, or None
            value = next(iter(data.values())) if data else None
            # convert to list if needed
            if return_list:
                value = _convert_to_list(value)
            return value

        error = data['err']
        raise ClientError(error['code'], error['msg'])


def _convert_to_list(value):
    """Convert a value to a list if it's not already a list"""
    if value is None:  # empty value
        return []
    if not isinstance(value, list):
        return [value]  # single value
    return value


def _value_postprocessor(_, key, value):
    """Post-process the string values parsed from the XML"""
    try:
        return key, int(value)
    except (ValueError, TypeError):
        return key, value
