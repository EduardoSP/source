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
import geocoder

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

        creadosNuevos = 0
        for nombreTenant in listadoTenants:
            print u"Verificando {}".format(nombreTenant)
                                        
            base   =  u'{}{}'.format(settings.BASEDB, nombreTenant)        
            db     = couch[base]

            filasPosicionesVehiculos = db.view(
                '_design/geoposiciones/_view/geoposicionesPendientes',
                #startkey      = ["paradaVehiculo"],
                #endkey        = ["paradaVehiculo"],
                include_docs  = True,
                
            )

            
            for filaPosicionVehiculos in filasPosicionesVehiculos:
                docParada = filaPosicionVehiculos.doc
                print docParada
                print "{} - {}".format(docParada["latitud"], docParada["longitud"])

                filasGeoPosicionesPrecalculadas = db.view(
                    '_design/geoposiciones/_view/geoposicionesPrecalculadas',
                    key         = [docParada["latitud"], docParada["longitud"]],
                    include_docs  = True,
                    limit         = 1
                )

                nombreGeoposicion = ""
                for fila in filasGeoPosicionesPrecalculadas:
                    nombreGeoposicion = fila.doc.get("nombreGeoposicion", "")


                if nombreGeoposicion == "":
                    creadosNuevos += 1
                    g = geocoder.google([docParada["latitud"], docParada["longitud"]], method='reverse')
                    print g.address
                    nombreGeoposicion = g.address

                docParada["nombreGeoposicion"] = nombreGeoposicion
                db.save(docParada)
                print docParada
                print "Creados: {}".format(creadosNuevos)
