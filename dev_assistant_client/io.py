import json
import logging
import requests

from time import sleep
from colorama import Fore, Style
from dev_assistant_client.modules.files import FilesModule
from dev_assistant_client.modules.git import GitModule
from dev_assistant_client.modules.terminal import TerminalModule
from dev_assistant_client.utils import HEADERS, API_PATH, APP_URL, DEVICE_ID, now, read_token

class IOAssistant:
    MAX_RETRIES = 3

    def __init__(self):
        pass

    @staticmethod
    def execute_request(instruction):
        print(
            now(),
            Fore.LIGHTYELLOW_EX + "Executando tarefa ... " + Style.RESET_ALL,
            sep="\t",
            end="\t",
        )

        response = ""
        module = instruction.get("module").lower()  # converter para minúsculas
        request = instruction.get("request")

        operation = request.get("operation")
        args = request.get("args")

        for _ in range(IOAssistant.MAX_RETRIES):
            try:
                if module == "files":
                    response = FilesModule().execute(operation, args)
                elif module == "git":
                    response = GitModule().execute(operation, args)
                elif module == "terminal":
                    response = TerminalModule().execute(operation, args)
                else:
                    response = "Módulo ou operação inválida"
                break
            except Exception as e:
                #  TODO: tratar exceções
                # logging.error("Erro", e)
                print(Fore.LIGHTRED_EX + "ERRO:" + Style.RESET_ALL)
                print(e)
                sleep(0.5)
            else:
                return response
        print(Fore.LIGHTGREEN_EX + "Concluído." + Style.RESET_ALL)
        return response

    @staticmethod
    def set_as_read(instruction):
        print(now(), "Setting as read ...", sep="\t", end="\t")

        token = read_token()
        url = f'{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
        HEADERS["Authorization"] = "Bearer " + token

        for _ in range(IOAssistant.MAX_RETRIES):
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

    @staticmethod
    def send_response(instruction, data):
        print(
            now(),
            Fore.LIGHTYELLOW_EX + "Sending response ... " + Style.RESET_ALL,
            sep="\t",
            end="\t",
        )

        token = read_token()
        url = f'{APP_URL}{API_PATH}/devices/{DEVICE_ID}/io/{instruction.get("id")}'
        HEADERS["Authorization"] = "Bearer " + token

        for _ in range(IOAssistant.MAX_RETRIES):
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

    @staticmethod
    def process_message(message):
        print(
            now(),
            Fore.LIGHTYELLOW_EX + "Receiving message ..." + Style.RESET_ALL,
            message.data.get("feedback"),
            sep="\t",
        )
        instruction = message.data

        try:
            IOAssistant.set_as_read(instruction)
        except Exception as e:
            logging.error("Error", e)

        try:
            response_data = IOAssistant.execute_request(instruction)

            token = read_token()
            HEADERS["Authorization"] = "Bearer " + token

            payload = json.dumps({"response": response_data})

            IOAssistant.send_response(instruction, payload)
        except Exception as e:
            logging.error("Error", e)
