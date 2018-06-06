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
          if doc.get('tipoRevision') == "pausaActiva":
            print key
            db.delete(doc)

        print "documentos de listarPausaActiva"
        filas = db.view('_design/seguridadVial/_view/listarPausaActiva',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print key
          db.delete(doc)

        print "documentos de listarSeguimientoPausaActiva"
        
        filas = db.view('_design/seguridadVial/_view/listarSeguimientoPausaActiva',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print key
          db.delete(doc)   



         # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos

        
