# -*- encoding: utf-8 -*-
import couchdb
from django.shortcuts   import render
from sendfile           import sendfile
from django.conf        import settings
import os, sys
from PIL import Image
import  logging


thumbnail   = 128, 128
medianita   = 300, 300
grandecita  = 600, 600

def getConexion():
    couch = couchdb.Server()
    #return couch['nisabu']
    return couch['nisabu']

#Copia un archivo tipo file a la rut de destino
def copiarArchivo(archivo, rutaDestino):
    destino = open(rutaDestino, 'wb+')
    destino.write(archivo.read())
    destino.close()

def getImage(request, imageId):
    db              = getConexion()
    doc             = db[imageId]
    sub1            = imageId[0:3]
    sub2            = imageId[3:6]
    sub3            = imageId[6:9]
    rev             = doc['_rev']
    carpetaImagen   = settings.NISABU_CACHE_DIR+'/'+sub1+'/'+sub2+'/'+sub3+'/'+imageId
    rutaImagen      = carpetaImagen+'/'+rev+'.png'
    if not os.path.exists(carpetaImagen):
        os.makedirs(carpetaImagen)
    if not os.path.exists(rutaImagen):
        imagen  = db.get_attachment(imageId, 'imagen')
        copiarArchivo(imagen, rutaImagen)
        
    logging.warning(rutaImagen)
    return sendfile(request, rutaImagen)

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
    rutaImagenThumb = carpetaImagen+'/'+rev+'_medianita.png'
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
    rutaImagenThumb = carpetaImagen+'/'+rev+'_grandecita.png'
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
