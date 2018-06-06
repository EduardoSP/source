# -*- coding: utf-8 -*-
from django.shortcuts           import render
from django.http                import HttpResponse
import json
from ProtocoloComunicacion      import responder, validarProtocoloPeticion
from jsonschema                 import validate, ValidationError
from datetime                   import datetime, timedelta

from rutas                      import rutas
from seguimientoAsignacionRutas import seguimientoAsignacionRutas
from permisos                   import permisos

#--------------------------------------------------------------
def wsDetalleSeguimientoAsignacionRuta(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsDetalleSeguimientoAsignacionRuta(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsDetalleAsignacionRuta",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = seguimientoAsignacionRutas.detalleSeguimientoAsignacionRuta(peticion)
    
    return responder(respuestaRaw)


def validacionWsDetalleSeguimientoAsignacionRuta(peticion):
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

