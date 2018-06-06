# -*- encoding: utf-8 -*-
import couchdb
from django.conf    import settings
import logging

#Ejemplo: huv
def getConexionTenant(codigoBase):
    couch  = couchdb.Server(url=settings.COUCHDB_URL)

    base = ""
    if codigoBase == settings.TENANT_ADMINISTRACION:    
        base   =  settings.BASEDB
    else:
        base   =  u'{}{}'.format(settings.BASEDB, codigoBase)
        
    try:
        print "Buscando {}".format(base)
        db     = couch[base]
    except:
        return None
    return db

def getConexionFleet():
    couch  = couchdb.Server(url=settings.COUCHDB_URL)
    base   = settings.BASEDB
    try:
        db     = couch[base]
    except:
        return None
    return db

def getConexionGeocoder():
    couch  = couchdb.Server(url=settings.COUCHDB_URL)
    base   = settings.GEOCODERDB
    try:
        db = couch[base]
    except:
        return None
    return db


#Retorna el couch plano
def getCouch():
    couch  = couchdb.Server(url=settings.COUCHDB_URL)
    return couch
