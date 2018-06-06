# -*- coding: utf-8 -*-
from django.shortcuts          import render
from django.http               import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from permisos                  import permisos
from generadoresCarga           import generadoresCarga
from jsonschema                import validate, ValidationError
import logging
import time
from reportes                  import reportes

#--------------------------------------------------------------
def wsReporteEstadisticasVehiculos(request):
    
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteEstadisticasVehiculos(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteEstadisticasVehiculos",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteEstadiscasVehiculos(peticion)
    #print respuestaRaw["data"]
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


def validacionWsReporteEstadisticasVehiculos(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                'autenticacion' : {
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio" : { 'type' : 'string'},
                        "fechaFin"    : { 'type' : 'string'},
                        "vehiculos"   : { 'type' : 'array' }
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin"
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
#==============================================================


#--------------------------------------------------------------
def wsReporteEstadisticasVehiculoPorDia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteEstadisticasVehiculoPorDia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteEstadisticasVehiculoPorDia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteEstadisticasVehiculoPorDia(peticion)
    
    return responder(respuestaRaw)


def validacionWsReporteEstadisticasVehiculoPorDia(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio" : { 'type' : 'string'},
                        "fechaFin"    : { 'type' : 'string'},
                        "idVehiculo"  : { 'type' : 'string' }
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin",
                        "idVehiculo"
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
#==============================================================


#--------------------------------------------------------------
def wsReporteParadasVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteParadasVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteParadasVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteParadasVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWsReporteParadasVehiculo(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio" : { 'type' : 'string'},
                        "fechaFin"    : { 'type' : 'string'},
                        "vehiculos"   : { 'type' : 'array' }
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin"
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
#==============================================================

#--------------------------------------------------------------
def wsReporteGraficoVehiculosPorEstadistica(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteGraficoVehiculosPorEstadistica(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteGraficoVehiculosPorEstadistica",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteGraficoVehiculosPorEstadistica(peticion)
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


def validacionWsReporteGraficoVehiculosPorEstadistica(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"     : { 'type' : 'string'},
                        "fechaFin"        : { 'type' : 'string'},
                        "vehiculos"       : { 'type' : 'array' },
                        "tipoEstadistica" : { 'type' : 'string'} 
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin",
                        "tipoEstadistica"
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

#==============================================================
def wsReporteGraficoVehiculoEstadisticaPorFecha(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteGraficoVehiculoEstadisticaPorFecha(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteGraficoVehiculoEstadisticaPorFecha",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteGraficoVehiculoEstadisticaPorFecha(peticion)
    
    return responder(respuestaRaw)


def validacionWsReporteGraficoVehiculoEstadisticaPorFecha(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"     : { 'type' : 'string'},
                        "fechaFin"        : { 'type' : 'string'},
                        "idVehiculo"      : { 'type' : 'string'},
                        "tipoEstadistica" : { 'type' : 'string'} 
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin",
                        "idVehiculo",
                        "tipoEstadistica"
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
#==============================================================

#==============================================================
def wsReporteParadasVehiculosEnZonas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteParadasVehiculosEnZonas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteParadasVehiculosEnZonas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteParadasVehiculosEnZonas(peticion)

    #---Evalua si la solicitud es de un generador de carga-----------
    codigoAcceso = peticion["autenticacion"].get("codigoAcceso","None")
    if(codigoAcceso != "None"):
        #envia un codigo de acceso. La peticion es de un generador de carga
        #consulto los vehiculos habilitados con ese codigo de acceso
        vehiculosSeleccionados = peticion["data"].get("vehiculos",[])
        #valida que ha seleccionado la opcion todos en el selectPicker vehiculos
        if len(vehiculosSeleccionados) == 0:
            #filtra la respuesta segun los vehiculos que estan habilitados con el codigo de acceso
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
        #consulto los tipo zonas habilitados con el codigo de acceso
        dataRaw = []
        tipoZonaSeleccionada = peticion["data"].get("tipoZonas",[])
        tipoZonas = peticion["data"].get("tipoZonasTodos",[])
        #valida que ha seleccionado la opcion todos en el selectPicker tiposZonas
        if len(tipoZonas) >= 0 and len(tipoZonaSeleccionada) == 0:
            for i in range(0, len(respuestaRaw["data"])):
                #valido si los tiposZonas habilitados por el codigo de acceso para filtrar la respuesta de la consulta 
                #print respuestaRaw["data"]
                tiposZonasHabilitadas    = generadoresCarga.buscarTipoZonasRegistro(tipoZonas, respuestaRaw["data"][i]["tipoZonas"])
                if len(tiposZonasHabilitadas) > 0:
                    #si tiene tipos zonas habilitadas se agrega a la respuesta todo el registro
                    respuestaRaw["data"][i]["tipoZonas"] = tiposZonasHabilitadas
                    dataRaw.append(respuestaRaw["data"][i])
                #print respuestaRaw["data"]
            respuestaRaw = {
                'success' : True,
                'data'    : dataRaw
            }
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)



def validacionWsReporteParadasVehiculosEnZonas(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"     : { 'type' : 'string'},
                        "fechaFin"        : { 'type' : 'string'} 
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin"
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
#==============================================================

#==============================================================
def wsReporteMapaCalorActividadVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteMapaCalorActividadVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteMapaCalorActividadVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteMapaCalorActividadVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWsReporteMapaCalorActividadVehiculo(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"  : { 'type' : 'string'},
                        "fechaFin"     : { 'type' : 'string'},
                        "idVehiculo"   : { 'type' : 'string'} 
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin",
                        "idVehiculo"
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
#==============================================================

#==============================================================
def wsReporteCalificacionConductores(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteCalificacionConductores(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteCalificacionConductores",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteCalificacionConductores(peticion)
    
    return responder(respuestaRaw)


def validacionWsReporteCalificacionConductores(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"  : { 'type' : 'string'},
                        "fechaFin"     : { 'type' : 'string'} 
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin"
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
#==============================================================

#==============================================================
def wsReporteConduccionPorFueraDeHorario(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReporteConduccionPorFueraDeHorario(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReporteConduccionPorFueraDeHorario",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReporteConduccionPorFueraDeHorario(peticion)
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

def validacionWsReporteConduccionPorFueraDeHorario(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"         : { 'type' : 'string'},
                        "fechaFin"            : { 'type' : 'string'},
                        "horaInicioOperacion" : { 'type' : 'string'},
                        "horaFinOperacion"    : { 'type' : 'string'} 
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin",
                        "horaInicioOperacion",
                        "horaFinOperacion"
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
#==============================================================

#==============================================================
def wsReportesCadenaFrio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsReportesCadenaFrio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsReportesCadenaFrio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = reportes.wsReportesCadenaFrio(peticion)
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
            'success'       : True,
            'data'    : dataRaw
        }        
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)

def validacionWsReportesCadenaFrio(peticion):
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
                'data': {
                    'type'       : 'object',
                    'properties' : {
                        "fechaInicio"         : { 'type' : 'string'},
                        "fechaFin"            : { 'type' : 'string'}
                    },
                    'required' : [
                        "fechaInicio",
                        "fechaFin"
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
#==============================================================
