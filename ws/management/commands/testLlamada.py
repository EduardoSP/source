# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
#from webbiodws.models            import *
import json
from django.conf                 import settings
import csv
from datetime                    import datetime
import urllib2
import logging
from apns import APNs, Payload
from twilio.rest import TwilioRestClient
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
        #Ahora mando los botones de pánico-------------------------------------------------------------
          #http://52.55.0.240:8082/api/reports/events?deviceId=1&type=alarm&from=2016-05-04&to=2018-05-04
          cabeceras = {
              "Content-Type"  : "application/json",
              "Accept"        : "application/json",
              "Authorization" : "Basic YWRtaW46bG9remFhc2Q="
              
          }
          
          identificadorGPS = "67"          
          fromPosicion     = "2017-10-18T16:30:12"
          toPosicion       = datetime.utcnow().isoformat()

          fechaParse   = parser.parse(fromPosicion) + timedelta(hours=5, seconds=1)
          fromPosicion = fechaParse.isoformat()
          
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
          print resultadoPeticion
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
                  #url = 'http://54.243.219.114:56899/ws/registrarPosicionesGPS'
                  url = 'http://localhost/ws/botonPanicoGPS'
                  print datos
                  response = requests.post(url, data=datos, headers=cabeceras)
                  print response.text
          
        
    def ahandle_noargs(self, **options):
        account_sid     = settings.TWILIO_ACCOUNT_SID 
        auth_token      = settings.TWILIO_AUTH_TOKEN
        client = TwilioRestClient(account_sid, auth_token)
        enviarLlamadaConVoz(client, "+573146488355", settings.TWILIO_NUMERO, "abc123" , "exxonmobil")
        pass
    
def enviarLlamadaConVoz(client, destino, origen, placa, nombreTenant):
    pass
    call = client.calls.create(url="{}/webfleetbigui/{}/llamada/{}".format(settings.RUTA_BASE_FLEETBI, str(nombreTenant), str(placa)),
        to=destino,
        from_= origen, record=True)
    return call.sid
