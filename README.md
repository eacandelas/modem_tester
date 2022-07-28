#TESTER MODEMS CELULARES version 0.0.1

Script para prueba de modems celulares basados en comandos AT.

Version 0.0.1 poc para Quectel BG95

Se puede portar para otros modulos modificando Commands.py y Modem.py
El truco lo hace la clase Command.py

###Instrucciones

Sumamente basicas. Dejen su nota si requieren ayuda.

Hardware 
- Consigue una tarjeta de desarrollo con modem BG95 o busca una tarjeta con ese modem.
- Conecta el modem mediante un convertidor USB-Serial (Ya sea TTL o RS232 depende de la interface)
- Detecta el puerto serial en la pc, anota el puerto.

Software.
- Clona el repositorio.
- Crea un ambiente virtual y activalo.
- Instala pyserial dentro del ambiente.
- Modifica el archivo "quectel_tester.py" en la linea 5, cambia el COM22 y el baudrate por el valor de tu setup.
- Modifica el archivo "CommandsBG95.py" en la linea 14, cambia el dominio y el puerto.
- Modifica el archivo "CommandsBG95.py" en la linea 9, cambia el nombre de la red.
- Ejecuta "quectel_tester.py"
