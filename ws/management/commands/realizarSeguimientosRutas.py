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
#from ws.serviciosweb.conexion import conexion

#Variables de configuracion:

PAR_MINUTOSMINIMODETECCION = 0 #Número de minito mínimos antes de detectar que el vehículo está en ruta
PAR_PUNTOSMINIMOSDETECCION = 2 #Número de puntos detectados en ruta.
PAR_PORCENTAJEMINIMOPUNTOSDETECCION = 0.50 #Relación entre puntos detectados y puntos no detectados
PAR_PUNTOSBUFFERREVISION   = 10 #Número de puntos que quedan en el buffer según la operacion
PAR_DISTANCIADETECCIONCERCANIA     = 0.001 #0.0001 #Distancia máxima en la cual se detecta que un punto está cerca de una ruta.
PAR_DISTANCIADETECCIONINICIORUTA   = 0.004 #Distancia que debe recocorrer el vehiculo para detecta el inicio de ruta

PAR_MINUTOSENTREINFRACCIONESVELOCIDAD   = 15 # Numero de minutos entre infraccion e infraccion

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

        for fila in filas:
            docTenant = fila.doc
            dbTenant  = couch[u"{}{}".format(settings.BASEDB, docTenant.get("urlTenant",""))]

            print u"Tenant {}".format(docTenant.get("urlTenant", ""))
            
            #cerrarAsignacionesVencidas(dbTenant)
            #detectarInicioSeguimientos(dbTenant)
            procesarSeguimientos(dbTenant)

# Funciones principales -------------------------------------
def cerrarAsignacionesVencidas(db):

    print u"cerrarAsignacionesVencidas".format()
    fechaActualMin = datetime.now().isoformat()[:19]
    fechaActualMax = (datetime.now() + timedelta(minutes = settings.SEG)).isoformat()

    filas = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoFechaFin',
        include_docs = True,
        startkey     = ["programada", 0],
        endkey       = ["programada", fechaActualMax]
    )

    for fila in filas:
        docAsignacion = fila.doc
        docAsignacion["estado"] = "noejecutada"
        print u"Cerrando Asignación {}".format(docAsignacion["_id"])
        db.save(docAsignacion)

def detectarInicioSeguimientos(db):

    print u"Detectando inicio de seguimiento".format()
    
    fechaActualMax = (datetime.now() + timedelta(minutes = settings.SEG)).isoformat()
    
    filas = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoFechaInicio',
        include_docs = True,
        startkey     = ["programada", 0],
        endkey       = ["programada", fechaActualMax]
    )

    print u"BUscando: {}".format(fechaActualMax)

    # REviso cada asignación pendiente y ver si ya inició.
    for fila in filas:
        # print "Analizando asignacion"
        docAsignacion = fila.doc
        estaAsignacionIniciada = False # Aquí pongo la determinación si la asignación inició.

        fechaInicioProgramada = docAsignacion.get("fechaInicioProgramada","")
        
        fechaInicioProgramadaMin = (parser.parse(fechaInicioProgramada) - timedelta(minutes = settings.SEG)).isoformat()[:19]

        existenPuntosRestantes = True
        fechaRevisionPuntos    = fechaInicioProgramadaMin

        docSeguimiento = getSeguimientoAsignacion(
            db               = db,
            docAsignacion    = docAsignacion,
            crearSeguimiento = True
        )

        docRuta               = db[docAsignacion.get("idRuta","")]
        docPuntosRutaDefinida = db[docRuta.get("idPuntosRutaDefinida", None)]
        docVehiculo           = db[docRuta.get("idVehiculo","")]

        #Las deque mantiene que el maximo largo de la lista sea
        #PAR_PUNTOSBUFFERREVISION, cuando se hace un append se saca el
        #primero (pos[0]) de la lista para abrir espacio.
        
        listaPuntosEnRuta     = deque([], PAR_PUNTOSBUFFERREVISION)
        listaPuntosFueraRuta  = deque([], PAR_PUNTOSBUFFERREVISION)

        
        #Analisando puntos
        while existenPuntosRestantes:
            #print "Existen puntos"
            idVehiculo = docAsignacion.get("idVehiculo","")
            filasPosiciones = db.view(
                '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
                include_docs = True,
                startkey     = [idVehiculo, fechaRevisionPuntos+"Z"],
                endkey       = [idVehiculo, {}],
                limit        = 1000
            )

            #print u"Buscando puntos con: {} - {}".format(idVehiculo, fechaRevisionPuntos+"Z")

            existenPuntosRestantes = False
            for filaPosicion in filasPosiciones:
                #print "Hubo puntos"
                existenPuntosRestantes = True                    
                docPosicion            = filaPosicion.doc

                fechaRevisionPuntos    = docPosicion.get("horaRegistrada")
                
                existePuntoEnRuta = verificarPuntoEnRuta(docPosicion, docPuntosRutaDefinida)
                if existePuntoEnRuta:
                    listaPuntosEnRuta.append(docPosicion)
                    #print u"Ruta {}".format(docPosicion.get("horaRegistrada"))
                else:
                    listaPuntosFueraRuta.append(docPosicion)
                    #print u"Fuera {}".format(docPosicion.get("horaRegistrada"))

                #Limpio según los tiempos, del primero del buffer de e
                #ruta tomo de referencia y eimino todos los puntos que
                #sean anteriores a este:
                if len(listaPuntosEnRuta) > 0:
                    docPrimeraPosicion = listaPuntosEnRuta[0]
                    fechaCorte         = docPrimeraPosicion.get("horaRegistrada", "")

                    if len(listaPuntosFueraRuta)> 0:
                        docPosicionFuera = listaPuntosFueraRuta[0]
                        while not docPosicionFuera == None and fechaCorte > docPosicionFuera.get("horaRegistrada", ""):
                            listaPuntosFueraRuta.popleft()
                            if len(listaPuntosFueraRuta)> 0:
                                docPosicionFuera = listaPuntosFueraRuta[0]
                            else:
                                docPosicionFuera = None
                
                if len(listaPuntosEnRuta) > PAR_PUNTOSMINIMOSDETECCION:
                   porcentaje = 1.0 - ( 1.0*len(listaPuntosFueraRuta) / len(listaPuntosEnRuta) * 1.0)

                   # print u"T1 Division: {} / {}".format(
                   #     len(listaPuntosFueraRuta),
                   #     len(listaPuntosEnRuta)
                   # )

                   primerPunto = listaPuntosEnRuta[0]
                   ultimoPunto = listaPuntosEnRuta[-1]

                   # print "T1 Primer {} - Ultimo {}".format(
                   #     primerPunto.get("horaRegistrada", ""),
                   #     ultimoPunto.get("horaRegistrada", "")
                   # )
                   distanciaEntrePrimeroPuntoYUltimo = lineMagnitude (
                       float( primerPunto.get("latitud","0") ), float( primerPunto.get("longitud","0") ),
                       float( ultimoPunto.get("latitud","0") ), float( ultimoPunto.get("longitud","0") )
                   )

                   # print u"T1 Decision: Porcentaje {} - Distancia  {}".format(
                   #     porcentaje,
                   #     distanciaEntrePrimeroPuntoYUltimo
                   # )
                   
                   if porcentaje > PAR_PORCENTAJEMINIMOPUNTOSDETECCION and distanciaEntrePrimeroPuntoYUltimo > PAR_DISTANCIADETECCIONINICIORUTA:
                       #RUTA DETECTADA!!!!!!!!!!!!
                       #print docAsignacion
                       #print docSeguimiento
                       # for punto in listaPuntosEnRuta:
                       #     print punto.get("horaRegistrada")
                       # print "-----------------------------------------"
                       # print listaPuntosEnRuta[0].get("horaRegistrada")
                       # print listaPuntosEnRuta[-1].get("horaRegistrada")
                       
                       print u"Ruta detectada para asignacion {} y seguimiento {}".format(docAsignacion["_id"], docSeguimiento["_id"])
                       docSeguimiento["estado"] = "enruta"
                       docSeguimiento["fechaHoraInicioSeguimiento"] = primerPunto.get("horaRegistrada", "")
                       docSeguimiento["fechaHoraUltimaRevision"] = primerPunto.get("horaRegistrada", "")
                       
                       docAsignacion["estado"]  = "enruta"
                       docAsignacion["fechaInicioReal"] = primerPunto.get("horaRegistrada", "")
                       db.save(docSeguimiento)
                       db.save(docAsignacion)
                       existenPuntosRestantes = False
                       break
                       

        #----------------------------------------------------------------------------            
def procesarSeguimientos(db):

    print "procesarSeguimiento"

    filas = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoFechaInicio',
        include_docs = True,
        startkey     = ["enruta", 0],
        endkey       = ["enruta", {}]
    )
        
    # Reviso cada asignación en ruta y reviso como va
    for fila in filas:

        docAsignacion  = fila.doc
        docSeguimiento = getSeguimientoAsignacion(
            db               = db,
            docAsignacion    = docAsignacion,
            crearSeguimiento = False
        )
        docRuta        = db[docAsignacion.get("idRuta", "")]
        docVehiculo    = {} 

        docPuntosRutaDefinida = {}
        if not docRuta.get("idPuntosRutaDefinida", "") == "":
            docPuntosRutaDefinida = db[docRuta.get("idPuntosRutaDefinida", "")]
        
        idVehiculo             = docAsignacion.get("idVehiculo","")
        
        if not idVehiculo == "":
            docVehiculo = db[idVehiculo]

        
        fechaRevisionPuntos    = docSeguimiento.get("fechaHoraUltimaRevision",0)
        existenPuntosRestantes = True
        docPosicionAnterior    = None
        
        puntosDeControlVirtual = docAsignacion.get("puntosDeControlVirtual",[])
        estaModificadoPuntosDeControlVirtual = False

        puntosParadas               = docAsignacion.get("puntosParadas",[])
        estaModificadoPuntosParadas = False

        limitesDeVelocidad             = docAsignacion.get("limitesDeVelocidad",[])
        estaModificadoLimitesVelocidad = False
        estaModificadoVehiculo         = False
        
        while existenPuntosRestantes:
            
            filasPosiciones = db.view(
                '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
                include_docs = True,
                startkey     = [idVehiculo, fechaRevisionPuntos+"Z"],
                endkey       = [idVehiculo, {}],
                limit        = 1000
            )

            existenPuntosRestantes = False
            for filaPosicion in filasPosiciones:
                existenPuntosRestantes = True                    
                docPosicion            = filaPosicion.doc
                fechaRevisionPuntos    = docPosicion.get("horaRegistrada")
                docSeguimiento["fechaHoraUltimaRevision"] = fechaRevisionPuntos
                estaModificadoSeguimiento = True

                print fechaRevisionPuntos
                # Reviso los puntos de control ===========================================
                for puntoDeControlVirtual in puntosDeControlVirtual:
                    if puntoDeControlVirtual.get("fechaHoraCruceReal", "") == "":
                        distanciaMinimaARuta = calcularDistanciaMinimaRutaPuntoControl(
                            puntoDeControlVirtual,
                            docPosicionAnterior,
                            docPosicion
                        )

                        if distanciaMinimaARuta < PAR_DISTANCIADETECCIONCERCANIA:                            
                            horaDeCruce = calcularHoraDeCrucePuntoControl(
                                puntoDeControlVirtual,
                                docPosicionAnterior,
                                docPosicion
                            )
                            print "Punto de control detectado en {}".format(horaDeCruce)
                            puntoDeControlVirtual["fechaHoraCruceReal"] = horaDeCruce
                            estaModificadoPuntosDeControlVirtual = True
                #===========================================================================


                #Reviso los puntos de paradas ==============================================
                for puntoParada in puntosParadas:
                    fechaHoraInicioParada = puntoParada.get("fechaHoraInicioParada","")
                    fechaHoraFinParada    = puntoParada.get("fechaHoraFinParada","")
                    if fechaHoraInicioParada == "": #No ha iniciado parada
                        distanciaPuntoParada = calcularDistanciaMinimaAPuntoParada(
                            puntoParada,
                            docPosicionAnterior,
                            docPosicion
                        )

                        if distanciaPuntoParada < PAR_DISTANCIADETECCIONCERCANIA:
                            horaDeCruce = calcularHoraDeCrucePuntoParada(
                                puntoParada,
                                docPosicionAnterior,
                                docPosicion
                            )
                            print "Entro en parada {}".format(horaDeCruce)
                            puntoParada["fechaHoraInicioParada"] = horaDeCruce
                            if puntoParada.get("tipo") == "Carga":
                                docVehiculo["cargado"] = True
                                estaModificadoVehiculo = True
                            else:
                                docVehiculo["cargado"] = False
                                estaModificadoVehiculo = True
                            
                            estaModificadoPuntosParadas = True
                        
                    elif fechaHoraFinParada == "":
                        distanciaPuntoParada = calcularDistanciaMinimaAPuntoParada(
                            puntoParada,
                            docPosicionAnterior,
                            docPosicion
                        )

                        if distanciaPuntoParada > PAR_DISTANCIADETECCIONCERCANIA:
                            horaDeCruce = calcularHoraDeCrucePuntoParada(
                                puntoParada,
                                docPosicionAnterior,
                                docPosicion
                            )
                            print "Salio de parada {}".format(horaDeCruce)
                            puntoParada["fechaHoraFinParada"] = horaDeCruce
                            estaModificadoPuntosParadas       = True
                #===========================================================================

                #Reviso los limites de velocidad ===========================================
                #TODO que carga sea en base al estado del vehiculo
                estadoCarga = ""
                if docVehiculo.get("cargado",False):
                    estadoCarga = "Descarga"
                else:
                    estadoCarga = "Carga"
                    
                if revisarExcesosDeVelocidad(db, docPuntosRutaDefinida, limitesDeVelocidad, docPosicion, estadoCarga):
                    print "Encontro excesos de velocidad"
                    print json.dumps(limitesDeVelocidad)
                    estaModificadoLimitesVelocidad = True
                    

                #===========================================================================
                                
                
                # Reviso si llegue al final de la ruta =====================================
                distanciaMinimaADestino = calcularDistanciaMinimaADestino(
                    docRuta,
                    docPosicionAnterior,
                    docPosicion
                )
                print "distaenciaMinimo {}".format(distanciaMinimaADestino)
                if distanciaMinimaADestino < PAR_DISTANCIADETECCIONCERCANIA:
                    horaDeCruce = calcularHoraDeCruceDestino(
                       docRuta,
                       docPosicionAnterior,
                       docPosicion
                    )
                    print u"Encontrado fin de ruta en {}".format(horaDeCruce)
                    horaDeCruce = docPosicion.get("horaRegistrada", "")
                    print u"Encontrado fin de ruta en {}".format(horaDeCruce)
                    
                    docAsignacion['estado']         = 'finalizada'
                    docAsignacion['fechaFinReal']   = horaDeCruce
                    docSeguimiento['estado']        = 'finalizadaCompleta'
                    docSeguimiento['fechaFinReal']  = horaDeCruce
                    #TODO Fabio cambiar pot doc 
                    docSeguimiento['velocidadDeCruce']  = docPosicion.get("velocidad", "0")

                    estaModificadoAsignacion  = True
                    estaModificadoSeguimiento = True                    
                    existenPuntosRestantes    = False #Ya no me interesan ver mas puntos
                    break
                #===========================================================================
                
                docPosicionAnterior    = docPosicion

        if estaModificadoPuntosDeControlVirtual:
            docAsignacion["puntosDeControlVirtual"] = puntosDeControlVirtual
            db.save(docAsignacion)

        
        if estaModificadoAsignacion:
            db.save(docAsignacion)
            pass

        if estaModificadoSeguimiento:
            db.save(docSeguimiento)
            pass

        if estaModificadoPuntosParadas:
            docAsignacion["puntosParadas"] = puntosParadas
            db.save(docAsignacion)

        if estaModificadoLimitesVelocidad:
            docAsignacion["limitesDeVelocidad"] = limitesDeVelocidad
            db.save(docAsignacion)
            
        if estaModificadoVehiculo:
            db.save(docVehiculo)
            pass
        #---------------------------------------------------
        
# -----------------------------------------------------------

# Auxiliares ------------------------------------------------
#crearSeguimiento  crea un seguimiento vacio si no existe.
def getSeguimientoAsignacion(db, docAsignacion, crearSeguimiento=True):

    docSeguimiento    = None
    
    filas = db.view(
        '_design/seguimientoAsignacionRuta/_view/seguimientoAsignacionRutaPorAsignacionRuta',
        include_docs = True,
        key          = [ docAsignacion["_id"] ],
        limit        = 1
    )

    for fila in filas:
        docSeguimiento    = fila.doc
        
    if docSeguimiento == None:
        docSeguimiento = {
            "tipoDato"        : "seguimientoAsignacionRuta",
	    
            "creadoEn"        : datetime.now().isoformat()[:19],
            "modificadoEn"    : datetime.now().isoformat()[:19],
            "modificadoPor"   : "",
            "activo"          : True,
            "eliminado"       : False,
	    
	    "idAsignacionRuta"           : docAsignacion["_id"],
	    "fechaHoraInicioSeguimiento" : "",
	    "fechaHoraFinSeguimiento"    : "",
	    "fechaHoraUltimaRevision"    : "",
            "estado"                     : "noiniciada"
        }
        db.save(docSeguimiento)

    return docSeguimiento

#Retorna True si la posicion de docPosicion está en la ruta definida.
def verificarPuntoEnRuta(docPosicion, docPuntosRutaDefinida):

    #print "verificarPuntoEnRuta"
    
    listaPuntosRuta = docPuntosRutaDefinida.get("puntosRuta", [])

    posLatitud  = float(docPosicion.get("latitud", "0"))
    posLongitud = float(docPosicion.get("longitud", "0"))
    
    for i in range(0, len(listaPuntosRuta) - 1 ):
        puntoA = listaPuntosRuta[i]
        puntoB = listaPuntosRuta[i+1]

        distancia = DistancePointLine(
            posLatitud, posLongitud,
            puntoA[0], puntoA[1],
            puntoB[0], puntoB[1]
        )
        
        if distancia < PAR_DISTANCIADETECCIONCERCANIA:
            return True
        
    return False

def calcularDistanciaMinimaRutaPuntoControl(puntoDeControlVirtual, docPosicionAnterior, docPosicion):

    distanciaPosicionAnterior = 99999
    distanciaPosicion         = 99999
    distanciaLineaRuta        = 99999 #Distancia perpendiculas a la
                                      #linea defina por los dos puntos
                                      #para calcular que tan cerca
                                      #está en la intersección


    latControl = float(puntoDeControlVirtual.get("latitud","0"))
    lonControl = float(puntoDeControlVirtual.get("longitud","0"))

    # latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
    # lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))

    # latPunto = float(docPosicion.get("latitud","0"))
    # lonPunto = float(docPosicion.get("longitud","0"))
    
    if not docPosicionAnterior == None and not docPosicion == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        
        latPunto = float(docPosicion.get("latitud","0"))
        lonPunto = float(docPosicion.get("longitud","0"))
    
        distanciaLineaRuta = DistancePointLine(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior,
            latPunto,         lonPunto            
        )

    if not docPosicionAnterior == None:
        latPuntoAnterior          = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior          = float(docPosicionAnterior.get("longitud","0"))
        distanciaPosicionAnterior = lineMagnitude(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior
        )

    if not docPosicion == None:
        latPunto          = float(docPosicion.get("latitud","0"))
        lonPunto          = float(docPosicion.get("longitud","0"))
        distanciaPosicion = lineMagnitude(
            latControl,       lonControl,
            latPunto, lonPunto
        )


    return min(
        distanciaPosicionAnterior,
        distanciaPosicion,
        distanciaLineaRuta    
    )


def calcularDistanciaMinimaADestino(docRuta, docPosicionAnterior, docPosicion):

    distanciaPosicionAnterior = 99999
    distanciaPosicion         = 99999
    distanciaLineaRuta        = 99999 #Distancia perpendiculas a la
                                      #linea defina por los dos puntos
                                      #para calcular que tan cerca
                                      #está en la intersección

    latControl = docRuta.get("destino", [0, 0])[0]
    lonControl = docRuta.get("destino", [0, 0])[1]
    
    if not docPosicionAnterior == None and not docPosicion == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        
        latPunto = float(docPosicion.get("latitud","0"))
        lonPunto = float(docPosicion.get("longitud","0"))
    
        distanciaLineaRuta = DistancePointLine(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior,
            latPunto,         lonPunto            
        )

    if not docPosicionAnterior == None:
        latPuntoAnterior          = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior          = float(docPosicionAnterior.get("longitud","0"))
        distanciaPosicionAnterior = lineMagnitude(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior
        )

    if not docPosicion == None:
        latPunto          = float(docPosicion.get("latitud","0"))
        lonPunto          = float(docPosicion.get("longitud","0"))
        distanciaPosicion = lineMagnitude(
            latControl,       lonControl,
            latPunto, lonPunto
        )


    return min(
        distanciaPosicionAnterior,
        distanciaPosicion,
        distanciaLineaRuta    
    )



def calcularDistanciaMinimaAPuntoParada( puntoParada, docPosicionAnterior, docPosicion ):

    distanciaPosicionAnterior = 99999
    distanciaPosicion         = 99999
    distanciaLineaRuta        = 99999 #Distancia perpendiculas a la
                                      #linea defina por los dos puntos
                                      #para calcular que tan cerca
                                      #está en la intersección

    latControl = float(puntoParada.get("latitud", "0"))
    lonControl = float(puntoParada.get("longitud", "0"))
    
    if not docPosicionAnterior == None and not docPosicion == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        
        latPunto = float(docPosicion.get("latitud","0"))
        lonPunto = float(docPosicion.get("longitud","0"))
    
        distanciaLineaRuta = DistancePointLine(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior,
            latPunto,         lonPunto            
        )

    if not docPosicionAnterior == None:
        latPuntoAnterior          = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior          = float(docPosicionAnterior.get("longitud","0"))
        distanciaPosicionAnterior = lineMagnitude(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior
        )

    if not docPosicion == None:
        latPunto          = float(docPosicion.get("latitud","0"))
        lonPunto          = float(docPosicion.get("longitud","0"))
        distanciaPosicion = lineMagnitude(
            latControl,       lonControl,
            latPunto, lonPunto
        )


    return min(
        distanciaPosicionAnterior,
        distanciaPosicion,
        distanciaLineaRuta    
    )

    
def calcularHoraDeCrucePuntoControl(
        puntoDeControlVirtual,
        docPosicionAnterior,
        docPosicion
):

    tiempoDeCruce = ""
    
    latControl = float(puntoDeControlVirtual.get("latitud","0"))
    lonControl = float(puntoDeControlVirtual.get("longitud","0"))

    
    if not docPosicionAnterior == None and not docPosicion == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        
        latPunto = float(docPosicion.get("latitud","0"))
        lonPunto = float(docPosicion.get("longitud","0"))

        fechaHoraPuntoAnterior = parser.parse(docPosicionAnterior.get("horaRegistrada"))
        fechaHoraPunto         = parser.parse(docPosicion.get("horaRegistrada"))
        segundosDiferencia     = (fechaHoraPunto - fechaHoraPuntoAnterior).total_seconds()

        distanciaPosicionAnterior = lineMagnitude(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior
        )

        distanciaPosicion = lineMagnitude(
            latControl,       lonControl,
            latPunto, lonPunto
        )

        totalDistancia    = distanciaPosicion
        relacionDistancia = 1.0 * distanciaPosicion / totalDistancia
        segundosRelacion  = int( relacionDistancia * segundosDiferencia  )
        tiempoDeCruce       = (fechaHoraPunto - timedelta(seconds = settings.SEG)).isoformat()[:19]

        
        
    elif not docPosicionAnterior == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        tiempoDeCruce      = docPosicionAnterior.get("horaRegistrada")
    
    else:
        latPunto      = float(docPosicion.get("latitud","0"))
        lonPunto      = float(docPosicion.get("longitud","0"))
        tiempoDeCruce = docPosicion.get("horaRegistrada")
    

    return tiempoDeCruce


def calcularHoraDeCruceDestino(
        docRuta,
        docPosicionAnterior,
        docPosicion
):

    tiempoDeCruce = ""

    latControl = docRuta.get("destino", [0, 0])[0]
    lonControl = docRuta.get("destino", [0, 0])[1]

    
    if not docPosicionAnterior == None and not docPosicion == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        
        latPunto = float(docPosicion.get("latitud","0"))
        lonPunto = float(docPosicion.get("longitud","0"))

        fechaHoraPuntoAnterior = parser.parse(docPosicionAnterior.get("horaRegistrada"))
        fechaHoraPunto         = parser.parse(docPosicion.get("horaRegistrada"))
        segundosDiferencia     = (fechaHoraPunto - fechaHoraPuntoAnterior).total_seconds()

        distanciaPosicionAnterior = lineMagnitude(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior
        )

        distanciaPosicion = lineMagnitude(
            latControl,       lonControl,
            latPunto, lonPunto
        )

        totalDistancia    = distanciaPosicion + distanciaPosicionAnterior
        relacionDistancia = 1.0 * distanciaPosicion / totalDistancia
        segundosRelacion  = int( relacionDistancia * segundosDiferencia  )
        tiempoDeCruce       = (fechaHoraPunto - timedelta(seconds = settings.SEG)).isoformat()[:19]

        
        
    elif not docPosicionAnterior == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        tiempoDeCruce      = docPosicionAnterior.get("horaRegistrada")
    
    else:
        latPunto      = float(docPosicion.get("latitud","0"))
        lonPunto      = float(docPosicion.get("longitud","0"))
        tiempoDeCruce = docPosicion.get("horaRegistrada")
    

    return tiempoDeCruce


def calcularHoraDeCrucePuntoParada(
        puntoParada,
        docPosicionAnterior,
        docPosicion
):

    tiempoDeCruce = ""


    latControl = float(puntoParada.get("latitud", "0"))
    lonControl = float(puntoParada.get("longitud", "0"))

    
    if not docPosicionAnterior == None and not docPosicion == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        
        latPunto = float(docPosicion.get("latitud","0"))
        lonPunto = float(docPosicion.get("longitud","0"))

        fechaHoraPuntoAnterior = parser.parse(docPosicionAnterior.get("horaRegistrada"))
        fechaHoraPunto         = parser.parse(docPosicion.get("horaRegistrada"))
        segundosDiferencia     = (fechaHoraPunto - fechaHoraPuntoAnterior).total_seconds()

        distanciaPosicionAnterior = lineMagnitude(
            latControl,       lonControl,
            latPuntoAnterior, lonPuntoAnterior
        )

        distanciaPosicion = lineMagnitude(
            latControl,       lonControl,
            latPunto, lonPunto
        )

        totalDistancia    = distanciaPosicion
        relacionDistancia = 1.0 * distanciaPosicion / totalDistancia
        segundosRelacion  = int( relacionDistancia * segundosDiferencia  )
        tiempoDeCruce       = (fechaHoraPunto - timedelta(seconds = settings.SEG)).isoformat()[:19]

        
        
    elif not docPosicionAnterior == None:
        latPuntoAnterior = float(docPosicionAnterior.get("latitud","0"))
        lonPuntoAnterior = float(docPosicionAnterior.get("longitud","0"))
        tiempoDeCruce      = docPosicionAnterior.get("horaRegistrada")
    
    else:
        latPunto      = float(docPosicion.get("latitud","0"))
        lonPunto      = float(docPosicion.get("longitud","0"))
        tiempoDeCruce = docPosicion.get("horaRegistrada")
    

    return tiempoDeCruce


# -----------------------------------------------------------

# -----------------------------------------------------------
# Retorna true cuando el hubo cambios en limitesDeVelocidad
def revisarExcesosDeVelocidad(db, docPuntosRutaDefinida, limitesDeVelocidad, docPosicion, estadoVehiculo):

    limiteSeleccionado = {}    
    if len(limitesDeVelocidad) > 0 :
        limiteSeleccionado = limitesDeVelocidad[0]
    
    puntoRutaAnterior = None
    
    for puntoRuta in docPuntosRutaDefinida.get("puntosRuta",[]):

        #Verifico si hay un cambio en el limite de velocidad
        contadorLimite = 0
        for limiteDeVelocidad in limitesDeVelocidad:    
            distanciaAlLimite = lineMagnitude(
                float(limiteDeVelocidad.get("latitud", "0")), float(limiteDeVelocidad.get("longitud",0)),                
                puntoRuta[0], puntoRuta[1]
            )

            if distanciaAlLimite < PAR_DISTANCIADETECCIONCERCANIA:
                
                if not limiteSeleccionado.get("latitud") == limiteDeVelocidad.get("latitud") and not limiteSeleccionado.get("longitud") == limiteDeVelocidad.get("longitud"):                    
                    #Es un limite distinto al anterior, eso quiere decir que ya lo paso
                    #if limiteDeVelocidad["estado"] == "vigilando":
                    if len(limiteSeleccionado.get("infracciones",[])) == 0 :
                        limiteSeleccionado["estado"] = "ok"
                        
                limiteSeleccionado = limiteDeVelocidad
                
            #print contadorLimite
            contadorLimite += 1
        
        #Verifico si el punto hace parte del punto ruta:
        
        distancia = 0
        
        if puntoRutaAnterior == None:
            distancia = lineMagnitude(
                float(docPosicion.get("latitud", "0")), float(docPosicion.get("longitud",0)),
                
                puntoRuta[0], puntoRuta[1]
            )
        else:
            distancia = DistancePointLine(
                float(docPosicion.get("latitud", "0")), float(docPosicion.get("longitud",0)),
                puntoRutaAnterior[0], puntoRutaAnterior[1],
                puntoRuta[0],         puntoRuta[1]
            )

        if distancia < PAR_DISTANCIADETECCIONCERCANIA:

            if float(limiteSeleccionado.get("velocidadMaximaRegistrada", "0")) < float(docPosicion.get("velocidad", "0")):
                limiteSeleccionado["velocidadMaximaRegistrada"] = float(docPosicion.get("velocidad", "0"))

            limiteVelocidadSegunEstado = "0"
            if estadoVehiculo == "Carga":
                limiteVelocidadSegunEstado = float(limiteSeleccionado.get("limiteCargado", "0"))
            else:
                limiteVelocidadSegunEstado = float(limiteSeleccionado.get("limiteDescargado", "0"))

            if not limiteVelocidadSegunEstado == 0:
                
                if limiteVelocidadSegunEstado < float(docPosicion.get("velocidad", "0")):
                    
                    infracciones = limiteSeleccionado.get("infracciones" , [])
                    
                    minutosDiferenciaEntreInfracciones = 0
                    if len(infracciones) > 0:
                        ultimaInfraccion = infracciones[-1]
                        fechaHoraUltimaInfraccion = parser.parse(ultimaInfraccion.get("fechaHoraInfraccion",""))
                        fechaHoraInfraccion       = parser.parse(docPosicion.get("horaRegistrada"))
                        minutosDiferencia = (fechaHoraInfraccion - fechaHoraUltimaInfraccion).total_seconds() / 60.0                        
                        if minutosDiferencia < PAR_MINUTOSENTREINFRACCIONESVELOCIDAD: #Es la misma infraccion
                            ultimaInfraccion["velocidad"] = docPosicion.get("velocidad", 0.0)
                        else:
                            limiteSeleccionado["estado"] = "excedido"
                            infracciones.append({
                                "latitud"          : docPosicion.get("latitud", ""),
				"longitud"         : docPosicion.get("longitud", ""),
				"direccion"        : "",
				"tipo"             : estadoVehiculo,
				"velocidad"        : docPosicion.get("velocidad", 0.0), 
				"fechaHoraInfraccion" : docPosicion.get("horaRegistrada", 0.0)
                            })
                        return True
                    else:
                        limiteSeleccionado["estado"] = "excedido"
                        infracciones.append({
                                "latitud"          : docPosicion.get("latitud", ""),
				"longitud"         : docPosicion.get("longitud", ""),
				"direccion"        : "",
				"tipo"             : estadoVehiculo,
				"velocidad"        : docPosicion.get("velocidad", 0.0), 
				"fechaHoraInfraccion" : docPosicion.get("horaRegistrada", 0.0)
                            })
                        return True
                
        puntoRutaAnterior = puntoRuta

    return False
        
            
# -----------------------------------------------------------


# Disancias -------------------------------------------------
def lineMagnitude (x1, y1, x2, y2):
    lineMagnitude = math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))
    return lineMagnitude
 
#Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
def DistancePointLine (px, py, x1, y1, x2, y2):
    #http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
    LineMag = lineMagnitude(x1, y1, x2, y2)
 
    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine
 
    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)
 
    if (u < 0.00001) or (u > 1):
        #// closest point does not fall within the line segment, take the shorter distance
        #// to an endpoint
        ix = lineMagnitude(px, py, x1, y1)
        iy = lineMagnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = lineMagnitude(px, py, ix, iy)
 
    return DistancePointLine
#----------------------------------------------------------
