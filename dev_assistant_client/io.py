import asyncio
import datetime
import json
import sys
import logging
from colorama import Fore, Style
from tabulate import tabulate
import requests
from ably import AblyRealtime
from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE, now, print_json
from dev_assistant_client.modules import files, git, terminal
from time import sleep


MAX_RETRIES = 5  # Define a maximum number of retries


def execute_request(instruction):
    """Executes the request from the server"""
    for _ in range(MAX_RETRIES):

        logging.info("Executing instruction")
        try:
            module = instruction.get('module')
            request = instruction.get('request')

            operation = request.get('operation')
            args = request.get('args')

            if module == 'files':
                response_data = files.execute(operation, args)
            elif module == 'git':
                response_data = git.execute(operation, args)
            elif module == 'terminal':
                response_data = terminal.execute(operation, args)
            else:
                response_data = "Invalid module or operation"
            break
        except Exception as e:
            logging.error("Error", e)
            sleep(1)  # Add a delay before retrying
        else:
            return

    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['Authorization'] = 'Bearer ' + token

    payload = json.dumps({
        'response': response_data
    })

    send_response(instruction, payload)


def inform_received(instruction):
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

                logging.info("Marked as received")
                break
            else:
                logging.error("Error", response.status_code,
                      response.json())
        except Exception as e:
            logging.error("Error", e)
            sleep(2)  # Add a delay before retrying
        else:
            return


def send_response(instruction, response):
    """Sends the response to the server"""
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()
    url = 'https://' + APP_URL + API_PATH + '/devices/' + \
        DEVICE_ID + '/io/'+instruction.get('id')
    HEADERS['Authorization'] = 'Bearer ' + token

    for _ in range(MAX_RETRIES):

        try:
            response = requests.put(url, data=response, headers=HEADERS)

            if response.status_code == 200:
                output = response.json()
                response = output.get('response')
                logging.info(Fore.LIGHTGREEN_EX +
                      "Sending response" + Style.RESET_ALL)
                print(tabulate(
                    [[json.dumps(response, indent=2)]],
                    headers=["Response"], tablefmt="fancy_grid"
                ), end="\n")
                break
            else:
                logging.error("Error", response.status_code)
        except Exception as e:
            logging.error("Error", e)
            sleep(2)  # Add a delay before retrying
        else:
            return


async def ably_connect():
    """Connects to the Ably server and subscribes to the private channel"""
    logging.info("Initiating WebSocket connection...")
    auth_url = 'https://' + APP_URL + API_PATH + '/ably-auth'
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    try:
        HEADERS['Authorization'] = 'Bearer ' + token
        response = requests.post(auth_url, headers=HEADERS)
        token_request = response.json()
    except Exception as e:
        logging.error("Error", e)
        return

    try:
        token_url = 'https://rest.ably.io/keys/' + \
            token_request['keyName'] + '/requestToken'
        response = requests.post(token_url, json=token_request)
        token = response.json()['token']
        realtime = AblyRealtime(token=token)
        logging.info("WebSocket connection established")
    except Exception as e:
        logging.error("Websocket error:", Fore.LIGHTYELLOW_EX + e + Style.RESET_ALL)
        return

    privateChannel = realtime.channels.get('private:dev-assistant-'+DEVICE_ID)
    await privateChannel.subscribe(check_message)

    logging.info("Ready!", "Waiting for instructions...")

    while True:
        await asyncio.sleep(1)


def check_message(message):
    """Checks the message received from the server"""
    try:
        logging.info(Fore.LIGHTGREEN_EX +
              "Receiving instruction" + Style.RESET_ALL)
        print(tabulate(
            [[message.data.get('module'), message.data.get('request').get(
                'operation'), json.dumps(message.data.get('request').get('args'), indent=2)]],
            headers=["Module", "Operation", "Arguments"], tablefmt="fancy_grid"
        ), end="\n")
        inform_received(message.data)
        execute_request(message.data)
    except Exception as e:
        logging.error("Error", e)
        return