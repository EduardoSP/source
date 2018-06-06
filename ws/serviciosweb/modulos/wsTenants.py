# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
from ProtocoloComunicacion     import responder, validarProtocoloPeticion
from tenants                   import tenants
from permisos                  import permisos
from jsonschema                import validate, ValidationError
import logging


#--------------------------------------------------------------
def wsPickerTenants(request):
    respuestaRaw = {'success'        : False,
                    'data'           : { }    }

    validacionProtocolo = validarProtocoloPeticion(request)
    if not validacionProtocolo['success']:
        return responder(validacionProtocolo)

    requestRaw  = request.POST['request']
    peticion    = json.loads(requestRaw)

    validacionPeticion = validacionWsPickerTenants(peticion)
    if not validacionPeticion['success']:
        return responder(validacionPeticion)

    validacionPermisos = permisos.validacionPermisos("wsPickerTenants",peticion)
    if not validacionPeticion['success']:
        return responder(validacionPermisos)

    respuestaRaw = tenants.pickerTenants(peticion)
    
    return responder(respuestaRaw)


def validacionWsPickerTenants(peticion):
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
