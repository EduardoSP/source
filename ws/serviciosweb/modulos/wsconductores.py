# -*- coding: utf-8 -*-
from django.shortcuts           import render
from django.http                import HttpResponse
import json
from ProtocoloComunicacion      import responder, validarProtocoloPeticion
from conductores                import conductores
from generadoresCarga           import generadoresCarga
from permisos                   import permisos
from jsonschema                 import validate, ValidationError
from datetime                   import datetime, timedelta
import logging
import csv

#--------------------------------------------------------------
def wslistarConductores(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarConductores(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarConductores",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.listarConductores(peticion)
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
    

    



def validacionWslistarConductores(peticion):
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
def wscrearConductor(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWscrearConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wscrearConductor",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.crearConductor(peticion)
    
    return responder(respuestaRaw)


def validacionWscrearConductor(peticion):
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
def wsEliminarConductor(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEliminarConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEliminarConductor",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.eliminarConductor(peticion)
    
    return responder(respuestaRaw)


def validacionWsEliminarConductor(peticion):
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
def wsDetalleConductor(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleConductor",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.detalleConductor(peticion)
    
    return responder(respuestaRaw)


def validacionWsDetalleConductor(peticion):
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
def wsEditarConductor(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEditarConductor",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.editarConductor(peticion)
    
    return responder(respuestaRaw)


def validacionWsEditarConductor(peticion):
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
def wsDescargarArchivoCsvConductores(request, usuario, tenant):
    print tenant
    response = conductores.descargarArchivoCsvConductores(usuario, tenant)
    return response

#---------------------------------------------------------------------------------
def wsCargarArchivoCsvConductores(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCargarArchivoCsvConductores",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.cargarArchivoCsvConductores(peticion, request)
    
    return responder(respuestaRaw)


def validacionWsCargarArchivoCsvConductores(peticion):
    success = True
    error   = ''

    try:
        
        data   = peticion['data']
        
        schema = {
            'type'      : 'object',
            'properties'    : {
                
                'autenticacion' : {
                    'type'      : 'object',
                    'properties'    : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                        'perfil'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'perfil'
                    ]
                },
            
                'data' : {
                    'type' : 'object'                    
                }
            }
        }
    except ValidationError as e:
        error   = e.message
        success = False
    except:
        error = 'Error desconocido-T016'
        success = False
                    
    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw

#=================================================================================

#--------------------------------------------------------------
def wsPickerConductores(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsPickerConductores(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsPickerConductores",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.pickerConductores(peticion)
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
    
    return responder(respuestaRaw)


def validacionWsPickerConductores(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'         : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'         : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                        'tenant'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
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
def wsAsignarConductor(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsAsignarConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsAsignarConductor",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.asignarConductor(peticion)
    
    return responder(respuestaRaw)


def validacionWsAsignarConductor(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'         : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'         : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                        'tenant'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
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
def wsVerificarConductorAsignado(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsVerificarConductorAsignado(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsVerificarConductorAsignado",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.verificarConductorAsignado(peticion)
    
    return responder(respuestaRaw)


def validacionWsVerificarConductorAsignado(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'         : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'         : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                        'tenant'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
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
def wsReAsignarConductor(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReAsignarConductor(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReAsignarConductor",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = conductores.reAsignarConductor(peticion)
    
    return responder(respuestaRaw)


def validacionWsReAsignarConductor(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'         : 'object',
            'properties'  : {
                "autenticacion" : {
                    'type'         : 'object',
                    'properties'  : {
                        'usuario' : { 'type' : 'string' },
                        'token'   : { 'type' : 'string' },
                        'tenant'   : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
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
