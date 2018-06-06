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

        #listadoTenants = ["exxonmobil"]
            
        for nombreTenant in listadoTenants:
            print u"Verificando {}".format(nombreTenant)
                                        
            base   =  u'{}{}'.format(settings.BASEDB, nombreTenant)        
            db     = couch[base]

            filasPosicionesVehiculos = db.view(
                '_design/estadisticas/_view/pendientesPorRenderizarEstadisticas',
                include_docs  = True
            )

            contador        = 0
            docAnterior     = None
            velocidadMaxima = 0
            for filaPosicionVehiculos in filasPosicionesVehiculos:
                #key   = filaPosicionVehiculos.key
                #value = filaPosicionVehiculos.value
                doc   = filaPosicionVehiculos.doc

                complementosEstadisticas = {}

                # Analizar distancia entre puntos-------------------------------
                if not docAnterior == None:
                    latInicial = float(docAnterior["latitud"])
                    lonInicial = float(docAnterior["longitud"])
                    latFinal   = float(doc["latitud"])
                    lonFinal   = float(doc["longitud"])
                                                            
                    puntoInicial    =   (latInicial, lonInicial)
                    puntoFinal      =   (latFinal,   lonFinal) 
                    distanciaMetros = vincenty(puntoInicial, puntoFinal).meters
                    complementosEstadisticas["metrosRecorridos"] = distanciaMetros
                else:
                    complementosEstadisticas["metrosRecorridos"] = 0.0
                #---------------------------------------------------------------

                
                #TODO hacer que el exceso de velocidad no sea constante.--------
                if doc.get("velocidad") > 80:
                    if not docAnterior == None:
                        complementosEstadisticasAnterior = docAnterior.get("complementosEstadisticas", {})
                        if not complementosEstadisticasAnterior.get("idPrimerPuntoExcesoVelocidad","") == "":
                            complementosEstadisticas["idPrimerPuntoExcesoVelocidad"] = complementosEstadisticasAnterior.get("idPrimerPuntoExcesoVelocidad","")
                        else:
                            complementosEstadisticas["idPrimerPuntoExcesoVelocidad"] = doc["_id"]
                    else:
                        complementosEstadisticas["idPrimerPuntoExcesoVelocidad"] = doc["_id"]
                else:
                    complementosEstadisticas["idPrimerPuntoExcesoVelocidad"] = ""
                #----------------------------------------------------------------------------

                #Diferencia en segundos------------------------------------------------------
                if not docAnterior == None:
                    horaRegistradaAnterior = dateutil.parser.parse(docAnterior["horaRegistrada"])
                    horaRegistrada         = dateutil.parser.parse(doc["horaRegistrada"])
                    diferenciaSegundos     = (horaRegistrada-horaRegistradaAnterior).total_seconds()
                    complementosEstadisticas["segundosAlPuntoAnterior"] = diferenciaSegundos
                else:
                    complementosEstadisticas["segundosAlPuntoAnterior"] = 0.0
                #----------------------------------------------------------------------------

                #Calcular el id del cambio en encendido.-------------------------------------
                if not docAnterior == None:
                    if docAnterior.get("estaEncendidoMotor", False) == doc.get("estaEncendidoMotor", False):
                        complementosEstadisticas["idPrimerPuntoCambioEncendido"] = docAnterior["_id"]
                    else:
                        complementosEstadisticas["idPrimerPuntoCambioEncendido"] = doc["_id"]
                else:
                    complementosEstadisticas["idPrimerPuntoCambioEncendido"] = doc["_id"]
                #-----------------------------------------------------------------------------
                
                #print u"Hay una distancia de: {}".format(complementosEstadisticas.get("metrosRecorridos",0))
                #print u"La velocidad fué de: {}".format(doc.get("velocidad"))
                #print u"La cantidad de segundos al punto anterior es: {}".format(complementosEstadisticas["segundosAlPuntoAnterior"])
                if doc.get("velocidad") > velocidadMaxima:
                    velocidadMaxima = doc.get("velocidad")

                #print complementosEstadisticas
                doc["complementosEstadisticas"] = complementosEstadisticas
                db.save(doc)
                
                docAnterior = doc
                contador += 1
                print contador
            #print u"Velocidad máxima: {}".format(str(velocidadMaxima))
                


         # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos

