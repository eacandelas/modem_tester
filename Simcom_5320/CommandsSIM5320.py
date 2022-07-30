import Command

class Commands:

    def __init__(self, ser):
        self.sim5320_cmd_at         = Command.Command("AT", "AT\r", 0.5, "OK", ser)
        self.sim5320_cmd_ate        = Command.Command("ATE0", "ATE0\r", 0.5, "OK", ser)
        self.sim5320_cmd_ccid       = Command.Command("CCID", "AT+CICCID\r", 0.5, "OK", ser)
        self.sim5320_cmd_srip       = Command.Command("CIPSRIP", "AT+CIPSRIP=1\r", 0.5, "OK", ser)
        self.sim5320_cmd_xget       = Command.Command("XGET", "AT+CIPRXGET=1\r", 0.5, "OK", ser)
        self.sim5320_cmd_netclose   = Command.Command("NETCLOSE", "AT+NETCLOSE\r", 0.5, "closed", ser)
        self.sim5320_cmd_creg       = Command.Command("CREG", "AT+CREG?\r", 5, "0,1", ser)
        self.sim5320_cmd_csq        = Command.Command("CSQ", "AT+CSQ?\r", 5, "OK", ser)
        self.sim5320_cmd_gsock      = Command.Command("CGSOCKCONT", "AT+CGSOCKCONT=1,\"IP\",\"ALTAN\"\r", 5, "OK", ser)
        self.sim5320_cmd_sockset    = Command.Command("CSOCKSETPN", "AT+CSOCKSETPN=1\r", 5, "OK", ser)
        self.sim5320_cmd_cipmode    = Command.Command("CIPMODE", "AT+CIPMODE=0\r", 5, "OK", ser)
        self.sim5320_cmd_netopen    = Command.Command("NETOPEN", "AT+NETOPEN=\"TCP\"\r", 5, "OK", ser)
        self.sim5320_cmd_ipaddr     = Command.Command("IPADDR", "AT+IPADDR\r", 5, "OK", ser)
        self.sim5320_cmd_tcpconnect = Command.Command("TCPCONNECT", "AT+TCPCONNECT=\"www.paradoxalabs.com\",7523\r", 10, "OK", ser )
        self.sim5320_cmd_tcpwrite   = Command.Command("TCPWRITE", "AT+TCPWRITE=0\r", 10, ">", ser )
        self.sim5320_cmd_tcpclose   = Command.Command("TCPCLOSE", "AT+TCPCLOSE=0\r", 10, "OK", ser )
        self.sim5320_cmd_reset      = Command.Command("RESET", "AT+CFUN=1,1\r", 10, "OK", ser )