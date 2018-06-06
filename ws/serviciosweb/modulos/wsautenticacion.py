# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion  import responder, validarProtocoloPeticion
from autenticacion          import autenticacion
from jsonschema             import validate, ValidationError
import logging
from ipware.ip import get_real_ip
#Autentica un usuario en el sistema y genera un token
def wsAutenticar(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsAutenticar(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.autenticar(peticion)
    return responder(respuestaRaw)

def validacionWsAutenticar(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'   	  : 'object',
            'properties'  : {
                'usuario' : { 'type' : 'string' },
                
            },
            'required' : [
                'usuario'
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

#Autentica un usuario en el sistema y genera un token
def wsAutenticarUnificado(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']

    peticion    = json.loads(requestRaw)
    if peticion["tipoIngreso"] == "fleetBiWeb":
        # si la peticion es desde la sistema web
        ip = get_real_ip(request)
        if ip is not None:
            # we have a real, public ip address for user
            direccionIp = ip
        else:
            # we don't have a real, public ip address for user
            direccionIp = "localhost"
        peticion["direccionIp"] = direccionIp
    validacionPeticion = validacionWsAutenticarUnificado(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.autenticarUnificado(peticion)
    return responder(respuestaRaw)

def validacionWsAutenticarUnificado(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'   	  : 'object',
            'properties'  : {
                'usuario' : { 'type' : 'string' },
                
            },
            'required' : [
                'usuario'
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

#Recuperar contraseña ----------------------------------------------------------
def wsRecuperarContrasena(request):
    respuestaRaw = {
        'success'        : False,
        'data'           : { }
    }
    
    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)
    
    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    
    validacionPeticion = validacionWsRecuperarContrasena(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.recuperarContrasena(peticion)
    return responder(respuestaRaw)


def validacionWsRecuperarContrasena(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                'usuario' : { 'type' : 'string' },
                
            },
            'required' : [
                'usuario'
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

#Recuperar contraseña ----------------------------------------------------------
def wsRecuperarContrasenaUnificado(request):
    respuestaRaw = {
        'success' : False,
        'data'    : { }
    }
    
    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)
    
    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)
    
    validacionPeticion = validacionWsRecuperarContrasenaUnificado(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.recuperarContrasenaUnificado(peticion)
    return responder(respuestaRaw)


def validacionWsRecuperarContrasenaUnificado(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                'usuario' : { 'type' : 'string' },
                
            },
            'required' : [
                'usuario'
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

#Cambiar contraseña ----------------------------------------------------------
def wsCambiarContrasena(request):
    respuestaRaw = {
        'success'        : False,
        'data'           : { }
    }
    
    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)
    
    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    
    validacionPeticion = validacionWsCambiarContrasena(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.cambiarContrasena(peticion)
    return responder(respuestaRaw)

def validacionWsCambiarContrasena(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                'token'      : { 'type' : 'string' },
                'contrasena' : { 'type' : 'string' }                
            },
            'required' : [
                'token',
                'contrasena'
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
#Valida los datos e autenticacion de un usuario.
def wsVerificarCredenciales(request):
    respuestaRaw = {
        'success'        : False,
        'data'           : { }
    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsVerificarCredenciales(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.verificarCredenciales(peticion)
    return responder(respuestaRaw)

def validacionWsVerificarCredenciales(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'   	  : 'object',
            'properties'  : {
                'usuario': { 'type' : 'string' },
                'token'  : { 'type' : 'string' },
                'tenant' : { 'type' : 'string' },
                
                
            },
            'required' : [
                'usuario',
                'token',
                'tenant'
            ]
        }
        validate(peticion ,schema)        
    except ValidationError as e:
        error   = e.message
        success = False
    except:
        error = 'Error desconocido-R002'
        success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw
#===============================================================================

#--------------------------------------------------------------
def wsActualizarCerrarSesion(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActualizarCerrarSesion(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = autenticacion.actualizarCerrarSesion(peticion)
    
    return responder(respuestaRaw)


def validacionWsActualizarCerrarSesion(peticion):
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
