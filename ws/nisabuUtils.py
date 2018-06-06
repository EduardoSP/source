# -*- encoding: utf-8 -*-
from ws import *
import couchdb
from django.shortcuts   import render
from sendfile           import sendfile
from django.conf        import settings
from django.http                    import HttpResponse
import os, sys
from PIL import Image
import logging
from shutil import copyfile
import json

def getConexion():
    couch = couchdb.Server(url=settings.COUCHDB_URL)
    return couch['nisabu']

def copiarArchivo(archivo, rutaDestino):
    destino = open(rutaDestino, 'wb+')
    for chunk in archivo.chunks():
        destino.write(chunk)
    destino.close()

def copiarArchivoNombre(archivo, rutaDestino):
    copyfile(archivo.name, rutaDestino)
    
#retorna el identificador con que quedó guardado.
def guardarImagenFile(archivo):
    db              = getConexion()
    imagen          =  {'nombre': archivo.name}
    db.save(imagen)
    nombreTemporal  = settings.NISABU_CACHE_DIR+'/tmp/'+imagen['_id']
    copiarArchivoNombre(archivo,nombreTemporal)
    f = open(nombreTemporal,'rb')
    db.put_attachment(imagen, f, filename="imagen")
    return imagen['_id']
#     return {
#         'success'   : True,
#         'id'        : imagen['_id'],
#         'url'       : nombreTemporal
#     }
#===============================================================================

def guardarImagen(request):
    db              = getConexion()
    
    if 'archivo' in  request.FILES:
        dato          = request.FILES['archivo']        
        #imagenId        = nisabuUtils.guardarImagen(imagen)    
        imagen          =  {'nombre': dato.name}
        db.save(imagen)
        nombreTemporal  = settings.NISABU_CACHE_DIR+'/tmp/'+imagen['_id']        
        copiarArchivo(dato,nombreTemporal)
        
        f = open(nombreTemporal,'rb')        
        db.put_attachment(imagen, f, filename="imagen")
        
        #return imagen['_id']
        dataRaw = {
                    'success'   : True,
                    'id'        : imagen['_id'],
                    'url'       : settings.NISABU_IMAGE_URL+''+imagen['_id']
                  }
        data = json.dumps(dataRaw)
        return HttpResponse(data, content_type='application/json')

def guardarArchivo(request):
    db              = getConexion()
    
    if 'archivo' in  request.FILES:
        dato           = request.FILES['archivo']        
        #imagenId        = nisabuUtils.guardarImagen(imagen)    
        archivo          =  {'nombre': dato.name}
        db.save(archivo)
        nombreTemporal  = settings.NISABU_CACHE_DIR+'/tmp/'+archivo['_id']        
        copiarArchivo(dato,nombreTemporal)
        
        f = open(nombreTemporal,'rb')        
        db.put_attachment(archivo, f, filename="archivo")
        
        #return imagen['_id']
        dataRaw = {
                    'success'   : True,
                    'id'        : archivo['_id'],
                    'url'       : u"{}{}/{}".format(settings.NISABU_ARCHIVO_URL,archivo['_id'],dato.name )
                  }
        data = json.dumps(dataRaw)
        return HttpResponse(data, content_type='application/json')

