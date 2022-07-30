from time import time
import serial
import Simcom_5320.CommandsSIM5320 as CommandsSIM5320
import time
import sys

CTRL_Z = chr(26)

class Modem:
    
    serial = serial.Serial()

    def __init__(self, port, baudrate ):
        self.estado_actual = "inicio"
        self.serial.baudrate = baudrate
        self.serial.port = port
        self.comandos = CommandsSIM5320.Commands(self.serial)

    def init(self):
        print('[sim5320]Abriendo puerto . . .')
        time.sleep(2)
        try:
            self.serial.open()
            print("[sim5320]puerto {} abierto".format( self.serial.name))
        # self.estado_actual = "open"
            if self.comandos.bg95_cmd_at.send():
                self.estado_actual = "open"
            else:
                self.estado_actual = "cerrado"

        except Exception as e:
            print('[sim5320]Error on ser.open(): %s' % e)
            self.estado_actual = "no port"

    def close(self):
        try:
            self.serial.close()
            print("[sim5320]puerto {} cerrado".format(self.serial.name))
            self.estado_actual = "cerrado"
        except Exception as e:
            print('[sim5320]Error on ser.close(): %s' % e) 
            self.estado_actual = "error"

    def terminate(self):
        print("[sim5320] Termina y reinicia")
        self.comandos.bg95_cmd_softreset.send()
        time.sleep(5)
        self.close()
        print("[sim5320] Adios")
        sys.exit() 

    def exit_no_port(self):
        print("[sim5320] Puerto no encontrado")
        print("[sim5320] Adios")
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

    def get_inputs(self): 
        self.port = input("Ingresa puerto: ")
        self.baudrate = int(input("Ingresa baudrate: "))
        self.url = input("ingresa url: ")
        self.port = input("Ingresa puerto: ")
        self.payload = input("Ingresa payload")

        print(f"======== tester params =======")
        print(f"{self.port} - {self.baudrate}")
        print(f"{self.url}:{self.port}")
        print(f"{self.payload}")

        self.estado_actual = "none"


    def fsm(self):
        if self.estado_actual == "inputs":
            self.get_inputs()

        # if self.estado_actual == "inicio":
        #     self.get_inputs()

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

        # elif self.estado_actual == "error":
        #     self.terminate()

        # elif self.estado_actual == "no port":
        #     self.exit_no_port()

        else:
            print("[bg95] Adios")
            sys.exit()

    def run(self):
        self.get_inputs()
        while True:
            self.fsm()
            time.sleep(0.1)