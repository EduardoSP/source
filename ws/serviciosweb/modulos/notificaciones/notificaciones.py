# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion              import conexion
from datetime                 import datetime
import urllib2
import json
from apns import APNs, Payload
import requests

#Envía una notificación a todos los notiers conectados
def notificarNotier(tipo,salas,parametros):

    peticion = {
        "tipo"       : tipo,
        "salas"      : salas,
        "parametros" : parametros
    }
    
    try:
        r = requests.post(settings.URL_NOTIER, data = {"request":json.dumps(peticion)})
    except:
        pass


#Envía una notificación a todos los notiers conectados
def notificarTenant(tenant, tipo, mensaje):

    peticion = {
        "tipo"    : tipo,
        "tenant"  : tenant,
        "mensaje" : mensaje
    }
    
    try:
        r = requests.post(settings.URL_NOTIER, data = {"request":json.dumps(peticion)})
        enviarNotificaciones(tenant,mensaje,peticion)
    except:
        pass

#Envía una notificación de la alerta generada
def notificarAlertaSeguridad(tenant, tipo, dispositivo, fecha):
    peticion = {
        "tipo"          : tipo,
        "tenant"        : tenant,
        "dispositivo"   : dispositivo,
        "fecha"         : fecha
    }
    
    try:
        r = requests.post(settings.URL_NOTIER, data = {"request":json.dumps(peticion)})
        #enviarNotificaciones(tenant,mensaje,peticion)
    except ValueError as e:
        print e
        pass


def enviarNotificaciones(tennant,mensaje,data):
    db = conexion.getConexionTenant(tennant)
        
    idPushsAndroid = []
    
    
    filas = db.view(
        '_design/autenticaciones/_view/autenticacionesPush',
        include_docs  = True,
        limit         = 1000
    )

    for fila in filas:
        doc   = fila.doc
        key   = fila.key
        value = fila.value

        if key[1] == "android":
            idPushsAndroid.append(key[2])
            
        

    enviarMensajeAndroid(idPushsAndroid,mensaje, data)
    


def enviarMensajeAndroid(idPushs, mensaje, data):
   
    dataRaw = {
        'success': True,
        'data': {}
    }

    reg_id_set = set()
    msg        = mensaje
    datos      = json.dumps(data)
    
    for idPush in idPushs:
        reg_id_set.add(idPush)

    data = {
      'registration_ids' :list(reg_id_set),
      'data' : {
        'msg'       : mensaje,
        'data'      : datos
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
      dataRaw = {
                       'success': True,
                       'data': {
                                'data': data

                                }
                       }

    except urllib2.HTTPError, e:
      dataRaw = {
                       'success': False,
                       'data': {
                                'errorcpde': e.code,
                                'errormesage': e.read()
                                }
                       }

    
# def enviarNotificaciones(tennant,loginUsuarios,mensaje,data):
#     db = conexion.getConexionTenant(tennant)
    
#     #print idDistribuidor
#     idPushsAndroid = []
#     idPushsIos     = []
#     idPushsIosJefe = []
#     for loginUsuario in loginUsuarios:
#         filas = db.view( '_design/autenticaciones/_view/autenticacionesPush',
#                          include_docs  = True,
#                          limit         = 100,
#                          startkey      = [loginUsuario,0,0],
#                          endkey        = [loginUsuario,{},{}]
#                          )
#     #print "EN FILA"
#         for fila in filas:
#             #print "dentro del fila"
#             doc = fila.doc
#             key = fila.key
#             value = fila.value
            
#             if key[1] == "android":
#                 idPushsAndroid.append(key[2])
#             elif key[1] == "ios":
#                 tipoUsuario = getTipoUsuario(loginUsuario, db)
#                 if tipoUsuario == "jefeUrgencias":
#                     idPushsIosJefe.append(key[2])
#                 if tipoUsuario == "personalMedico":
#                     idPushsIos.append(key[2])
        

#     enviarMensajeAndroid(idPushsAndroid,mensaje, data)
#     enviarMensajeIosJefe(idPushsIosJefe, mensaje, data)
#     enviarMensajeIos(idPushsIos, mensaje, data)

# def getTipoUsuario(loginUsuario, db):
#     tipoUsuario = ""
#     filas = db.view(
#         '_design/usuarios/_view/usuariosPorLoginUsuario',
#         limit    = 1,
#         key      = [loginUsuario],
#         endkey   = [loginUsuario]
        
#     )
#     for fila in filas:
#         tipoUsuario = fila.value.get("perfil","")
#     return tipoUsuario

# def enviarMensajeAndroid(idPushs, mensaje, data):
   
#     dataRaw = {
#         'success': True,
#         'data': {}
#     }

#     reg_id_set = set()
#     msg        = mensaje
#     datos      = json.dumps(data)
    
#     for idPush in idPushs:
#         reg_id_set.add(idPush)

#     data = {
#       'registration_ids' :list(reg_id_set),
#       'data' : {
#         'msg'       : mensaje,
#         'data'      : datos
#       }
#     }

#     headers = {
#       'Content-Type' : 'application/json',
#       'Authorization' : 'key=' + 'AIzaSyCqJosSOqhsEdQHJ32fmYeDVFx2wtodbZM'
#       #'Authorization' : 'key=' + tenantData["androidapikey"]
#     }

#     url = 'https://android.googleapis.com/gcm/send'
#     request = urllib2.Request(url, json.dumps(data), headers)

#     try:
#       response = urllib2.urlopen(request)
#       dataRaw = {
#                        'success': True,
#                        'data': {
#                                 'data': data

#                                 }
#                        }

#     except urllib2.HTTPError, e:
#       dataRaw = {
#                        'success': False,
#                        'data': {
#                                 'errorcpde': e.code,
#                                 'errormesage': e.read()
#                                 }
#                        }


# def enviarMensajeIos(idPushsIos, mensaje, data):
#     logging.warning(json.dumps(data))
#     logging.warning(data)
#     data = data.get('id','')
    
#     apns = APNs(
#         use_sandbox = True,
#         cert_file   = settings.CERTIOSPUSHDEV
#     )
    
#     payload   = Payload(
#         alert    = mensaje,
#         sound    = "default",
#         badge    = 1,
#         custom  = {"d":data}
#     )

#     for idPush in idPushsIos:
#         resultado = apns.gateway_server.send_notification(idPush, payload)

# def enviarMensajeIosJefe(idPushsIos, mensaje, data):
#     logging.warning(json.dumps(data))
#     logging.warning(data)
#     data = data.get('id','')
    
#     apns = APNs(
#         use_sandbox = True,
#         cert_file   = settings.CERTIOSPUSHJEFEDEV
#     )
    
#     payload   = Payload(
#         alert    = mensaje,
#         sound    = "default",
#         badge    = 1,
#         custom = {"d":data}
#     )

    
    
#     for idPush in idPushsIos:
#         resultado = apns.gateway_server.send_notification(idPush, payload)
    
#     #resultado = apns.gateway_server.send_notification(idPush, payload)

#     #----
#     #identifier = random.getrandbits(32)
#     #apns.gateway_server.register_response_listener(response_listener)
#     #apns.gateway_server.send_notification(idPush, payload, identifier=identifier)
#     #print resultado
    
#     #print resultado
