from time import time
import sys
import serial
import Quectel_BG95.CommandsBG95 as CommandsBG95
import time

CTRL_Z = chr(26)

class Modem:

    serial = serial.Serial()

    def __init__(self, port, baudrate ):
        self.estado_actual = "inicio"
        self.serial.baudrate = baudrate
        self.serial.port = port
        self.comandos = CommandsBG95.Commands(self.serial)
        self.port = port
        self.baudrate = baudrate
    
    def init(self):
        print('[bg95]Abriendo puerto . . .')
        time.sleep(2)
        try:
            self.serial.open()
            print("[bg95]puerto {} abierto".format( self.serial.name))
        # self.estado_actual = "open"
            if self.comandos.bg95_cmd_at.send():
                self.estado_actual = "open"
            else:
                self.estado_actual = "cerrado"

        except Exception as e:
            print('[bg95]Error on ser.open(): %s' % e)
            self.estado_actual = "no port"

    def close(self):
        try:
            self.serial.close()
            print("[bg95]puerto {} cerrado".format(self.serial.name))
            self.estado_actual = "cerrado"
        except Exception as e:
            print('[bg95]Error on ser.close(): %s' % e) 
            self.estado_actual = "error"

    def terminate(self):
        print("[bg95] Termina y reinicia")
        self.comandos.bg95_cmd_softreset.send()
        time.sleep(5)
        self.close()
        print("[bg95] Adios")
        sys.exit() 

    def exit_no_port(self):
        print("[bg95] Puerto no encontrado")
        print("[bg95] Adios")
        sys.exit(2) 
    
    def timer(self, t_inicio, delay):
        self.actual_time = time.time()
        if (self.actual_time - t_inicio) > delay: 
            return False
        else:
            return True

    def check_server_response(self, response_str, ok_value):
        if ok_value in response_str:
            print("[bg95]response ok")
            return True
        else:
            print("[bg95]response unknown")
            return False
    
    def wait_for_server_response(self, timeout):
        self.initial_time = time.time()
        self.serial_time = 0
        self.datarx = ""

        while self.timer(self.initial_time, timeout):
            if self.serial.in_waiting > 0:
                while self.serial.in_waiting > 0:
                    self.x = self.serial.read()
                    self.datarx += self.x.decode()
                    time.sleep(0.01)
                print(self.datarx)
                self.serial_time = time.time()
                print ("serial time: {}".format(self.serial_time))
                return self.datarx
            else: 
                #do nothing
                continue
    
        self.timeout_time = time.time()
        print (f"[bg95]timeout time: {self.timeout_time}")
        print("[bg95]No response")
        return ""

    def write_to_server(self, data):
        self.datatx = data
        self.serial.write(self.datatx.encode())
        self.serial.write(CTRL_Z.encode())
    
    #ESTADOS
    
    def attach(self):
        self.comandos.bg95_cmd_at.send()
        self.comandos.bg95_cmd_ate.send()
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

        elif self.estado_actual == "open":
            self.attach()

        elif self.estado_actual == "attached":
            self.connect()

        elif self.estado_actual == "conectado":
            self.send()
        
        elif self.estado_actual == "receive":
            self.receive()
        
        elif self.estado_actual == "completo":
            self.terminate()

        elif self.estado_actual == "cerrado":
            self.terminate()

        elif self.estado_actual == "error":
            self.terminate()

        elif self.estado_actual == "no port":
            self.exit_no_port()

        else:
            print("[bg95] Adios")
            sys.exit()

    def run(self):
        while True:
            self.fsm()
            time.sleep(0.1)