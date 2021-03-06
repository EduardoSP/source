# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
#from webbiodws.models            import *
import json
from django.conf                 import settings
from datetime                    import datetime,timedelta
import urllib2
import logging
import couchdb
import requests
import json
from dateutil import parser
import time
#from ws.serviciosweb.conexion import conexion

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        archivo    = open("/tmp/revisar.txt","w") 
        couch      = couchdb.Server(url=settings.COUCHDB_URL)
        base       = settings.BASEDB
        db         = couch[base]
        dbsTenants = [] #Guarda una reerencia a todas las conexiones de los tenants
        archivo.write("Iniciando {}".format(time.time()))
        filas = db.view('_design/GPS/_view/gpsPorId',
                    include_docs  = True)
        
        for fila in filas:
          key      = fila.key
          value    = fila.value
          doc      = fila.doc
          
          dbTenant = None
          
          identificadorGPS = doc.get("identificadorGPS","")
          tenantGps        = doc.get("tenant")
          idVehiculo       = doc.get("idVehiculo")
          #if not identificadorGPS == "39" and not identificadorGPS == "40":
          #    continue
          if tenantGps == "":
              break

          if tenantGps in dbsTenants:
              dbTenant = dbsTenants[tenantGps]
          else:
              dbTenant = couch[u"{}{}".format(settings.BASEDB, tenantGps)]
              
          docVehiculo  = dbTenant[idVehiculo]

          ultimaPosicionDoc = getUltimaPosicionVehiculo(idVehiculo, dbTenant)

          fromPosicion = ""
          toPosicion   = ""

          if ultimaPosicionDoc == None:
              fromPosicion = "2017-07-14T18:00:00-0500"
          else:
              fromPosicion = ultimaPosicionDoc.get("horaRegistrada","1990-01-01")
              fechaParse   = parser.parse(fromPosicion) + timedelta(hours=5, seconds=1)
              fromPosicion = fechaParse.isoformat()
            

          toPosicion = datetime.utcnow().isoformat()
                   
          print identificadorGPS
          print fromPosicion
          
 
          cabeceras = {
              "Content-Type"  : "application/json",
              "Accept"        : "application/json",
              "Authorization" : "Basic YWRtaW46bG9remFhc2Q=",
              
          }
          #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
          #url = 'http://192.168.0.34:8082/api/positions'
          data = {
              "deviceId" : identificadorGPS,
              "from"     : fromPosicion,
              "to"       : toPosicion
              
          }
          archivo.write(u"Consultando {}".format(json.dumps(data)))
          print u"Consultando {}".format(json.dumps(data))
          #url               = "http://localhost:8082/api/positions"
          url               = "http://10.0.0.106:8082/api/positions"
          response          = requests.get(url, params=data, headers=cabeceras)
          resultadoPeticion = response.text
          #print resultadoPeticion
          #archivo.write(u"{} - {} __".format(url, cabeceras)) 
          #archivo.write(resultadoPeticion.encode("UTF-8")) 
          posiciones   = json.loads(resultadoPeticion)
          posicionesWs = []
          print u"Encontrados: {}".format(len(posiciones))
          for posicion in posiciones[:100]:

              latitude = posicion.get("latitude","")
              
              if not latitude == "" and not latitude == "0" and not latitude == 0:
                  posicionesWs.append({
                      "latitud"            : posicion.get("latitude",""),
                      "longitud"           : posicion.get("longitude",""),
                      "velocidad"          : posicion.get("speed",0)*1.852,
                      "estaMotorEncendido" : False,
                      "horaRegistrada"     : posicion.get("deviceTime","")
                  })
              
          peticion = {            
              "autenticacion" : {
                  "usuario" : "admin",
                  "token" : "5776d71ff8f8442ca8326d04987a9bdc",
                  "tenant" : "exxonmobil"        
              },    
              "data" : {        
                  "posiciones"        : posicionesWs,
                  "identificadorGPS"  : identificadorGPS
              }
          }

          #print peticion
          
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
          #print peticion

          #Ahora mando los botones de pánico-------------------------------------------------------------
          #http://52.55.0.240:8082/api/reports/events?deviceId=1&type=alarm&from=2016-05-04&to=2018-05-04
          cabeceras = {
              "Content-Type"  : "application/json",
              "Accept"        : "application/json",
              "Authorization" : "Basic YWRtaW46bG9remFhc2Q="
              
          }
          #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
          #url = 'http://192.168.0.34:8082/api/positions'
          data = {
              "deviceId" : identificadorGPS,
              "from"     : fromPosicion,
              "to"       : toPosicion,
              "type"     : "alarm"
              
          }
          
          #url               = "http://localhost:8082/api/reports/events"
          url               = "http://10.0.0.106:8082/api/reports/events"
          response          = requests.get(url, params=data, headers=cabeceras)
          resultadoPeticion = response.text
          #print resultadoPeticion
          alarmas   = json.loads(resultadoPeticion)
          alarmasWs = []    
          for alarma in alarmas:
              tipoAlarma = alarma.get("attributes", {}).get("alarm", "")
              if tipoAlarma == "sos":
                  peticion = {            
                      "autenticacion" : {
                          "usuario" : "admin",
                          "token" : "5776d71ff8f8442ca8326d04987a9bdc",
                          "tenant" : "exxonmobil"        
                      },    
                      "data" : {                                  
                          "identificadorGPS"  : identificadorGPS,                
		          "latitud"           : "", 
		          "longitud"          : "",
		          "velocidad"         : "", 
		          "horaRegistrada"    : "",		          		
                      }
                  }
                  print peticion
                  datos ={
                      "request": json.dumps(peticion)
                  }

                  cabeceras = {
                      "Content-Type" : "application/x-www-form-urlencoded"
                  }
                  #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
                  url = 'http://localhost/ws/botonPanicoGPS'
                  response = requests.post(url, data=datos, headers=cabeceras)
                  print response.text
                  

     
def getUltimaPosicionVehiculo(idVehiculo, dbTenant):

    resultado = None
    
    filas = dbTenant.view(
        '_design/posicionVehiculos/_view/posicionFechaCreacion',
        startkey      = [idVehiculo, {}],
        endkey        = [idVehiculo, 0],
        include_docs  = True,
        descending    = True,
        limit         = 1

    )
    for fila in filas:
        resultado = fila.doc

    return resultado
    
