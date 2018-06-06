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
            print u"Verificando {}".format(nombreTenant)
                                        
            base   =  u'{}{}'.format(settings.BASEDB, nombreTenant)        
            db     = couch[base]

            filasVehiculos = db.view(
                '_design/vehiculos/_view/vehiculos',
                include_docs  = True
            )

            for filaVehiculo in filasVehiculos:
                docVehiculo = filaVehiculo.doc                        
            
                contadorIteracion = 2000
                #startkey          = [docVehiculo["_id"], 0]
                #endkey            = [docVehiculo["_id"], {}]
                startkey          = [docVehiculo["_id"], "2017-08-01"]
                endkey            = [docVehiculo["_id"], "2017-09-01"]
                while contadorIteracion == 2000:

                    contadorIteracion = 0

                    # filasPosicionesVehiculos = db.view(
                    #     '_design/estadisticas/_view/pendientesPorRenderizarEstadisticasReversa',
                    #     include_docs  = True,
                    #     descending    = True,
                    #     startkey      = startkey,
                    #     limit         = 1000
                    # )
                    
                    filasPosicionesVehiculos = db.view(
                        '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
                        include_docs  = True,
                        startkey      = startkey,
                        endkey        = endkey,
                        limit         = 2000
                    )

                    contador        = 0
                    docAnterior     = None
                    velocidadMaxima = 0

                    docsUpdated     = [] 
                    
                    for filaPosicionVehiculos in filasPosicionesVehiculos:
                        #key   = filaPosicionVehiculos.key
                        #value = filaPosicionVehiculos.value
                        doc      = filaPosicionVehiculos.doc
                        startkey = filaPosicionVehiculos.key
                        startkey[1] += "Z"
                        #print startkey
                        contadorIteracion        += 1
                        complementosEstadisticas = {}

                        skipDocAnterior = False #Indica si este punto no me sirve como punto anterior debido al problema del gps.
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
                            
                            datetimeInicio  = dateutil.parser.parse(docAnterior.get("horaRegistrada", ""))
                            datetimeFin     = dateutil.parser.parse(doc.get("horaRegistrada", ""))
                            distanciaTiempo = (datetimeFin - datetimeInicio).total_seconds()

                            velocidadAprox  = 0
            
                            if distanciaTiempo > 0 :
                                velocidadAprox = (distanciaMetros/1000.0) / ( distanciaTiempo/(60.0*60.0) )
                                if velocidadAprox < 300: #Menor a 300                                                                
                                    complementosEstadisticas["metrosRecorridos"] = distanciaMetros
                                else:
                                    skipDocAnterior = True
                                    complementosEstadisticas["metrosRecorridos"] = 0.0
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
                        if not isinstance(complementosEstadisticas["metrosRecorridos"], numbers.Number):
                            print "ERROR {}".format(complementosEstadisticas["metrosRecorridos"])
                            complementosEstadisticas["metrosRecorridos"] = 0.0
                        
                        doc["complementosEstadisticas"] = complementosEstadisticas


                        #Verificar la direccion -------------------------------------------------------
                        nombreGeoposicion = doc.get("nombreGeoposicion","")
                        if nombreGeoposicion == "":
                            pass
                            #TODO fabio verificar si es necesario la geoposición en estadisticas.
                            #nombreGeoposicion        = geocoderFleet.getDireccion(doc.get("latitud"), doc.get("longitud"))
                            #print nombreGeoposicion
                            #doc["nombreGeoposicion"] = nombreGeoposicion
                        #db.save(doc)
                        docsUpdated.append(doc)

                        if not skipDocAnterior:
                             docAnterior = doc
                        #docAnterior = doc
                        contador   += 1
                        #print contador
                    #print u"Velocidad máxima: {}".format(str(velocidadMaxima))
                    db.update(docsUpdated)


                 # python /home/ubuntu/asdasdasd/manage.py pruebaUltimos
