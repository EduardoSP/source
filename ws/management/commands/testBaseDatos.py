# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
import json
from django.conf                 import settings
import couchdb

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        couch  = couchdb.Server(url=settings.COUCHDB_URL)
        dbModelo = couch['fleetbiexxonmobil']
        nuevaBase = 'fleetbimodelo'        
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

