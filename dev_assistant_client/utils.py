from datetime import datetime
import json
import os
import sys
import uuid
from pathlib import Path
from colorama import Fore, Style
from dotenv import load_dotenv

# Define the exclusive directory for dot files
DOTFILES_DIR = Path.home() / ".dev-assistant-client"
DOTFILES_DIR.mkdir(mode=775, parents=True, exist_ok=True)

# Load environment variables from .env file
load_dotenv()

# Get application URL and API path from environment variables
APP_URL = os.getenv("APP_URL", "https://devassistant.tonet.dev")
API_PATH = os.getenv("API_PATH", "api")
API_URL = f"{APP_URL}/{API_PATH}"

# Define file paths for token, user data, ably token and device id
TOKEN_FILE = DOTFILES_DIR / "auth_token"
USER_DATA_FILE = DOTFILES_DIR / "user_data"
ABLY_TOKEN_FILE = DOTFILES_DIR / "ably_token"
DEVICE_ID_FILE = DOTFILES_DIR / "device_id"

# Get certificate file and key file paths from environment variables
CERT_FILE = os.getenv("CERT_FILE", "")
KEY_FILE = os.getenv("KEY_FILE", "")

# Function to print arguments and exit the program
def dd(*args):
    """
    Function similar to 'dump and die' from Laravel
    """
    for arg in args:
        print(arg)
    sys.exit(1)

# Function to get the device id
def get_device_id():
    try:
        # Try to read the device id from the file
        return DEVICE_ID_FILE.read_text()
    except FileNotFoundError:
        # If the file does not exist, generate a new device id
        device_id = str(uuid.uuid4())
        # Save the device id to the file
        DEVICE_ID_FILE.write_text(device_id)
        # Return the device id
        return device_id

# Get the device id
DEVICE_ID = get_device_id()
    
# Define headers for API requests
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "DevAssistant/0.2",
}

# Function to flatten a dictionary
def flatten_dict(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            # If the value is a dictionary, flatten it
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Function to print a JSON object
def print_json(request):
    print(json.dumps(request, indent=4))

# Function to get the current date and time TODO: Fix this, pls
def now():
    # Return just the date and time in a string format
    return Fore.LIGHTGREEN_EX + "\u203A " + Style.RESET_ALL # TODO: Fix this, pls

# Function to read the token from the file
def read_token():
    try:
        return TOKEN_FILE.read_text()
    except FileNotFoundError:
        # If the token file does not exist, return None
        return None

# Function to save the token to the file
def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

# Function to delete the token file
def delete_token():
    TOKEN_FILE.unlink()