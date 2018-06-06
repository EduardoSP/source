# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
#from webbiodws.models            import *
import json
from django.conf                 import settings
from datetime                    import datetime
import urllib2
import logging
import couchdb
#from ws.serviciosweb.conexion import conexion

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        
        couch  = couchdb.Server(url=settings.COUCHDB_URL)
        base   =  u'{}{}'.format(settings.BASEDB, "exxonmobil")        
        db     = couch[base]

        filas = db.view('_design/posicionVehiculos/_view/posicionVehiculosUltimaPosicion',
                    include_docs  = True,
                    startkey      = [True, 0],
                    endkey        = [True, {}] )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print key
          print value
          print doc  

          print doc["placa"]
          print value["latitud"]
          print value["longitud"] 



         # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos

        
