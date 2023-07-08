import asyncio
import os
import getpass
import http.client
import json
import platform
import socket
import uuid
import re
import ably
from colorama import Fore, Style
from dev_assistant_client.utils import CERT_FILE, KEY_FILE, TOKEN_FILE, APP_URL, API_PATH, DEVICE_ID
from dev_assistant_client.modules import file_management, version_control, shell_prompter

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

    print("Connecting...")

    CONN.request("POST", API_PATH + '/devices', body=payload, headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        response_body = response.read().decode()
        # print("Server response: ", response_body)
        device_data = json.loads(response_body)
        print(Fore.LIGHTGREEN_EX + "Connected!" + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + "Device ID: " +
              Style.RESET_ALL, device_data['id'])
        with open('.device_id', 'w') as f:
            f.write(device_data['id'])
        # connect_to_pusher()
        await connect_to_ably()
    else:
        print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL)
        if response.status == 401:
            print("Error: ", response.read().decode())
            print("Please log in again.")
            os.remove(TOKEN_FILE)
        else:
            print("Response: ", response.read().decode())
            print("Status code: ", response.status)


def send_response(data):
    print(Fore.LIGHTYELLOW_EX + "Received command: " +
          Style.RESET_ALL, data.get('id'))

    # Extract the module, operation and arguments from the command data
    module = data.get('module')
    operation = data.get('operation')
    args = data.get('args')

    # Execute the appropriate function based on the module and operation
    if module == 'file_management':
        response_data = file_management.execute(operation, args)
    elif module == 'version_control':
        response_data = version_control.execute(operation, args)
    elif module == 'shell_prompter':
        response_data = shell_prompter.execute(operation, args)
    else:
        response_data = {'error': f'Unknown module: {module}'}

    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['Authorization'] = 'Bearer ' + token

    payload = json.dumps({
        'response': response_data  # Send the actual response data
    })

    CONN.request("PUT", API_PATH + '/devices/' + DEVICE_ID +
                 '/io/'+data.get('id'), body=payload, headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        print(Fore.LIGHTGREEN_EX + "Response sent!" + Style.RESET_ALL)
    else:
        print(Fore.LIGHTRED_EX + "Failed to send response!" + Style.RESET_ALL)


async def connect_to_ably():
    auth_url = 'https://' + APP_URL + API_PATH + '/devices/' + DEVICE_ID + '/ably-token-request'
    realtime = ably.AblyRealtime(auth_url=auth_url)
    
    client = realtime
    privateChannel = client.channels.get('private:device.' + DEVICE_ID)
    print("Connected to Ably!", privateChannel.name)

    def listener(message):
        send_response(message.data)

    await privateChannel.subscribe(listener)

    while True:
        await asyncio.sleep(1)
