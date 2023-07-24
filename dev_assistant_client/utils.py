from io import BytesIO
import threading
from pystray import Icon as icon, MenuItem as item
from PIL import Image
from datetime import datetime
import json
import os
import sys
from colorama import Fore, Style
from dotenv import load_dotenv
import requests

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


def load_icon(icon):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
               'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'}
    url = 'https://devassistant.tonet.dev/img/' + icon
    response = requests.get(url, headers=headers)
    image = Image.open(BytesIO(response.content))
    return image


def create_icon(image, name):
    return icon(name, image, "Dev Assistant")


def show_icon(icon):
    def run_icon():
        icon.run()
    threading.Thread(target=run_icon).start()


def change_icon_color(icon, new_color_icon):
    icon.stop()
    new_color_icon.run()


green_icon = load_icon('tray_icon_green.png')
red_icon = load_icon('tray_icon_red.png')
yellow_icon = load_icon('tray_icon_yellow.png')
blue_icon = load_icon('tray_icon_blue.png')
tray_icon = create_icon(green_icon, 'dev_assistant')
show_icon(tray_icon)

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