from datetime import datetime
import json
import os
import sys
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.getenv('APP_URL').replace('https://', '').replace('/', '') or 'devassistant.tonet.dev'
API_PATH = '/api'

TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA_FILE = os.path.expanduser("~/.dev_assistant_user")
ABLY_TOKEN_FILE = os.path.expanduser("~/.dev_assistant_ably_token")
DEVICE_ID_FILE = os.path.expanduser("~/.dev_assistant_device_id")
TERMINAL_STATE_FILE = os.path.expanduser("~/.dev_assistant_terminal_state")

# if is set in the env file, use it, otherwise use none
CERT_FILE = os.getenv('CERT_FILE', '')
KEY_FILE = os.getenv('KEY_FILE', '')

def get_device_id():
    try:
        with open(DEVICE_ID_FILE, 'r') as f:
            return f.readline()
    except FileNotFoundError:
        return None


DEVICE_ID = get_device_id()
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'DevAssistantClient/1.0'
}


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def print_json(request):
    print(json.dumps(request, indent=4))

def now ():
    """
    The function "now" returns the current date and time as a string.
    :return: The current date and time as a string.
    """
    now = datetime.now()
    return str(now)