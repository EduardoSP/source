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
from ws.serviciosweb.modulos.conexion      import conexion
from datetime                              import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
from geopy.distance              import vincenty


urlWSRepetidora            = "http://13.58.121.171:8080/ws/enviarTrazaPegaso"


fechaInicioDefecto         = "2017-09-18T20:24:00"
limiteDePuntosPorVehiculo  = 10 #Cuantos puntos máximos por vehiculos se enviaran
defaultSatelites           = 3
defaultHdop                = 9
defaultTipoPosicion        = 2

CODIGOEVENTOSEGUIMIENTO    = 4 

cedulasPorVehiculo = {
    "a6a9368d6c64bb1cdbab24cd05bec5ed" : "1111111111",
    "376ab4cad78e3a90cc318dd08196c34d" : "2222222222"
}

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        
        # fechaInicio = "2017-08-16T16:40:42" #fecha inicio de la consulta de
        #                                     #puntos                                            
        # fechaFin    = "2017-08-16T16:44:30" # fecha fin de la consulta de
                                            # puntos                                            
        docsTenants = consultarTenants()
        
        for docTenant in docsTenants:
            print "==================================="
            tenant = docTenant.get("urlTenant","")            
            print tenant
            if tenant == "":
                continue

            db = conexion.getConexionTenant(tenant)
            if db == None:
                return { 'success' : False, 'mensaje': "NO existe el bd" }

            tramas = []
            #por cada tenant se sonsultara la informacion
            docsVehiculos = consultarVehiculos(db)

            for docVehiculo in docsVehiculos:
                #Sale si NO debe exportar a pegaso
                if not docVehiculo.get("debeExportarPegaso", True):
                    print u"{} saltado!!!!!!!".format(docVehiculo.get("placa", ""))
                    continue

                idVehiculo                          = docVehiculo["_id"]                
                docSeguimientoPegaso                = consultarSeguimientoPegaso(db, idVehiculo)
                estaActualizadoDocSeguimientoPegaso = False
                fechaInicio                         = docSeguimientoPegaso.get("fechaHoraUltimaRevision","")
                fechaFin                            = {} #No hay necesita de limitar por fecha, pero sería interesante.

                #COrrijo si lafechaIncio es anterior a la que quiero por defecto.
                #print "fecha incio {} contr fecha defecto {} ".format(fechaInicio, fechaInicioDefecto)
                if fechaInicio < fechaInicioDefecto:
                    fechaInicio = fechaInicioDefecto
                
                docsPosicionesVehiculos = consultarPosicionesVehiculos(db, idVehiculo, fechaInicio+"Z", fechaFin, limiteDePuntosPorVehiculo)

                #Itero por cada punto ------------------------------------------

                docAnterior = None
                
                idCompania     = docTenant.get("nit", "")
                placaVehiculo  = docVehiculo.get("placa", "")

                #idConductor    = float(docVehiculo.get("docConductor",{}).get("cedula", ""))

                #idConductor    = float(docVehiculo.get("docConductor",{}).get("cedula", ""))                
                idConductor    = float(cedulasPorVehiculo[docVehiculo["_id"]])
                ultimaDistancia = docSeguimientoPegaso.get("ultimaDistanciaRecorridaDia", "")
                ultimoTiempo    = docSeguimientoPegaso.get("ultimoTiempoRecorridoDia", "")
                
                for docPosicion in docsPosicionesVehiculos:
                    if docAnterior == None:
                        docAnterior = consultarPuntoAnterior(db,idVehiculo, fechaInicio)
                    
                    estaActualizadoDocSeguimientoPegaso = True
                    dataTraccar           = docPosicion.get("dataTraccar",{})
                    
                    horaRegistradaParser  = parser.parse(docPosicion.get('horaRegistrada'))
                    docSeguimientoPegaso["fechaHoraUltimaRevision"] = docPosicion.get('horaRegistrada')
                    
                    timeStamp             = int(time.mktime(horaRegistradaParser.timetuple())) #fecha del reporte

                    noSecuencia           = docSeguimientoPegaso.get("ultimoNumeroSecuencia", 65535)
                    noSecuencia           = noSecuencia + 1
                    if noSecuencia > 65535:
                        # si es 65535 el noSecuencia comienza en cero
                        noSecuencia = 0
                    docSeguimientoPegaso["ultimoNumeroSecuencia"] = noSecuencia
                    
                    latitud             = "{0:.5f}".format(float(docPosicion.get('latitud',0)))
                    longitud            = "{0:.5f}".format(float(docPosicion.get('longitud',0)))
                    altitud             = "{0:.5f}".format(float(dataTraccar.get('altitude',0))) # Altitud sobre el nivel del mar en metros
                    
                    velocidad           = convertirKmsToMs(docPosicion.get('velocidad',0 )) # velocidad instantanea en metros sobre segundos.
                    
                    heading             = int(dataTraccar.get("course",0)) #orientacion del movimiento del vehiculo
                    satelites           = defaultSatelites # numero de satelites usados
                    hdop                = defaultHdop # Disolucion de precision horizontal
                    tipoPosicion        = defaultTipoPosicion # Tipo de posicion (Estado del la posicion)
                    inputs              = 0# estado de las entradas digitales
                    if velocidad > 0:
                        inputs = 1 #HACK si hay velocidad está encendido.
                    
                    codigoEvento    = CODIGOEVENTOSEGUIMIENTO # codigo del evento estandarizado. Obligatorio
                    mensajeEvento   = "posicion" # Mensaje del evento (Mensajes adicionales)

                    #TODO FABIO Optimizar
                    distancia       = 0 # distancia recorrida por el vehiculo en metros
                    tiempoDeTrabajo = 0 # corresponde al tiempo de trabajo del vehiculo expresado en segundos

                    distancia, tiempoDeTrabajo = calcularDistanciaTiempoRecorridaDia(db, idVehiculo, docPosicion.get('horaRegistrada'), docAnterior.get('horaRegistrada'), ultimaDistancia, ultimoTiempo )
                    ultimaDistancia = distancia
                    ultimoTiempo = tiempoDeTrabajo
                    docSeguimientoPegaso["ultimaDistanciaRecorridaDia"] = ultimaDistancia
                    docSeguimientoPegaso["ultimoTiempoRecorridoDia"]    = ultimoTiempo

                    magnitudFalta   = 0 # Magnitud de la falta por exceso de velocidad,
                                         # detenciones prolongadas, alerta panico, aceleracion
                                         # brusca, curvas bruscas
                    tiempoFalta     = 0 # Tiempo de la falta por exceso de velocidad,
                                         # detenciones prolongadas, alerta panico, aceleracion
                                         # brusca, curvas bruscas

                    trama = [
                        str(int(idCompania)),
                        str(placaVehiculo),
                        str(int(idConductor)),
                        str(int(timeStamp)),
                        str(int(noSecuencia)),
                        str(latitud),
                        str(longitud),
                        str(altitud),
                        str(velocidad),
                        str(heading),
                        str(satelites),
                        str(hdop),
                        str(tipoPosicion),
                        str(inputs),
                        str(codigoEvento),
                        str(mensajeEvento),
                        str(distancia),
                        str(tiempoDeTrabajo),
                        str(magnitudFalta),
                        str(tiempoFalta)                    
                    ]

                    tramaExport =  ";".join(trama)
                    tramaExport = tramaExport+"|"
                    print tramaExport
                    tramas.append(tramaExport)

                if estaActualizadoDocSeguimientoPegaso:
                    print "Actualizando seguimiento pegaso"
                    db.save(docSeguimientoPegaso)
                    pass
                print u"{} Tramas encontradas".format(len(tramas))
                if len(tramas)>0:
                    enviarTramas(tramas)
                    tramas = []


def consultarTenants():
    #funcion que busca los tenants en la bd fleetbi
    dbFleet = conexion.getConexionFleet()
    listaTenants = []
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view(
            '_design/tenant/_view/visualizarTenants',
            include_docs  = True
        )
        
        for fila in filas:
            #key                     = fila.key
            #value                   = fila.value
            doc                     = fila.doc

            urlTenant               = doc.get('urlTenant')
            if urlTenant == "mauriciogiraldo":
                listaTenants.append(doc)
        
    except ValueError:
        pass

    return listaTenants


# Se retorna un listado de DOCS vehiículos, se le añade en el camo docConductor el documento del conductor.
# NO SAVEAR o UPDATEAR ESTE DOC, ESTA CORRUPTO POR EL DOCCONDUCTOR AGREGARDO
def consultarVehiculos(db):
    docVehiculos = [] 
    try:
        filas = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs  = True
        )
        
        for fila in filas:
            #key         = fila.key
            #value       = fila.value
            docVehiculo = fila.doc
            
            #Obtiene el conductor del vehículo
            idConductor = docVehiculo.get("conductor", "")
            if not idConductor == "":
                docConductor              = db[idConductor]
                docVehiculo["docConductor"] = docConductor

            docVehiculos.append(docVehiculo)
                        
    except ValueError:
        pass

    return docVehiculos


def consultarSeguimientoPegaso(db, idVehiculo):
    docSeguimientoPegaso = None

    filas = db.view(
        '_design/pegaso/_view/seguimientoPegaso',
        key          = [idVehiculo],
        include_docs = True,
        limit        = 1
    )

    for fila in filas:
        docSeguimientoPegaso = fila.doc

    if docSeguimientoPegaso == None:
        print "Creando seguimiento"

        docSeguimientoPegaso = {
            "tipoDato"        : "seguimientoPegaso",
            "creadoEn"        :  datetime.now().isoformat()[:19],
            "modificadoEn"    :  datetime.now().isoformat()[:19],
            "modificadoPor"   : "",
            "activo"          : True,
            "eliminado"       : False,
	    
	    "idVehiculo"               : idVehiculo,
	    "fechaHoraUltimaRevision"  : "", #Importante "" para hacer las
                                             #consultas e indicar que es el
                                             #primer punto creado
            "ultimaDistanciaRecorridaDia" : "",
	    "ultimoTiempoRecorridoDia"    : ""
        }

        id_doc, id_rev       = db.save(docSeguimientoPegaso)
        print "Guardando seguimiento {}".format(id_doc)
        docSeguimientoPegaso = db[id_doc]
        
    return docSeguimientoPegaso



def consultarPosicionesVehiculos(db, idVehiculo, fechaInicio, fechaFin, limiteDePuntosPorVehiculo):

    docsPosicionesVehiculos = []
    
    
    try:

        filas = db.view(
            '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
            startkey      = [idVehiculo, fechaInicio],
            endkey        = [idVehiculo, fechaFin],   
            include_docs  = True,
            limit         = limiteDePuntosPorVehiculo
        )
        
        for fila in filas:
            #key   = fila.key
            #value = fila.value
            doc   = fila.doc
            docsPosicionesVehiculos.append(doc)

            
            # horaRegistradaParser  = parser.parse(doc.get('horaRegistrada'))
            # timeStamp           = int(time.mktime(horaRegistradaParser.timetuple())) #fecha del reporte
            # if noSecuencia == 65535:
            #     # si es 65535 el noSecuencia comienza en cero
            #     noSecuencia = 0
            # noSecuencia         = noSecuencia + 1 #Numero de secuencia
            # #latitud            = doc.get('latitud') # Latitud
            # latitud             = convertirFormatoLatitud(str(doc.get('latitud')))
            # #longitud           = doc.get('longitud') # Longitud
            # longitud        = convertirFormatoLongitud(str(doc.get('longitud')))
            # altitud             = doc.get('altitud') #
            # altitud             = "" # Altitud sobre el nivel del mar
            # velocidad           = doc.get('velocidad') # velocidad instantanea
            # heading             = "" #orientacion del movimiento del vehiculo
            # satelites           = "" # numero de satelites usados
            # hdop                = "" # Disolucion de precision horizontal
            # posicion            = "" # Tipo de posicion (Estado del la posicion)
            # inputs              = "" # estado de las entradas digitales
            # codigoEvento        = "" # codigo del evento estandarizado. Obligatorio
            # mensajeEvento   = "" # Mensaje del evento (Mensajes adicionales)
            # distancia       = "" # distancia recorrida por el vehiculo en metros
            # tiempoDeTrabajo = "" # corresponde al tiempo de trabajo del vehiculo expresado en segundos
            # magnitudFalta   = "" # Magnitud de la falta por exceso de velocidad, detenciones prolongadas, alerta panico, aceleracion brusca, curvas bruscas
            # tiempoFalta     = "" # Tiempo de la falta por exceso de velocidad, detenciones prolongadas, alerta panico, aceleracion brusca, curvas bruscas                    
            # #print timeStamp
            # #print noSecuencia
            # print latitud
            # print longitud
    except ValueError:
        pass


    return docsPosicionesVehiculos

def convertirKmsToMs( velocidadKms):
    velocidadms = float(velocidadKms)*1000.0 / 3600.0
    velocidadms = "{0:.2f}".format(velocidadms)
    return velocidadms
    

def consultarPuntoAnterior(db,idVehiculo, fecha):
    docPuntoAnterior = None
    
    filas = db.view(
        '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
        startkey      = [idVehiculo, fecha],
        include_docs  = True,
        descending    = True,
        limit         = 1
    )
    
    for fila in filas:
        docPuntoAnterior = fila.doc
        
    return docPuntoAnterior


def calcularDistanciaTiempoRecorridaDia(db, idVehiculo, fecha, fechaAnterior, ultimaDistancia, ultimoTiempo ):
    distanciaMetros = 0
    tiempoDeTrabajo = 0

    fechaInicio = fecha[:10]
    fechaFin    = fecha

    if not ultimaDistancia == "":
        if fecha[:10] == fechaAnterior[:10]:
            fechaInicio = fechaAnterior+"Z"
            distanciaMetros = ultimaDistancia
            tiempoDeTrabajo = ultimoTiempo
    
    filas = db.view(
        '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
        startkey      = [idVehiculo, fechaInicio],
        endkey        = [idVehiculo, fechaFin],
        include_docs  = True
    )

    docAnterior = None #TODO fabio deberìa ser el punto del dìa
                            #anterior.
    #contador = 0
    for fila in filas:
        #print contador
        #contador += 1
        docPosicion = fila.doc

        if docAnterior == None:
            docAnterior = docPosicion
            continue
        
        latInicial = float(docAnterior["latitud"])
        lonInicial = float(docAnterior["longitud"])
        latFinal   = float(docPosicion["latitud"])
        lonFinal   = float(docPosicion["longitud"])
        datetimeInicio = parser.parse(docAnterior.get("horaRegistrada"))
        datetimeFin    = parser.parse(docPosicion.get("horaRegistrada"))
        
        puntoInicial    =   (latInicial, lonInicial)
        puntoFinal      =   (latFinal,   lonFinal)
        distanciaTemp   = vincenty(puntoInicial, puntoFinal).meters
        if distanciaTemp < 1000:
            distanciaMetros += distanciaTemp

        if docPosicion["velocidad"] > 0.01: #TODO FABIO debería ser con el encendido del vehiculo
            segundos = (datetimeFin - datetimeInicio).total_seconds()
            #print "Segundos: entre {} y {} es {} segundos".format(docAnterior.get("horaRegistrada"), docPosicion.get("horaRegistrada"), segundos)
            tiempoDeTrabajo += segundos
        docAnterior = docPosicion
    return [distanciaMetros, tiempoDeTrabajo]

def enviarTramas(tramas):
    print "Enviando tramas"
    headers = {u'content-type': u'application/x-www-form-urlencoded'}
    r = requests.post(urlWSRepetidora, data={ 'request': json.dumps( { "trazas" : tramas } ) }, headers=headers)
    print(r.status_code, r.reason)
    print r.text
    

#-----MAGINOT------------------------------------------------------------------

#Pendiente
def consultarUltimoNumSecuenciaVehiculo(db, identificadorDocVehiculo):
        #Pendiente ojo
        #Consulta el ultimo numero de secuencia del vehiculo
        return 0-1


def convertirFormatoLatitud(latitud):
        latitud = "{0:.5f}".format(float(latitud)) # 5 decimales
        return latitud

def convertirFormatoLongitud(longitud):
        longitud = "{0:.5f}".format(float(longitud)) # 5 decimales
        return longitud






