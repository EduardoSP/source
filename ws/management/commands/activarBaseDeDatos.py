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
from geopy.distance              import vincenty
import dateutil.parser
import numbers
#from ws.serviciosweb.conexion import conexion

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        
        couch    = couchdb.Server(url=settings.COUCHDB_URL)

        dbTenant = couch[settings.BASEDB]

        filasTenants = dbTenant.view(
            '_design/tenantPorTenant/_view/tenantPorTenant',
            include_docs  = False
        )

        listadoTenants = []
        
        for filaTenant in filasTenants:
            llave = filaTenant.key
            listadoTenants.append(llave[0])

        #listadoTenants = ["exxonmobil"]
        for nombreTenant in listadoTenants:
            #print u"Verificando {}".format(nombreTenant)
                                        
            base   =  u'{}{}'.format(settings.BASEDB, nombreTenant)        
            db     = couch[base]
            print u"Verificando {}".format(base)
            #Datos origen ------------------------------------
            filas = db.view(
                '_all_docs',
                startkey      = '_design/',
                endkey        = '_design0',
                include_docs  = True,
                
            )

            for fila in filas:
                key      = fila.key
                value    = fila.value
                doc      = fila.doc
                #print json.dumps( doc.get("views").keys() )
                for vista in doc.get("views").keys():
                    vistaUrl = u"{}/_view/{}".format(doc.get("_id"), vista)

                    #if vistaUrl.startswith("_design/estadisticas"):                        
                        #continue
                    print vistaUrl
                    #Datos origen ------------------------------------
                    filasVista = db.view(
                        vistaUrl,
                        #include_docs  = True,
                        limit = 1
                    )
                    for filaVista in filasVista:
                        print filaVista
            #--------------------------------------------------
