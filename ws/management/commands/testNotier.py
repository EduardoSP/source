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
from  ws.serviciosweb.modulos.notificaciones.notificaciones import notificarTenant
#from ws.serviciosweb.conexion import conexion

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        
        notificarTenant("exxonmobil", "alarma", "hola mundo")



         # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos

        
