import asyncio
import json
import sys
from colorama import Fore, Style
import requests
from ably import AblyRealtime
from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE
from dev_assistant_client.modules import file_management, version_control, shell_prompter


def execute_request(instruction):
    try:
        module = instruction.get('module')
        request = instruction.get('request')
        
        print(Fore.LIGHTYELLOW_EX + "\nInstruction:\t" +
              Style.RESET_ALL, request)

        # Extract the module, operation and arguments from the command request
        print(Fore.LIGHTYELLOW_EX + "Module:\t" + Style.RESET_ALL, module)
        operation = request.get('operation')
        print(Fore.LIGHTYELLOW_EX + "Operation:\t" + Style.RESET_ALL, operation)
        args = request.get('args')
        print(Fore.LIGHTYELLOW_EX + "Args:\t" + Style.RESET_ALL, args)

        # Execute the appropriate function based on the module and operation
        if module == 'files':
            response_data = file_management.execute(operation, args)
        elif module == 'git':
            response_data = version_control.execute(operation, args)
        elif module == 'terminal':
            response_data = shell_prompter.execute(operation, args)
        else:
            response_data = "Invalid module or operation"
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Error: \t" + Style.RESET_ALL, e)
        print("Retrying...")
        execute_request(instruction)

    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['Authorization'] = 'Bearer ' + token

    payload = json.dumps({
        'response': response_data  # Send the actual response data
    })

    send_response(instruction, payload)


def send_response(instruction, response):
    try:
        CONN.request("PUT", API_PATH + '/devices/' + DEVICE_ID +
                     '/io/'+instruction.get('id'), body=response, headers=HEADERS)
        response = CONN.getresponse()

        if response.status == 200:
            output = json.loads(response.read().decode())
            print(Fore.LIGHTGREEN_EX + "Response:\t" +
                  Style.RESET_ALL, output.get('response'))
        else:
            print(Fore.LIGHTRED_EX + "Failed to send response!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Error on save: \t" + Style.RESET_ALL, e)
        print("Retrying...")
        send_response(instruction, response)


async def ably_connect():
    auth_url = 'https://' + APP_URL + API_PATH + '/ably-auth'
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    try:
        HEADERS['Authorization'] = 'Bearer ' + token
        response = requests.post(auth_url, headers=HEADERS)
        token_request = response.json()
    except Exception as e:
        print("Error getting token request: ", e)
        return

    try:
        token_url = 'https://rest.ably.io/keys/' + \
            token_request['keyName'] + '/requestToken'
        response = requests.post(token_url, json=token_request)
        token = response.json()['token']
        realtime = AblyRealtime(token=token)
    except Exception as e:
        print("Error connecting to Ably: ", e)
        return

    # Inscreva-se em um canal privado
    privateChannel = realtime.channels.get('private:dev-assistant-'+DEVICE_ID)
    await privateChannel.subscribe(check_message)
    print("Waiting for instructions...")

    while True:
        await asyncio.sleep(0.3)


async def check_message(message):
    try:
        execute_request(message.data)
    except:
        print("Error sending response" + Style.RESET_ALL, sys.exc_info()[0])
        return


def connect_to_pusher():
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()
    HEADERS['Authorization'] = 'Bearer ' + token

    response = requests.get('https://' + APP_URL +
                            API_PATH + '/pusher-auth', headers=HEADERS)
    response.raise_for_status()
    auth_info = response.json()
    print("Auth info: ", auth_info)
