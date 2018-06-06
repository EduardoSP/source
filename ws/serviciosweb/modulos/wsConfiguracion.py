# -*- coding: utf-8 -*-
from django.shortcuts          import render
from django.http               import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from configuracion             import configuracion
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging

#--------------------------------------------------------------
def wsActualizarConfiguracion(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActualizarConfiguracion(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsActualizarConfiguracion",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = configuracion.actualizarConfiguracion(peticion)
    
    return responder(respuestaRaw)

def validacionWsActualizarConfiguracion(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'   	  : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'   	  : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                },
                "data" : {
                    'type'   	  : 'object'
                }                                
            },
            'required' : [
                'autenticacion',
                'data'
            ]
        }
        validate(peticion ,schema)        
    except ValidationError as e:
        error   = e.message
        success = False
    except:
        error = 'Error desconocido-R001'
        success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw

#--------------------------------------------------------------
def wsListarConfiguraciones(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw = request.POST['request']
    peticion   = json.loads(requestRaw)

    validacionPeticion = validacionWsListarConfiguraciones(peticion)
    
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarConfiguraciones",peticion)
    
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = configuracion.listarConfiguraciones(peticion)
    
    return responder(respuestaRaw)

def validacionWsListarConfiguraciones(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'   	  : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'   	  : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                },
                "autenticacion" : {
                    'type'   	  : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                }
            },
            'required' : [
                'autenticacion',
                'data'
            ]
        }
        validate(peticion ,schema)        
    except ValidationError as e:
        error   = e.message
        success = False
    except:
        error = 'Error desconocido-R001'
        success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw
#===============================================================================
