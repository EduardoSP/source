# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
import json
from django.conf                 import settings
import couchdb

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        couch     = couchdb.Server(url=settings.COUCHDB_URL)
        db        = couch['fleetbimauriciogiraldo']
        
        filas = db.view(
            '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
            include_docs  = True,
            startkey = ['a6a9368d6c64bb1cdbab24cd05bec5ed', '2017-07-01T09:00:00'],
            endkey   = ['a6a9368d6c64bb1cdbab24cd05bec5ed', '2017-08-01T12:17:00']
        )
        
        for fila in filas:
            doc = fila.doc
            if doc.get("latitud", 0 ) == 0:
                print doc["_id"]
                doc["activo"] = False
                db.save(doc)
            

