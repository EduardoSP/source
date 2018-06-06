# -*- coding: utf-8 -*-
from django.shortcuts           import render
from django.http                import HttpResponse
import json
from ProtocoloComunicacion      import responder, validarProtocoloPeticion
from generadoresCarga           import generadoresCarga
from permisos                   import permisos
from jsonschema                 import validate, ValidationError
from datetime                   import datetime, timedelta
import logging

#--------------------------------------------------------------

#--------------------------------------------------------------
def wsListarCodigosGenerados(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListarCodigosGenerados(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarCodigosGenerados",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.listarCodigosGenerados(peticion)
    
    return responder(respuestaRaw)


def validacionWsListarCodigosGenerados(peticion):
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
def wsConsultarDetalleVehiculosCodigoGenerado(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarDetalleVehiculosCodigoGenerado(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarDetalleVehiculosCodigoGenerado",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.consultarDetalleVehiculosCodigoGenerado(peticion)
    
    return responder(respuestaRaw)


def validacionWsConsultarDetalleVehiculosCodigoGenerado(peticion):
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
def wsAnularCodigoGenerado(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsAnularCodigoGenerado(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsAnularCodigoGenerado",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.anularCodigoGenerado(peticion)
    
    return responder(respuestaRaw)


def validacionWsAnularCodigoGenerado(peticion):
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
def wsGenerarCodigoAcceso(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsGenerarCodigoAcceso(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsGenerarCodigoAcceso",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.generarCodigoAcceso(peticion)
    
    return responder(respuestaRaw)


def validacionWsGenerarCodigoAcceso(peticion):
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


#--------------------------------------------------------------
def wsCrearCodigoAcceso(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearCodigoAcceso(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCrearCodigoAcceso",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.crearCodigoAcceso(peticion)
    
    return responder(respuestaRaw)


def validacionWsCrearCodigoAcceso(peticion):
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

#Autentica un usuario en el sistema y genera un token
def wsAutenticarGeneradorCarga(request):
    respuestaRaw = {
        'success'        : False,
        'data'           : { }
    }
    
    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)
    
    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    
    validacionPeticion = validacionWsAutenticarGeneradorCarga(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = generadoresCarga.autenticarGeneradorCarga(peticion)
    return responder(respuestaRaw)


def validacionWsAutenticarGeneradorCarga(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object'
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
def wsAutenticarGeneradorCargaLogin(request):
    respuestaRaw = {
        'success'        : False,
        'data'           : { }
    }
    
    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)
    
    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    
    validacionPeticion = validacionWsAutenticarGeneradorCargaLogin(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = generadoresCarga.autenticarGeneradorCargaLogin(peticion)
    return responder(respuestaRaw)


def validacionWsAutenticarGeneradorCargaLogin(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object'
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
def wsRecuperarContrasenaGeneradorCarga(request):
    respuestaRaw = {
        'success' : False,
        'data'    : { }
    }
    
    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)
    
    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)
    
    validacionPeticion = validacionWsRecuperarContrasenaGeneradorCarga(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    respuestaRaw = generadoresCarga.recuperarContrasena(peticion)
    return responder(respuestaRaw)


def validacionWsRecuperarContrasenaGeneradorCarga(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                'correo' : { 'type' : 'string' },
                
            },
            'required' : [
                'correo'
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
def wsListarCodigosAgregados(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListarCodigosAgregados(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarCodigosAgregados",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.listarCodigosAgregados(peticion)
    
    return responder(respuestaRaw)


def validacionWsListarCodigosAgregados(peticion):
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

#--------------------------------------------------------------
def wsAgregarCodigoAcceso(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsAgregarCodigoAcceso(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsAgregarCodigoAcceso",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.agregarCodigoAcceso(peticion)
    
    return responder(respuestaRaw)


def validacionWsAgregarCodigoAcceso(peticion):
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


#--------------------------------------------------------------
def wsActualizarDatosCuentaGeneradorCarga(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActualizarDatosCuentaGeneradorCarga(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsActualizarDatosCuentaGeneradorCarga",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.actualizarDatosCuentaGeneradorCarga(peticion)
    
    return responder(respuestaRaw)


def validacionWsActualizarDatosCuentaGeneradorCarga(peticion):
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

#--------------------------------------------------------------
def wsClientesCodGenerados(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsClientesCodGenerados(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsClientesCodGenerados",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = generadoresCarga.clientesCodGenerados(peticion)
    
    return responder(respuestaRaw)


def validacionWsClientesCodGenerados(peticion):
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

