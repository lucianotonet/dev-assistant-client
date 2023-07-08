import os
import http.client
import json
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

APP_URL = os.getenv('APP_URL').replace('https://', '').replace('/', '')
API_PATH = '/api'

TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA_FILE = os.path.expanduser("~/.dev_assistant_user")
ABLY_TOKEN_FILE = os.path.expanduser("~/.dev_assistant_ably_token")

# if is set in the env file, use it, otherwise use the default
CERT_FILE = os.getenv('CERT_FILE') or None
KEY_FILE = os.getenv('KEY_FILE') or None

def get_device_id():
    try:
        with open('.device_id', 'r') as f:
            return f.readline()
    except FileNotFoundError:
        return None


DEVICE_ID = get_device_id()
