
import sys
from Quectel_BG95.ModuloBG95 import ModuloBG95 as BG95
from Simcom_5320.ModuloSIM5320 import Modulo5320 as SIM5320
import getopt

class Tester:
    def __init__(self):
        self.puerto = "COM1"
        self.puerto = 115200
        self.tipoModulo = "BG95" 
        self.mode   = "param_mode"
        self.modulo  = None

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
 


if __name__ == '__main__':
    tester = Tester()
    tester.procesar_parametros_entrada(sys.argv)
    tester.obtener_parametros_cli()
    tester.crear_modulo()

    tester.run()


        
