import Command

class Commands:

    def __init__(self, ser):
        # Configuracion previo attach.
        self.bc660k_cmd_at         = Command.Command("AT", "AT\r", 2, "OK", ser)
        self.bc660k_cmd_ate0       = Command.Command("ATE0", "ATE0\r", 2, "OK", ser)
        self.bc660k_cmd_qclsk0     = Command.Command("QSCLK", "AT+QSCLK=0\r", 2, "OK", ser)
        self.bc660k_cmd_qband      = Command.Command("QBAND", "AT+QBAND=1,28\r", 2, "OK", ser)
        self.bc660k_cmd_eviotevt   = Command.Command("NBIOTEVT", "AT+QNBIOTEVENT=1,1\r", 2, "OK", ser)
        self.bc660k_cmd_cereg      = Command.Command("CEREG", "AT+CEREG=5\r", 2, "OK", ser)

        # Comandos informacion de contexto    
        self.bc660k_cmd_qgmr       = Command.Command("QGMR", "AT+QGMR\r", 5, "Quectel_Ltd", ser) #version y fabricante
        self.bc660k_cmd_qccid      = Command.Command("QCCID", "AT+QCCID\r", 5, "+QCCID", ser) #SIM
        self.bc660k_cmd_cpsmsq     = Command.Command("CPSMSQ", "AT+CPSMS?\r", 10, "+CPSMS", ser) #PSMS estatus
        self.bc660k_cmd_cedrx      = Command.Command("CEDRXS", "AT+CEDRXS?\r", 5, "+CEDRXS", ser) #edrx
        self.bc660k_cmd_qeng       = Command.Command("QENG", "AT+QENG=0\r", 5, "+QENG", ser) #intensidad de señal.
        self.bc660k_cmd_contrdp    = Command.Command("CONTRDP", "AT+CGCONTRDP\r", 5, "IOT.ALTAN", ser) #contexto, apn y modo de operacion actual

        # Comandos contexto de red
        self.bc660k_cmd_ceregq     = Command.Command("CEREGQ", "AT+CEREG?\r", 5, "+CEREG: 5,1", ser)
        self.bc660k_cmd_cregq      = Command.Command("CREGQ", "AT+CREG?\r", 5, "+CREG: 0,0", ser)
        self.bc660k_cmd_cgpaddr    = Command.Command("CGPADDR",  "AT+CGPADDR=0\r", 5, "+CGPADDR:", ser)

        # Configuracion post attach
        self.bc660k_cmd_dnscfg     = Command.Command("DNSCFG", "AT+QIDNSCFG=0,\"8.8.8.8\"\r", 5, "OK", ser)
        
        # Comandos control red

        # Comandos envio TCP

        # Comandos de conexion MQTT
        self.bc660k_cmd_qmtopen    = Command.Command("QMTOPEN", "AT+QMTOPEN=0,\"pruebastelemetry.paradoxalabs.com\",1883\r", 5, "+QMTOPEN: 0,0", ser)
        self.bc660k_cmd_qmtconn    = Command.Command("QMTCONN", "AT+QMTCONN=0,\"mqtt_pdx1\",\"vacio\",\"vacio\"\r", 10, "+QMTCONN: 0,0,0", ser)

        # Comandos de envio MQTT
        self.bc660k_cmd_qmtpub     = Command.Command("QMTPUB", "AT+QMTPUB=0,1,1,0,\"pdx/quectel/test\"\r", 5, ">", ser)
        self.bc660k_cmd_payload    = Command.Command("MQTTPAYLOAD", "Your base is belong to us\r\n\x1A", 5, "OK", ser)

        # Comandos control dispositivo
        self.bc660k_cmd_cfun0      = Command.Command("CFUN0", "AT+CFUN=0\r", 10, "OK", ser) #modo avion 
        self.bc660k_cmd_cfun1      = Command.Command("CFUN1", "AT+CFUN=1\r", 10, "OK", ser) #modo aporativo
        self.bc660k_cmd_softreset  = Command.Command("SoftReset", "AT+CFUN=1,1\r", 10, "OK", ser) #reinicio