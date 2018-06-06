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
        couch      = couchdb.Server(url=settings.COUCHDB_URL)
        base       = settings.BASEDB
        db         = couch[base]
        dbsTenants = [] #Guarda una reerencia a todas las conexiones de los tenants

        filas = db.view(
            '_design/GPS/_view/gpsPorId',
            include_docs  = True
        )
        
        for fila in filas:
          key      = fila.key
          value    = fila.value
          doc      = fila.doc

          dbTenant = None
          
          identificadorGPS = doc.get("identificadorGPS","")
          tenantGps        = doc.get("tenant")
          idVehiculo       = doc.get("idVehiculo")

          print u"Identificador GPS {}".format(identificadorGPS)

          if tenantGps == "":
              continue

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
              #PRODUCCION
              #fechaParse   = parser.parse(fromPosicion) + timedelta(hours=5, seconds=1)
              fechaParse   = parser.parse(fromPosicion) + timedelta( seconds=1)
              fromPosicion = fechaParse.isoformat()
            
        
          #toPosicion = datetime.utcnow().isoformat()
          toPosicion   = (parser.parse(fromPosicion) + timedelta( hours=24)).isoformat()
          
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

          print u"Consultando {}".format(json.dumps(data))
          url               = settings.URL_TRACCAR+"/api/positions"
          response          = requests.get(url, params=data, headers=cabeceras)
          resultadoPeticion = response.text
          #print resultadoPeticion
          posiciones   = json.loads(resultadoPeticion)
          posicionesWs = []

          
          for posicion in posiciones[:100]:
                  
              latitude  = posicion.get("latitude","")
              longitude = posicion.get("longitude","")
              
              if not latitude == "" and not latitude == "0" and not latitude == 0 and not longitude > -45.00:
                  posicionesWs.append({
                      "latitud"            : posicion.get("latitude",""),
                      "longitud"           : posicion.get("longitude",""),
                      "velocidad"          : posicion.get("speed",0)*1.852,
                      "estaMotorEncendido" : False,
                      "horaRegistrada"     : posicion.get("deviceTime",""),
                      "dataTraccar"        : posicion                   
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

          datos ={
              "request": json.dumps(peticion)
          }
          
          cabeceras = {
              "Content-Type" : "application/x-www-form-urlencoded"
          }
          #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
          url = '{}/ws/registrarPosicionesGPS'.format(settings.BASE_URL_LOCAL)
          #url = 'http://localhost:8080/ws/registrarPosicionesGPS'
          response = requests.post(url, data=datos, headers=cabeceras)
          #print response.text
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
          

          url               = settings.URL_TRACCAR+"/api/reports/events"
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
                  #print peticion
                  datos ={
                      "request": json.dumps(peticion)
                  }

                  cabeceras = {
                      "Content-Type" : "application/x-www-form-urlencoded"
                  }
   
                  url = '{}/ws/botonPanicoGPS'.format(settings.BASE_URL_LOCAL)
                  #url = 'http://localhost/ws/botonPanicoGPS'
                  if len(posicionesWs)>0:
                      response = requests.post(url, data=datos, headers=cabeceras)
                  #print response.text
                  

     
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
    
