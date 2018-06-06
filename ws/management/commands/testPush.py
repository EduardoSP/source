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

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        llave = 'cAvMKS_l54E:APA91bE3KqaWJlm7whEUYB8DuTGgdLT4Z7FIhDFfK1v7Ti6J0X3xsAsIfvKNgGHb3VdpORWJwhNaJzeEU_vu1x4Z1VhorbJy1qK71B5abJej02ms8hMKWJUY5GLUWMTmXUyQM3tNxvw9'
        llave = 'd6mWIjIy0lo:APA91bFXwRuKXbamCs9hklhAzA2IjDhEg-J8LQKIWVsGBt8gkFkDPoHyXeYp5oUatOAtMzYuSGc7bkE1BzmxqGWiToIQlR2J8jIJTq6kCk1GSL0iSLh2ssBPxBN9cqC0W3u2otaO8f1S'
        mensaje = "Prueba de mensaje"
        enviarMensajeAndroid( [ llave ] , mensaje )
        #enviarMensajeIOS( llave, mensaje )

def enviarMensajeAndroid(idPushs,mensaje):

    dataRaw = {
        'success': True,
        'data': {}
    }

    reg_id_set = set()
    msg = mensaje

    for idPush in idPushs:
        reg_id_set.add(idPush)

    data = {
      'registration_ids' :list(reg_id_set),
      'data' : {
        'msg'       : mensaje
      }
    }

    headers = {
      'Content-Type' : 'application/json',
      'Authorization' : 'key=' + 'AIzaSyBApIYr3eZs3XXXYC57PoXbZM78quPW4a8'
      #'Authorization' : 'key=' + tenantData["androidapikey"]
    }

    url = 'https://android.googleapis.com/gcm/send'
    request = urllib2.Request(url, json.dumps(data), headers)

    try:
      response = urllib2.urlopen(request)
      logging.warning(response)
      dataRaw = {
                       'success': True,
                       'data': {
                                'data': data

                                }
                       }
      logging.warning(dataRaw)

    except urllib2.HTTPError, e:
      dataRaw = {
          'success': False,
          'data': {
              'errorcpde': e.code,
              'errormesage': e.read()
          }
      }
      logging.warning(dataRaw)
         

def response_listener(error_response):
    print "client get error-response: " + str(error_response) 
      
            
def enviarMensajeIOS(idPush, mensaje):
    print "enviando mensaje"
    print "{} - {}".format(idPush, mensaje)
    #print settings.IOSPUSHCERT
    #print settings.IOSPUSHKEY

    apns = APNs(
        use_sandbox = True,
        cert_file   = '/Users/fasozu/irengines/proyectos/emergencia/src/ambulanciasWebAdmin/llaves/apns-dev.pem',
        #enhanced    = True
        
    )
    payload   = Payload(alert=mensaje, sound="default", badge=1)
    resultado = apns.gateway_server.send_notification(idPush, payload)
    #identifier = random.getrandbits(32)
    #apns.gateway_server.register_response_listener(response_listener)
    #apns.gateway_server.send_notification(idPush, payload, identifier=identifier)
    print resultado
    
    #print resultado

    
