import asyncio
import json
import logging
from time import sleep
from colorama import Back, Fore, Style

import requests
from ably import AblyRealtime
from pygments import highlight, lexers, formatters
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Number,
    Operator,
    Generic,
)
from tabulate import tabulate

from .auth import CONN, HEADERS
from .modules import files
from .modules import git_module
from .modules import terminal
from .utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE, now

MAX_RETRIES = 2


def colorize(content: str, lexer) -> str:
    if content is not None:
        content = highlight(
            content.strip(), lexer, formatters.TerminalFormatter(bg="dark")
        )

    return content


def execute_request(instruction):
    print(
        now(),
        Fore.LIGHTYELLOW_EX + "Executing task ... " + Style.RESET_ALL,
        sep="\t",
        end="\t",
    )

    response = ""
    module = instruction.get("module").lower()  # convert to lowercase
    request = instruction.get("request")

    operation = request.get("operation")
    args = request.get("args")

    for _ in range(MAX_RETRIES):
        try:
            if module == "files":
                response = files.execute(operation, args)
            elif module == "git":
                response = git_module.execute(operation, args)
            elif module == "terminal":
                response = terminal.execute(operation, args)
            else:
                response = "Invalid module or operation"
            break
        except Exception as e:
            #  TODO: handle exceptions
            # logging.error("Error", e)
            print(Fore.LIGHTRED_EX + "ERROR:" + Style.RESET_ALL)
            print(e)
            sleep(0.5)
        else:
            return response
    print(Fore.LIGHTGREEN_EX + "Done." + Style.RESET_ALL)
    return response


def set_as_read(instruction):
    print(now(), "Setting as read ...", sep="\t", end="\t")

    token = read_token()
    url = f'https://{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
    HEADERS["Authorization"] = "Bearer " + token

    for _ in range(MAX_RETRIES):
        try:
            response = requests.put(url, headers=HEADERS)

            if response.status_code == 200:
                output = response.json()
                response = output.get("response")
                break
            else:
                logging.error("Error", response.status_code, response.json())
        except Exception as e:
            logging.error("Error", e)
            sleep(1)
        else:
            return
    print(Fore.LIGHTGREEN_EX + "Done." + Style.RESET_ALL)
    return


def send_response(instruction, data):
    print(
        now(),
        Fore.LIGHTYELLOW_EX + "Sending response ... " + Style.RESET_ALL,
        sep="\t",
        end="\t",
    )

    token = read_token()
    url = f'https://{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
    HEADERS["Authorization"] = "Bearer " + token

    for _ in range(MAX_RETRIES):
        try:
            response = requests.put(url, data=data, headers=HEADERS)
            if response.status_code == 200:
                output = response.json()
                response = output.get("response")
                break
            else:
                logging.error("Error", response.status_code, response.json())
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Error:" + Style.RESET_ALL, e)
            sleep(0.5)
        else:
            return
    print(Fore.LIGHTGREEN_EX + "Done. " + Style.RESET_ALL)
    return


async def ably_connect():
    logging.info("Initiating WebSocket connection...")
    auth_url = f"https://{APP_URL}{API_PATH}/ably-auth"
    token = read_token()

    try:
        HEADERS["Authorization"] = "Bearer " + token
        response = requests.post(auth_url, headers=HEADERS)
        token_request = response.json()
    except Exception as e:
        logging.error("Error", e)
        return

    try:
        token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
        response = requests.post(token_url, json=token_request)
        token = response.json()["token"]
        realtime = AblyRealtime(token=token)
        logging.info("WebSocket connection established")
    except Exception as e:
        logging.error("Websocket error:", e)
        return

    privateChannel = realtime.channels.get(f"private:dev-assistant-{DEVICE_ID}")
    await privateChannel.subscribe(process_message)

    logging.info("Ready!", "Waiting for instructions...")

    while True:
        await asyncio.sleep(1)


def process_message(message):
    print(
        now(),
        Fore.LIGHTYELLOW_EX + "Receiving message ..." + Style.RESET_ALL,
        message.data.get("feedback"),
        sep="\t",
    )
    instruction = message.data

    try:
        set_as_read(instruction)
    except Exception as e:
        logging.error("Error", e)

    try:
        response_data = execute_request(instruction)

        token = read_token()
        HEADERS["Authorization"] = "Bearer " + token

        payload = json.dumps({"response": response_data})

        send_response(instruction, payload)
    except Exception as e:
        logging.error("Error", e)


def read_token():
    with open(TOKEN_FILE, "r") as file:
        token = file.read()
    return token
