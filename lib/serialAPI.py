import sys, os, serial, glob

class SerialApi:
    def __init__(self) -> None:
        pass
    def availableDevices(self):
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    def sistemComPort(self):
        """
        Regresa el puerto COM del sistema
        """
        if sys.platform == "win32":
            return "COM1"
        elif sys.platform == "linux":
            return "/dev/ttyCOM0"
        elif sys.platform == "darwin":
            return "/dev/tty.usbserial-0001"
        else:
            return "Desconocido"
    def listadoBaudratesDisponibles(self):
        """
        Regresa una lista de los baudrates disponibles
        """
        return [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]