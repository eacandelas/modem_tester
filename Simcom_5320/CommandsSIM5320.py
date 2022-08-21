import Command

class Commands:

    def __init__(self, ser):
        self.at         = Command.Command("AT", "AT\r", 0.5, "OK", ser)
        self.ate        = Command.Command("ATE0", "ATE0\r", 0.5, "OK", ser)
        self.ccid       = Command.Command("CCID", "AT+CICCID\r", 0.5, "OK", ser)
        self.srip       = Command.Command("CIPSRIP", "AT+CIPSRIP=1\r", 0.5, "OK", ser)
        self.xget       = Command.Command("XGET", "AT+CIPRXGET=1\r", 0.5, "OK", ser)
        self.netclose   = Command.Command("NETCLOSE", "AT+NETCLOSE\r", 0.5, "closed", ser)
        self.creg       = Command.Command("CREG", "AT+CREG?\r", 5, "0,1", ser)
        self.csq        = Command.Command("CSQ", "AT+CSQ?\r", 5, "OK", ser)
        self.gsock      = Command.Command("CGSOCKCONT", "AT+CGSOCKCONT=1,\"IP\",\"ALTAN\"\r", 5, "OK", ser)
        self.sockset    = Command.Command("CSOCKSETPN", "AT+CSOCKSETPN=1\r", 5, "OK", ser)
        self.cipmode    = Command.Command("CIPMODE", "AT+CIPMODE=0\r", 5, "OK", ser)
        self.netopen    = Command.Command("NETOPEN", "AT+NETOPEN=\"TCP\"\r", 5, "OK", ser)
        self.ipaddr     = Command.Command("IPADDR", "AT+IPADDR\r", 5, "OK", ser)
        self.tcpconnect = Command.Command("TCPCONNECT", "AT+TCPCONNECT=\"www.paradoxalabs.com\",7523\r", 10, "OK", ser )
        self.tcpwrite   = Command.Command("TCPWRITE", "AT+TCPWRITE=0\r", 10, ">", ser )
        self.update_tcpwrite_data("dummy")
        self.tcpclose   = Command.Command("TCPCLOSE", "AT+TCPCLOSE=0\r", 10, "OK", ser )
        self.reset      = Command.Command("RESET", "AT+CFUN=1,1\r", 10, "OK", ser )


    def update_tcpwrite_data(self, data):
        self.dataToSend = data
        self.dataLen = len(data)
        command = f"AT+TCPWRITE={dataLen}\r"
        self.tcpwrite.cmd = command
        