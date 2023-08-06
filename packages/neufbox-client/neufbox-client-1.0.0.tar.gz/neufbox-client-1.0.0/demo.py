"""
Test script
"""
import os
from pprint import pprint
from dotenv import load_dotenv
from neufbox import Client, username_password


def main():
    """Main program"""
    load_dotenv()
    hostname = os.getenv('NEUFBOX_HOSTNAME')
    username = os.getenv('NEUFBOX_USERNAME')
    password = os.getenv('NEUFBOX_PASSWORD')

    client = Client(hostname)
    client.login(username_password(username, password))

    print('System info:')
    pprint(client.system.get_info())
    print()

    print('DSL info:')
    pprint(client.dsl.get_info())
    print()

    print('LAN info:')
    pprint(client.lan.get_info())
    print()

    print('WAN info:')
    pprint(client.wan.get_info())
    print()

    print('WLAN info:')
    pprint(client.wlan.get_info())
    print()


if __name__ == '__main__':
    main()
