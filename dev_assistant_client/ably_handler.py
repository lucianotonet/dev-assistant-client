import asyncio
from ably import AblyRealtime
from colorama import Fore, Style
from dev_assistant_client.config import api_client, json, requests, logging, DEVICE_ID
from dev_assistant_client.io import IOAssistant
from dev_assistant_client.utils import APP_URL, CERT_FILE, KEY_FILE, DEVICE_ID, dd, delete_token, now, read_token, save_token

class AblyHandler:
    def init_ably(self):
        try:
            api_client.token = read_token()
            api_client.headers["Authorization"] = f"Bearer {api_client.token}"
            response = api_client.post("/api/ably-auth")
            token_request = json.loads(response.content)

            token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
            response = requests.post(token_url, json=token_request)
            token = response.json()["token"]
            realtime = AblyRealtime(token=token)
        except Exception as e:
            return None

        return realtime

    async def ably_connect(self):
        print(now(), "Connecting websocket...", sep="\t", end="\t")
        realtime = self.init_ably()

        if realtime is None:
            print(Fore.LIGHTRED_EX + "Failed to connect to Ably." + Style.RESET_ALL)
            return

        privateChannel = realtime.channels.get(f"private:dev-assistant-python-{DEVICE_ID}")

        if privateChannel is None:
            print(Fore.LIGHTRED_EX + "Failed to connect to private channel." + Style.RESET_ALL)
            return

        print(Fore.LIGHTGREEN_EX + "Connected" + Style.RESET_ALL)

        await privateChannel.subscribe(self.ably_message)
        print(now(), "Ready! Listening for instructions...", sep="\t")
              
        while True:
            await asyncio.sleep(1)
        
    def ably_message(self, message):
        IOAssistant.process_message(message)