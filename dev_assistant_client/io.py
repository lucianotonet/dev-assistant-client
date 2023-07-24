import asyncio
import json
import logging
from time import sleep
from colorama import Back, Fore, Style

import requests
from ably import AblyRealtime
from pygments import highlight, lexers, formatters
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic
from tabulate import tabulate

from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.modules import files, git_module, terminal
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE, now, change_icon_color, blue_icon, yellow_icon, green_icon

MAX_RETRIES = 5


def colorize(content: str, lexer) -> str:
    if content is not None:
        content = highlight(content.strip(), lexer,
                            formatters.TerminalFormatter(bg='dark'))

    return content


def execute_request(instruction):
    print(now(), Fore.LIGHTYELLOW_EX + "Executing task ... " +
          Style.RESET_ALL, sep='\t', end='\t')
    change_icon_color(blue_icon)

    response = ""
    module = instruction.get('module').lower()  # convert to lowercase
    request = instruction.get('request')

    operation = request.get('operation')
    args = request.get('args')

    for _ in range(MAX_RETRIES):
        try:
            if module == 'files':
                response = files.execute(operation, args)
            elif module == 'git':
                response = git_module.execute(operation, args)
            elif module == 'terminal':
                response = terminal.execute(operation, args)
            else:
                response = "Invalid module or operation"
            break
        except Exception as e:
            logging.error("Error", e)
            sleep(0.3)
        else:
            return
    print(Fore.LIGHTGREEN_EX + "Done." + Style.RESET_ALL)
    return response


def set_as_read(instruction):
    print(now(), "Setting as read ...", sep='\t', end='\t')

    token = read_token()
    url = f'https://{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
    HEADERS['Authorization'] = 'Bearer ' + token

    for _ in range(MAX_RETRIES):
        try:
            response = requests.put(url, headers=HEADERS)

            if response.status_code == 200:
                output = response.json()
                response = output.get('response')
                break
            else:
                logging.error("Error", response.status_code,
                              response.json())
        except Exception as e:
            logging.error("Error", e)
            sleep(1)
        else:
            return
    print(Fore.LIGHTGREEN_EX + "Done." + Style.RESET_ALL)
    return response


def send_response(instruction, data):
    print(now(), Fore.LIGHTYELLOW_EX + "Sending response ... " +
          Style.RESET_ALL, sep='\t', end='\t')

    token = read_token()
    url = f'https://{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
    HEADERS['Authorization'] = 'Bearer ' + token

    for _ in range(MAX_RETRIES):
        try:
            response = requests.put(url, data=data, headers=HEADERS)
            if response.status_code == 200:
                output = response.json()
                response = output.get('response')
                break
            else:
                logging.error("Error", response.status_code,
                              response.json())
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Error:" + Style.RESET_ALL, e)
            sleep(0.5)
        else:
            return
    print(Fore.LIGHTGREEN_EX + "Done. " + Style.RESET_ALL)
    return response


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

    ably = AblyRealtime(token_details=token_request)
    channel = ably.channels.get(DEVICE_ID)

    def on_message(message):
        instruction = json.loads(message.data)
        print(now(), Fore.LIGHTYELLOW_EX + "New instruction received." +
              Style.RESET_ALL, sep='\t')
        change_icon_color(yellow_icon)
        response = execute_request(instruction)
        set_as_read(instruction)
        send_response(instruction, response)
        change_icon_color(green_icon)

    channel.subscribe(on_message)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        ably.close()
        print(now(), "Closing app", "See you soon!", sep='\t')
        change_icon_color(red_icon)
        sleep(1)
        sys.exit(0)


async def main():
    await ably_connect()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)