from time import time
import sys
import serial
from Modem import Modem
from lib.utilidades import Utilidades
import Quectel_BG95.CommandsBG95 as CommandsBG95
import time

CTRL_Z = chr(26)

systemUtils = Utilidades()

class ModuloBG95(Modem):

    serial = serial.Serial()

    def __init__(self, port, baudrate, url, portServer, payload ):
        Modem.__init__(self, port, baudrate)
        self.estadoFSM = "inicio"
        self.url = url
        self.portServer = portServer
        self.payload = payload
        self.comandos = CommandsBG95.Commands(self.serial)
        systemUtils.printSuccessCLI("[cmt]Modem BG95 creado")

    #ESTADOS

    def config(self):
        if self.comandos.bg95_cmd_at.send() == False:
            self.estado_fsmConfig = "error"
            return
 
        if self.comandos.bg95_cmd_ate.send() == False:
            self.estado_fsmConfig = "error"
            return

        self.estado_fsmConfig = "ok"

            
    def attach(self):
        if self.comandos.bg95_cmd_cereg.send() == False:
            self.estado_fsmAttach = "error"
            return
        if self.comandos.bg95_cmd_qicsgp.send() == False:
            self.estado_fsmAttach = "error"
            return
        if self.comandos.bg95_cmd_cgattQ.send() == False:
            self.estado_fsmAttach = "error"
            return
        if self.comandos.bg95_cmd_copsQ.send() == False:
            self.estado_fsmAttach = "error"
            return
        if self.comandos.bg95_cmd_qiactQ.send()  == False:
            self.estado_fsmAttach = "error"
            return

        self.estado_fsmAttach = "ok"


    def connect(self):
        self.result = self.comandos.bg95_cmd_qiopen.send()
        print(f"[bg95] qiopen.datarx: {self.comandos.bg95_cmd_qiopen.datarx}")
        if self.result:
            self.status_response = self.check_server_response(self.comandos.bg95_cmd_qiopen.datarx, "+QIOPEN:") 
            if self.status_response:
                print("[bg95]open answer") 
                self.status_response = self.check_server_response(self.comandos.bg95_cmd_qiopen.datarx, "+QIOPEN: 0,0")
                if self.status_response:
                    systemUtils.printSuccessCLI("[bg95] ========= conectado =========\r\n")
                    self.estado_actual = "conectado"
                else:
                    systemUtils.printErrorCLI("[bg95] error al abrir puerto")
                    self.estado_actual = "error"
                    #TODO manejar error
            else:
                self.response_str = self.wait_for_server_response(20)
                self.status_response = self.check_server_response(self.response_str, "+QIOPEN: 0,0")
                if self.status_response:
                    systemUtils.printSuccessCLI("[bg95] ========= conectado =========\r\n")
                    self.estado_actual = "conectado"
                else:
                    systemUtils.printErrorCLI("[bg95] error al abrir puerto")
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
                systemUtils.printSuccessCLI("[bg95] Send correcto")
                self.estado_actual = "receive"
            else:
                self.comandos.bg95_cmd_qiclose.send()
                systemUtils.printErrorCLI("[bg95]No hubo +QIURC")
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

    def complete():
        pass

    def fsm(self):
        if self.estadoFSM == "inicio":
            self.init()
            if self.estadoModem == "abierto":
                self.estadoFSM = "config"
            else:
                self.estadoFSM = "error_no_port"
        
        elif self.estadoFSM == "config":
            self.config()
            if self.estado_fsmConfig == "ok":
                print(" === Config OK ===")
                self.estadoFSM = "attach"
            else:
                self.estadoFSM = "error_cfg"

        elif self.estadoFSM == "attach":
            self.attach()
            if self.estado_fsmAttach == "ok":
                print(" === Attach OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_attach"

        elif self.estadoFSM == "connect":
            self.connect()
            if self.estado_fsmConnect == "ok":
                print(" === Connect OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_connect"

        elif self.estadoFSM == "send":
            self.send()
            if self.estado_fsmSend == "ok":
                print(" === Connect OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_send"            
        
        elif self.estadoFSM == "receive":
            self.receive()
            if self.estado_fsmReceive == "ok":
                print(" === Connect OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_receive"   
        
        elif self.estadoFSM == "complete":
            self.complete()
            if self.estado_fsmReceive == "ok":
                print(" === Connect OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_receive"  

        elif self.estadoFSM == "cerrar":
            self.close()

        elif self.estadoFSM == "error_no_port" :
            print("[SIM5320] Puerto no encontrado")
            print("[SIM5320] Adios")
            sys.exit(2) 

        elif self.estadoFSM == "error_cfg":
            self.close()
            self.estadoFSM = "none"

        # elif self.estadoFSM == "no port":
        #     self.exit_no_port()

        else:
            print("[bg95] Adios")
            sys.exit()

    def run(self):
        while True:
            self.fsm()
            time.sleep(0.1)