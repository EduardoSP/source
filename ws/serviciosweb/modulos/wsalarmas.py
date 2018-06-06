# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from alarmas                   import alarmas
from generadoresCarga           import generadoresCarga
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging




#--------------------------------------------------------------
def wslistarAlarmas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarVehiculos(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarVehiculos",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.listarAlarmas(peticion)
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

def validacionWslistarVehiculos(peticion):
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
def wsListarUltimasAlarmas(request):
    respuestaRaw = {
        'success'        : False,
        'data'           : { }
    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarUltimasAlarmas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarUltimasAlarmas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.listarUltimasAlarmas(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarUltimasAlarmas(peticion):
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
def wslistarAlarmasPorVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarAlarmasPorVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarAlarmasPorVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.listarAlarmasPorVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarAlarmasPorVehiculo(peticion):
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
def wslistarParadaVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarParadaVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarParadaVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.listarParadaVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarParadaVehiculo(peticion):
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
def wslistarDetalleVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarDetalleVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarDetalleVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.listarDetalleVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarDetalleVehiculo(peticion):
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
def wsposicionVehiculoRangoFecha(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsposicionVehiculoRangoFecha(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsposicionVehiculoRangoFecha",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.posicionVehiculoRangoFecha(peticion)
    
    return responder(respuestaRaw)


def validacionWsposicionVehiculoRangoFecha(peticion):
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
def wsvehiculoRangoFechaCapturaImagen(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsvehiculoRangoFechaCapturaImagen(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsvehiculoRangoFechaCapturaImagen",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.vehiculoRangoFechaCapturaImagen(peticion)
    
    return responder(respuestaRaw)


def validacionWsvehiculoRangoFechaCapturaImagen(peticion):
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
def wsvehiculoRangoFechaCapturaAudio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsvehiculoRangoFechaCapturaAudio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsvehiculoRangoFechaCapturaAudio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.vehiculoRangoFechaCapturaAudio(peticion)
    
    return responder(respuestaRaw)


def validacionWsvehiculoRangoFechaCapturaAudio(peticion):
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
def wsvehiculoRangoFechaAlarma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsvehiculoRangoFechaAlarma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsvehiculoRangoFechaAlarma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.vehiculoRangoFechaAlarma(peticion)
    
    return responder(respuestaRaw)


def validacionWsvehiculoRangoFechaAlarma(peticion):
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
def wsultimaPosicionVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsultimaPosicionVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsultimaPosicionVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.ultimaPosicionVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWsultimaPosicionVehiculo(peticion):
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
def wslistVehiculos(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistVehiculos(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistVehiculos",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.listVehiculos(peticion)
    
    return responder(respuestaRaw)


def validacionWslistVehiculos(peticion):
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
def wssolicitarCapturaAudio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWssolicitarCapturaAudio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wssolicitarCapturaAudio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.solicitarCapturaAudio(peticion)
    
    return responder(respuestaRaw)


def validacionWssolicitarCapturaAudio(peticion):
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
def wsdetenerCapturaAudio(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsdetenerCapturaAudio(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsdetenerCapturaAudio",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.detenerCapturaAudio(peticion)
    
    return responder(respuestaRaw)


def validacionWsdetenerCapturaAudio(peticion):
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


def wsverificarEstadoLlamada(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsverificarEstadoLlamada(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsverificarEstadoLlamada",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vehiculos.verificarEstadoLlamada(peticion)    
    return responder(respuestaRaw)


def validacionWsverificarEstadoLlamada(peticion):
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


#===============================================================================


def wslistarDetalleAlarmaPanico(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarDetalleAlarmaPanico(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarDetalleAlarmaPanico",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.listarDetalleAlarmaPanico(peticion)    
    return responder(respuestaRaw)


def validacionWslistarDetalleAlarmaPanico(peticion):
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

#===============================================================================


def wslistarCapturaImagenesPanico(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarCapturaImagenesPanico(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarCapturaImagenesPanico",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.listarCapturaImagenesPanico(peticion)    
    return responder(respuestaRaw)


def validacionWslistarCapturaImagenesPanico(peticion):
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


#===============================================================================


def wslistarCapturaAudiosPanico(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarCapturaAudiosPanico(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarCapturaAudiosPanico",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.listarCapturaAudiosPanico(peticion)    
    return responder(respuestaRaw)


def validacionWslistarCapturaAudiosPanico(peticion):
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

#===============================================================================

def wsactualizarIngresoAlarmasUsuario(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsactualizarIngresoAlarmasUsuario(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsactualizarIngresoAlarmasUsuario",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)
    #---Evalua si la solicitud es de un generador de carga-----------
    codigoAcceso = peticion["autenticacion"].get("codigoAcceso","None")
    if(codigoAcceso != "None"):
        #generador de carga
        respuestaRaw = alarmas.actualizarIngresoAlarmasUsuarioGeneradorCarga(peticion)
    else:
        respuestaRaw = alarmas.actualizarIngresoAlarmasUsuario(peticion)


    return responder(respuestaRaw)



def validacionWsactualizarIngresoAlarmasUsuario(peticion):
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



#===============================================================================

def wsmostrarAlarmasNoVistasUsuario(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsmostrarAlarmasNoVistasUsuario(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsmostrarAlarmasNoVistasUsuario",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = alarmas.mostrarAlarmasNoVistasUsuario(peticion)    
    return responder(respuestaRaw)



def validacionWsmostrarAlarmasNoVistasUsuario(peticion):
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

