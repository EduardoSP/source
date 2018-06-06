# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from cuentausuario             import cuentausuario
from administracion            import administracion
from gps                       import gps
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging

#--------------------------------------------------------------
def wslistadoGps(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistadoGps(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistadoGps",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = gps.listarGps(peticion)
    
    return responder(respuestaRaw)


def validacionWslistadoGps(peticion):
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
                        'token'   : { 'type' : 'string' }
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
def wsCrearGps(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearGps(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCrearGps",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = gps.crearGps(peticion)
    return responder(respuestaRaw)


def validacionWsCrearGps(peticion):
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
                        'tenant'  : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
                    ]
                },
                "data" : {
                    'type'         : 'object',
                    'properties'  : {
                        'identificadorGPS'            : { 'type' : 'string' },
                        'numSimCard'      : { 'type' : 'string' },
                        'tipo'  : { 'type' : 'string' },
                        'imei'  : { 'type' : 'string' },
                        'observaciones'   : { 'type' : 'string' },
                     
                    },
                    'required' : [
                        'identificadorGPS'            ,
                        'numSimCard'      ,
                        'tipo', 
                        'imei'  
                        
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
def wsDetalleGps(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleGps(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleGps",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = gps.detalleGps(peticion)
    return responder(respuestaRaw)


def validacionWsDetalleGps(peticion):
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
                        'tenant'  : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
                    ]
                },
                "data" : {
                    'type'               : 'object',
                    'properties'         : {
                        'id'            : { 'type' : 'string' }
                        
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
def wsEditarGps(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarGps(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEditarGps",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = gps.editarGps(peticion)
    
    return responder(respuestaRaw)

def validacionWsEditarGps(peticion):
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
                        'tenant'  : { 'type' : 'string' },
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
                    ]
                },
                "data" : {
                    'type'          : 'object',
                    'properties'    : {
                        'id'             : { 'type' : 'string' },
                        'activo'         : { 'type' : 'boolean' },
                        'identificadorGPS'            : { 'type' : 'string' },
                        'numSimCard'            : { 'type' : 'string' },
                        'tipo'          : { 'type' : 'string' },
                        'imei'          : { 'type' : 'string' },
                        'observaciones' : { 'type' : 'string' },
                        
                    },
                    'required' : [
                        'id',
                        'activo',
                        'identificadorGPS',
                        'numSimCard',
                        'tipo',
                        'imei', 
                        'observaciones'
                       
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
def wsCrearUsuarioAdminTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearUsuarioAdminTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCrearAdminTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.crearAdminTenant(peticion)
    
    return responder(respuestaRaw)

def validacionWsCrearUsuarioAdminTenant(peticion):
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
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                },
                "data" : {
                    'type'         : 'object',
                    'properties'  : {
                        'idTenant'       : { 'type' : 'string' },
                        'nombres'        : { 'type' : 'string' },
                        'correo'         : { 'type' : 'string' },
                        'loginUsuario'   : { 'type' : 'string' },
                        'identificacion' : { 'type' : 'string' },
                        'contrasena'     : { 'type' : 'string' },
                        'telefono'       : { 'type' : 'string' },
                    },
                    'required' : [
                        'idTenant',
                        'nombres',                        
                        'correo',                        
                        'loginUsuario',
                        'identificacion',
                        'contrasena',
                        'telefono'
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
def wsEditarUsuarioAdminTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarUsuarioAdminTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEditarAdminTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.editarAdminTenant(peticion)
    
    return responder(respuestaRaw)

def validacionWsEditarUsuarioAdminTenant(peticion):
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
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                },
                "data" : {
                    'type'         : 'object',
                    'properties'  : {
                        'idTenant'       : { 'type' : 'string' },
                        'nombres'        : { 'type' : 'string' },
                        'correo'         : { 'type' : 'string' },
                        'loginUsuario'   : { 'type' : 'string' },
                        'identificacion' : { 'type' : 'string' },
                        'contrasena'     : { 'type' : 'string' },
                        'telefono'       : { 'type' : 'string' },
                        'activo'         : { 'type' : 'boolean' },
                        
                    },
                    'required' : [
                        'idTenant',
                        'nombres',                        
                        'correo',                        
                        'loginUsuario',
                        'identificacion',
                        'contrasena',
                        'telefono',
                        'activo'
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
def wsEliminarUsuarioAdminTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEliminarUsuarioAdminTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEliminarAdminTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.eliminarAdminTenant(peticion)
    
    return responder(respuestaRaw)

def validacionWsEliminarUsuarioAdminTenant(peticion):
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
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                },
                "data" : {
                    'type'         : 'object',
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
def wsDetalleUsuarioAdminTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleUsuarioAdminTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleAdminTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.detalleAdminTenant(peticion)
    
    return responder(respuestaRaw)

def validacionWsDetalleUsuarioAdminTenant(peticion):
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
                    },
                    'required' : [
                        'usuario',
                        'token'
                    ]
                },
                "data" : {
                    'type'         : 'object',
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




#----- 8< --------------- 8< ------------------------------------
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

#--------------------------------------------------------------
def wsPickerGps(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsPickerGps(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsPickerGps",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = gps.pickerGps(peticion)
    
    return responder(respuestaRaw)


def validacionWsPickerGps(peticion):
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
