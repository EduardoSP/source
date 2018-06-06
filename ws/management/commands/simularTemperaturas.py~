# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
#from webbiodws.models            import *
import json
from django.conf                 import settings
from datetime                    import datetime, timedelta
import urllib2
import logging
import couchdb
from geopy.distance              import vincenty
import dateutil.parser
import numbers
from dateutil import parser
import random
#from ws.serviciosweb.conexion import conexion

vehiculosSimular = ["a6a9368d6c64bb1cdbab24cd05bec5ed"]

fechaInicioSimulacion = "2017-12-01T00:00:01" #Deberia ser el ultimo

limSuperior  = 7
limInferior  = 3
tempObjetivo = 5
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

        listadoTenants = ["transcolombia"]
            
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
                idVehiculo  = docVehiculo["_id"]
                if not idVehiculo in vehiculosSimular:
                    continue

                #borrarPuntosSimulados(db,idVehiculo)
                #continue
                
                ultimaGeoposicion   = getUltimaGeoposicion(db,idVehiculo)
                print ultimaGeoposicion.get("horaRegistrada")
                ultimoPuntoSimulado = getUltimoPuntoSimulado(db, idVehiculo)
                siguienteFecha      = (parser.parse (ultimoPuntoSimulado.get("horaRegistrada","")) + timedelta(seconds=random.randint(55,90))).isoformat()

                puntosGuardar = []
                while ultimaGeoposicion.get("horaRegistrada","") > siguienteFecha:

                    estaEnZonaFria = calcularZonaFria(db,idVehiculo,siguienteFecha)

                    nuevoPuntoSimulado = {
                        
                    }
                    
                    if estaEnZonaFria:
                        nuevoPuntoSimulado = generarSimuladoEnFrio(db,ultimoPuntoSimulado,siguienteFecha)
                    else:
                        nuevoPuntoSimulado = generarSimuladoEnAmbiente(db,ultimoPuntoSimulado,siguienteFecha)

                    #db.save( nuevoPuntoSimulado)
                    print nuevoPuntoSimulado
                    puntosGuardar.append(nuevoPuntoSimulado)
                    if len(puntosGuardar) > 2000:
                        db.update(puntosGuardar)
                        puntosGuardar = []
                    ultimoPuntoSimulado = nuevoPuntoSimulado
                    siguienteFecha      = ( parser.parse(siguienteFecha) + timedelta(seconds=random.randint(55,90))).isoformat()
                db.update(puntosGuardar)
                puntosGuardar = []
def getUltimaGeoposicion(db,idVehiculo):

    docPosicion = {}
    filasPosicion = db.view(
        '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
        include_docs  = True,
        limit         = 1,
        descending    = True,
        startkey      = [idVehiculo, {}],
        endkey        = [idVehiculo, 0]
    )
    
    for filaPosicion in filasPosicion:
        docPosicion = filaPosicion.doc
        
    return docPosicion

def getUltimoPuntoSimulado(db,idVehiculo):

    docPosicion = None
    filasPosicion = db.view(
        '_design/cadenaFrio/_view/puntoCadenaFrio',
        include_docs  = True,
        limit         = 1,
        descending    = True,
        startkey      = [idVehiculo, {}],
        endkey        = [idVehiculo, 0],
        reduce        = False
    )
    
    for filaPosicion in filasPosicion:
        docPosicion = filaPosicion.doc
        
    if docPosicion == None:
        docPosicion = {
            "tipoDato"       : "puntoCadenaFrio",
            "idVehiculo"     : idVehiculo,
            "horaRegistrada" : fechaInicioSimulacion,
            "horaRecibida"   : fechaInicioSimulacion,
            "temperatura"    : 20,
            "activo"         : True
        }
        
    return docPosicion

def generarSimuladoEnFrio(db,ultimoPuntoSimulado,siguienteFecha):

    temperatura = 0
    
    if ultimoPuntoSimulado["temperatura"] > limSuperior:
        temperatura = ultimoPuntoSimulado["temperatura"] - random.randint(1,2)
    elif ultimoPuntoSimulado["temperatura"] < limInferior:
        temperatura = ultimoPuntoSimulado["temperatura"] + random.randint(1,2)
    else:
        if ultimoPuntoSimulado["temperatura"] == tempObjetivo:
            if random.random()>0.95:
                temperatura = ultimoPuntoSimulado["temperatura"] + random.randint(-1,1)
            else:
                
                temperatura = ultimoPuntoSimulado["temperatura"]
        else:
            if ultimoPuntoSimulado["temperatura"] > tempObjetivo:
                temperatura = ultimoPuntoSimulado["temperatura"] - random.randint(0,1)
            else:
                temperatura = ultimoPuntoSimulado["temperatura"] + random.randint(0,1)
                
            
    docPosicion = {
        "tipoDato"       : "puntoCadenaFrio",
        "idVehiculo"     : ultimoPuntoSimulado["idVehiculo"],
        "horaRegistrada" : siguienteFecha,
        "horaRecibida"   : siguienteFecha,
        "temperatura"    : temperatura,
        "activo"         : True,
        "generado"       : "frio"
    }
        
                                           
    
    return docPosicion

def generarSimuladoEnAmbiente(db,ultimoPuntoSimulado,siguienteFecha):
    temperaturaAmbiente = calcularTemperaturaAmbiente(siguienteFecha)
    
    temperatura = 0
    
    if ultimoPuntoSimulado["temperatura"] > temperaturaAmbiente:
        temperatura = ultimoPuntoSimulado["temperatura"] - random.randint(0,2)
    elif ultimoPuntoSimulado["temperatura"] < temperaturaAmbiente:
        temperatura = ultimoPuntoSimulado["temperatura"] + random.randint(0,2)
    else:
        if ultimoPuntoSimulado["temperatura"] == temperaturaAmbiente:
            if random.random()>0.95:
                temperatura = ultimoPuntoSimulado["temperatura"] + random.randint(-1,1)
            else:                
                temperatura = ultimoPuntoSimulado["temperatura"]
        else:
            if ultimoPuntoSimulado["temperatura"] > temperaturaAmbiente:
                temperatura = ultimoPuntoSimulado["temperatura"] - random.randint(0,1)
            else:
                temperatura = ultimoPuntoSimulado["temperatura"] + random.randint(0,1)
    
    docPosicion = {
        "tipoDato"       : "puntoCadenaFrio",
        "idVehiculo"     : ultimoPuntoSimulado["idVehiculo"],
        "horaRegistrada" : siguienteFecha,
        "horaRecibida"   : siguienteFecha,
        "temperatura"    : temperatura,
        "activo"         : True,
        "generado"       : "ambiente"
    }
        
                                           
    
    return docPosicion


temperaturasAmbientes = [
    21,#0
    21,#1
    20,#2
    20,#3
    20,#4
    19,#5
    20,#6
    21,#7
    21,#8
    22,#9
    25,#10
    27,#11
    29,#12
    30,#13
    31,#14
    31,#15
    30,#16
    29,#17
    28,#18
    26,#19
    24,#20
    22,#22
    21,#23
    21,#24
]

def calcularTemperaturaAmbiente(siguienteFecha):
    hora = parser.parse(siguienteFecha).hour
    temperatura = temperaturasAmbientes[hora] + random.randint(-2,2) 
    return temperatura

def calcularZonaFria(db,idVehiculo,siguienteFecha):

    esZonaFria = False
    
    fechaAnterior = (parser.parse (siguienteFecha) - timedelta(minutes=15)).isoformat()

    filasPosicionesVehiculos = db.view(
        '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
        include_docs  = True,
        startkey      = [idVehiculo,fechaAnterior],
        endkey        = [idVehiculo,siguienteFecha],
        limit         = 1000
    )

    velocidad     = 0
    velocidadSum  = 0
    cantidadTotal = 0
    for filaPosicionVehiculos in filasPosicionesVehiculos:
        #key   = filaPosicionVehiculos.key
        #value = filaPosicionVehiculos.value
        doc            = filaPosicionVehiculos.doc
        velocidadSum  += doc.get("velocidad",0)
        cantidadTotal += 1

    if cantidadTotal > 0:
        velocidad = velocidadSum/cantidadTotal

    if velocidad > 5:
        esZonaFria = True
    else:
        esZonaFria = False

    return esZonaFria
        
def borrarPuntosSimulados(db,idVehiculo):
    filasPosicion = db.view(
        '_design/cadenaFrio/_view/puntoCadenaFrio',
        include_docs  = True,
        #limit         = 1,
        descending    = True,
        startkey      = [idVehiculo, {}],
        endkey        = [idVehiculo, 0],
        reduce        = False
    )
        
    for filaPosicion in filasPosicion:
        docPosicion = filaPosicion.doc
        print docPosicion
        db.delete(docPosicion)
        
