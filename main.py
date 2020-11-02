from models.enums.response_type import ResponseType

from models.console import Console
from models.futbin import Futbin
from models.player import Player
from models.proxy import Proxy

from utils.file_writer import write_csv

from rich import print

import datetime

Console = Console('FutScrape')


def run():
    Console.print_name()
    email = Console.ask_string('Futbin Email: ')
    Console.print_name()
    password = Console.ask_string('Futbin Password: ')

    futbin = Futbin(email, password)

    Console.print_name()
    print(f'[yellow]Attempting login...[/yellow]')
    status = futbin.login(Proxy(None, None))

    if status != ResponseType.SUCCESS:
        print(f'[red]Error logging in.[/red]')
        return
    
    print(f'[green]Successfully logged in![/green]')

    print(f'[yellow]Attempting to pull your favorites...[/yellow]')
    players = futbin.pull_favorites()
    if players == ResponseType.BANNED:
        print(f'[red]Error pulling favorites.[/red]')
        return

    print(f'[green]Successfully pulled {len(players)} players![/green]')

    for player in players:
        player.pull_sales(Proxy(None, None))
        print(f'[green]Successfully pulled sales record for {player.NAME}![/green]')

    filename = datetime.datetime.now().strftime("%m.%d.%Y.%H.%M")

    print(f'[green]Successfully saved to {filename}.csv![/green]')


    write_csv(players, filename)

if __name__ == '__main__':
    run()