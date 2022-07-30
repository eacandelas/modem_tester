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
        self.estadoFSM = "none"
        self.url = url
        self.portServer = portServer
        self.payload = payload
        self.comandos = CommandsSIM5320.Commands(self.serial)
        print("[cmt]Modem SIM5320 creado")

#ESTADOS

    def config(self):
        if self.comandos.bg95_cmd_at.send() == False:
            self.estadoFSM = "error_at"
        else:
            self.comandos.bg95_cmd_ate.send()
    
    def attach(self):
        self.comandos.bg95_cmd_cereg.send()
        self.comandos.bg95_cmd_qicsgp.send()
        self.comandos.bg95_cmd_cgattQ.send()
        self.comandos.bg95_cmd_copsQ.send()
        result = self.comandos.bg95_cmd_qiactQ.send() #TODO agregar busqueda de IP
        if result:
            print("[bg95] ========= attached =========\r\n")
            self.estado_actual = "attached"
        else:
            print("[bg95] falla en attach")
            self.estado_actual = "open"

    def connect(self):
        self.result = self.comandos.bg95_cmd_qiopen.send()
        print(f"[bg95] qiopen.datarx: {self.comandos.bg95_cmd_qiopen.datarx}")
        if self.result:
            self.status_response = self.check_server_response(self.comandos.bg95_cmd_qiopen.datarx, "+QIOPEN:") 
            if self.status_response:
                print("[bg95]open answer") 
                self.status_response = self.check_server_response(self.comandos.bg95_cmd_qiopen.datarx, "+QIOPEN: 0,0")
                if self.status_response:
                    print("[bg95] ========= conectado =========\r\n")
                    self.estado_actual = "conectado"
                else:
                    print("[bg95] error al abrir puerto")
                    self.estado_actual = "error"
                    #TODO manejar error
            else:
                self.response_str = self.wait_for_server_response(20)
                self.status_response = self.check_server_response(self.response_str, "+QIOPEN: 0,0")
                if self.status_response:
                    print("[bg95] ========= conectado =========\r\n")
                    self.estado_actual = "conectado"
                else:
                    print("[bg95] error al abrir puerto")
                    self.estado_actual = "error"
                    #TODO manejar error
        else:
            print("[bg95]Prompt falla")
            self.estado_actual = "error"
    
    def send(self):
        print("[bg95] send")
        self.status_response = self.comandos.bg95_cmd_qisend0.send()
        if self.status_response:
            self.write_to_server("All your base belong to us\r\n")
            self.response_str = self.wait_for_server_response(20)
            self.status_response = self.check_server_response(self.response_str, "SEND OK")
            if  self.status_response:          
                print("[bg95] Send correcto")
                self.estado_actual = "receive"
            else:
                self.comandos.bg95_cmd_qiclose.send()
                print("[bg95]No hubo +QIURC")
                self.estado_actual = "error"

        else:
            print("[bg95] error prompt")
            self.comandos.bg95_cmd_qiclose.send()
            self.estado_actual = "error"

    def receive(self):
        self.response_str = self.wait_for_server_response(20)
        self.status_response = self.check_server_response(self.response_str, "+QIURC: \"recv\"")
        if  self.status_response:          
            print("[bg95] receive hay datos desde server")
            self.comandos.bg95_cmd_qird.send()
            self.comandos.bg95_cmd_qiclose.send()
            self.estado_actual = "completo"
        else:
            self.comandos.bg95_cmd_qiclose.send()
            print("[bg95]No hubo +QIURC")
            self.estado_actual = "error"

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