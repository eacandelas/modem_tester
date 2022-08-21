from time import time
import sys
import serial
from Modem import Modem
from lib.utilidades import Utilidades
import Quectel_BC660K.CommandsBC660K as CommandsBC660K
import time

CTRL_Z = chr(26)

systemUtils = Utilidades()

class ModuloBC660K(Modem):

    def __init__(self, port, baudrate, url, portServer, payload ):
        Modem.__init__(self, port, baudrate)
        self.estadoFSM = "inicio"
        self.url = url
        self.portServer = portServer
        self.payload = payload
        self.automata = False       #TODO definir para envios periodicos
        self.salir    = True        #TODO añadir logica para forzar salida de programa
        self.comandos = CommandsBC660K.Commands(self.serial)
        systemUtils.printSuccessCLI("[BC660K]Modem BG95 creado")

    #ESTADOS

    def config(self):
        self.comandos.bc660k_cmd_at.send()


        # if self.comandos.bc660k_cmd_at.send() == False:
        #     self.estado_fsmConfig = "error"
        #     return
 
 
        if self.comandos.bc660k_cmd_ate0.send() == False:
            self.estado_fsmConfig = "error"
            return
 
        if self.comandos.bc660k_cmd_qband.send() == False:
            self.estado_fsmConfig = "error"
            return

        if self.comandos.bc660k_cmd_eviotevt.send() == False:
            self.estado_fsmConfig = "error"
            return

        if self.comandos.bc660k_cmd_cereg.send() == False:
            self.estado_fsmConfig = "error"
            return

        self.estado_fsmConfig = "ok"

    def contexto(self):

        if self.comandos.bc660k_cmd_qgmr.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_qccid.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_cpsmsq.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_cedrx.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_qeng.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_contrdp.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_ceregq.send() == False:
            self.estado_fsmContexto = "error"
            return

        if self.comandos.bc660k_cmd_cregq.send() == False:
            self.estado_fsmContexto = "error"
            return



        self.estado_fsmContexto = "ok"

            
    def attach(self):
        if self.comandos.bc660k_cmd_cgpaddr.send() == False:
            self.estado_fsmAttach = "error"
            return

        if self.comandos.bc660k_cmd_dnscfg.send() == False:
            self.estado_fsmAttach = "error"
            return

        self.estado_fsmAttach = "ok"


    def connect(self):
        if self.comandos.bc660k_cmd_qmtopen.send() == False:
            self.estado_fsmConnect = "error"
            return

        if self.comandos.bc660k_cmd_qmtconn.send() == False:
            self.estado_fsmConnect = "error"
            return

        self.estado_fsmConnect = "ok"
    
    def send(self):
        print("[BC660K] send")
        if self.comandos.bc660k_cmd_qmtpub.send() == False:
                self.estado_fsmSend = "error"
                return

        if self.comandos.bc660k_cmd_payload.send() == False:
                self.estado_fsmSend = "error"
                return

        self.estado_fsmSend = "ok"

    def receive(self):
        self.response_str = self.wait_for_server_response(20)
        self.status_response = self.check_server_response(self.response_str, "+QIURC: \"recv\"")
        if  self.status_response:          
            print("[BC660K] receive hay datos desde server")
            self.comandos.bg95_cmd_qird.send()
            self.comandos.bg95_cmd_qiclose.send()
            self.estado_fsmReceive = "completo"
        else:
            self.comandos.bg95_cmd_qiclose.send()
            print("[BC660K]No hubo +QIURC")
            self.estado_fsmReceive = "error"

    def complete(self):
        
        self.estado_fsmComplete = "ok"

    def idle(self):
        #do nothing
        pass

    def fsm(self):
        if self.estadoFSM == "inicio":
            self.init()
            if self.estadoModem == "abierto":
                self.estadoFSM = "config"
                time.sleep(5)
            else:
                self.estadoFSM = "error_no_port"
        
        elif self.estadoFSM == "config":
            self.config()
            if self.estado_fsmConfig == "ok":
                print(" === Config OK ===")
                self.estadoFSM = "contexto"
            else:
                self.estadoFSM = "error_cfg"
        
        elif self.estadoFSM == "contexto":
            self.contexto()
            if self.estado_fsmContexto == "ok":
                print(" === Contexto OK ===")
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
                self.estadoFSM = "send"
            else:
                self.estadoFSM = "error_connect"

        elif self.estadoFSM == "send":
            self.send()
            if self.estado_fsmSend == "ok":
                print(" === Send OK ===")
                self.estadoFSM = "complete"
            else:
                self.estadoFSM = "error_send"            
        
        elif self.estadoFSM == "receive":
            self.receive()
            if self.estado_fsmReceive == "ok":
                print(" === Receive OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_receive"   
        
        elif self.estadoFSM == "complete":
            self.complete()
            if self.estado_fsmComplete == "ok" and self.salir == True:
                print(" === Complete OK ===")
                self.estadoFSM = "cerrar"
            elif self.estado_fsmComplete == "ok" and self.salir == False:
                print(" === Complete OK ===")
                self.estadoFSM = "idle"
            else:
                self.estadoFSM = "error_receive"  

        elif self.estadoFSM == "idle":
            self.idle()
            if self.estado_fsmIdle == "ok":
                print(" === Idle OK ===")
                self.estadoFSM = "connect"
            else:
                self.estadoFSM = "error_receive"  

        elif self.estadoFSM == "cerrar":
            self.close()
            if self.salir == True:
                self.estadoFSM = "salir"
            elif self.salir == False:
                self.estadoFSM = "salir"
            else:
                self.estadoFSM = "error_receive"  

        elif self.estadoFSM == "error_no_port" :
            print("[BC660K] Puerto no encontrado")
            print("[BC660K] Adios")
            sys.exit(2) 

        elif self.estadoFSM == "error_cfg":
            self.close()
            self.estadoFSM = "none"

        elif self.estadoFSM == "error_default":
            print("[BC660K] Error default -> Close y Exit")
            self.close()
            sys.exit(2) 

        elif self.estadoFSM == "salir":
            print("[BC660K] Salir")
            sys.exit()

        else:
            print("[BC660K] Adios")
            sys.exit()

    def run(self):
        while True:
            self.fsm()
            time.sleep(0.1)