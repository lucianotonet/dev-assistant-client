import asyncio
import json
import sys
import logging
from colorama import Fore, Style
from tabulate import tabulate
import requests
from ably import AblyRealtime
from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE
from dev_assistant_client.modules import file_management, version_control, shell_prompter
from time import sleep

logging.basicConfig(level=logging.DEBUG)

MAX_RETRIES = 5  # Define a maximum number of retries


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def print_json(request):
    print(json.dumps(request, indent=4))


def execute_request(instruction):
    for _ in range(MAX_RETRIES):
        try:
            module = instruction.get('module')
            request = instruction.get('request')

            set_received(instruction)

            operation = request.get('operation')
            args = request.get('args')

            if module == 'files':
                response_data = file_management.execute(operation, args)
            elif module == 'git':
                response_data = version_control.execute(operation, args)
            elif module == 'terminal':
                response_data = shell_prompter.execute(operation, args)
            else:
                response_data = "Invalid module or operation"
            break
        except Exception as e:
            logging.error("Error: \t", e)
            print("Retrying...")
            sleep(1)  # Add a delay before retrying
        else:
            return

    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['Authorization'] = 'Bearer ' + token

    payload = json.dumps({
        'response': response_data
    })

    print("Task done!\t Sending response...")
    send_response(instruction, payload)


def set_received(instruction):
    """Just sets the instruction as received"""
    for _ in range(MAX_RETRIES):
        with open(TOKEN_FILE, "r") as f:
            token = f.readline()
        try:
            url = 'https://' + APP_URL + API_PATH + '/devices/' + \
                DEVICE_ID + '/io/'+instruction.get('id')
            HEADERS['Authorization'] = 'Bearer ' + token
            response = requests.put(url, headers=HEADERS)

            if response.status_code == 200:
                output = response.json()
                response = output.get('response')
                print(Fore.LIGHTGREEN_EX + "✔️" + Style.RESET_ALL)
                break
            else:
                print(Fore.LIGHTRED_EX +
                      "Failed to set as received!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Error:\t\t" + Style.RESET_ALL, e)
            print("Retrying...")
            sleep(1)  # Add a delay before retrying
        else:
            return


def send_response(instruction, response):
    """Sends the response to the server"""
    for _ in range(MAX_RETRIES):
        with open(TOKEN_FILE, "r") as f:
            token = f.readline()
        try:
            url = 'https://' + APP_URL + API_PATH + '/devices/' + \
                DEVICE_ID + '/io/'+instruction.get('id')
            HEADERS['Authorization'] = 'Bearer ' + token
            response = requests.put(url, data=response, headers=HEADERS)

            if response.status_code == 200:
                output = response.json()
                response = output.get('response')
                print(Fore.LIGHTGREEN_EX + "Sent:\n" + Style.RESET_ALL)
                print_json(response)
                break
            else:
                print(Fore.LIGHTRED_EX +
                      "Failed to send response!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Error:\t\t" + Style.RESET_ALL, e)
            print("Retrying...")
            sleep(1)  # Add a delay before retrying
        else:
            return


async def ably_connect():
    auth_url = 'https://' + APP_URL + API_PATH + '/ably-auth'
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    try:
        HEADERS['Authorization'] = 'Bearer ' + token
        response = requests.post(auth_url, headers=HEADERS)
        token_request = response.json()
    except Exception as e:
        logging.error("Error getting token request: ", e)
        return

    try:
        token_url = 'https://rest.ably.io/keys/' + \
            token_request['keyName'] + '/requestToken'
        response = requests.post(token_url, json=token_request)
        token = response.json()['token']
        realtime = AblyRealtime(token=token)
    except Exception as e:
        logging.error("Error connecting to Ably: ", e)
        return

    privateChannel = realtime.channels.get('private:dev-assistant-'+DEVICE_ID)
    await privateChannel.subscribe(check_message)
    print("Waiting for instructions...")

    while True:
        await asyncio.sleep(0.3)


async def check_message(message):
    try:
        execute_request(message.data)
    except:
        logging.error("Error sending response", sys.exc_info()[0])
        return
