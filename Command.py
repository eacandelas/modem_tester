import time
#TODO Command solo debe traer los parametros elaborados del comando.
class Command:
    ERROR_COUNT_MAX = 3
    error_count = 0

    def __init__(self, name, cmd, timeout, ok_val, modem):
        self.name = name
        self.cmd = cmd
        self.timeout = timeout
        self.ok_val = ok_val
        self.modem = modem

    def __str__(self) -> str:
        return f"Comando: {self.name} - String: {self.cmd}\r\nTimeout: {self.timeout} - OkVal: {self.ok_val}" 

    def timer(self, t_inicio, delay):
        self.actual_time = time.time()
        if (self.actual_time - t_inicio) > delay: 
            return False
        else:
            return True

    def check_response(self, response_str, ok_value):
        if ok_value in response_str:
            print("[cmd]cmd ok")
            return True
        else:
            print("[cmd]cmd wrong")
            return False

    def get_response(self, timeout):
        self.datarx = ""
        self.initial_time = time.time()
        print ("initial time: {}".format(self.initial_time))

        while self.timer(self.initial_time, timeout):
            if self.modem.in_waiting > 0:
                while self.modem.in_waiting > 0:
                    self.x = self.modem.read()
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
        print (f"[cmd]timeout time: {self.timeout_time}")
        print("[cmd]No response")
        return ""

    def send(self):
        print(f"[cmd] Send {self.cmd}")
        if self.modem.is_open == True:
            self.modem.write(self.cmd.encode())
            while self.error_count < self.ERROR_COUNT_MAX: 
                self.str_response = self.get_response(self.timeout)
                status_response = self.check_response(self.str_response, self.ok_val)
                if status_response:
                    return True
                else:
                    self.error_count += 1
            
            return False 

        else:
            print("[cmd]Puerto no abierto")
            return False