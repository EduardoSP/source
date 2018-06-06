# -*- coding: utf-8 -*-
from django.shortcuts   import render
from django.http        import HttpResponse
import json
import logging

def validarProtocoloPeticion(request):
    respuestaRaw = { 'success'        : False,
                     'error'          : ''}
    
    if not request.method == "POST":
        respuestaRaw['error'] =  u'No es una petición POST, debe ser POST'
    elif not 'request' in request.POST:
        respuestaRaw['error'] =  u'No se especificó el valor request en el POST'
    else:
        respuestaRaw['success'] = True
    return respuestaRaw

def validarProtocoloPeticionGet(request):
    respuestaRaw = { 'success'        : False,
                     'error'          : ''}
 
    if not request.method == "GET":
        respuestaRaw['error'] =  u'No es una petición GET, debe ser GET'
    elif not 'request' in request.GET:
        respuestaRaw['error'] =  u'No se especificó el valor request en el POST'
    else:
        respuestaRaw['success'] = True
    return respuestaRaw


#Recibe un objeto simple para responder y retorna la respuesta adecuada.
def responder(dataRaw):
    data = json.dumps(dataRaw)
    return HttpResponse(data, content_type='application/json')
