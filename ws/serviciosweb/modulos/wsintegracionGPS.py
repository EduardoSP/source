# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from integracionGPS          import integracionGPS
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging

#--------------------------------------------------------------
def wslistadoGPS(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistadoGPS(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistadoGPS",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = integracionGPS.wslistadoGPS(peticion)
    
    return responder(respuestaRaw)


def validacionWslistadoGPS(peticion):
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
                        'token'   : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                }                
            },
            'required' : [
                'autenticacion'
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



#--------------------------------------------------------------
def wssolicitarCapturaImagen(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWssolicitarCapturaImagen(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wssolicitarCapturaImagen",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = integracionGPS.ejecutarSolicitudCapturaImagen(peticion)
    
    return responder(respuestaRaw)


def validacionWssolicitarCapturaImagen(peticion):
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
                }                
            },
            'required' : [
                'autenticacion'
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

#--------------------------------------------------------------
def wsregistrarPosicionesGPS(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsregistrarPosicionesGPS(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsregistrarPosicionesGPS",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = integracionGPS.registrarPosicionesGPS(peticion)
    
    return responder(respuestaRaw)


def validacionWsregistrarPosicionesGPS(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'        : 'object',
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
                'autenticacion'
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



