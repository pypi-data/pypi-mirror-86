# Neufbox API Client

[![Build Status][build_badge]][travis_link]
[![License][license_badge]][pypi_link]
[![Version][version_badge]][pypi_link]

This is a python API client library to interact with Neufbox NB4, NB5, NB6, NB6V, NB6VAC modem/routers sold by Neuf Telecom, SFR or Red by SFR companies.

See the [API specification][api_spec_link] for details about the API itself.


## Installation

To install the package:
```bash
pip install neufbox-client
```


## Getting started

Here is a simple example that retrieves the neufbox "system" information:
```python
from neufbox import Client, username_password
from pprint import pprint


client = Client('192.168.1.1')
system_info = client.system.get_info()
pprint(system_info)
```

We can also login to access private information from the neufbox. A ` username_password` helper is provided by the library, which sends the credentials (in hashed format) to validate the token received by the client from the neufbox (only if the neufbox allows username/password authentication):
```python
client.login(username_password('admin', 'p4ssw0rd'))
wlan_info = client.wlan.get_info()
pprint(wlan_info)
```

The client also allows changing some parameters of the neufbox by using the setters available in the different namespaces. See the [API specification][api_spec_link] for details.

You can also have a look on the [demo](./demo.py) file to see a working example.


## Support

This project is hosted on [Github][github_link]. Please report issues via the bug tracker.


[github_link]:   https://github.com/sprat/neufbox-client
[travis_link]:   https://travis-ci.com/sprat/neufbox-client
[pypi_link]:     https://pypi.org/project/neufbox-client
[api_spec_link]: https://lafibre.info/sfr-les-news/spec-api-rest-box-de-sfr/?action=dlattach;attach=85818

[build_badge]:   https://travis-ci.com/sprat/neufbox-client.svg?branch=master
[license_badge]: https://img.shields.io/pypi/l/neufbox-client
[version_badge]: https://img.shields.io/pypi/v/neufbox-client
