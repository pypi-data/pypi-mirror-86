"""
Client tests
"""
# pylint: disable=protected-access,unused-argument
import pytest
from neufbox import ClientError, username_password


def test_compute_hash(client):
    """Check that the hash computation match the example given in the documentation"""
    result = client._compute_hash('43f6168e635b9a90774cc4d3212d5703c11c9302', 'admin')
    assert result == '7aa3e8b3ed7dfd7796800b4c4c67a0c56c5e4a66502155c17a7bcef5ae945ffa'


def test_api_url(client):
    """Check that the api url is properly computed"""
    assert client.api_url == 'http://192.168.1.1/api/1.0'


def test_get_single_result(client, mock_get_request):
    """Test that a method returning a single result returns a properly formatted dict"""
    mock = mock_get_request('?method=lan.getInfo', 'lan.getInfo.xml')

    result = client.lan.get_info()
    assert mock.called_once
    assert result == {
        'ip_addr': '192.168.1.1',
        'netmask': '255.255.255.0',
        'dhcp_active': 'on',
        'dhcp_start': '192.168.1.20',
        'dhcp_end': '192.168.1.100',
        'dhcp_lease': 86400
    }


def test_get_empty_list_result(client, mock_get_request):
    """Test that a method returning a list can return an empty list"""
    mock_get_request('?method=lan.getDnsHostList', 'lan.getDnsHostList_empty.xml')
    result = client.lan.get_dns_host_list()
    assert result == []


def test_get_single_item_list_result(client, mock_get_request):
    """Test that a method returning a list can return an empty list"""
    mock_get_request('?method=lan.getDnsHostList', 'lan.getDnsHostList_1item.xml')
    result = client.lan.get_dns_host_list()
    assert result == [
        {
            'ip': '192.168.1.10',
            'name': 'host1.lan'
        }
    ]


def test_get_two_items_list_result(client, mock_get_request):
    """Test that a method returning a list can return an empty list"""
    mock_get_request('?method=lan.getDnsHostList', 'lan.getDnsHostList_2items.xml')
    result = client.lan.get_dns_host_list()
    assert result == [
        {
            'ip': '192.168.1.10',
            'name': 'host1.lan'
        },
        {
            'ip': '192.168.1.11',
            'name': 'host2.lan'
        }
    ]


def test_login_success_with_passwd(client, mock_get_request, mock_post_request):
    """Check that we can login if the username/password are correct"""
    get_token_mock = mock_get_request('?method=auth.getToken', 'auth.getToken_passwd.xml')
    check_mock = mock_get_request('?method=auth.checkToken', 'auth.checkToken_ok.xml')

    client.login(username_password('admin', 'password'))
    assert 'token' not in get_token_mock.last_request.qs

    # check that the hash value sent to the API is correct
    hash_value = check_mock.last_request.qs['hash'][0]
    assert hash_value == (
        '2df1e5ddeba2c14262e594c62effd0ecf80ff09a02d223c381487e4a5851302f'
        '0a4d44947b410abbec4ab1da8b6de783d10f8284fcf528ae7c91c4b8ffd91fc5'
    )

    # check that the token is passed in the next request
    add_dns_host_mock = mock_post_request('?method=lan.addDnsHost')
    client.lan.add_dns_host(name='host.lan', ip='192.168.1.25')
    assert add_dns_host_mock.called_once
    assert add_dns_host_mock.last_request.qs['token'][0] == 'fe5be7az1v9cb45zeogger8b4re145g3'

    # logout
    client.logout()

    # check that the token is not passed anymore
    client.lan.add_dns_host(name='host.lan', ip='192.168.1.25')
    assert 'token' not in add_dns_host_mock.last_request.qs


def test_login_failure_invalid_password(client, mock_get_request):
    """Check that we cannot login if the username/password are incorrect"""
    mock_get_request('?method=auth.getToken', 'auth.getToken_passwd.xml')
    mock_get_request('?method=auth.checkToken', 'auth.checkToken_invalid_login_password.xml')

    with pytest.raises(ClientError) as error:
        client.login(username_password('admin', 'password'))

    assert client._token is None
    assert error.value.code == 204
    assert str(error.value) == 'Invalid login and/or password'


def test_login_failure_with_login_password_in_button_method(client, mock_get_request):
    """Check that we cannot login with username/password if the method is 'button'"""
    mock_get_request('?method=auth.getToken', 'auth.getToken_button.xml')

    with pytest.raises(RuntimeError):
        client.login(username_password('admin', 'password'))


def test_missing_parameter(client):
    """Check that an error is raised when a parameter is missing"""
    with pytest.raises(TypeError):
        client.wlan.set_wl0_enc()


def test_invalid_parameter_name(client):
    """Check that an error is raised when an invalid parameter is used"""
    with pytest.raises(TypeError):
        client.wlan.set_wl0_enc(invalid='value')


def test_invalid_parameter_value(client):
    """Check that an error is raised when an invalid value is provided in a parameter"""
    with pytest.raises(ValueError):
        client.wlan.set_wl0_enc(enc='invalid')


def test_valid_string_parameter_value(client, mock_post_request):
    """Check that the method is called when a valid string parameter value is provided """
    mock = mock_post_request('?method=wlan.setWl0Enc')
    client.wlan.set_wl0_enc(enc='WPA2-PSK')
    assert mock.called_once


def test_valid_int_parameter_value(client, mock_post_request):
    """Check that integer parameters are converted to string and method is called"""
    mock = mock_post_request('?method=wlan.setChannel')
    client.wlan.set_channel(channel=12)
    assert mock.last_request.text == 'channel=12'


def test_missing_optional_parameter(client, mock_post_request):
    """Check that no error is raised when an optional parameter is not passed"""
    mock = mock_post_request('?method=ont.push')
    client.ont.push(name='slid', value='1234')
    assert mock.called_once


def test_ip_validation_failure(client, mock_post_request):
    """Check that the ip validation works"""
    with pytest.raises(ValueError):
        client.lan.add_dns_host(name='host.lan', ip='192.168.1.256')
