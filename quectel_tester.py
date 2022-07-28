import serial
import ModemBG95

ser = serial.Serial()
modem = ModemBG95.Modem(ser, "COM22", 115200)

if __name__ == '__main__':
    try: 
        modem.run()
    except Exception as e:
        print('[tester]Error: %s' % e)

        
