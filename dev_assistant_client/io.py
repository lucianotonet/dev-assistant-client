from ast import dump
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
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE, print_json
from dev_assistant_client.modules import file_management, version_control, shell_prompter
from time import sleep

logging.basicConfig(level=logging.ERROR)

MAX_RETRIES = 5  # Define a maximum number of retries


def execute_request(instruction):
    """Executes the request from the server"""
    for _ in range(MAX_RETRIES):
        now = datetime.datetime.now()
        print(
            str(now),
            "Executing instruction",
            sep="\t", end="\n")
        try:
            module = instruction.get('module')
            request = instruction.get('request')            

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
            print(
                str(now) + Style.RESET_ALL,
                Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL,
                e,
                sep="\t", end="\n")
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
                now = datetime.datetime.now()
                print(str(now),
                    "Marked as received",
                    sep="\t", end="\n")
                break
            else:
                print(
                    Fore.LIGHTRED_EX + str(now) + Style.RESET_ALL,
                    Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL,
                    response.status_code,
                    sep="\t", end="\n")
        except Exception as e:
            print(
                Fore.LIGHTRED_EX + str(now) + Style.RESET_ALL,
                Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL,
                e,
                sep="\t", end="\n")
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
        now = datetime.datetime.now()
        print(str(now), Fore.LIGHTGREEN_EX + "Sending response" + Style.RESET_ALL, sep="\t", end="\n")
        try:
            response = requests.put(url, data=response, headers=HEADERS)

            if response.status_code == 200:
                output = response.json()
                response = output.get('response')
                print(
                    tabulate(
                        [[json.dumps(response, indent=2)]],
                        headers=["Response"], tablefmt="fancy_grid"
                    ), sep="\t", end="\n")
                break
            else:
                print(str(now), Fore.LIGHTRED_EX + "Error" + response.status_code,
                      Style.RESET_ALL + response.json(), sep="\t", end="\n")
        except Exception as e:
            print(str(now), Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL, e,
                  sep="\t", end="\n")
            sleep(2)  # Add a delay before retrying
        else:
            return


async def ably_connect():
    """Connects to the Ably server and subscribes to the private channel"""
    auth_url = 'https://' + APP_URL + API_PATH + '/ably-auth'
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    try:
        HEADERS['Authorization'] = 'Bearer ' + token
        response = requests.post(auth_url, headers=HEADERS)
        token_request = response.json()
    except Exception as e:
        now = datetime.datetime.now()
        print(str(now), Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL, e,
              sep="\t", end="\n")
        return

    try:
        token_url = 'https://rest.ably.io/keys/' + \
            token_request['keyName'] + '/requestToken'
        response = requests.post(token_url, json=token_request)
        token = response.json()['token']
        realtime = AblyRealtime(token=token)
        now = datetime.datetime.now()
        print(str(now), "Connected to websocket server",
              sep="\t", end="\n")
    except Exception as e:
        now = datetime.datetime.now()
        print(str(now),
              Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL,
              e,
              sep="\t", end="\n")
        return

    privateChannel = realtime.channels.get('private:dev-assistant-'+DEVICE_ID)
    await privateChannel.subscribe(check_message)

    now = datetime.datetime.now()
    print(str(now),
          Fore.LIGHTGREEN_EX + "Ready!" + Style.RESET_ALL,
          "Waiting for instructions...",
          sep="\t", end="\n")

    while True:
        await asyncio.sleep(1)


def check_message(message):
    """Checks the message received from the server"""
    try:
        now = datetime.datetime.now()
        print(str(now),
              Fore.LIGHTGREEN_EX + "Receiving instruction" + Style.RESET_ALL,
              sep="\t", end="\n")
        print(tabulate(
            [[message.data.get('module'), message.data.get('request').get(
                'operation'), json.dumps(message.data.get('request').get('args'), indent=2)]],
            headers=["Module", "Operation", "Arguments"], tablefmt="fancy_grid"
        ), sep="\t", end="\n")
        inform_received(message.data)
        execute_request(message.data)
    except Exception as e:
        now = datetime.datetime.now()
        print(str(now), Fore.LIGHTRED_EX + "Error" + Style.RESET_ALL, e,
              sep="\t", end="\n")
        return
