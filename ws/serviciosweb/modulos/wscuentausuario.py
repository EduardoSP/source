# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from cuentausuario             import cuentausuario
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging




#--------------------------------------------------------------
def wsActualizarCuentaUsuario(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActualizarCuentaUsuario(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsActualizarCuentaUsuario",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cuentausuario.actualizarCuentaUsuario(peticion)
    
    return responder(respuestaRaw)

def validacionWsActualizarCuentaUsuario(peticion):
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
                    'type'   	  : 'object',
                    'properties'  : {
                        
                        'nombres'      : { 'type' : 'string' },
                        'correo'   : { 'type' : 'string' },
                        'loginUsuario'      : { 'type' : 'string' }
                       
                    },
                    'required' : [
                        
                        'nombres',
                        'correo',
                        'loginUsuario'
                        
                      
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

#--------------------------------------------------------------
def wsDetalleCuentaUsuario(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleCuentaUsuario(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleCuentaUsuario",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cuentausuario.detalleCuentaUsuario(peticion)
    
    return responder(respuestaRaw)

def validacionWsDetalleCuentaUsuario(peticion):
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
