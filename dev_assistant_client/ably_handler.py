import asyncio
from ably import AblyRealtime
from dev_assistant_client.config import api_client, json, requests, logging, DEVICE_ID
from dev_assistant_client.io import IOAssistant
from dev_assistant_client.utils import APP_URL, CERT_FILE, KEY_FILE, DEVICE_ID, dd, delete_token, read_token, save_token

class AblyHandler:
    def init_ably(self):
        try:
            print("Initiating WebSocket connection...")
            api_client.token = read_token()
            api_client.headers["Authorization"] = f"Bearer {api_client.token}"
            response = api_client.post("/api/ably-auth") # Get requestToken from server
            token_request = json.loads(response.content)

            token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
            response = requests.post(token_url, json=token_request) # Get token from Ably
            token = response.json()["token"]
            realtime = AblyRealtime(token=token)
            print("WebSocket connection established")
        except Exception as e:
            logging.error("Websocket error:", e)
            return None

        return realtime

    async def ably_connect(self):
        # Initiate Ably connection
        realtime = self.init_ably()

        # Check if the connection was successful before proceeding
        if realtime is None:
            print("Failed to establish WebSocket connection.")
            return

        # Get the private channel for the device
        privateChannel = realtime.channels.get(f"private:dev-assistant-{DEVICE_ID}")

        # Check if the channel was successfully retrieved
        if privateChannel is None:
            print("Failed to get private channel.")
            return

        print("Successfully connected to private channel.")

        # Subscribe to the channel
        await privateChannel.subscribe(self.ably_message)

        # Wait for messages
        await asyncio.sleep(1000)
        
    def ably_message(self, message):
        """
        Callback function for Ably messages.
        """
        print(f"Message received: {message.data}") # TODO: Implement message handling
        
        IOAssistant().process_message(message.data)
