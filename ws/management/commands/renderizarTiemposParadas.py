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

        listadoTenants = ["exxonmobil"]

        for nombreTenant in listadoTenants:
            print u"Verificando {}".format(nombreTenant)
                                        
            base   =  u'{}{}'.format(settings.BASEDB, nombreTenant)        
            db     = couch[base]

            filasPosicionesVehiculos = db.view(
                '_design/posicionVehiculos/_view/paradaVehiculo',
                include_docs  = True
            )

            contador        = 0
            for filaPosicionVehiculos in filasPosicionesVehiculos:
                
                docParada       = filaPosicionVehiculos.doc
                fechahoraInicio = docParada.get("fechahoraInicio")[:19]
                fechahoraFin    = docParada.get("fechahoraFin")[:19]
                
                fechahoraInicioDateTime = dateutil.parser.parse(fechahoraInicio)
                fechahoraFinDateTime    = dateutil.parser.parse(fechahoraFin)

                diferencia = (fechahoraFinDateTime-fechahoraInicioDateTime).total_seconds()
                
                contador += 1
                print "Segundo: {}s".format(diferencia)
                docParada["duracionParadaSegundos"] = diferencia
                print docParada
                db.save(docParada)
                print contador
                
