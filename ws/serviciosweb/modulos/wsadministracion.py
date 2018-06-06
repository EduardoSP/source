# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from cuentausuario             import cuentausuario
from administracion             import administracion
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging

#--------------------------------------------------------------
def wslistadoTenants(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWslistadoTenants(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wslistarTenants",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.listarTenants(peticion)
    
    return responder(respuestaRaw)


def validacionWslistadoTenants(peticion):
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
def wsCrearTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsCrearTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsCrearTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.crearTenant(peticion)
    return responder(respuestaRaw)


def validacionWsCrearTenant(peticion):
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
                        'nit'            : { 'type' : 'string' },
                        'urlTenant'      : { 'type' : 'string' },
                        'celularEmergencia'  : { 'type' : 'string' },
                        'nombreGeneral'  : { 'type' : 'string' },
                        'idImagenLogo'   : { 'type' : 'string' },
                        'telefono'       : { 'type' : 'string' },
                        'direccion'      : { 'type' : 'string' }
                    },
                    'required' : [
                        'nit'            ,
                        'urlTenant'      ,
                        'celularEmergencia', 
                        'nombreGeneral'  ,
                        'idImagenLogo'   ,
                        'telefono'       ,
                        'direccion'
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
def wsDetalleTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.detalleTenant(peticion)
    return responder(respuestaRaw)


def validacionWsDetalleTenant(peticion):
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
def wsEditarTenant(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsEditarTenant(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsEditarTenant",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.editarTenant(peticion)
    
    return responder(respuestaRaw)

def validacionWsEditarTenant(peticion):
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
                        'id'             : { 'type' : 'string' },
                        'activo'         : { 'type' : 'boolean' },
                        'nit'            : { 'type' : 'string' },
                        'correo'            : { 'type' : 'string' },
                        'urlTenant'      : { 'type' : 'string' },
                        'celularEmergencia'  : { 'type' : 'string' },
                        'nombreGeneral'  : { 'type' : 'string' },
                        'idImagenLogo'   : { 'type' : 'string' },
                        'telefono'       : { 'type' : 'string' },
                        'direccion'      : { 'type' : 'string' }
                    },
                    'required' : [
                        'id',
                        'activo',
                        'nit',
                        'correo',
                        'urlTenant',
                        'celularEmergencia', 
                        'nombreGeneral',
                        'idImagenLogo'
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
def wsActivarPermisosPlataforma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsActivarPermisosPlataforma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsActivarPermisosPlataforma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.activarPermisosPlataforma(peticion)
    
    return responder(respuestaRaw)

def validacionWsActivarPermisosPlataforma(peticion):
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
def wsDesactivarPermisosPlataforma(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDesactivarPermisosPlataforma(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDesactivarPermisosPlataforma",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = administracion.desactivarPermisosPlataforma(peticion)
    
    return responder(respuestaRaw)

def validacionWsDesactivarPermisosPlataforma(peticion):
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
