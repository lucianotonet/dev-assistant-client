import json
import logging
import os

from time import sleep
from colorama import Fore, Style
import pkg_resources
from dev_assistant_client.api_client import APIClient
from dev_assistant_client.modules.files import FilesModule
from dev_assistant_client.modules.git import GitModule
from dev_assistant_client.modules.terminal import TerminalModule
from dev_assistant_client.client_auth import ClientAuth
from dev_assistant_client.utils import CALLBACK_URL, CERT_FILE, HEADERS, API_URL, CLIENT_ID, KEY_FILE, dd, now, read_token

class IOAssistant:
    MAX_RETRIES = 3

    def __init__(self):
        pass

    @staticmethod
    def execute_request(instruction):
        print(
            now(),
            "Executing task ... ",
            sep="\t",
            end="\t",
        )

        response = ""
        # module = instruction.get("module").lower()  # convert to lowercase
        request = instruction.get("request")

        moduleOperation = request.get("operation")
        args = request.get("args")
        
        # split moduleOperation by _ and underline each word
        module = moduleOperation.split("_")[0] # get the first part of the string
        operation = moduleOperation.split("_")[1] # get the second part of the string
        
        for _ in range(IOAssistant.MAX_RETRIES):
            try:
                if module == "files":
                    response = FilesModule().execute(operation, args)
                elif module == "git":
                    response = GitModule().execute(operation, args)
                elif module == "terminal":
                    response = TerminalModule().execute(operation, args)
                else:
                    response = "Invalid module or operation"
                break
            except Exception as e:
                #  TODO: handle exceptions
                logging.error("Error", e)
                print(now(), "Error: ", e)
                print(Fore.LIGHTRED_EX + "ERROR:" + Style.RESET_ALL)
                print(e)
                sleep(0.5)
            else:
                return response
        print(Fore.LIGHTGREEN_EX + "Done ✓" + Style.RESET_ALL)
        return response

    @staticmethod
    async def process_message(message):
        print(
            now(),
            "Receiving request ...",
            message.data.get("feedback"),
            sep="\t",
        )
        
        instruction = message.data
        
        try:
            await IOAssistant.set_as_read(instruction)
        except Exception as e:
            # logging.error("Error", e)
            print(now(), "Error: ", e)        

        try:
            response_data = IOAssistant.execute_request(instruction)

            token = read_token()
            HEADERS["Authorization"] = f'Bearer ${token}'

            payload = json.dumps({"response": response_data})

            IOAssistant.send_response(instruction, payload)
        except Exception as e:
            # logging.error("Error", e)
            print(now(), "Error: ", e)
            
    @staticmethod
    async def set_as_read(instruction):
        print(now(), "Setting as received ...", sep="\t", end="\t")
        
        url = f'/clients/{CLIENT_ID}/io/{instruction.get("id")}'

        for _ in range(IOAssistant.MAX_RETRIES):
            try:
                api_client = APIClient(f"{API_URL}")
                response = api_client.put(url)
                                
                if response.status_code == 401:
                    print(now(), "Invalid token. Reauthenticating...", sep="\t")
                    client_auth = ClientAuth()
                    await client_auth.authenticate()

                if response.status_code in [200, 201, 202, 204]:
                    output = json.loads(response.content.decode("utf-8"))
                    response = output.get("response")
                    break
                else:
                    # logging.error("Error", response.status_code, response.content)
                    print(now(), "Error: ", response.status_code, json.loads(response.content.decode("utf-8")))
            except Exception as e:
                # logging.error("Error", e)
                print(now(), "Error: ", e)
                sleep(1)
            else:
                return
        print(Fore.LIGHTGREEN_EX + "Done ✓" + Style.RESET_ALL)
        return

    @staticmethod
    def send_response(instruction, data):
        print(
            now(),
            "Returning response ... ",
            sep="\t",
            end="\t",
        )

        url = f'/clients/{CLIENT_ID}/io/{instruction.get("id")}'

        for _ in range(IOAssistant.MAX_RETRIES):
            try:
                api_client = APIClient(f"{CALLBACK_URL or API_URL}")
                response = api_client.put(url, data=json.loads(data))
                if response.status_code == 200:
                    output = json.loads(response.content.decode("utf-8"))
                    response = output.get("response")
                    break
                else:
                    # logging.error("Error", response.status_code, response.content)
                    print(now(), "Error: ", response.status_code, json.loads(response.content.decode("utf-8")))
            except Exception as e:
                print(Fore.LIGHTRED_EX + "Error:" + Style.RESET_ALL, e)
                sleep(0.5)
            else:
                return
        print(Fore.LIGHTGREEN_EX + "Done ✓ " + Style.RESET_ALL)
        return