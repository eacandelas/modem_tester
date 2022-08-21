from time import time
import serial
from Modem import Modem
import Simcom_5320.CommandsSIM5320 as CommandsSIM5320
import time
import sys

CTRL_Z = chr(26)

class Modulo5320(Modem):


    def __init__(self, port, baudrate, url, portServer, payload ):
        Modem.__init__(self, port, baudrate)
        self.estadoFSM = "inicio"
        self.url = url
        self.portServer = portServer
        self.payload = payload
        self.comandos = CommandsSIM5320.Commands(self.serial)
        print("[cmt]Modem SIM5320 creado")

#ESTADOS
    def config(self):
        if self.comandos.at.send() == False:
            self.estado_fsmConfig = "error"
            return
        
        if self.comandos.ate.send() == False:
            self.estado_fsmConfig = "error"
            return

        if self.comandos.ccid.send() == False:
            self.estado_fsmConfig = "error"  
            return

        if self.comandos.srip.send() == False:
            self.estado_fsmConfig = "error"  
            return

        if self.comandos.xget.send() == False:
            self.estado_fsmConfig = "error"  
            return

        if self.comandos.netclose.send() == False:
            self.estado_fsmConfig = "error" 
            return

        print("[sim5320] ========= inited =========\r\n")

        self.estado_fsmConfig = "ok"
    
    def attach(self):
        
        self.estado_fsmAttach = "error"
        for i in 3:
            if self.comandos.creg.send() == False:
                pass
            else:
                self.estado_fsmAttach = "pass"
                break
        
        if self.estado_fsmAttach == "error":
            return

        print("[sim5320] creg ok\r\n")
        
        if self.comandos.csq.send() == False:
            self.estado_fsmAttach = "error" 
            return 
        
        if self.comandos.gsock.send() == False:
            self.estado_fsmAttach = "error" 
            return 
        
        if self.comandos.sockset.send() == False:
            self.estado_fsmAttach = "error" 
            return 
        
        if self.comandos.cipmode.send() == False:
            self.estado_fsmAttach = "error" 
            return 
        
        if self.comandos.netopen.send() == False:
            self.estado_fsmAttach = "error" 
            return 
        
        if self.comandos.ipaddr.send() == False:
            self.estado_fsmAttach = "error" 
            return 
        print("[sim5320] ========= attached =========\r\n")

        self.estado_fsmAttach = "ok"

    def connect(self):

        if self.comandos.tcpconnect.send() == False:
            self.estado_fsmAttach = "error" 
            return   

        print("[sim5320] ========= conectado =========\r\n")

        self.estado_fsmConnect = "ok"
    
    def send(self):
        print("[sim5320] sending")
        self.comandos.update_tcpwrite_data("all your base belong to us")
        print(f"[sim5320] {self.comandos.tcpwrite.cmd}")
        if self.comandos.tcpwrite.send() == False:
            self.estado_fsmAttach = "error" 
            return  
        if self.status_response:
            self.write_to_server(f"{self.comandos.dataToSend}\r\n")
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

    def complete(self):
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
                self.estadoFSM = "attach"
            else:
                self.estadoFSM = "error_cfg"

        elif self.estadoFSM == "attach":
            self.attach()
            if self.estado_fsmAttach == "ok":
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_attach"

        elif self.estadoFSM == "connect":
            self.connect()
            if self.estado_fsmConnect == "ok":
                self.estadoFSM = "send"
            else:
                self.estadoFSM = "error_connect"

        elif self.estadoFSM == "send":
            self.send()
            if self.estado_fsmConnect == "ok":
                self.estadoFSM = "receive"
            else:
                self.estadoFSM = "error_send"
        
        elif self.estadoFSM == "receive":
            self.receive()
            if self.estado_fsmConnect == "ok":
                self.estadoFSM = "receive"
            else:
                self.estadoFSM = "error_receive"
        
        # elif self.estado_actual == "completo":
        #     self.terminate()

        # elif self.estado_actual == "cerrado":
        #     self.terminate()

        elif self.estadoFSM == "error_no_port":
            self.exit_no_port()

        else:
            print("[bg95] Adios")
            sys.exit()

    def run(self):
        # self.init()
        while True:
            self.fsm()
            time.sleep(0.1)