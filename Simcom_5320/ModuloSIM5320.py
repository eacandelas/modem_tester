from time import time
import serial
from Modem import Modem
import Simcom_5320.CommandsSIM5320 as CommandsSIM5320
import time
import sys

CTRL_Z = chr(26)

class Modulo5320(Modem):
    
    serial = serial.Serial()

    def __init__(self, port, baudrate, url, portServer, payload ):
        Modem.__init__(self, port, baudrate)
        self.estado_actual = "none"
        self.url = url
        self.portServer = portServer
        self.payload = payload
        self.comandos = CommandsSIM5320.Commands(self.serial)
        print("[cmt]Modem SIM5320 creado")


    def fsm(self):
        if self.estado_actual == "inicio":
            self.init()
            if self.estadoModem == "abierto":
                self.estadoFSM = "open"
            else:
                self.estadoFSM = "error"

        # elif self.estado_actual == "open":
        #     self.attach()

        # elif self.estado_actual == "attached":
        #     self.connect()

        # elif self.estado_actual == "conectado":
        #     self.send()
        
        # elif self.estado_actual == "receive":
        #     self.receive()
        
        # elif self.estado_actual == "completo":
        #     self.terminate()

        # elif self.estado_actual == "cerrado":
        #     self.terminate()

        elif self.estado_actual == "error":
            self.exit_no_port()

        # elif self.estado_actual == "no port":
        #     self.exit_no_port()

        else:
            print("[bg95] Adios")
            sys.exit()

    def run(self):
        # self.init()
        while True:
            self.fsm()
            time.sleep(0.1)