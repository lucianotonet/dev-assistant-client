import asyncio
from pusherclient import Pusher
import argparse
import os
import time
from dotenv import load_dotenv
from colorama import Fore, Style
from dev_assistant_client.auth import login, logout
from dev_assistant_client.device import connect, connect_to_ably
from dev_assistant_client.utils import APP_URL, TOKEN_FILE, PUSHER_APP_ID, PUSHER_APP_KEY, PUSHER_APP_SECRET, PUSHER_APP_CLUSTER
from pusher import Pusher
import pkg_resources

# Get the version of the current package
package_version = pkg_resources.get_distribution(
    "dev-assistant-client").version

print(Fore.LIGHTGREEN_EX +
      '''
    .-----.   Dev Assistant
    | >_< |   ''' + Fore.YELLOW + 'v' + package_version + Fore.LIGHTGREEN_EX + ''' 
    '-----'   ''' + Fore.YELLOW + 'https://' + (APP_URL or 'devassistant.tonet.dev') + Fore.LIGHTGREEN_EX + '''
'''
      + Style.RESET_ALL)

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
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        await start(args)


async def start(args):
    # Check if the user is logged in, if not, prompt for login
    if not os.path.exists(TOKEN_FILE):
        login(args)
        await start(args)
    else:
        try:
            await connect()
        except Exception as e:
            print(f"Failed to start: {e}")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
