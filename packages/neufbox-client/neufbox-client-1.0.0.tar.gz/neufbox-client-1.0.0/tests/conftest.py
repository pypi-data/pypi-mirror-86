"""
Fixtures for tests
"""
# pylint: disable=redefined-outer-name
import pytest
import pkg_resources
from neufbox import Client


@pytest.fixture
def client():
    """Return a client instance"""
    return Client('192.168.1.1')


def read_xml(filename):
    """Read a XML test file"""
    filepath = pkg_resources.resource_filename(__name__, filename)
    with open(filepath, 'r') as xml_file:
        return xml_file.read()


@pytest.fixture
def mock_get_request(client, requests_mock):
    """Mock a GET request to the API"""
    def func(url_query, xml_filename):
        return requests_mock.get(f'{client.api_url}{url_query}', text=read_xml(xml_filename))
    return func


@pytest.fixture
def mock_post_request(client, requests_mock):
    """Mock a POST request to the API"""
    def func(url_query):
        return requests_mock.post(f'{client.api_url}{url_query}', text=read_xml('empty.xml'))
    return func
