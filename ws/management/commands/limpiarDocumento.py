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
        limpiarDocumento("_design/seguridadVial/_view/listarConduccionContinua", "exxonmobil")
        limpiarDocumento("_design/seguridadVial/_view/listarSeguimientoConduccionContinua", "exxonmobil")
        #limpiarDocumento("_design/seguridadVial/_view/listarPausaActiva", "exxonmobil")
        #limpiarDocumento("_design/seguridadVial/_view/listarSeguimientoPausaActiva", "exxonmobil")


def limpiarDocumento(nombreVista, tenant):
        couch  = couchdb.Server(url=settings.COUCHDB_URL)
        base   =  u'{}{}'.format(settings.BASEDB, tenant)        
        db     = couch[base]

        filas = db.view(nombreVista,
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print key
          db.delete(doc)



         # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos