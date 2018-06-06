# -*- coding: utf-8 -*-
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
import geocoder
import math
from geopy.distance import vincenty
import random

RANGO_PUNTOSREFERENCIAS_LATITUD  = 0.5
RANGO_PUNTOSREFERENCIAS_LONGITUD = 0.5 

RANGOS_PUNTOS_REFERENCIA = [
    {
        "tipo"          : "municipio",
        "rangoLatitud"  : 0.5,
        "rangoLongitud" : 0.5
    },
    {
        "tipo"          : "peaje",
        "rangoLatitud"  : 0.2,
        "rangoLongitud" : 0.2
    },
    {
        "tipo"          : "poste",
        "rangoLatitud"  : 0.03,
        "rangoLongitud" : 0.03
    }
]



def buscarPuntosReferencias(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']

    latitud          = datos["latitud"]
    longitud         = datos["longitud"]
    buscarDireccion  = datos["buscarDireccion"]

    db = conexion.getConexionGeocoder()

    docMunicipio = None
    docPeaje     = None
    docPoste     = None

    for rangoTipoPuntoReferencia in RANGOS_PUNTOS_REFERENCIA:

        tipoReferencia                   = rangoTipoPuntoReferencia["tipo"]
        RANGO_PUNTOSREFERENCIAS_LATITUD  = rangoTipoPuntoReferencia["rangoLatitud"]
        RANGO_PUNTOSREFERENCIAS_LONGITUD = rangoTipoPuntoReferencia["rangoLongitud"]
        
        minLatitud  = latitud  - RANGO_PUNTOSREFERENCIAS_LATITUD
        maxLatitud  = latitud  + RANGO_PUNTOSREFERENCIAS_LATITUD
        minLongitud = longitud - RANGO_PUNTOSREFERENCIAS_LONGITUD
        maxLongitud = longitud + RANGO_PUNTOSREFERENCIAS_LONGITUD

        filas = db.view(
            '_design/geocoder/_view/latitudportiporeferencia',
            startkey      = [tipoReferencia, minLatitud],
            endkey        = [tipoReferencia, maxLatitud],
            include_docs  = True
        )
        
        for fila in filas:
            docPuntoReferencia      = fila.doc
            latitudPuntoReferencia  = docPuntoReferencia["latitud"]
            longitudPuntoReferencia = docPuntoReferencia["longitud"]

            if longitudPuntoReferencia >= minLongitud and longitudPuntoReferencia <= maxLongitud:

                if docPuntoReferencia["tipoReferencia"] == "municipio":
                    if esMasCerca(docPuntoReferencia, docMunicipio, latitud, longitud):
                        docMunicipio = docPuntoReferencia
                elif docPuntoReferencia["tipoReferencia"] == "peaje":
                    if esMasCerca(docPuntoReferencia, docPeaje, latitud, longitud):
                        docPeaje = docPuntoReferencia
                elif docPuntoReferencia["tipoReferencia"] == "poste":
                    if esMasCerca(docPuntoReferencia, docPoste, latitud, longitud):
                        docPoste = docPuntoReferencia


    
    direccion = ""
    if buscarDireccion:
        direccion = getDireccion(latitud, longitud)
        
    dataRaw = {
        "direccion" : direccion
    }
    
    if not docMunicipio == None:
        dataRaw["municipio"] = {
            "latitud"      : docMunicipio["latitud"],
            "longitud"     : docMunicipio["longitud"],
            "nombre"       : docMunicipio["nombre"],
            "departamento" : docMunicipio["departamento"],
            "distancia"    : calcularDistancia(docMunicipio["latitud"], docMunicipio["longitud"], latitud, longitud),
            "direccion"    : calcularDireccion(docMunicipio["latitud"], docMunicipio["longitud"], latitud, longitud)
        }

    if not docPeaje == None:
        dataRaw["peaje"] = {
            "latitud"      : docPeaje["latitud"],
            "longitud"     : docPeaje["longitud"],
            "nombre"       : docPeaje["nombre"],
            "departamento" : docPeaje["departamento"],
            "sector"       : docPeaje["sector"],
            "distancia"    : calcularDistancia(docPeaje["latitud"], docPeaje["longitud"], latitud, longitud),
            "direccion"    : calcularDireccion(docPeaje["latitud"], docPeaje["longitud"], latitud, longitud)
        }

    if not docPoste == None:
        dataRaw["poste"] = {
            "latitud"      : docPoste["latitud"],
            "longitud"     : docPoste["longitud"],
            "nombre"       : docPoste["nombre"],
            "tramo"        : docPoste["tramo"],
            "sector"       : docPoste["sector"],
            "distancia"    : calcularDistancia(docPoste["latitud"], docPoste["longitud"], latitud, longitud),
            "direccion"    : calcularDireccion(docPoste["latitud"], docPoste["longitud"], latitud, longitud)
        }
    
                    
    return {
        'success' : True,
        'data'    : dataRaw
    }
    
def getDireccion(latitud, longitud):
    db    = conexion.getConexionGeocoder()

    latitudS  = "{0:.4f}".format(float(latitud))
    longitudS = "{0:.4f}".format(float(longitud))
    
    filas = db.view(
        '_design/geocoder/_view/direcciones',
        key           = [latitudS, longitudS],
        include_docs  = False,
        
    )

    direccion = ""
    for fila in filas:
        key       = fila.key
        direccion = fila.value

    if direccion == "":
       g = geocoder.google([latitud, longitud], method='reverse')
       direccion = g.address
       if not direccion == None and not direccion == "":
           guardarPosicionesGeocoder(db, latitud, longitud, direccion)
       else:
           direccion = ""

    return direccion


def getLatLngDireccionIp(direccionIp, tipoSesion):
    #direccionIp = "127.125.85.00"
    #direccionIp = "190.130.107.225" #bogota
    datos = {
        'latitud'           : 0,
        'longitud'          : 0,
        'direccionCompleta' : "Oficina",
        'ciudad'            : "Cali"            
    }
    if not(direccionIp == "localhost") and tipoSesion == "fleetBiWeb":
        db    = conexion.getConexionGeocoder()
        encontroDatos = False
        filas = db.view(
            '_design/geocoder/_view/UbicacionDireccionIpPorIp',
            key           = [direccionIp],
            include_docs  = True,
            limit = 1
        )
        direccion = ""
        for fila in filas:
            doc = fila.doc
            datos = {
                'latitud'           : doc.get("latitud", ""),
                'longitud'          : doc.get("longitud", ""),
                'direccionCompleta' : doc.get("direccionCompleta", ""),
                'ciudad'            : doc.get("ciudad", "")            
            }
            encontroDatos = True
        if not(encontroDatos):
            datos = guardarUbicacionDireccionIpPorIp(db, direccionIp)
    if not(tipoSesion == "fleetBiWeb"):
        #datos dese la app android o ios
        datos = {
            'latitud'           : 0,
            'longitud'          : 0,
            'direccionCompleta' : "Movil",
            'ciudad'            : "Movil"            
        }
    return datos

def guardarUbicacionDireccionIpPorIp(db, direccionIp):
    #Guarda la direccion ip con sus datos en la bd de geocoder
    if db == None:
        return {'success': False, 'mensaje': "No exixte el tenant"}
    try:
        g                   = geocoder.ip(direccionIp)
        latitud             = g.lat
        longitud            = g.lng
        g                   = geocoder.google([latitud, longitud], method='reverse')
        direccionCompleta   = g.address
        ciudad              = g.city
        doc_id, doc_rev = db.save({
            "tipoDato"          : "ubicacionDireccionIp",
            "creadoEn"          : datetime.now().isoformat(),
            "activo"            : True,
            "direccionIp"       : direccionIp,
            "latitud"           : latitud,
            "longitud"          : longitud,
            "direccionCompleta" : direccionCompleta,
            "ciudad"            : ciudad
        })
        datos = {
            'latitud'           : latitud,
            'longitud'          : longitud,
            'direccionCompleta' : direccionCompleta,
            'ciudad'            : ciudad            
        }
        return datos
    except ValueError as error:
        return {'success': False}


def guardarPosicionesGeocoder(db, latitud, longitud, direccion):
    print "----------------------------Guardo-------------------------"
    #funcion para guardar la geoposición en el documento posicionesGeocoder
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"      : "geocoder",
            "creadoEn"      : datetime.now().isoformat(),
	    "activo"        : True,	    
	    "latitud"       : latitud,
	    "longitud"      : longitud,
	    "direccion"     : direccion
            
        })
        print doc_id

    except ValueError:
        return { 'success' : False }

#Retorn true si docNUevo es mas cercano a docVehiejo a la latitud longitud
def esMasCerca(docNuevo, docViejo, latitud, longitud):
    if docViejo == None:
        return True

    distanciaNuevo = math.sqrt(
        ((docNuevo["latitud"] - latitud)**2) +
        ((docNuevo["longitud"] - longitud)**2)        
    )

    distanciaViejo = math.sqrt(
        ((docViejo["latitud"] - latitud)**2) +
        ((docViejo["longitud"] - longitud)**2)        
    )

    if distanciaNuevo < distanciaViejo:
        return True
    else:
        return False
    

def calcularDistancia(latitud1, longitud1, latitud2, longitud2):
    puntoInicial    = (
        float(latitud1),
        float(longitud1)
    )

    puntoFinal      = (
        float(latitud2),
        float(longitud2)
    )

    distanciaMetros = vincenty(puntoInicial, puntoFinal).meters

    return distanciaMetros

def calcularDireccion(latitud2, longitud2, latitud1, longitud1):
    #print latitud1, longitud1, latitud2, longitud2
    longitud1 *= 1.25
    longitud2 *= 1.25
    radianes = math.atan2(latitud2-latitud1, longitud2-longitud1)
    grados   = math.degrees(radianes)

    #print grados
    respuesta = "Norte"
    
    if grados >= 0:
        if grados <= 22.5:
            respuesta = "Oriente"
        elif grados <= 67.5:
            respuesta = "Nororiente"
        elif grados <= 112.5:
            respuesta = "Norte"
        elif grados <= 157.5:
            respuesta = "Noroccidente"
        elif grados <= 180:
            respuesta = "Occidente"
    else:
        if grados <= -22.5:
            respuesta = "Oriente"
        elif grados <= -67.5:
            respuesta = "Suroriente"
        elif grados <= -112.5:
            respuesta = "Sur"
        elif grados <= -157.5:
            respuesta = "Suroccidente"
        elif grados <= -180:
            respuesta = "Occidente"

    #print respuesta
    return respuesta
