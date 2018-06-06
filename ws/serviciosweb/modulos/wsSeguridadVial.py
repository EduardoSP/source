# -*- coding: utf-8 -*-
from django.shortcuts           import render
from django.http                import HttpResponse
import json
from ProtocoloComunicacion      import responder, validarProtocoloPeticion
from seguridadVial              import seguridadVial
from generadoresCarga           import generadoresCarga
from permisos                   import permisos
from jsonschema                 import validate, ValidationError
from datetime                   import datetime, timedelta
import logging

#--------------------------------------------------------------
def wsConsultarConduccionAgresiva(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarConduccionAgresiva(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarConduccionAgresiva",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarConduccionAgresiva(peticion)
    #---Evalua si la solicitud es de un generador de carga-----------
    codigoAcceso = peticion["autenticacion"].get("codigoAcceso","None")
    if(codigoAcceso != "None"):
        #envia un codigo de acceso. La peticion es de un generador de carga
        #consulto los vehiculos habilitados con ese codigo de acceso
        dataRaw = []
        tipoConsulta    = peticion["data"].get("posicionConduccionAgresiva","")
        listaVehiculosActivados = generadoresCarga.buscarVehiculosActivados(peticion)
        i = 0
        if tipoConsulta == "0":
            #la peticion de la consuta es por vehiculo
            for vehiculo in listaVehiculosActivados:
                for i in range(0, len(respuestaRaw["data"])):
                    if vehiculo == respuestaRaw["data"][i]["id"]:
                        dataRaw.append(respuestaRaw["data"][i])
        else:
            for vehiculo in listaVehiculosActivados:
                for i in range(0, len(respuestaRaw["data"])):
                    #busca el conductor segun un id del vehiculo
                    conductor = generadoresCarga.buscarConductorDelVehiculo(peticion, vehiculo)
                    #compara si los conductores son iguales. si es asi se agrega a la lista para enviarlo al html
                    if conductor == respuestaRaw["data"][i]["id"]:
                        dataRaw.append(respuestaRaw["data"][i])
        respuestaRaw = {
            'success' : True,
            'data'    : dataRaw
        }        
        return responder(respuestaRaw)
    #---Fin evaluacion ------------------------------------------------------------
    else:
        return responder(respuestaRaw)


def validacionWsConsultarConduccionAgresiva(peticion):
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
def wsConsultarDetalleAceleracion(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarDetalleAceleracion(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarDetalleAceleracion",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarDetalleAceleracion(peticion)
    
    return responder(respuestaRaw)


def validacionWsConsultarDetalleAceleracion(peticion):
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
def wsConsultarDetalleFrenadas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarDetalleFrenadas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarDetalleFrenadas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarDetalleFrenadas(peticion)
    
    return responder(respuestaRaw)


def validacionWsConsultarDetalleFrenadas(peticion):
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
def wsConsultarDetalleMovimientosAbruptos(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarDetalleMovimientosAbruptos(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarDetalleMovimientosAbruptos",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarDetalleMovimientosAbruptos(peticion)
    
    return responder(respuestaRaw)


def validacionWsConsultarDetalleMovimientosAbruptos(peticion):
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
def wsConsultarDetalleExcesosVelocidad(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarDetalleExcesosVelocidad(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarDetalleExcesosVelocidad",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarDetalleExcesosVelocidad(peticion)
    
    return responder(respuestaRaw)


def validacionWsConsultarDetalleExcesosVelocidad(peticion):
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
def wsConsultarEncendidoApagado(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarEncendidoApagado(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarEncendidoApagado",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarEncendidoApagado(peticion)
    
    return responder(respuestaRaw)


def validacionWsConsultarEncendidoApagado(peticion):
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
def wsConsultarPausaActiva(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarPausaActiva(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarPausaActiva",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarPausaActiva(peticion)
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
                    #print respuestaRaw["data"][i]
                    dataRaw.append(respuestaRaw["data"][i])
        respuestaRaw = {
            'success' : True,
            'data'    : dataRaw
        }        
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)


def validacionWsConsultarPausaActiva(peticion):
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
def wsConsultarConduccionContinua(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsConsultarConduccionContinua(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsConsultarConduccionContinua",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.consultarConduccionContinua(peticion)
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
                    #print respuestaRaw["data"][i]
                    dataRaw.append(respuestaRaw["data"][i])
        respuestaRaw = {
            'success' : True,
            'data'    : dataRaw
        }        
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)


def validacionWsConsultarConduccionContinua(peticion):
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
def wsRegistrarAceleracionVehiculoGPS(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsRegistrarAceleracionVehiculoGPS(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsRegistrarAceleracionVehiculoGPS",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.registrarAceleracionVehiculoGPS(peticion)
    
    return responder(respuestaRaw)


def validacionWsRegistrarAceleracionVehiculoGPS(peticion):
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
def wsRegistrarFrenadasVehiculoGPS(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsRegistrarFrenadasVehiculoGPS(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsRegistrarFrenadasVehiculoGPS",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.registrarFrenadasVehiculoGPS(peticion)
    
    return responder(respuestaRaw)


def validacionWsRegistrarFrenadasVehiculoGPS(peticion):
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
def wsRegistrarMovimientosAbruptosVehiculoGPS(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsRegistrarMovimientosAbruptosVehiculoGPS(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsRegistrarMovimientosAbruptosVehiculoGPS",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguridadVial.registrarMovimientosAbruptosVehiculoGPS(peticion)
    
    return responder(respuestaRaw)


def validacionWsRegistrarMovimientosAbruptosVehiculoGPS(peticion):
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





