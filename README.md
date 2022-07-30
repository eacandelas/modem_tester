# TESTER MODEMS CELULARES version 0.1.0

Script para prueba de modems celulares basados en comandos AT.

Version 0.1.0 poc para Quectel BG95

Tres clases principales:

Tester() - Se encarga de la adquisicion de los parametros desde el cli, crear el modulo a utilizar y ejecutarlo.
ModuloXXXX() - Crea una instancia del modulo seleccionado. Modulo extiende Modem() que tiene el manejo del puerto serial y sus estados (abierto, cerrado).
Command() - Es el driver para la comunicacion serial con el modulo fisico.

Hay un Moduloxxxx.py y un CommandsXXX.py por cada dispositivo soportado.

### Instrucciones

Sumamente basicas. Dejen su nota si requieren ayuda.

Hardware 
- Consigue una tarjeta de desarrollo con modem BG95 o busca una tarjeta con ese modem.
- Conecta el modem mediante un convertidor USB-Serial (Ya sea TTL o RS232 depende de la interface)
- Detecta el puerto serial en la pc, anota el puerto.

Software.
- Clona el repositorio.
- Crea un ambiente virtual y activalo.
- Instala pyserial dentro del ambiente.
- Ejecuta "quectel_tester.py" con los tres parametros: -b <puerto serial> -b <baudrate> -m <modulo>
- o Ejecuta solo el parametro.
- Hay un prompt inicial que te pide los parametros faltantes.
- El tester corre automaticamente.

TODO: Muchas cosas por mejorar aun ... revisa el Roadmap.md

