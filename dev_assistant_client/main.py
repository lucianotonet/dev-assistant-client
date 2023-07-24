import logging
import asyncio
import sys
import argparse
import os
import time
from dotenv import load_dotenv
from colorama import Fore, Style
from dev_assistant_client.auth import login, logout
from dev_assistant_client.device import connect
from dev_assistant_client.utils import APP_URL, TOKEN_FILE, USER_DATA_FILE
import pkg_resources

# Get the version of the current package
package_version = pkg_resources.get_distribution(
    "dev-assistant-client").version

print(Fore.LIGHTGREEN_EX +
      '''
    .-----.   Dev Assistant
    | >_< |   ''' + Fore.LIGHTYELLOW_EX + 'v' + package_version + Fore.LIGHTGREEN_EX + ''' 
    '-----'   ''' + Fore.LIGHTYELLOW_EX + 'https://' + (APP_URL or 'devassistant.tonet.dev') + Fore.LIGHTGREEN_EX + '''
''' + Style.RESET_ALL)

load_dotenv()

async def main(args=None):
    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='dev-assistant')
    subparsers = parser.add_subparsers()

    # Use 'start' as an alias for the main command
    parser_main = subparsers.add_parser('start')
    parser_main.set_defaults(func=start)

    parser_logout = subparsers.add_parser('logout')
    parser_logout.set_defaults(func=logout)

    args = parser.parse_args(args)

    if 'func' in args:
        try:
            await args.func(args)
        except KeyboardInterrupt:
            print("Closing app", "See you soon!")
        except Exception as e:
            logging.error("Error:", e)
    else:
        await start(args)


async def start(args):
    try:
        if not os.path.exists(TOKEN_FILE) or not os.path.exists(USER_DATA_FILE):
            login(args)
        await connect()
    except Exception as e:
        logging.error("Error:", e)
    while True:
        time.sleep(1)


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    run()
