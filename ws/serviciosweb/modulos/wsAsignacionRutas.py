# -*- coding: utf-8 -*-
from django.shortcuts           import render
from django.http                import HttpResponse
import json
from ProtocoloComunicacion      import responder, validarProtocoloPeticion
from jsonschema                 import validate, ValidationError
from datetime                   import datetime, timedelta

from rutas                      import rutas
from generadoresCarga          import generadoresCarga
from asignacionRutas            import asignacionRutas
from permisos                   import permisos


#--------------------------------------------------------------
def wsListarAsignacionesRutas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListarAsignacionesRutas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarAsignacionesRutas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = asignacionRutas.listarAsignacionesRutas(peticion)
    #-------Evalua si la solicitud es de un generador de carga-----------
    codigoAcceso = peticion["autenticacion"].get("codigoAcceso","None")
    if(codigoAcceso != "None"):
        #si es un generador de carga habilita si puede actualizar los datos segun la configuracion del cliente
        dataRaw = []
        idUsuarioPeticion       = peticion["autenticacion"].get("usuario","") #se obtiene el identificador del generador
        dataRaw                 = generadoresCarga.procesarPermisoDatosGeneradorCarga(peticion, respuestaRaw, idUsuarioPeticion)
        respuestaRaw = {
            'success' : True,
            'data'    : dataRaw
        }
        #envia un codigo de acceso. La peticion es de un generador de carga
        #consulto los vehiculos habilitados con ese codigo de acceso
        dataRaw = []
        listaVehiculosActivados = generadoresCarga.buscarVehiculosActivados(peticion)
        i = 0
        for vehiculo in listaVehiculosActivados:
            for i in range(0, len(respuestaRaw["data"])):
                if vehiculo == respuestaRaw["data"][i]["idVehiculo"]:
                    dataRaw.append(respuestaRaw["data"][i])
        respuestaRaw = {
            'success' : True,
            'data'    : dataRaw
        }        
        return responder(respuestaRaw)
    #---Fin evaluacion ------------------------------------------------------------
    else:
        return responder(respuestaRaw)


def validacionWsListarAsignacionesRutas(peticion):
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
                },
                "data"  : {
                    'type'        : 'object',
                    'properties'  : {                        
                    }
                    
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
    except ValueError:
        error = 'Error desconocido-R001'
        success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw
#===============================================================================

#--------------------------------------------------------------
def wsCrearAsignacionRuta(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearAsignacionRuta(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCrearAsignacionRuta",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = asignacionRutas.crearAsignacionRuta(peticion)
    
    return responder(respuestaRaw)


def validacionWsCrearAsignacionRuta(peticion):
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
                },
                "data"  : {
                    'type'        : 'object',
                    'properties'  : {                        
                    }
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
def wsDetalleAsignacionRuta(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleAsignacionRuta(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleAsignacionRuta",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = asignacionRutas.detalleAsignacionRuta(peticion)
    
    return responder(respuestaRaw)


def validacionWsDetalleAsignacionRuta(peticion):
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
                },
                "data"  : {
                    'type'        : 'object',
                    'properties'  : {                        
                    }
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
def wsEditarAsignacionRuta(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarAsignacionRuta(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEditarAsignacionRuta",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = asignacionRutas.editarAsignacionRuta(peticion)
    
    return responder(respuestaRaw)


def validacionWsEditarAsignacionRuta(peticion):
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
                },
                "data"  : {
                    'type'        : 'object',
                    'properties'  : {                        
                    }
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
def wsEliminarAsignacionRuta(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEliminarAsignacionRuta(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEliminarAsignacionRuta",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = asignacionRutas.eliminarAsignacionRuta(peticion)
    
    return responder(respuestaRaw)


def validacionWsEliminarAsignacionRuta(peticion):
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
                },
                "data"  : {
                    'type'        : 'object',
                    'properties'  : {                        
                    }
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
def wsAbortarAsignacionRuta(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsAbortarAsignacionRuta(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsAbortarAsignacionRuta",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = asignacionRutas.abortarAsignacionRuta(peticion)
    
    return responder(respuestaRaw)


def validacionWsAbortarAsignacionRuta(peticion):
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
                },
                "data"  : {
                    'type'        : 'object',
                    'properties'  : {                        
                    }
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

