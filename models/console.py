from sys import platform
from rich import print
import pyfiglet
import ctypes
import os

class Console:
    def __init__(self, PROGRAM_NAME):
        self.PROGRAM_NAME = PROGRAM_NAME
        self.default_title()

    @staticmethod
    def clear_console():
        if platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')

    def default_title(self):
        if platform == 'win32':
            ctypes.windll.kernel32.SetConsoleTitleW(f'{self.PROGRAM_NAME} by JFK')

    def print_center(self, text):
        print(f'{text}'.center(os.get_terminal_size().columns))

    def set_title(self, counter):
        if platform == 'win32':
            module = counter['Module']
            valid = counter['Valid']
            invalid = counter['Invalid']
            errors = counter['Errors']
            ctypes.windll.kernel32.SetConsoleTitleW(f'{self.PROGRAM_NAME} by JFK | {module} | Valid: {valid} | Invalid: {invalid} | Errors: {errors}')
            

    def print_name(self):
        self.clear_console()
        figlet = pyfiglet.figlet_format(self.PROGRAM_NAME, font="slant")
        for part in figlet.split('\n'):
            self.print_center(f'[green]{part}[/green]')
        print()

    @staticmethod
    def ask_string(question, allow_empty=False):
        while True:
            print(f'[yellow]{question}[/yellow]')
            response = input()
            if allow_empty:
                return response
            if len(response) > 0:
                return response

    @staticmethod
    def ask_integer(question):
        while True:
            print(f'[yellow]{question}[/yellow]')
            response = input()
            if response.isnumeric() and int(response) >= 0:
                return int(response)
                