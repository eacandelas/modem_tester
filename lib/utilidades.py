import os
import click
import datetime
class Utilidades:
    def __init__(self) -> None:
        pass
    @staticmethod
    def headerCLI(titulo="Quectel Tester"):
        """Imprime el encabezado de la CLI"""
        terminalRows = os.get_terminal_size().columns
        stringLength = len(titulo)
        totalEspaciado = (terminalRows - stringLength) / 2
        print("="*int(totalEspaciado), end="")
        print(titulo, end="")
        print("="*int(totalEspaciado))
    def printErrorCLI(self, mensaje):
        """Imprime el mensaje de error en la CLI"""
        click.secho("[Error] ", fg="red", bold=True, nl=False)
        click.secho(mensaje)
    def printSuccessCLI(self, mensaje):
        """Imprime el mensaje de exito en la CLI"""
        click.secho("[Exito] ", fg="green", bold=True, nl=False)
        click.secho(mensaje)
    def printWarningCLI(self, mensaje):
        """Imprime el mensaje de advertencia en la CLI"""
        click.secho("[Advertencia] ", fg="yellow", bold=True, nl=False)
        click.secho(mensaje)
    def printWebServiceMessage(self, mensaje):
        """Imprime el mensaje de la API en la CLI"""
        click.secho("[API] ", fg="blue", bold=True, nl=False)
        click.secho(mensaje)
    def printLogMessage(self, mensaje):
        """Imprime el mensaje de log en el CLI"""
        click.secho("[Log - {}] ".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), fg="magenta", bold=True, nl=False)
        click.secho(mensaje)