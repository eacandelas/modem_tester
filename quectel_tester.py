
from operator import mod
import sys
import os
import subprocess
import signal
from wsgiref import simple_server
import click
import time
import getopt
from tqdm import tqdm
from termcolor import colored, cprint
from pyfiglet import Figlet
from pprint import pprint
from threading import Thread, ThreadError
from lib.serialAPI import SerialApi
from lib.webService import WebService
from lib.utilidades import Utilidades
from Quectel_BG95.ModuloBG95 import ModuloBG95 as BG95
from Simcom_5320.ModuloSIM5320 import Modulo5320 as SIM5320

class TesterCLI:
    def __init__(self):
        self.listadoModulos = {
            "BG95": BG95,
            "SIM5320": SIM5320
        }
        self.sapi = SerialApi()
        self.puerto = self.sapi.sistemComPort()
        self.baudrate = 115200
        self.tipoModulo = "BG95" 
        self.mode   = "param_mode"
        self.modulo  = None
    
    def listadoModulosDisponibles(self):
        """
        Listado de modulos disponibles.
        """
        return self.listadoModulos
    
    def headerConfiguration(self):
        """
        Configuracion del header del programa.
        """
        systemUtils.headerCLI(" Configuracion del tester ")
        click.echo("Puerto: {}".format(self.puerto))
        click.echo("Baudrate: {}".format(self.baudrate))
        click.echo("Modulo: {}".format(self.tipoModulo))
        click.echo("Modo: {}".format(self.mode))
        click.echo("")

    def interrumpirCli(self):
        """
        Interrumpir la ejecucion del programa.
        """
        print("Interrumpiendo CLI")
        sys.exit(0)
class Tester:
    def __init__(self):
        self.puerto = "COM1"
        self.baudrate = 115200
        self.tipoModulo = "BG95" 
        self.mode   = "param_mode"
        self.modulo  = None
        self.serialUtilidades = SerialApi()

    def procesar_parametros_entrada(self, argv):

        arg_help = "\r\n[cmt]{0} -p <puerto> -b <bauds> -m <modulo>\r\n".format(argv[0])

        try:
            opts, args = getopt.getopt(argv[1:], "h:p:b:m:", ["help", "puerto=", "bauds=", "modulo="])
        except:
            print(arg_help)
            sys.exit(2)

        if len(argv) == 1:
            print("Input mode")
            self.mode = "input_mode"
            return self.mode
        elif len(argv) == 7:
            print("Param mode")
            self.mode = "param_mode"

        else:
            print("[cmt]Debe especificar los tres parametros")
            print(arg_help)
            sys.exit(2)
        
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(arg_help)  # print the help message
                sys.exit(2)
            elif opt in ("-p", "--puerto"):
                self.puerto = arg
            elif opt in ("-b", "--bauds"):
                self.bauds = arg
            elif opt in ("-m", "--modulo"):
                self.tipoModulo = arg

        print("[cmt]puerto: {}".format(self.puerto))
        print('[cmt]bauds: {}'.format(self.bauds))
        print('[cmt]tipoModulo: {}'.format(self.tipoModulo))

    def obtener_parametros_cli(self): 
        if self.mode == "input_mode":
            self.tipoModulo = input("Ingresa modulo [BG95, SIM5320]: ")
            self.port = input("Ingresa puerto: ")
            self.baudrate = int(input("Ingresa baudrate: "))
        
        self.url = input("ingresa url: ")
        self.serverPort = input("Ingresa puerto: ")
        self.payload = input("Ingresa payload: ")

        print(f"\r\n======== tester params =======")
        print(f"Tipo Modulo: {self.tipoModulo}")
        print(f"Serial: {self.port} - {self.baudrate}")
        print(f"Server: {self.url}:{self.serverPort}")
        print(f"Payload: {self.payload}")
        print(f"================================\r\n")

        self.estado_actual = "none"

   
    def crear_modulo(self):

        if self.tipoModulo == "BG95":
            self.modulo = BG95(self.port, int(self.baudrate), self.url, self.serverPort, self.payload)
        elif self.tipoModulo == "SIM5320":
            self.modulo = SIM5320(self.port, int(self.baudrate), self.url, self.serverPort, self.payload)
        else:
            print("[cmt]Modulo desconocido ")
            sys.exit(2)

    def run(self):
        self.modulo.run()
 
@click.group()
@click.pass_context
def mainTester(ctx):
    """
    Simple testing library for modems.
    """
    ctx.obj = {}
    pass

@mainTester.command()
@click.option('--module', '-m', nargs=3, type=click.Tuple([str, str,int]), help='Module type, port and baudrate', required=True)
def test(module):
    """
    Tester el modulo de comunicacion.
    """
    modulo, puerto, baudrate = module
    try:
        listadoModulos = testercli.listadoModulosDisponibles()
        if modulo in listadoModulos:
            print("Aqui se configura el modulo")
        else:
            systemUtils.printErrorCLI("Modulo {} no soportado".format(modulo))
    except Exception as e:
        print(e)
        sys.exit(2)
    
@mainTester.command()
def run():
    """
    Ejecuta el tester
    """
    #Configuracion puerto serie
    testercli.headerConfiguration()
    listadoModulos = testercli.listadoModulosDisponibles()
    systemUtils.headerCLI(" Puertos seriales disponibles ")
    serialDevicesAvailable = sapi.availableDevices()
    for count, serialDevice in enumerate(serialDevicesAvailable):
        click.echo("[{}] {}".format(count,serialDevice))
    
    serialDeviceSelected = click.prompt('Selecciona el numero del puerto serial: ', type=int)
    testercli.puerto = serialDevicesAvailable[serialDeviceSelected]
    click.clear()
    testercli.headerConfiguration()

    #Configuracion baudrate
    systemUtils.headerCLI(" Baudrates disponibles ")
    listaBaudrate = sapi.listadoBaudratesDisponibles()
    for count, baudrate in enumerate(listaBaudrate):
        click.echo("[{}] {}".format(count, baudrate))
    baudrateSelected = click.prompt('Selecciona el numero del baudrate: ', type=int)
    testercli.baudrate = listaBaudrate[baudrateSelected]
    click.clear()
    testercli.headerConfiguration()
    #Configuracion del modulo
    systemUtils.headerCLI(" Modulos disponibles ")
    modulosDisponibles = listadoModulos.keys()
    arrayModulosDisponibles = list(modulosDisponibles)
    for count, modulo in enumerate(modulosDisponibles):
        click.echo("[{}] {}".format(count,modulo))
    moduloSelected = click.prompt('Selecciona el numero del modulo: ', type=int)
    testercli.tipoModulo = arrayModulosDisponibles[moduloSelected]
    testercli.modulo = listadoModulos[testercli.tipoModulo](testercli.puerto, testercli.baudrate, "localhost", 5000, "Hola mundo")
    click.clear()
    testercli.headerConfiguration()
    
    if click.confirm('Es correcta la configuracion?'):
        click.echo("Lanzar el modulo aqui")
        testercli.estado_actual = "inicio"
        testercli.modulo.run()
    else:
        click.clear()
        os.system("python quectel_tester.py run")

@mainTester.command()
def show():
    """
    Muestra la lista de los dispositivos seriales disponibles.
    """
    systemUtils.headerCLI(" Buscar dispositivos seriales ")
    listDevices = sapi.availableDevices()  
    for i in tqdm (range (100),
               desc="Buscando dispositivios...", 
               ascii=False, ncols=75):
        time.sleep(0.01)

    if len(listDevices) > 0:
        systemUtils.printSuccessCLI("Dispositivos encontrados {}:".format(len(listDevices)))
        for count, device in enumerate(listDevices):
            click.echo("[{}] {}".format(count,device))
    else:
        systemUtils.printWarningCLI("No se encontraron dispositivos seriales")
    

@mainTester.command()
def modulos():
    """
    Muestra los modulos disponibles.
    """
    systemUtils.headerCLI(" Listado Modulos disponibles ")
    listadoModulos = testercli.listadoModulosDisponibles()
    for count, modulo in enumerate(listadoModulos.keys()):
        click.echo("[{}] {}".format(count,modulo))
    

@mainTester.command()
def web():
    """
    Corre un servidor de pruebas.
    """
    systemUtils.headerCLI(" Correiendo servidor de pruebas ")
    systemUtils.printSuccessCLI("Servidor corriendo en http://localhost:5000")
    webService.runWebService()

@mainTester.command()
def stop():
    """
    Detiene el servidor web.
    """
    systemUtils.headerCLI(" Detener servidor web ")
    webService.stopWebService()
    systemUtils.printSuccessCLI("Servidor web detenido")


@mainTester.command()
@click.argument('subcommand')
@click.pass_context
def help(ctx, subcommand):
    """
    Muestra la descripcion de la funciona seleccionada.
    """
    subcommand_obj = mainTester.get_command(ctx, subcommand)
    if subcommand_obj is None:
        click.echo("I don't know that command.")
    else:
        click.echo(subcommand_obj.get_help(ctx))

if __name__ == '__main__':
    testercli   = TesterCLI()
    sapi        = SerialApi()
    systemUtils = Utilidades()
    webService  = WebService()
    threadWebservice = Thread(target=webService.runWebService)
    mainTester()
    signal.signal(signal.SIGINT, testercli.interrumpirCli)


        
