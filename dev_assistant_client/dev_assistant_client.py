import tracemalloc
tracemalloc.start()
import asyncio
import argparse
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
from plyer import notification
from dotenv import load_dotenv
from colorama import Fore, Style
from .client import connect_client
from .client_auth import ClientAuth
from .utils import APP_URL, dd, read_token

import pkg_resources

load_dotenv()

class DevAssistant:
    def print_header(self):
        print(Fore.LIGHTGREEN_EX +
            '''
        ╭─────╮   Dev Assistant
        │ ''' + Fore.WHITE + '>_<' + Fore.LIGHTGREEN_EX + ''' │   ''' + Fore.LIGHTYELLOW_EX + 'Python CLI v' + self.package_version + Fore.LIGHTGREEN_EX + ''' 
        ╰─────╯   ''' + Fore.LIGHTYELLOW_EX + APP_URL + Fore.LIGHTGREEN_EX + '''
        ''' + Style.RESET_ALL)

    async def cli(self):
        from .cli import cli
        await cli()

    async def run(self, args=None):
        self.auth = ClientAuth()
        self.systray = SysTray()
        
        self.package_version = pkg_resources.get_distribution("dev_assistant-client").version
        self.print_header()
        
        token = read_token()
        
        if token is None:
            await self.auth.authenticate()                        
        
        # Parse command line arguments
        parser = argparse.ArgumentParser(prog='dev-assistant-client')
        subparsers = parser.add_subparsers()

        parser_logout = subparsers.add_parser('close')
        parser_logout.set_defaults(func=self.auth.deauthenticate)
                    
        try:
            await connect_client()
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Saindo...")
            await self.close_resources()
        except asyncio.CancelledError:
            print("\nTarefas do main_loop canceladas. Executando a limpeza...")
            await self.close_resources()
            
    
    async def close_resources(self):
        """
        This method is used to close any resources or connections.
        """
        # Cancel all tasks lingering
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Close WebSocket connections, files, database sessions, etc.
        if hasattr(self, 'ably_handler') and self.ably_handler is not None:
            await self.ably_handler.close()
        # Add the closing of other asynchronous resources here if necessary

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DevAssistant().run())

class SysTray:
    def on_start(self):
        print('Start')

    def on_stop(self):
        print('Stop')

    def on_status(self):
        print('Status')
    
    def show_notification(self, title, message):
        icon_path = pkg_resources.resource_filename('dev_assistant_client', 'icon.ico')
        return notification.notify(
            title=title,
            message=message,
            app_name='Dev Assistant',
            app_icon=icon_path, 
        )
    
    async def run(self):
        image = Image.open("icon.ico")  # Replace with the correct path of the icon
        menu = menu(
            item('Start', lambda: self.on_start()),
            item('Stop', lambda: self.on_stop()),
            item('Status', lambda: self.on_status())
        )

        self.icon = icon
        self.menu = menu
        self.icon.run()
