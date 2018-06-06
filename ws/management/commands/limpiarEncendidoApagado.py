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
        base   =  u'{}{}'.format(settings.BASEDB, "transcolombia")        
        db     = couch[base]
        print "documentos de listarFechasRevision"
        filas = db.view('_design/seguridadVial/_view/listarFechasRevision',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          if doc.get('tipoRevision') == "encendidoApagado":
            print key
            db.delete(doc)

        print "documentos de listarEncendidoApagadoPorVehiculo"
        filas = db.view('_design/seguridadVial/_view/listarEncendidoApagadoPorVehiculo',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print key
          db.delete(doc)


         # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos

        
