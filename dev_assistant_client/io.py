import asyncio
import json
import sys
from colorama import Fore, Style
import requests
from ably import AblyRealtime
from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.utils import API_PATH, APP_URL, DEVICE_ID, TOKEN_FILE
from dev_assistant_client.modules import file_management, version_control, shell_prompter

def send_response(data):
    try:
        print(Fore.LIGHTYELLOW_EX + "Request:\t" +
              Style.RESET_ALL, data.get('request'))

        # Extract the module, operation and arguments from the command data
        module = data.get('module')
        operation = data.get('operation')
        args = data.get('args')

        # Execute the appropriate function based on the module and operation
        if module == 'file_management':
            response_data = file_management.execute(operation, args)
        elif module == 'version_control':
            response_data = version_control.execute(operation, args)
        elif module == 'shell_prompter':
            response_data = shell_prompter.execute(operation, args)
        else:
            # Just for testing purposes
            response_data = version_control.execute(
                'status', {'directory': '.'}
            )

        with open(TOKEN_FILE, "r") as f:
            token = f.readline()

        HEADERS['Authorization'] = 'Bearer ' + token

        payload = json.dumps({
            'response': response_data  # Send the actual response data
        })

        CONN.request("PUT", API_PATH + '/devices/' + DEVICE_ID +
                     '/io/'+data.get('id'), body=payload, headers=HEADERS)
        response = CONN.getresponse()

        if response.status == 200:
            output = json.loads(response.read().decode())
            print(Fore.LIGHTGREEN_EX + "Response:\t" +
                  Style.RESET_ALL, output.get('response'))
        else:
            print(Fore.LIGHTRED_EX + "Failed to send response!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Error sending response: " + Style.RESET_ALL, e)
        return


async def ably_connect():
    auth_url = 'https://' + APP_URL + API_PATH + '/ably-auth'
    # Faça uma solicitação HTTP para o seu endpoint Laravel para obter o TokenRequest
    response = requests.get(auth_url)
    token_request = response.json()

    # Faça uma solicitação HTTP para o endpoint de token do Ably para obter um token usando o token_request
    token_url = 'https://rest.ably.io/keys/' + \
        token_request['keyName'] + '/requestToken'
    response = requests.post(token_url, json=token_request)
    token = response.json()['token']

    # Inicialize o cliente AblyRealtime com o token
    realtime = AblyRealtime(token=token)

    # Inscreva-se em um canal
    # publicChannel = realtime.channels.get('public:dev-assistant')
    # await publicChannel.subscribe(check_message)

    # Inscreva-se em um canal privado
    privateChannel = realtime.channels.get('private:dev-assistant-'+DEVICE_ID)
    await privateChannel.subscribe(check_message)

    while True:
        await asyncio.sleep(0.3)


async def check_message(message):
    try:
        send_response(message.data)
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
