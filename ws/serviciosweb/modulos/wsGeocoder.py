# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from permisos                  import permisos
from jsonschema                import validate, ValidationError
from geocoderFleet             import geocoderFleet
import logging


#--------------------------------------------------------------
def wsBuscarPuntosReferencias(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsBuscarPuntosReferencias(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsBuscarPuntosReferencias",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = geocoderFleet.buscarPuntosReferencias(peticion)
    
    return responder(respuestaRaw)


def validacionWsBuscarPuntosReferencias(peticion):
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
                        'tenant'  : { 'type' : 'string' }
                    },
                    'required' : [
                        'usuario',
                        'token',
                        'tenant'
                    ]
                },
                'data':{
                    'type' : 'object',
                    'properties' : {
                        "latitud"         : { 'type' : 'number'},
		        "longitud"        : { 'type' : 'number'},
		        "buscarDireccion" : { 'type' : 'boolean'} 
                    },
                    'required' : [
                        "latitud",
		        "longitud",
		        "buscarDireccion"
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
    #except:
    #    error = 'Error desconocido-R001'
    #    success = False

    respuestaRaw = { 'success'        : success,
                     'error'          : error}    
    return respuestaRaw
#===============================================================================

