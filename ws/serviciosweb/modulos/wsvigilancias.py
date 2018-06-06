# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from vigilancias               import vigilancias, tiposZonas
from generadoresCarga          import generadoresCarga
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging


#--------------------------------------------------------------
def wsmonitoreoZonas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsmonitoreoZonas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsmonitoreoZonas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarMonitoreoZonas(peticion)

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
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)
    #----------------------------------

def validacionWsmonitoreoZonas(peticion):
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
def wslistarVigilancias(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarVigilancias(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarVigilancias",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarVigilancias(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarVigilancias(peticion):
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
def wscrearZonas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearZonas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wscrearZonas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.crearZonas(peticion)
    
    return responder(respuestaRaw)

def validacionWsCrearZonas(peticion):
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
                        'nombre'      : { 'type' : 'string' },
                        'descripcion'   : { 'type' : 'string' },
                        'registrarAudio' : {'type' : 'boolean'},
                        'registrarImagen': {'type' : 'boolean'},
                        'tiempoMaxGrabAudio': {'type' : 'string'},
                        'numeroCapturasMax' : {'type' : 'string'},
                        'latitud': {'type' : 'string'},
                        'longitud': {'type' : 'string'},
                        'radio': {'type': 'string'}
                    },
                    'required' : [
                        'nombre',
                        'descripcion',
                        'tiempoMaxGrabAudio',
                        'numeroCapturasMax'

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


#--------------------------------------------------------------
def wseditarZona(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarZona(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wseditarZona",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.editarZonas(peticion)
    
    return responder(respuestaRaw)

def validacionWsEditarZona(peticion):
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
                "data" : {
                    'type'        : 'object',
                    'properties'  : {
                        'id'      :{'type': 'string'},
                        'nombre'      : { 'type' : 'string' },
                        'descripcion'   : { 'type' : 'string' },
                        'registrarAudio' : {'type' : 'boolean'},
                        'registrarImagen': {'type' : 'boolean'},
                        'tiempoMaxGrabAudio': {'type' : 'string'},
                        'numeroCapturasMax' : {'type' : 'string'},
                        'latitud': {'type' : 'string'},
                        'longitud': {'type' : 'string'},
                        'radio': {'type': 'string'}
                    },
                    'required' : [
                        'nombre',
                        'descripcion',
                        'tiempoMaxGrabAudio',
                        'numeroCapturasMax'

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

#--------------------------------------------------------------
def wseliminarZonas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEliminarZonas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wseliminarZonas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.eliminarZonas(peticion)
    
    return responder(respuestaRaw)

def validacionWsEliminarZonas(peticion):
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
                "data" : {
                    'type'        : 'object',
                    'properties'  : {
                        'id'      : { 'type' : 'string' }
                    },
                    'required' : [
                        'id'
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





#--------------------------------------------------------------
def wscrearProgramacion(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearProgramacion(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wscrearProgramacion",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.crearProgramacion(peticion)
    
    return responder(respuestaRaw)

def validacionWsCrearProgramacion(peticion):
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
                        'idVehiculo'      : { 'type' : 'string' },
                        'registrarAudio'   : { 'type' : 'boolean' },
                        'registrarImagen': {'type' : 'boolean'},
                        'fechaInicio': {'type' : 'string'},
                        'fechaFin' : {'type' : 'string'},
                        'horaInicio': {'type' : 'string'},
                        'horaFin': {'type' : 'string'}
                    },
                    'required' : [
                        'idVehiculo',
                        'registrarAudio',
                        'registrarImagen',
                        'fechaInicio',
                        'fechaFin',
                        'horaInicio',
                        'horaFin'

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


#--------------------------------------------------------------
def wsEliminarProgramacionVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEliminarProgramacionVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEliminarprogramacionVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.eliminarProgramacionVigilancia(peticion)
    
    return responder(respuestaRaw)

def validacionWsEliminarProgramacionVigilancia(peticion):
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
                        'id'      : { 'type' : 'string' }
                    },
                    'required' : [
                        'id'
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

#--------------------------------------------------------------
def wszonaAlarmas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsZonaAlarmas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wszonaAlarmas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.zonaAlarmas(peticion)
    
    return responder(respuestaRaw)

def validacionWsZonaAlarmas(peticion):
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
                "data" : {
                    'type'        : 'object',
                    'properties'  : {
                        'id'      : { 'type' : 'string' }
                    },
                    'required' : [
                        'id'
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


#--------------------------------------------------------------
def wslistarDetalleZona(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarDetalleZona(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarDetalleZona",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarDetalleZona(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarDetalleZona(peticion):
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
def wslistarDetalleZonaAlarma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarDetalleZonaAlarma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarDetalleZonaAlarma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarDetalleZonaAlarma(peticion)
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


def validacionWslistarDetalleZonaAlarma(peticion):
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
def wslistarDetalleVehiculoZonaAlarma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarDetalleVehiculoZonaAlarma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarDetalleVehiculoZonaAlarma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarDetalleVehiculoZonaAlarma(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarDetalleVehiculoZonaAlarma(peticion):
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
def wslistarPosicionZonaAlarma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarPosicionZonaAlarma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarPosicionZonaAlarma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarPosicionZonaAlarma(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarPosicionZonaAlarma(peticion):
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
def wslistarCapturaImagenesZonaAlarma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarCapturaImagenesZonaAlarma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarCapturaImagenesZonaAlarma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarCapturaImagenesZonaAlarma(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarCapturaImagenesZonaAlarma(peticion):
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
def wslistarCapturaAudiosZonaAlarma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarCapturaAudiosZonaAlarma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarCapturaAudiosZonaAlarma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarCapturaAudiosZonaAlarma(peticion)
    
    return responder(respuestaRaw)


def validacionWslistarCapturaAudiosZonaAlarma(peticion):
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
        error   = 'Error desconocido-R001'
        success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw
#===============================================================================
#--------------------------------------------------------------
def wslistarProgramacionVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarProgramacionVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarProgramacionVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarProgramacionVigilancia(peticion)

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
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)
    #----------------------------------

def validacionWslistarProgramacionVigilancia(peticion):
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
def wscrearProgramacionVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWscrearProgramacionVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wscrearProgramacionVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.crearProgramacionVigilancia(peticion)
    
    return responder(respuestaRaw)


def validacionWscrearProgramacionVigilancia(peticion):
    success = True
    error   = ''    
    try:                
        schema = {
            'type'        : 'object',
            'properties'  : {
                "autenticacion"   : {
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
                "data" : {
                    'type'        : 'object',
                    'properties'  : {
                        'idVehiculo'        : { 'type'  : 'string' },
                        'registrarAudio'    : {'type'   : 'boolean'},
                        'registrarImagen'   : {'type'   : 'boolean'},
                        'capturasMax'       : {'type'   : 'string'},
                        'grabMax'           : {'type'   : 'string'},
                        'fechaInicio'       : {'type'   : 'string'},
                        'fechaFin'          : {'type'   : 'string'},
                        'horaInicio'        : {'type'   : 'string'},
                        'horaFin'           : {'type'   : 'string'}
                    },
                    'required' : [
                        'idVehiculo',
                        'fechaInicio',
                        'fechaFin',
                        'horaInicio',
                        'horaFin'


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


#--------------------------------------------------------------
def wslistarPosicionesVehiculoVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarPosicionesVehiculoVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarPosicionesVehiculoVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarPosicionesVehiculoVigilancia(peticion)
    
    return responder(respuestaRaw)



def validacionWslistarPosicionesVehiculoVigilancia(peticion):
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

def wslistarDetalleVehiculoProgramacionVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarDetalleVehiculoProgramacionVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarDetalleVehiculoProgramacionVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarDetalleVehiculoProgramacionVigilancia(peticion)
    
    return responder(respuestaRaw)

def validacionWslistarDetalleVehiculoProgramacionVigilancia(peticion):
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

def wslistarImagenesProgramacionVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarImagenesProgramacionVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarImagenesProgramacionVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarImagenesProgramacionVigilancia(peticion)
    
    return responder(respuestaRaw)

def validacionWslistarImagenesProgramacionVigilancia(peticion):
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

def wslistarAudiosProgramacionVigilancia(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistarAudiosProgramacionVigilancia(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarAudiosProgramacionVigilancia",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.listarAudiosProgramacionVigilancia(peticion)
    
    return responder(respuestaRaw)

def validacionWslistarAudiosProgramacionVigilancia(peticion):
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
def wsparadaPorRangoFecha(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsparadaPorRangoFecha(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsparadaPorRangoFecha",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.paradaPorRangoFecha(peticion)
    
    return responder(respuestaRaw)


def validacionWsparadaPorRangoFecha(peticion):
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


#Tipo de Zonas -----------------------------------------------------------------

#--------------------------------------------------------------
def wsCrearTipoZona(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearTipoZona(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCrearTipoZona",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = tiposZonas.crearTipoZona(peticion)
    
    return responder(respuestaRaw)


def validacionWsCrearTipoZona(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'  ,
                        'tenant'
                    ]
                },
                "data" : {
                    'type'       : 'object',
                    'properties' : {
                        'nombre' : { 'type' : 'string' }
                    },
                    'required' : [
                        'nombre'
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

#--------------------------------------------------------------
def wsEditarTipoZona(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarTipoZona(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEditarTipoZona",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = tiposZonas.editarTipoZona(peticion)
    
    return responder(respuestaRaw)


def validacionWsEditarTipoZona(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'  ,
                        'tenant'
                    ]
                },
                "data" : {
                    'type'       : 'object',
                    'properties' : {
                        'id'     : { 'type' : 'string' },
                        'nombre' : { 'type' : 'string' }
                        # 'activo' : { 'type' : 'boolean' }
                    },
                    'required' : [
                        'id',
                        'nombre'
                        # 'activo'
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
    except Exception as e:
        # Exception , e --> tambien se puede de esta forma
        print (e)
        error = 'Error desconocido-R001'
        success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw
#===============================================================================

#--------------------------------------------------------------
def wsDetalleTipoZona(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleTipoZona(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleTipoZona",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)
 
    respuestaRaw = tiposZonas.detalleTipoZona(peticion)
    
    return responder(respuestaRaw)


def validacionWsDetalleTipoZona(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'  ,
                        'tenant'
                    ]
                },
                "data" : {
                    'type'       : 'object',
                    'properties' : {
                        'id' : { 'type' : 'string' }
                    },
                    'required': [
                        'id'
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


#--------------------------------------------------------------
def wsEliminarTipoZona(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEliminarTipoZona(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEliminarTipoZona",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = tiposZonas.eliminarTipoZona(peticion)
    
    return responder(respuestaRaw)


def validacionWsEliminarTipoZona(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'  ,
                        'tenant'
                    ]
                },
                "data" : {
                    'type'       : 'object',
                    'properties' : {
                        'id' : { 'type' : 'string' }
                    },
                    'required': [
                        'id'
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


#--------------------------------------------------------------
def wsListarTiposZonas(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsListarTiposZonas(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsListarTiposZonas",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = tiposZonas.listarTiposZonas(peticion)

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
        return responder(respuestaRaw)
    #---------------------------------------------------------------
    else:
        return responder(respuestaRaw)
    #----------------------------------


def validacionWsListarTiposZonas(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'  ,
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
def wsValidarAudioImagenVehiculo(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsValidarAudioImagenVehiculo(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsValidarAudioImagenVehiculo",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = vigilancias.validarAudioImagenVehiculo(peticion)
    
    return responder(respuestaRaw)


def validacionWsValidarAudioImagenVehiculo(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token'  ,
                        'tenant'
                    ]
                },
                "data" : {
                    'type'       : 'object',
                    'properties' : {
                    },
                    'required': [
                        'idVehiculo'
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
