# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from django.conf                 import settings
import json
import couchdb
import logging
from datetime                    import datetime
from geopy.distance              import vincenty
import time
import datetime
import requests
import dateutil.parser
import random

class Command(BaseCommand):
    help = 'Simula la gestión de un vehiculo'

    def add_arguments(self, parser):
        parser.add_argument('--archivo', type=str, help=u"path del archivo del cual se simulará")
        
    def handle(self, *args, **options):


        archivo1 = "ws/management/commands/simulacionAvanzadaBugaFlorida.json"
        archivo2 = "ws/management/commands/simulacionAvanzadaBugaBogota.json"
        archivo3 = "ws/management/commands/simulacionAvanzadaBugaMedellin.json"
        
        
        idVehiculo       = "20160801",
	fechaHoraInicial = "2017-01-02T09:47:09",
        fechaHoraFinal   = "2017-01-08T09:49:00",
        
        while fechaHoraInicial < fechaHoraFinal:
            fechaHoraInicial = generarRuta(archivo1, True,  idVehiculo, fechaHoraInicial )
            fechaHoraInicial = generarRuta(archivo2, False, idVehiculo, fechaHoraInicial )
            fechaHoraInicial = generarRuta(archivo2, True,  idVehiculo, fechaHoraInicial )
            fechaHoraInicial = generarRuta(archivo3, False, idVehiculo, fechaHoraInicial )
            fechaHoraInicial = generarRuta(archivo3, True,  idVehiculo, fechaHoraInicial )
            fechaHoraInicial = generarRuta(archivo1, False, idVehiculo, fechaHoraInicial )
            




def sample():

        
        archivo    = options["archivo"]
        file       = open(archivo, 'r')
        contenido  = file.read()
        parametros = json.loads(contenido)
        idVehiculo = parametros.get("idVehiculo","")
        reversar   = parametros.get("reverse",False)
        fechaHoraInicial = dateutil.parser.parse(parametros.get("fechaHoraInicial","") )
        
        print u"Vehiculo: {}".format(idVehiculo)
        print u"GüeService: {}".format(parametros.get("ws",""))
        print u"Notificar cada: {}minutos".format(parametros.get("ping",""))

        notificarSegundos = int( float(parametros.get("ping",1.0)) * 60.0)
        print u"Notificar cada: {}segundos".format(notificarSegundos)
        
        ruta = parametros.get("ruta",[])

        if len(ruta) < 2:
            print "No existen suficiente puntos"
            return

        simulacion = [] #Todos los pasos de la simulacion
        

        iterador = range (0, (len(ruta)-1))
        if reversar:
            iterador = reversed(iterador)
        
        
        contadorSegundos = 0
        for i in iterador:
            pos          = ruta[i]
            posSiguiente = ruta[i+1]

            # parr los tipoPaso avance-----------------------------------
            if pos.get("tipoPaso","") == "avance":
                lat       = float(pos["lat"])
                lon       = float(pos["lon"])
                velocidad = pos["velocidad"]
                latSiguiente = float(posSiguiente["lat"])
                lonSiguiente = float(posSiguiente["lon"])
                variacionVelocidad = int(pos["variacionVelocidad"])
                
                
                puntoInicial    =   (lat, lon)
                puntoFinal      =   (latSiguiente, lonSiguiente) 
                distanciaMetros = vincenty(puntoInicial, puntoFinal).meters
                velocidad = int(velocidad) + random.randrange((-1*variacionVelocidad),variacionVelocidad)
            
                # print "Desde ({},{}) hasta ({},{}) a {}km/h (distancia: {}metros)".format(
                #     lat, lon,
                #     latSiguiente, lonSiguiente,
                #     velocidad,
                #     distanciaMetros
                # )

                velocidadMS = (float(velocidad)*1000.0)/(60.0*60.0) #Velocidad de metros por segundo
            
                partes = int(distanciaMetros / velocidadMS)

                #print u"Recorrido en {} minutos".format(partes/60.0)
                
                
                for p in range(0,partes):

                    latFragmento = ( ( (latSiguiente-lat) + (partes*lat) ) / partes ) - lat
                    lonFragmento = ( ( (lonSiguiente-lon) + (partes*lon) ) / partes ) - lon
                
                    latCalculado = lat + p*latFragmento
                    lonCalculado = lon + p*lonFragmento
                    #print "Segundo {} , pos ({},{})".format(contadorSegundos, latCalculado, lonCalculado)

                    hacerPing = False
                    #print "Modulo: {}".format(contadorSegundos % notificarSegundos)
                    if (contadorSegundos % notificarSegundos) == 0:
                        #print "TRUE"
                        hacerPing = True

                    if hacerPing:
                        simulacion.append({
                            "segundo" : contadorSegundos,
                            "hacerPing" : hacerPing,
                            "lat"  : latCalculado,
                            "lon"  : lonCalculado,
                            "velocidad" : float(velocidad),
                            "estaMotorEncendido" : True
                        })

                    print contadorSegundos
                    contadorSegundos += 1

            if pos.get("tipoPaso","") == "parada":
                lat       = float(pos["lat"])
                lon       = float(pos["lon"])
                estaMotorEncendido = pos.get("estaMotorEncendido", True)
                duracionParada = int(pos["duracionParada"])
                for p in range(0,duracionParada*60):
                    hacerPing = False
                    #print "Modulo: {}".format(contadorSegundos % notificarSegundos)
                    if (contadorSegundos % notificarSegundos) == 0:
                        #print "TRUE"
                        hacerPing = True
                
                    if hacerPing:
                        simulacion.append({
                            "segundo" : contadorSegundos,
                            "hacerPing" : hacerPing,
                            "lat"  : lat,
                            "lon"  : lon,
                            "velocidad" : 0,
                            "estaMotorEncendido" : estaMotorEncendido
                        })

                    print contadorSegundos
                    contadorSegundos += 1
            
        for paso in simulacion:
            #print paso
            print "Fecha {} - segundos {}".format( fechaHoraInicial.isoformat(), paso["segundo"])
            print (
                fechaHoraInicial +
                datetime.timedelta(
                    seconds=(
                        paso["segundo"]+random.randint(0,20)
                    ))).isoformat()
            if paso["hacerPing"]:
                #if False:
                
                peticion = { 
                    "autenticacion" : {
                        "usuario" : "admin",
                        "token" : "5776d71ff8f8442ca8326d04987a9bdc",
                        "tenant" : "exxonmobil"        
                    },    
                    "data" : {        
                        "posiciones"            : [
                            {
                                "latitud"            : paso["lat"], 
                                "longitud"           : paso["lon"],
                                "velocidad"          : paso["velocidad"],
                                "estaMotorEncendido" : paso["estaMotorEncendido"],
                                #"horaRegistrada" : datetime.datetime.utcnow().isoformat()[:19]+"Z"
                                "horaRegistrada"     : (
                                    fechaHoraInicial +
                                    datetime.timedelta(
                                        seconds=(
                                            paso["segundo"]+random.randint(0,20)
                                    ))).isoformat()+"-05:00" 
                            }
                        ],
                        "identificadorGPS"  : idVehiculo          
                    }
                } 

                #print json.dumps(peticion)
                    
                datos ={
                    "request": json.dumps(peticion)
                }

                cabeceras = {
                    "Content-Type" : "application/x-www-form-urlencoded"
                }
                #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
                url = 'http://localhost:8080/ws/registrarPosicionesGPS'
                response = requests.post(url, data=datos, headers=cabeceras)
                print response.text

                #time.sleep(1)

        
