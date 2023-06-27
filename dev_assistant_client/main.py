import socket
import os
import getpass
import http.client
import argparse
import json

API_URL = 'devassistant.tonet.dev'
API_PATH = '/api'
TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA = os.path.expanduser("~/.dev_assistant_user")


def main(args=None):
    parser = argparse.ArgumentParser(prog='dev-assistant')
    subparsers = parser.add_subparsers()

    # Use 'start' as an alias for the main command
    parser_main = subparsers.add_parser('start')
    parser_main.set_defaults(func=start)

    parser_logout = subparsers.add_parser('logout')
    parser_logout.set_defaults(func=logout)

    args = parser.parse_args(args)

    if 'func' in args:
        args.func(args)
    else:
        start(args)


def start(args):
    if not os.path.exists(TOKEN_FILE):
        login(args)
    else:
        connect()


def connect():
    with open(TOKEN_FILE, "r") as f:
        token = f.read()

    headers = {
        'authorization': 'Bearer ' + token,
        'accept': 'application/json'
    }

    conn = http.client.HTTPSConnection(API_URL)
    conn.request("GET", API_PATH, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        print("Successfully connected to the server.")
        print("Server response:", response.read().decode())
    else:
        print("Failed to connect to the server.")
        print("Response: ", response.read().decode())
        print("Status code:", response.status)


def login(args):
    email = input("Enter your e-mail: ")
    password = getpass.getpass("Enter your password: ")

    payload = json.dumps({
        'email': email,
        'password': password,
        'device_name': socket.gethostname()
    })

    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    conn = http.client.HTTPSConnection(API_URL)
    conn.request("POST", API_PATH + 'login', body=payload, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        token = response.read().decode()
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        print("Logged in.")

        headers = {
            'authorization': 'Bearer ' + token,
            'accept': 'application/json'
        }

        conn.request("GET", API_PATH + 'user', headers=headers)
        response = conn.getresponse()
        user = json.loads(response.read().decode())

        if 'name' in user:
            with open(USER_DATA, "w") as f:
                json.dump(user, f)
            print("Hello,", user['name'])

        connect()
    else:
        print("Failed to log in!")
        print("Error: ", response.read().decode())


def logout(args):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    if os.path.exists(USER_DATA):
        with open(USER_DATA, "r") as f:
            user = json.load(f)
        print("See you soon,", user['name'])
        os.remove(USER_DATA)
    print("Logged out.")
