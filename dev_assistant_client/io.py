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


logging.basicConfig(level=logging.INFO)


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
    logging.info(json.dumps(request, indent=4))


def execute_request(instruction):
    try:
        module = instruction.get('module')
        request = instruction.get('request')

        print_json(request)

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
    except Exception as e:
        logging.error("Error: \t", e)
        logging.info("Retrying...")
        return

    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['Authorization'] = 'Bearer ' + token

    payload = json.dumps({
        'response': response_data
    })

    logging.info("Task done!\t Sending response...")
    send_response(instruction, payload)


def send_response(instruction, response):
    try:
        CONN.request("PUT", API_PATH + '/devices/' + DEVICE_ID +
                     '/io/'+instruction.get('id'), body=response, headers=HEADERS)
        response = CONN.getresponse()

        if response.status == 200:
            output = json.loads(response.read().decode())
            response = output.get('response')
            logging.info("Sent:\n")
            print_json(response)
        else:
            logging.error("Failed to send response!")
    except Exception as e:
        logging.error("Error:\t\t", e)
        logging.info("Retrying...")
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
    logging.info("Waiting for instructions...")

    while True:
        await asyncio.sleep(0.3)


async def check_message(message):
    try:
        execute_request(message.data)
    except:
        logging.error("Error sending response", sys.exc_info()[0])
        return


def connect_to_pusher():
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()
    HEADERS['Authorization'] = 'Bearer ' + token

    response = requests.get('https://' + APP_URL +
                            API_PATH + '/pusher-auth', headers=HEADERS)
    response.raise_for_status()
    auth_info = response.json()
    logging.info("Auth info: ", auth_info)