import asyncio
import getpass
import json
import logging

import requests
from dev_assistant_client.api_client import APIClient
from ably import AblyRealtime
from dev_assistant_client.io import IOAssistant
from dev_assistant_client.utils import APP_URL, CERT_FILE, KEY_FILE, DEVICE_ID, dd, delete_token, read_token, save_token
api_client = APIClient(APP_URL, CERT_FILE, KEY_FILE)

class Auth:
    """
    The Auth class handles authentication operations, including logging in,
    logging out, and establishing a WebSocket connection with Ably.
    """
    
    def login(self):
        """
        Prompts the user for email and password, and attempts to log in.
        If successful, the received token is saved locally and returns True.
        If login fails, returns False.
        """
        
        email = input("Enter your email: ") or "tonetlds@gmail.com"
        password = getpass.getpass("Enter your password: ") or "password"
        data = {"email": email, "password": password}
     
        response = api_client.post("/api/login", data=data)
        
        if response.status_code in [200, 201, 202, 204]:
            token = response.json()["token"]
            save_token(token)
            return True
        else:
            print("Login failed. Please check your credentials and try again.")
            return False
        
    def logout(self):
        """
        Logs out the user by deleting the locally stored token.
        """
        try:
            delete_token()
            print("Logged out successfully.")
        except FileNotFoundError:
            print("You aren't logged in.")

    async def ably_connect(self):
        """
        Initiates a WebSocket connection using the Ably library.
        Starts by getting an authentication token for Ably, then establishes a WebSocket connection,
        and subscribes to a private channel to listen for messages.
        """
    
        print("Initiating WebSocket connection...")
        api_client.token = read_token()
        api_client.headers["Authorization"] = f"Bearer {api_client.token}"
        response = api_client.post("/api/ably-auth") # Get requestToken from server
        token_request = json.loads(response.content)

        try:
            token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
            response = requests.post(token_url, json=token_request) # Get token from Ably
            token = response.json()["token"]
            realtime = AblyRealtime(token=token)
            print("WebSocket connection established")
        except Exception as e:
            logging.error("Websocket error:", e)
            return

        privateChannel = realtime.channels.get(f"private:dev-assistant-{DEVICE_ID}")
        await privateChannel.subscribe(IOAssistant.process_message)

        print("Ready!", "Waiting for instructions...")

        while True:
            await asyncio.sleep(1)