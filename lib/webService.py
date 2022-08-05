from concurrent.futures import process
import os
import sys
import socket
import click
import datetime
import requests
from .utilidades import Utilidades
from flask import Flask, request, make_response
from pprint import pprint

app = Flask(__name__)
systemUtils = Utilidades()


class WebService:
    def __init__(self):
        self.localIP = socket.gethostbyname(socket.gethostname())
        self.app = app
    
    def runWebService(self):
        """Ejecuta el servicior web de Flask"""
        try: 
            self.app.run(host=self.localIP, port=5001, debug=True)
        except Exception as e:
            systemUtils.printErrorCLI("Error al iniciar el servidor web{0}".format(e))
            systemUtils.printLogMessage(" {0}".format(e))
            systemUtils.printErrorCLI("Reiniciando el servidor web...")
            self.stopWebService()
            self.runWebService()
    
    def stopWebService(self):
        """Detiene el servicior web de Flask"""
        try:
            os.system("killall Python")
        except:
            pass
    
    @app.route('/', methods={"GET","POST"})
    def index():
        if request.method == "GET":
            print("Respuesta GET")
            return make_response("PDX TESTING MODULE\n", 200)
        elif request.method == "POST":
            getRequest = request.get_json()
            systemUtils.printWebServiceMessage("Recibido: {0}".format(getRequest))
            return make_response({
                "status": "OK",
                "message": "Bienvenido a la API de Quectel Tester",
                "data": {
                    "request": getRequest
                },
                "timestamp": datetime.datetime.now()
            })
    @app.route("/shutdown", methods=['GET'])
    def shutdown():
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return "Shutting down..."