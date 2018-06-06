# -*- encoding: utf-8 -*-
import couchdb
from django.shortcuts   import render
from sendfile           import sendfile
from django.conf        import settings
import os, sys
import logging
from django.http import HttpResponse
from PIL import Image
 
 
thumbnail   = 128, 128
medianita   = 300, 300
grandecita  = 600, 600
 
def getConexion():
    couch = couchdb.Server(url=settings.COUCHDB_URL)
    return couch['nisabu']
 
#Copia un archivo tipo file a la rut de destino
def copiarArchivo(archivo, rutaDestino):
    destino = open(rutaDestino, 'wb+')
    destino.write(archivo.read())
    destino.close()
 
def getImage(request, imageId):
    logging.warning("iniciando")
    db              = getConexion()
    doc             = db[imageId]
    sub1            = imageId[0:3]
    sub2            = imageId[3:6]
    sub3            = imageId[6:9]
    rev             = doc['_rev']
    carpetaImagen   = settings.NISABU_CACHE_DIR+'/'+sub1+'/'+sub2+'/'+sub3+'/'+imageId
    rutaImagen      = carpetaImagen+'/'+rev+'.png'
    logging.warning("buscando en: "+rutaImagen)
    if not os.path.exists(carpetaImagen):
        os.makedirs(carpetaImagen)
    if not os.path.exists(rutaImagen):
        imagen  = db.get_attachment(imageId, 'imagen')
        copiarArchivo(imagen, rutaImagen)
        
    logging.warning("sending")    
    #return sendfile(request, rutaImagen)
    try:
        with open(rutaImagen, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response

def getArchivo(request, archivoId, archivoName):

    db              = getConexion()
    doc             = db[archivoId]
    sub1            = archivoId[0:3]
    sub2            = archivoId[3:6]
    sub3            = archivoId[6:9]
    rev             = doc['_rev']
    carpetaArchivo  = settings.NISABU_CACHE_DIR+'/'+sub1+'/'+sub2+'/'+sub3+'/'+archivoId
    rutaArchivo      = carpetaArchivo+'/'+rev
    logging.warning("buscando en: "+rutaArchivo)
    if not os.path.exists(carpetaArchivo):
        os.makedirs(carpetaArchivo)
    if not os.path.exists(rutaArchivo):
        archivo  = db.get_attachment(archivoId, 'archivo')
        print archivo
        copiarArchivo(archivo, rutaArchivo)
        
    logging.warning("sending")    
    #return sendfile(request, rutaArchivon)
    try:
        with open(rutaArchivo, "rb") as f:
            return HttpResponse(f.read(), content_type="application/*")
    except IOError:
        red = Archivo.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response


    
def getThumbnail(request, imageId):
    db              = getConexion()
    doc             = db[imageId]
    sub1            = imageId[0:3]
    sub2            = imageId[3:6]
    sub3            = imageId[6:9]
    rev             = doc['_rev']
    carpetaImagen   = settings.NISABU_CACHE_DIR+'/'+sub1+'/'+sub2+'/'+sub3+'/'+imageId
    rutaImagen      = carpetaImagen+'/'+rev+'.png'
    rutaImagenThumb = carpetaImagen+'/'+rev+'_thumbnail.png'
 
    if not os.path.exists(carpetaImagen):
        os.makedirs(carpetaImagen)
    if not os.path.exists(rutaImagen):
        imagen  = db.get_attachment(imageId, 'imagen')
        copiarArchivo(imagen, rutaImagen)
    if not os.path.exists(rutaImagenThumb):
        im = Image.open(rutaImagen)
        im.thumbnail(thumbnail)
        im.save(rutaImagenThumb)
        #except IOError:
        #    os.remove(rutaImagenThumb)
        #copiarArchivo(imagen, rutaImagen)
    return sendfile(request, rutaImagenThumb)
 
 
def getMedianita(request, imageId):
    db              = getConexion()
    doc             = db[imageId]
    sub1            = imageId[0:3]
    sub2            = imageId[3:6]
    sub3            = imageId[6:9]
    rev             = doc['_rev']
    carpetaImagen   = settings.NISABU_CACHE_DIR+'/'+sub1+'/'+sub2+'/'+sub3+'/'+imageId
    rutaImagen      = carpetaImagen+'/'+rev+'.png'
    rutaImagenThumb = carpetaImagen+'/'+rev+'_thumbnail.png'
    if not os.path.exists(carpetaImagen):
        os.makedirs(carpetaImagen)
    if not os.path.exists(rutaImagen):
        imagen  = db.get_attachment(imageId, 'imagen')
        copiarArchivo(imagen, rutaImagen)
    if not os.path.exists(rutaImagenThumb):
        im = Image.open(rutaImagen)
        im.thumbnail(medianita)
        im.save(rutaImagenThumb)
        #except IOError:
        #    os.remove(rutaImagenThumb)
        #copiarArchivo(imagen, rutaImagen)
    return sendfile(request, rutaImagenThumb)
 
def getGrandecita(request, imageId):
    db              = getConexion()
    doc             = db[imageId]
    sub1            = imageId[0:3]
    sub2            = imageId[3:6]
    sub3            = imageId[6:9]
    rev             = doc['_rev']
    carpetaImagen   = settings.NISABU_CACHE_DIR+'/'+sub1+'/'+sub2+'/'+sub3+'/'+imageId
    rutaImagen      = carpetaImagen+'/'+rev+'.png'
    rutaImagenThumb = carpetaImagen+'/'+rev+'_thumbnail.png'
    if not os.path.exists(carpetaImagen):
        os.makedirs(carpetaImagen)
    if not os.path.exists(rutaImagen):
        imagen  = db.get_attachment(imageId, 'imagen')
        copiarArchivo(imagen, rutaImagen)
    if not os.path.exists(rutaImagenThumb):
        im = Image.open(rutaImagen)
        im.thumbnail(grandecita)
        im.save(rutaImagenThumb)
        #except IOError:
        #    os.remove(rutaImagenThumb)
        #copiarArchivo(imagen, rutaImagen)
    return sendfile(request, rutaImagenThumb)
 
def saveImage(request):
    dataRaw = {"success":True}
    data = json.dumps(dataRaw)
    return HttpResponse(data, content_type='application/json')
