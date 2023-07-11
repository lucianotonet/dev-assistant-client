import os
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.getenv('APP_URL').replace('https://', '').replace('/', '') or 'devassistant.tonet.dev'
API_PATH = '/api'

TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA_FILE = os.path.expanduser("~/.dev_assistant_user")
ABLY_TOKEN_FILE = os.path.expanduser("~/.dev_assistant_ably_token")
DEVICE_ID_FILE = os.path.expanduser("~/.dev_assistant_device_id")

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