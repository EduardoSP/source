# -*- coding: utf-8 -*-
from django.shortcuts           import render
from django.http                import HttpResponse
import json
from ProtocoloComunicacion      import responder, validarProtocoloPeticion
from permisos                   import permisos
from jsonschema                 import validate, ValidationError
import logging
from cadenaFrio                 import cadenaFrio
from generadoresCarga           import generadoresCarga

# wsListadoPuntosCadenaFrio
# wsActualizarAlarmaCadenaFrio
# wsListadoVehiculosCadenaFrio
# wsReporteTemperaturaVehiculos

#--------------------------------------------------------------
def wsListadoAlarmasCadenaFrio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListadoAlarmasCadenaFrio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListadoAlarmasCadenaFrio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.listadoAlarmasCadenaFrio(peticion)
    
    #TODO FABIO DUMMY
    #dataRaw = []
    #respuestaRaw = {
    #    'success' : True,
    #    'data'    : dataRaw
    #}        
    return responder(respuestaRaw)
    #---------------------------------------------------------------
    

def validacionWsListadoAlarmasCadenaFrio(peticion):
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


# wsListadoPuntosCadenaFrio
#--------------------------------------------------------------
def wsListadoPuntosCadenaFrio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListadoPuntosCadenaFrio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListadoPuntosCadenaFrio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.listadoPuntosCadenaFrio(peticion)
    
    #TODO FABIO DUMMY
    #dataRaw = []
    #respuestaRaw = {
    #    'success' : True,
    #    'data'    : dataRaw
    #}        
    return responder(respuestaRaw)
    #---------------------------------------------------------------
    

def validacionWsListadoPuntosCadenaFrio(peticion):
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

# wsActualizarAlarmaCadenaFrio
#--------------------------------------------------------------
def wsActualizarAlarmaCadenaFrio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActualizarAlarmaCadenaFrio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsActualizarAlarmaCadenaFrio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.actualizarAlarmaCadenaFrio(peticion)
    
    #TODO FABIO DUMMY
    #dataRaw = []
    #respuestaRaw = {
    #    'success' : True,
    #    'data'    : dataRaw
    #}        
    return responder(respuestaRaw)
    #---------------------------------------------------------------
    

def validacionWsActualizarAlarmaCadenaFrio(peticion):
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

# wsListadoVehiculosCadenaFrio
#--------------------------------------------------------------
def wsListadoVehiculosCadenaFrio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListadoVehiculosCadenaFrio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListadoVehiculosCadenaFrio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.listadoVehiculosCadenaFrio(peticion)
    
    #TODO FABIO DUMMY
    #dataRaw = []
    #respuestaRaw = {
    #    'success' : True,
    #    'data'    : dataRaw
    #}        
    return responder(respuestaRaw)
    #---------------------------------------------------------------
    

def validacionWsListadoVehiculosCadenaFrio(peticion):
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

# wsReporteTemperaturaVehiculos
#--------------------------------------------------------------
def wsReporteTemperaturaVehiculos(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteTemperaturaVehiculos(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteTemperaturaVehiculos",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.reporteTemperaturaVehiculos(peticion)
    
    #TODO FABIO DUMMY
    #dataRaw = []
    #respuestaRaw = {
    #    'success' : True,
    #    'data'    : dataRaw
    #}        
    return responder(respuestaRaw)
    #---------------------------------------------------------------
    

def validacionWsReporteTemperaturaVehiculos(peticion):
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

def getTemperaturaVehiculo(db,idVehiculo):
    pass


# wsListarVehiculosCadenaFrio
#--------------------------------------------------------------
def wsListarVehiculosCadenaFrio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListarVehiculosCadenaFrio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarVehiculosCadenaFrio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.listarVehiculosCadenaFrio(peticion)
    #---Evalua si la solicitud es de un generador de carga-----------
    codigoAcceso = peticion["autenticacion"].get("codigoAcceso","None")
    if(codigoAcceso != "None"):
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

    #---------------------------------------------------------------
    

def validacionWsListarVehiculosCadenaFrio(peticion):
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

# wsActivarDesactivarCadenaFrioVehiculos
#--------------------------------------------------------------
def wsActivarDesactivarCadenaFrioVehiculos(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActivarDesactivarCadenaFrioVehiculos(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsActivarDesactivarCadenaFrioVehiculos",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = cadenaFrio.activarDesactivarCadenaFrioVehiculos(peticion)       
    return responder(respuestaRaw)
    #---------------------------------------------------------------
    

def validacionWsActivarDesactivarCadenaFrioVehiculos(peticion):
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
