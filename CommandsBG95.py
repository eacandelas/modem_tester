import Command

class Commands:

    def __init__(self, ser):
        self.bg95_cmd_at         = Command.Command("AT", "AT\r", 0.5, "OK", ser)
        self.bg95_cmd_ate        = Command.Command("ATE0", "ATE0\r", 0.5, "OK", ser)
        self.bg95_cmd_cereg      = Command.Command("CEREG", "AT+CEREG?\r", 5, "0,1", ser)
        self.bg95_cmd_qicsgp     = Command.Command("QICSGP", "AT+QICSGP=1,1,\"ALTAN\",\"\",\"\",1\r", 5, "OK", ser)
        self.bg95_cmd_cgattQ     = Command.Command("CGATT?", "AT+CGATT?\r", 10, "OK", ser)
        self.bg95_cmd_copsQ      = Command.Command("COPS?", "AT+COPS?\r", 10, "OK", ser)
        self.bg95_cmd_qiact      = Command.Command("QIACT", "AT+QIACT=1\r", 10, "OK", ser)
        self.bg95_cmd_qiactQ     = Command.Command("QIACT?", "AT+QIACT?\r", 10, "OK", ser)
        self.bg95_cmd_qiopen     = Command.Command("QIOPEN", "AT+QIOPEN=1,0,\"TCP\",\"www.paradoxalabs.com\",7523,0,0\r", 150, "OK", ser)
        self.bg95_cmd_qisend0    = Command.Command("QISEND0", "AT+QISEND=0\r", 10, ">", ser)
        self.bg95_cmd_qird       = Command.Command("QIRD", "AT+QIRD=0,1500\r", 5, "OK", ser)
        self.bg95_cmd_qiclose    = Command.Command("QICLOSE", "AT+QICLOSE=0\r", 11, "OK", ser)
        self.bg95_cmd_softreset  = Command.Command("SoftReset", "AT+CFUN=1,1\r", 10, "OK", ser)