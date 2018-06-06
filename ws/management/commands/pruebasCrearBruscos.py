# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
#from webbiodws.models            import *
import json
from django.conf                 import settings
from datetime                    import datetime,timedelta
import urllib2
import logging
import couchdb
import requests
import json
from dateutil import parser
import time
from collections import deque
import math
import random
from random import randint
import geocoder

#from ws.serviciosweb.conexion import conexion

#Variables de configuracion:

acelMinHour = 8
acelMaxHour = 20
acelMinRange = 48
acelMaxRange = 120

fechaInicio = "2017-08-15T01:00"
fechaFin    = "2017-08-30T01:00"

horasSinPausaActiva = 3
horasSinDescanso    = 6

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        
        couch      = couchdb.Server(url=settings.COUCHDB_URL)
        base       = settings.BASEDB
        db         = couch[base]
        dbsTenants = [] #Guarda una reerencia a todas las conexiones de los tenants

        filas = db.view(
            '_design/tenantPorTenant/_view/tenantPorTenant',
            include_docs  = True
        )

        print u"Base : {} ".format(settings.BASEDB)
        for fila in filas:
            docTenant = fila.doc
            dbTenant  = couch[u"{}{}".format(settings.BASEDB, docTenant.get("urlTenant",""))]
            
            
            print u"Tenant {}".format(docTenant.get("urlTenant", ""))
            #generarAceleraciones(dbTenant)
            generarEncendidosApagados(dbTenant)
            
            
            
def generarAceleraciones(db):

    filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
    for fila in filas:
        key   = fila.key
        value = fila.value
        doc   = fila.doc

        
    
        fechaActual = parser.parse(fechaInicio).isoformat()
        while fechaActual < fechaFin:
            horasDiferencia = randint(acelMinRange, acelMaxRange)
            minutos         = randint(0, 59)
            segundos        = randint(0, 59)
            nuevaFecha = parser.parse(fechaActual) + timedelta(hours=horasDiferencia, minutes=minutos, seconds=segundos)
            print nuevaFecha
            hora = nuevaFecha.hour
            if hora > acelMinHour and hora < acelMaxHour:
                print "HACER {}".format(nuevaFecha.isoformat())
                idVehiculo = doc["_id"]
                
                
                direccion = buscarPosicion(db, idVehiculo, nuevaFecha.isoformat())
                print u"Direccion: --{}--".format(direccion)

                if not direccion == "":
                    print "GOOD"
                    nuevoDoc = {
 
                        "tipoDato"        : random.choice(["aceleracion","frenadas","movimientoAbrupto","excesoVelocidad"]),
                        "creadoEn"        : "", ##creado por el sistema
                        "horaRegistrada"  : nuevaFecha.isoformat(),
                        "ubicacion"       : direccion,
                        "idConductor"     : doc.get("conductor",""),
                        "idVehiculo"      : doc["_id"],  
                        "activo"          : True
                        
                    }
                    db.save(nuevoDoc)
            fechaActual = nuevaFecha.isoformat()



            
def buscarPosicion(db, idVehiculo, fecha):
    print "buscarPosicion"
    filas = db.view(
        '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
        include_docs = True ,
        #descending  = True,
        startkey     = [idVehiculo, fecha],
        endkey       = [idVehiculo, {}],
        limit        = 1
    )

    direccion = ""
    for fila in filas:
        doc = fila.doc
        latitud  = doc.get("latitud")
        longitud = doc.get("longitud")
        direccion = obtenerDireccionGeocoder(db, latitud, longitud)

    return direccion



def obtenerDireccionGeocoder(db, latitud, longitud):
    latitud  = str(latitud)
    longitud = str(longitud)
    lat1 = latitud.split(".")[0]
    lat2 = latitud.split(".")[1]
    lng1 = longitud.split(".")[0]
    lng2 = longitud.split(".")[1]
    nuevaLatitud    = lat1+"."+lat2[0:3]
    nuevaLongitud   = lng1+"."+lng2[0:3]

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        nombreGeoposicion = ""
        filas = db.view('_design/geoposiciones/_view/geoposicionesPrecalculadas',
                    key         = [nuevaLatitud, nuevaLongitud],
                    include_docs  = True,
                    limit         = 1
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          nombreGeoposicion = doc.get("nombreGeoposicion", "")
          direccion         = nombreGeoposicion

        if nombreGeoposicion == "":
            time.sleep(5)
            g         = geocoder.google([nuevaLatitud, nuevaLongitud], method='reverse')
            direccion = g.address
            if not direccion == None:
                guardarPosicionesGeocoder(db, nuevaLatitud, nuevaLongitud, direccion)
            else:
                return ""
        return direccion


def guardarPosicionesGeocoder(db, latitud, longitud, direccion):
    print "----------------------------Guardo-------------------------"
    #funcion para guardar la geoposición en el documento posicionesGeocoder
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"          : "posicionesGeocoder",
            "latitud"           : latitud,
            "longitud"          : longitud,
            "nombreGeoposicion" : direccion,
            "activo"            : True
        })
        print doc_id

    except ValueError:
        return { 'success' : False }

def generarEncendidosApagados(db):

    filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
    for fila in filas:
        key   = fila.key
        value = fila.value
        doc   = fila.doc

        idVehiculo  = doc.get("_id")
        idConductor = doc.get("conductor")
        estaEncendido = False
        contador      = 0 
        
        filasPosiciones = db.view(
            '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
            include_docs = True ,
            #descending  = True,
            startkey     = [idVehiculo, fechaInicio],
            endkey       = [idVehiculo, fechaFin]
        )


        puntosDeteccion = 20
        valorAnterior = ""
        for filaPosicion in filasPosiciones:
            docPosicion = filaPosicion.doc

            if docPosicion.get("velocidad",0) == 0:
                if estaEncendido:
                    if contador > puntosDeteccion:
                        estaEncendido = False
                        #print u"Apagado en : {}".format(docPosicion.get("horaRegistrada", ""))
                        if not valorAnterior == "":
                            #print u"Encendido entre: {} y {}".format(valorAnterior, docPosicion.get("horaRegistrada", ""))
                            nuevoDoc = {
                                "tipoDato"        : "encendidoApagado",
                                "creadoEn"        : "",
                                "evento"          : "Encendido", 
                                "horaInicio"      : valorAnterior,
                                "horaFin"         : docPosicion.get("horaRegistrada", ""),
                                "idVehiculo"      : idVehiculo,  
                                "activo"          : True
                            }
                            db.save(nuevoDoc)

                            segundos = (parser.parse(docPosicion.get("horaRegistrada", "")) - parser.parse(valorAnterior)).total_seconds()

                            if segundos > horasSinDescanso*60*60:
                                #print u"No tuvo descanso continuo entre: {} y {}".format(valorAnterior, docPosicion.get("horaRegistrada", ""))
                                nuevoDoc = {                                    
                                    "tipoDato"        : "conduccionContinua",
                                    "creadoEn"        : "",
                                    "fechaInfraccion" : docPosicion.get("horaRegistrada", ""),
                                    "conduceDesde"    : valorAnterior,
                                    "idVehiculo"      : idVehiculo,
                                    "idConductor"     : idConductor, 
                                    "activo"          : True
                                }
                                db.save(nuevoDoc)
                            elif segundos > horasSinPausaActiva*60*60:
                                #print u"No tuvo pausa activa entre: {} y {}".format(valorAnterior, docPosicion.get("horaRegistrada", ""))
                                nuevoDoc =  {
                                    
                                    "tipoDato"        : "pausaActiva",
                                    "creadoEn"        : "",
                                    "fechaInfraccion" : docPosicion.get("horaRegistrada", ""),
                                    "conduceDesde"    : valorAnterior,
                                    "idVehiculo"      : idVehiculo,
                                    "idConductor"     : idConductor, 
                                    "activo"          : True
                                }
                                db.save(nuevoDoc)

                                
                                

                                
                        valorAnterior = docPosicion.get("horaRegistrada", "")
                    else:
                        contador +=1

                else:
                    contador = 0
            else:
                if not estaEncendido:
                    if contador > puntosDeteccion:
                        estaEncendido = True
                        #print u"Encendido en : {}".format(docPosicion.get("horaRegistrada", ""))
                        if not valorAnterior == "":
                            #print u"Apagado entre: {} y {}".format(valorAnterior, docPosicion.get("horaRegistrada", ""))

                            
                            
                            nuevoDoc = {
                                "tipoDato"        : "encendidoApagado",
                                "creadoEn"        : "",
                                "evento"          : "Apagado", 
                                "horaInicio"      : valorAnterior,
                                "horaFin"         : docPosicion.get("horaRegistrada", ""),
                                "idVehiculo"      : idVehiculo,  
                                "activo"          : True
                            }
                            db.save(nuevoDoc)
                        valorAnterior = docPosicion.get("horaRegistrada", "")
                    else:
                        contador +=1

                else:
                    contador = 0
            

