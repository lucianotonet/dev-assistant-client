import os
import http.client
import json
import logging
from colorama import Fore, Style
from dev_assistant_client.auth import CONN, HEADERS
from dev_assistant_client.utils import API_PATH, DEVICE_ID, TOKEN_FILE, now


def register(args):
    """Registers the device"""
    logging.info("Registering device...")

    payload = json.dumps({
        'device_id': DEVICE_ID,
        'name': args.get('name'),
        'description': args.get('description')
    })

    CONN.request("POST", API_PATH + '/devices', body=payload, headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        logging.info("Device registered")
    else:
        logging.error("Error: " + response.read().decode())


def unregister(args):
    """Unregisters the device"""
    logging.info("Unregistering device...")

    CONN.request("DELETE", API_PATH + '/devices/' + DEVICE_ID, headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        logging.info("Device unregistered")
    else:
        logging.error("Error: " + response.read().decode())


def list(args):
    """Lists the devices"""
    logging.info("Listing devices...")

    CONN.request("GET", API_PATH + '/devices', headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        devices = json.loads(response.read().decode())
        logging.info("Devices:")
        for device in devices:
            logging.info(Fore.LIGHTCYAN_EX + device.get('name') +
                  Style.RESET_ALL + " (" + device.get('device_id') + ")")
    else:
        logging.error("Error: " + response.read().decode())