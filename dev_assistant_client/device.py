import logging
import os
import sys
from pusherclient import Pusher
import getpass
import http.client
import json
import platform
import socket
import time
import uuid
import re
from colorama import Fore, Style
from dev_assistant_client.utils import TOKEN_FILE, APP_URL, API_PATH, PUSHER_APP_KEY, PUSHER_APP_SECRET, PUSHER_APP_ID


def get_device_id():
    try:
        with open('.device_id', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


DEVICE_ID = get_device_id()


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


def connect():
    with open(TOKEN_FILE, "r") as f:
        token = f.read()

    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    payload = create_device_payload()

    print("Connecting to the server...")

    conn = http.client.HTTPSConnection(APP_URL)
    conn.request("POST", API_PATH + '/devices/connect',
                 body=payload, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        print(Fore.LIGHTGREEN_EX + "Successfully connected!" + Style.RESET_ALL)
        response_body = response.read().decode()
        # print("Server response: ", response_body)
        device_data = json.loads(response_body)
        with open('.device_id', 'w') as f:
            f.write(device_data['id'])
        connect_to_pusher()
    else:
        if response.status == 401:
            print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL)
            print("Error: ", response.read().decode())
            print("Please log in again.")
            os.remove(TOKEN_FILE)
        else:
            print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL)
            print("Response: ", response.read().decode())
            print("Status code: ", response.status)


def connect_to_pusher():
    # Add a logging handler so we can see the raw communication data
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    root.addHandler(ch)

    global pusher

    # We can't subscribe until we've connected, so we use a callback handler
    # to subscribe when able
    def connect_handler(data):
        channel = pusher.subscribe('dev-assistant')
        channel.bind('my-event', callback)

    pusher = Pusher(key=PUSHER_APP_KEY, secret=PUSHER_APP_SECRET,
                    secure=True, log_level=logging.INFO)
    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

    while True:
        time.sleep(1)


def callback(data):
    print('Received event with data: %s' % data)
