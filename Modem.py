from time import time
import serial
# import Simcom_5320.CommandsSIM5320 as CommandsSIM5320
import time
import sys

CTRL_Z = chr(26)

#TODO Modem trae la logica de envio que trae Command. Debe ser el driver hacia el dispositivo fisico.

class Modem(object):
    
    serial = serial.Serial()

    def __init__(self, port, baudrate ):
        # self.estado_actual = "inicio"
        self.serial.baudrate = baudrate
        self.serial.port = port
        self.estadoModem = "cerrado"
 

    def init(self):
        print('[modem]Abriendo puerto . . .')
        time.sleep(2)
        try:
            self.serial.open()
            print("[modem]puerto {} abierto".format( self.serial.name))
            self.estadoModem = "abierto"
        except Exception as e:
            print('[modem]Error on ser.open(): %s' % e)
            self.estadoModem = "error_no_port"

    def close(self):
        try:
            self.serial.close()
            print("[modem]puerto {} cerrado".format(self.serial.name))
            self.estadoModem = "cerrado"
        except Exception as e:
            print('[modem]Error on ser.close(): %s' % e) 
            self.estadoModem = "error_on_close"

    def terminate(self):
        print("[modem] Termina y reinicia")
        time.sleep(5)
        self.close()


    def exit_no_port(self):
        print("[modem] Puerto no encontrado")
        print("[modem] Adios")
        sys.exit(2) 
    
    def timer(self, t_inicio, delay):
        self.actual_time = time.time()
        if (self.actual_time - t_inicio) > delay: 
            return False
        else:
            return True

    def check_server_response(self, response_str, ok_value):
        if ok_value in response_str:
            print("[modem]response ok")
            return True
        else:
            print("[modem]response unknown")
            return False
    
    def wait_for_port_response(self, timeout):
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
                print ("[modem]serial time: {}".format(self.serial_time))
                return self.datarx
            else: 
                #do nothing
                continue
    
        self.timeout_time = time.time()
        print (f"[modem]timeout time: {self.timeout_time}")
        print("[modem]No response")
        return ""

    def write_to_port(self, data):
        self.datatx = data
        self.serial.write(self.datatx.encode())
        self.serial.write(CTRL_Z.encode())