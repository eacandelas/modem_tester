import sys, os
import click
import time
from tqdm import tqdm
from termcolor import colored, cprint
from pyfiglet import Figlet

from lib.serialAPI import SerialApi
from pprint import pprint

sapi = SerialApi()

__version__ = "0.0.1"


def headerMessage():
    """headerMessage
    This function create a Figlet text from the header message
    """
    f = Figlet(font="standard", justify="center")
    print(colored(f.renderText("PDX MODEM TESTER"), "green", attrs=["bold"]))

def libraryDescription():
    print("="*(os.get_terminal_size().columns))
    cprint("Description: Library for testing modems with serial interface.")
    cprint("Author: Eden Candelas")
    cprint("Version: 0.0.1")
    print("="*(os.get_terminal_size().columns))

@click.group()
def main():
    """
    Simple testing library for modems
    """
    pass


@main.command()
def show():
    """
    Show the list of the current serial devices.
    """
    for i in tqdm (range (101), 
               desc="Buscando dispositivios...", 
               ascii=False, ncols=75):
        time.sleep(0.01)

    listDevices = sapi.availableDevices()  
    if len(listDevices) > 0:
        cprint("Dispositivos encontrados {}:".format(len(listDevices)), "green")
    else:
        cprint("No se encontraron dispositivos", "red")
    for count, device in enumerate(listDevices):
        click.echo("[{}] {}".format(count,device))

@main.command()
@click.option('--modulo', help='Tipo de modulo a usar [BG95, SIM5320]')
@click.option('--port', help='Direccion del puerto serial')
@click.option('--baudrate', help='Frecuencia de baudios')
@click.argument('modulo')
@click.argument('puerto')
@click.argument('baudrate')
def test(serial,port, baudrate):
    """
    Testing the connection of the device.
    """
    print(serial)
    print(port)
    print(baudrate)
    click.echo("Testing modem")

@main.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

@main.command()
def version():
    """
    Show the version of the library
    """
    click.echo(__version__)

if __name__ == "__main__":
    main()

