import os
import json
import logging
import getpass
import platform
import socket
import uuid
import re
from colorama import Fore, Style
from dev_assistant_client.api_client import APIClient
from dev_assistant_client.auth import Auth
from dev_assistant_client.utils import (
    CERT_FILE,
    DEVICE_ID_FILE,
    KEY_FILE,
    TOKEN_FILE,
    APP_URL,
    API_PATH,
    DEVICE_ID,
    dd,
    now,
    read_token,
    
)

def create_device_payload():
    """
    Creates a payload with information about the device, such as hostname, IP address,
    MAC address, OS, Python version, etc.
    Returns:
        str: A JSON string representation of the device payload.
    """
    
    return json.dumps(
        {
            "id": DEVICE_ID or "",
            "name": socket.gethostname(),
            "type": "desktop",
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "mac_address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "username": getpass.getuser(),
        },
        indent=4,
    )

api_client = APIClient(f"{APP_URL}/{API_PATH}", CERT_FILE, KEY_FILE)

async def connect_device():
    """
    Tries to connect the device to the server. It starts by reading a token, creates
    a device payload and makes a POST call to the server. If the call is successful,
    the device is connected and the device ID is saved locally. Then, it tries to establish
    a WebSocket connection using the ably_connect() function from auth.py.
    """
    auth = Auth()
    if not auth.login():
        print("Login failed. Exiting...")
        return
    
    token = read_token()
    
    payload = create_device_payload()
    print(now(), "Connecting...", sep="\t")

    api_client.headers["Authorization"] = "Bearer " + token
    
    response = api_client.post("/devices", data=payload)
    
    if response.status_code in [200, 201]:
        print(now(),"Connected.","Device ID " + Fore.LIGHTYELLOW_EX + json.loads(response.content).get("id") + Style.RESET_ALL,sep="\t")
        with open(DEVICE_ID_FILE, "w") as f:
            f.write(json.loads(response.content).get("id"))
        await Auth().ably_connect()
    else:
        print(now(), "Failed to connect!", sep="\t")
        if response.status_code == 401:
            print(now(), "Error: ", json.loads(response.content).get('error'), sep="\t")
            print(now(), "Please do login again.", sep="\t")
            os.remove(TOKEN_FILE)
        else:
            print(now(), "Status code: ", response.status_code, sep="\t")

def register(args):
    logging.info("Registering device...")

    payload = json.dumps(
        {
            "device_id": DEVICE_ID,
            "name": args.get("name"),
            "description": args.get("description"),
        }
    )

    response = api_client.post("/devices", data=payload)

    if response.status == 200:
        logging.info("Device registered")
    else:
        logging.error("Error: " + response.read().decode())

def unregister(args):
    logging.info("Unregistering device...")

    response = api_client.delete("/devices/" + str(DEVICE_ID))
    
    if response.status == 200:
        logging.info("Device unregistered")
    else:
        logging.error("Error: " + response.read().decode())

def list(args):
    logging.info("Listing devices...")

    response = api_client.get("/devices")

    if response.status == 200:
        devices = json.loads(response.read())
        logging.info("Devices:")
        for device in devices:
            logging.info(
                Fore.LIGHTCYAN_EX
                + device.get("name")
                + Style.RESET_ALL
                + " ("
                + device.get("device_id")
                + ")"
            )
    else:
        logging.error("Error: " + response.read().decode())

