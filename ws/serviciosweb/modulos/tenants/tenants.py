# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
import time
from twilio.rest import TwilioRestClient

#-------------------------------------------------------------

def pickerTenants( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/tenant/_view/visualizarTenants',
            include_docs  = True
        )
        
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          
          dataRaw.append(
              {
          	  'id'         : doc.get('urlTenant',       ''),
          	  'nombre'     : doc.get('nombreGeneral', '')
              }
          )            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#Solo recibe el nombre de la base, por ejemplo el 'terpel' para 'fleetbiterpel'
def crearNuevaBaseDatos(codigobase):
    couch      = couchdb.Server(url=settings.COUCHDB_URL)
    modeloBase = u'{}{}'.format(settings.BASEDB,settings.TENANT_MODELO)
    nuevaBase  = u'{}{}'.format(settings.BASEDB,codigobase)        


    dbModelo = couch[modeloBase]
    
    if not existeDB(nuevaBase, couch):
        couch.create(nuevaBase)
        
    dbDestino = couch[nuevaBase]
            

    filas = dbModelo.view(
        '_all_docs',
        include_docs  = True,
        startkey = '_design/',
        endkey   = '_design0'
    )
    
    for fila in filas:
        doc = fila.doc
        print doc
        del doc['_rev']
        dbDestino.save(doc)
            

def existeDB(nombreBase, couch):
    resultado = True
        
    try:
        db = couch[nombreBase]
    except:
        resultado = False
        
    return resultado


    
