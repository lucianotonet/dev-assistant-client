import datetime
import getpass
import http.client
import json
import os
from colorama import Fore, Style
from dev_assistant_client.utils import ABLY_TOKEN_FILE, TOKEN_FILE, USER_DATA_FILE, APP_URL, API_PATH, DEVICE_ID, CERT_FILE, KEY_FILE, HEADERS

CONN = http.client.HTTPSConnection(
    APP_URL, cert_file=CERT_FILE, key_file=KEY_FILE)


def login(args):
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    payload = json.dumps({
        'email': email,
        'password': password,
    })

    CONN.request("POST", API_PATH + '/login', body=payload, headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        token = response.read().decode()
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        now = datetime.datetime.now()
        print(Fore.LIGHTGREEN_EX + str(now), "Logged in." +
              Style.RESET_ALL, sep="\t", end="\n")

        headers = {
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        # Request user data
        CONN.request("GET", API_PATH + '/user', headers=headers)
        response = CONN.getresponse()

        if response.status == 200:
            user = json.loads(response.read().decode())

            if 'name' in user:
                with open(USER_DATA_FILE, "w") as f:
                    json.dump(user, f)
                print(Fore.LIGHTGREEN_EX + str(now), "Hello, " + Fore.LIGHTCYAN_EX +
                      user['name'] + Style.RESET_ALL + "!", sep="\t", end="\n")

    else:
        error = json.loads(response.read().decode())
        now = datetime.datetime.now()
        print(Fore.LIGHTRED_EX + str(now), "Error:", Fore.LIGHTRED_EX +
              response.read().decode() + Style.RESET_ALL, error.get('message'), sep="\t", end="\n")
        return


def logout(args):
    with open(TOKEN_FILE, "r") as f:
        token = f.readline()

    HEADERS['authorization'] = 'Bearer ' + token
    CONN.request("POST", API_PATH + '/logout', headers=HEADERS)
    response = CONN.getresponse()

    if response.status == 200:
        now = datetime.datetime.now()
        print(str(now), "You are now logged out", sep="\t", end="\n")
        print("Bye!")
    else:
        now = datetime.datetime.now()
        print(str(now), "Failed to log out!", sep="\t", end="\n")

    os.remove(USER_DATA_FILE)
    os.remove(TOKEN_FILE)
