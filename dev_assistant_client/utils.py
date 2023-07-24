from datetime import datetime
import json
import os
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.getenv('APP_URL').replace(
    'https://', '').replace('/', '') if os.getenv('APP_URL') else 'devassistant.tonet.dev'
API_PATH = '/api'

TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA_FILE = os.path.expanduser("~/.dev_assistant_user")
ABLY_TOKEN_FILE = os.path.expanduser("~/.dev_assistant_ably_token")
DEVICE_ID_FILE = os.path.expanduser("~/.dev_assistant_device_id")

# if is set in the env file, use it, otherwise use none
CERT_FILE = os.getenv('CERT_FILE', '')
KEY_FILE = os.getenv('KEY_FILE', '')

IS_PREMIUM_USER = os.getenv('IS_PREMIUM_USER', 'false').lower() == 'true'

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


def now():
    # return just the date and time in a string format
    now = datetime.now()
    return Fore.WHITE + now.strftime("%d/%m/%Y %H:%M:%S") + Style.RESET_ALL

# read the token from the token file
def read_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return f.readline()
    except FileNotFoundError:
        return None