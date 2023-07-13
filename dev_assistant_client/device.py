import os
import getpass
import http.client
import json
import platform
import socket
import uuid
import re
from colorama import Fore, Style
from dev_assistant_client.utils import CERT_FILE, DEVICE_ID_FILE, KEY_FILE, TOKEN_FILE, APP_URL, API_PATH, DEVICE_ID, now
from dev_assistant_client.io import ably_connect


def create_device_payload():
    return json.dumps({
        'id': DEVICE_ID or '',
        'name': socket.gethostname(),
        'type': 'desktop',
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'mac_address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
        'os': platform.system(),
        'os_version': platform.release(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'username': getpass.getuser(),
    }, indent=4)


CONN = http.client.HTTPSConnection(
    APP_URL, cert_file=CERT_FILE, key_file=KEY_FILE)
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


async def connect():
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['Authorization'] = 'Bearer ' + token

    payload = create_device_payload()

    print(now(), "Connecting...", sep="\t")

    CONN.request("POST", API_PATH + '/devices', body=payload, headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        response_body = response.read().decode()
        device_data = json.loads(response_body)
        print(now(), "Connected.",  "Device ID " + Fore.LIGHTYELLOW_EX +
                     device_data['id'] + Style.RESET_ALL, sep="\t")
        with open(DEVICE_ID_FILE, 'w') as f:
            f.write(device_data['id'])
        # Connect to Ably
        await ably_connect()
    else:
        print(now(), "Failed to connect!", sep="\t")
        if response.status == 401:
            print(now(), "Error: ", response.read().decode(), sep="\t")
            print(now(), "Please do login again.", sep="\t")
            os.remove(TOKEN_FILE)
        else:
            print(now(), "Response: ", response.read().decode(), sep="\t")
            print(now(), "Status code: ", response.status, sep="\t")
