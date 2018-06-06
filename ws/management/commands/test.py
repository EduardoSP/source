# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
import json
from django.conf                 import settings
import couchdb

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        couch     = couchdb.Server(url=settings.COUCHDB_URL)
        db        = couch['fleetbibtranscolombia']
        
        #---------------------------------------------------


        total = 2000

        while total == 2000:

            total = 0
        
            filas = db.view(
                '_design/estadisticas/_view/kilometrosRecorridosPorVehiculoPorFechaHora',
                include_docs = True,            
                reduce       = False,
                startkey     = [0, 0],
                endkey       = [{}, {}],
                limit        = 2000
            )

        
            for fila in filas:
                distanciaMetros  = fila.value
                key              = fila.key
                startkey         = key
                print distanciaMetros
                total           += 1
                
