# Roadmap
### version 0.1.0

- Opcion de configuracion de puerto y bauds como parametros al ejecutar el script.
- Opcion de seleccion de modulo a utilizar.
- Soporte para modulo BC660K de Quectel.
- Soporte para modulo SIM5320 de SIMCOM.

### version 0.2.0

- Implementacion de CLI.
    - Menu de acciones.
    - Seleccion de puerto. Lee los puertos disponibles y los muestra en un listado para seleccionar la opcion.
    - Acciones individuales:
        - Configurar modem.
        - Attach a red (llega hasta la ip asignada al dispositivo)
        - Conectar (Abrir conexion TCP al server)
        - Enviar (Ingresar datos y enviarlos)
        - Terminar (Cerrar conexion con servidor)
        - Reiniciar (Reiniciar modem)
        - Apagar (Apagar modem)
    - Salir (Cierra puerto graciosamente)
- Soporte para modulo SIM7020 de SIMCOM.
- Soporte para modulo SIM7000 de SIMCOM.

### version 0.3.0

- Modo automatico. 
    - Crea/carga payload.
    - Asigna timer.
    - Asigna contador (0 para indefinido). Veces que se repetira el envio.
    - Envia cada que timer se vence, aumenta contador.
    - Termina cuando se llega a contador.
- Modo conexion. Estado en el que se queda el modem despues del envio.
    - Conectado. Se deja abierta la conexion al servidor.
    - Attached. Se cierra conexion al server pero se deja conectado a la red celular.
    - Dettached. Se desconecta de server y red celular pero se deja encendido.
    - Sleep. Dormimos el modulo.
    - Off. Apagamos el modulo. (No posible ya que no hay acceso al pin de encendido.)

### version 0.4.0

- Modo HTTP. Usar el stack HTTP directo desde el modem.
    - Logica de operacion.
    - Opciones del CLI.
    - Modo Automatico.
- Modo FTP. Usar el stack FTP directo desde el modem.
    - Logica de operacion.
    - Opciones del CLI.
    - Modo Automatico.
- Soporte para BG95
- Soporte para Simcom 7000

### version 0.5.0

- Modo MQTT - Cliente. Usar el stack MQTT - Cliente directo desde el modem.
    - Logica de operacion.
    - Opciones del CLI.
    - Modo Automatico.
- Modo CoAP. Usar el stack CoAP - Cliente directo desde el modem.
    - Logica de operacion.
    - Opciones del CLI.
    - Modo Automatico.
- Soporte para BG95
- Soporte para Simcom 7000

### version 0.6.0

- Modo NBIOT. Usar transmisiones sin reattach.
    - Logica de operacion.
    - Opciones CLI.
    - Modo automatico.
- Soporte para Quectel BC660K
- Soporte para Simcom SIM7020

