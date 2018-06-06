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


class Command(BaseCommand):
    help = 'Simula la gestión de un vehiculo'

    def add_arguments(self, parser):
        parser.add_argument('--archivo', type=str, help=u"path del archivo del cual se simulará")
        
    def handle(self, *args, **options):
              
        archivo    = options["archivo"]
        file       = open(archivo, 'r')
        contenido  = file.read()
        parametros = json.loads(contenido)
        idVehiculo = parametros.get("idVehiculo","")
        
        print u"Vehiculo: {}".format(idVehiculo)
        print u"GueService: {}".format(parametros.get("ws",""))
        print u"Notificar cada: {}minutos".format(parametros.get("ping",""))

        notificarSegundos = int( float(parametros.get("ping",1.0)) * 60.0)
        print u"Notificar cada: {}segundos".format(notificarSegundos)
        
        ruta = parametros.get("ruta",[])

        if len(ruta) < 2:
            print "No existen suficiente puntos"
            return

        simulacion = [] #Todos los pasos de la simulacion
        

        contadorSegundos = 0
        for i in range (0, (len(ruta)-1)):
            pos          = ruta[i]
            posSiguiente = ruta[i+1]            
            lat       = float(pos["lat"])
            lon       = float(pos["lon"])
            velocidad = pos["velocidad"]
            latSiguiente = float(posSiguiente["lat"])
            lonSiguiente = float(posSiguiente["lon"])

            puntoInicial    =   (lat, lon)
            puntoFinal      =   (latSiguiente, lonSiguiente) 
            distanciaMetros = vincenty(puntoInicial, puntoFinal).meters
            
            print "Desde ({},{}) hasta ({},{}) a {}km/h (distancia: {}metros)".format(
                lat, lon,
                latSiguiente, lonSiguiente,
                velocidad,
                distanciaMetros
            )

            velocidadMS = (float(velocidad)*1000.0)/(60.0*60.0) #Velocidad de metros por segundo
            
            partes = int(distanciaMetros / velocidadMS)

            print u"Recorrido en {} minutos".format(partes/60.0)
            
            
            for p in range(0,partes):

                latFragmento = ( ( (latSiguiente-lat) + (partes*lat) ) / partes ) - lat
                lonFragmento = ( ( (lonSiguiente-lon) + (partes*lon) ) / partes ) - lon
                
                latCalculado = lat + p*latFragmento
                lonCalculado = lon + p*lonFragmento
                #print "Segundo {} , pos ({},{})".format(contadorSegundos, latCalculado, lonCalculado)

                hacerPing = False
                print "Modulo: {}".format(contadorSegundos % notificarSegundos)
                if (contadorSegundos % notificarSegundos) == 0:
                    print "TRUE"
                    hacerPing = True
                
                simulacion.append({
                    "segundo" : contadorSegundos,
                    "hacerPing" : hacerPing,
                    "lat"  : latCalculado,
                    "lon"  : lonCalculado
                })

                contadorSegundos += 1
            
            for paso in simulacion:
                print paso

                #if paso["hacerPing"]:
                if False:
                    
                    peticion = { 
                        "autenticacion" : {
                            "usuario" : "admin",
                            "token" : "5776d71ff8f8442ca8326d04987a9bdc",
                            "tenant" : "exxonmobil"        
                        },    
                        "data" : {        
                            "posiciones"            : [
                                {
                                    "latitud"        : paso["lat"], 
                                    "longitud"       : paso["lon"],
                                    "velocidad"      : "10", 
                                    "horaRegistrada" : datetime.datetime.utcnow().isoformat()[:19]+"Z" 
                                }
                            ],
                            "identificadorGPS"  : idVehiculo          
                        }
                    } 

                    datos ={
                        "request": json.dumps(peticion)
                    }

                    cabeceras = {
                        "Content-Type" : "application/x-www-form-urlencoded"
                    }
                    #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
                    url = 'http://localhost/ws/registrarPosicionesGPS'
                    response = requests.post(url, data=datos, headers=cabeceras)
                    print response.text
                time.sleep(1)

        
