import asyncio
import json
import logging
from time import sleep
from colorama import Back

import requests
from ably import AblyRealtime
from pygments import highlight, lexers, formatters
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic
from tabulate import tabulate

from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.modules import files, git, terminal
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE

MAX_RETRIES = 5

def print_data(data, headers):
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"), end="\n")


def colorize(content: str, lexer) -> str:
    if content is not None:
        content = highlight(content.strip(), lexer, formatters.TerminalFormatter(bg='dark'))

    return content

def execute_request(instruction):
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
            sleep(0.3)
        else:
            return

    token = read_token()
    HEADERS['Authorization'] = 'Bearer ' + token

    payload = json.dumps({
        'response': response_data
    })

    send_response(instruction, payload)
    
def inform_received(instruction):
    for _ in range(MAX_RETRIES):
        token = read_token()
        try:
            url = f'https://{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
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
            sleep(0.5)
        else:
            return

def send_response(instruction, response):
    token = read_token()
    url = f'https://{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
    HEADERS['Authorization'] = 'Bearer ' + token

    for _ in range(MAX_RETRIES):
        try:
            response = requests.put(url, data=response, headers=HEADERS)
            response.raise_for_status()

            output = response.json()
            content = output.get('response', {}).get('content') or output.get('response', {}).get('message') or response.content
            path = instruction.get('request', {}).get('args', {}).get('path')
            lexer = lexers.get_lexer_for_filename(path) if path else lexers.JsonLexer()
            content = colorize(content, lexer)

            logging.info("Sending response")
            print_data([[content]], ["Response"])
            break
        except requests.exceptions.HTTPError as e:
            logging.error("HTTP error:", e)
            break
        except Exception as e:
            logging.error("Error:", e)
            sleep(1)

async def ably_connect():
    logging.info("Initiating WebSocket connection...")
    auth_url = f'https://{APP_URL}{API_PATH}/ably-auth'
    token = read_token()

    try:
        HEADERS['Authorization'] = 'Bearer ' + token
        response = requests.post(auth_url, headers=HEADERS)
        token_request = response.json()
    except Exception as e:
        logging.error("Error", e)
        return

    try:
        token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
        response = requests.post(token_url, json=token_request)
        token = response.json()['token']
        realtime = AblyRealtime(token=token)
        logging.info("WebSocket connection established")
    except Exception as e:
        logging.error("Websocket error:", e)
        return

    privateChannel = realtime.channels.get(
        f'private:dev-assistant-{DEVICE_ID}')
    await privateChannel.subscribe(check_message)

    logging.info("Ready!", "Waiting for instructions...")

    while True:
        await asyncio.sleep(1)
        
def check_message(message):
    try:
        logging.info("Receiving instruction")
        args = json.dumps(message.data.get('request').get('args'), indent=2)
        path = message.data.get('request').get('args').get('path')
        lexer = lexers.get_lexer_for_filename(path) if path else lexers.JsonLexer()
        args = colorize(args, lexer)
        print_data(
            [[message.data.get('module'), message.data.get('request').get(
                'operation'), args]],
            ["Module", "Operation", "Arguments"])
        inform_received(message.data)
        execute_request(message.data)
    except Exception as e:
        logging.error("Error", e)
        
def read_token():
    with open(TOKEN_FILE, 'r') as file:
        token = file.read()
    return token