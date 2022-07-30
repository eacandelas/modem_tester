
import sys
import Quectel_BG95.ModemBG95 as ModemBG95
import Simcom_5320.ModemSIM5320 as sim5320
import getopt

#defaults 

g_puerto    = "COM1"
g_bauds     = 9600
g_modulo    = "BG95"
g_mode      = "param_mode"



def cmt_procesar_parametros(argv):
    global g_puerto
    global g_bauds
    global g_modulo
    global g_mode
    arg_help = "\r\n[cmt]{0} -p <puerto> -b <bauds> -m <modulo>\r\n".format(argv[0])



    try:
        opts, args = getopt.getopt(argv[1:], "h:p:b:m:", ["help", "puerto=", "bauds=", "modulo="])
    except:
        print(arg_help)
        sys.exit(2)

    if len(argv) == 1:
        print("input mode")
        g_mode = "input_modem"
    elif len(argv) == 7:
        print("param mode")
        g_mode = "param_mode"

    else:
        print("[cmt]Debe especificar los tres parametros")
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-p", "--puerto"):
            g_puerto = arg
        elif opt in ("-b", "--bauds"):
            g_bauds = arg
        elif opt in ("-m", "--modulo"):
            g_modulo = arg

    print("[cmt]puerto: {}".format(g_puerto))
    print('[cmt]bauds: {}'.format(g_bauds))
    print('[cmt]modulo: {}'.format(g_modulo))
    
def cmt_crear_modem(_puerto, _bauds, _modulo, _mode):

    if _modulo == "BG95":
        print("[cmt]Modem BG95 creado")
        _modem = ModemBG95.Modem(_puerto, int(_bauds), _mode)
    elif _modulo == "SIM5320":
        print("[cmt]Modem SIM5320 creado")
        _modem = sim5320.Modem(_puerto, int(_bauds), _mode)
    else:
        print("[cmt]Modulo desconocido ")
        sys.exit(2)

    return _modem  


if __name__ == '__main__':
    cmt_procesar_parametros(sys.argv)
    modem = cmt_crear_modem(g_puerto, g_bauds, g_modulo, g_mode)
       
    try: 
        modem.run()
    except Exception as e:
        print('[tester]Error: %s' % e)

        
