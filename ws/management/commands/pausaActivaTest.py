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
from ws.serviciosweb.modulos.conexion import conexion
from datetime                 import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
import sys

cacheDocumentos = {} #diccionario que almacenara en cache los documentos para guardarlos posteriormente
cacheDocSeguimientoPausaActiva = {}

#Inicio prueba----------------------------------------------------------------------
datosEventosVehiculoTemp = {} #estructura puntos para prueba vehiculo SNQ209


# datosEventosVehiculoTemp["376ab4cad78e3a90cc318dd08196c34d"] = [{
#     "estaEncendidoMotor" : True,
#     "horaRegistrada"     : "2017-11-17T08:47:19",
#     "velocidad"          : 2      

#     },
#     {
#     "estaEncendidoMotor" : True,
#     "horaRegistrada"     : "2017-11-17T09:47:19",
#     "velocidad"          : 3      

#     },
#     {
#     "estaEncendidoMotor" : True,
#     "horaRegistrada"     : "2017-11-17T15:47:19",
#     "velocidad"          : 0          

#     }


#     ]


datosEventosVehiculoTemp["376ab4cad78e3a90cc318dd08196c34d"] = [{
    "estaEncendidoMotor" : False,
    "horaRegistrada"     : "2017-11-17T08:47:19",
    "velocidad"          : 0      

    },
    {
    "estaEncendidoMotor" : True,
    "horaRegistrada"     : "2017-11-17T13:47:19",
    "velocidad"          : 3      

    },
    {
    "estaEncendidoMotor" : True,
    "horaRegistrada"     : "2017-11-17T13:50:19",
    "velocidad"          : 5          

    },

    {
    "estaEncendidoMotor" : True,
    "horaRegistrada"     : "2017-11-17T14:50:19",
    "velocidad"          : 0          

    },

    {
    "estaEncendidoMotor" : True,
    "horaRegistrada"     : "2017-11-17T15:50:19",
    "velocidad"          : 0          

    },

    {
    "estaEncendidoMotor" : True,
    "horaRegistrada"     : "2017-11-17T20:50:19",
    "velocidad"          : 3          

    },

    {
    "estaEncendidoMotor" : True,
    "horaRegistrada"     : "2017-11-17T21:50:19",
    "velocidad"          : 0         

    },

    ]
#fin prueba----------------------------------------------------------------------


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        #import pdb; pdb.set_trace() #depurador python
        tenants = buscarTenants()
        # if "376ab4cad78e3a90cc318dd08196c34d" in datosEventosVehiculoTemp:
        #     for doc in datosEventosVehiculoTemp["376ab4cad78e3a90cc318dd08196c34d"]:
        #         print doc.get("velocidad")
        for tenant in tenants:
            print "==================================="
            print tenant
            #por cada tenant se procesara la informacion
            procesarEvaluacionPausaActiva(tenant)


def obtenerUltimaRevisionPausaActiva(db, idVehiculo):
    ultimaRevision      = {}
    ultimaRevision["fechaHoraRegistrada"]       = ""
    ultimaRevision["idDocUltimaRevision"]       = ""
    #ultimaRevision["revisado"]                  = ""    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/seguridadVial/_view/listarFechasRevision',
            key             = ["pausaActiva", idVehiculo],
            include_docs    = True)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value
            doc                             = fila.doc
            ultimaRevision["idDocUltimaRevision"]  = doc.get('_id')
            ultimaRevision["fechaHoraRegistrada"]  = doc.get('fechaHoraRegistrada')  
        return ultimaRevision
    except ValueError:
        pass


def procesarEvaluacionPausaActiva(tenant):
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        PAUSAACTIVATIEMPOCONDUCCION     = obtenerValorPausaActivaTiempoConduccion(db)
        PAUSAACTIVATIEMPOPAUSAACTIVA    = obtenerValorPausaActivaTiempoPausaActiva(db)
        PAUSAACTIVATIEMPOTOLERANCIA     = obtenerValorPausaActivaTiempoTolerancia(db)
        filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
        for fila in filas:
            key                     = fila.key
            value                   = fila.value
            doc                     = fila.doc
            #Obtiene el identficador de cada vehiculo
            idVehiculo           = doc.get('_id')
            ultimaFechaRevision = obtenerUltimaRevisionPausaActiva(db, idVehiculo)
            procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)
    except ValueError:
        pass



def obtenerDocSeguimientoPausaActiva(db, idVehiculo):
    doc = None    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/seguridadVial/_view/listarSeguimientoPausaActiva',
            key             = [idVehiculo],
            include_docs    = True)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value
            doc                             = fila.doc
        return doc
    except ValueError:
        pass


def actualizarFechaFinDocPausaActiva(db, horaRegistradaPosicion, idPausaActiva, docSeguimientoPausaActiva, fechaHoraReset, idVehiculo):
    #actualizar fechafin
    #actualiza la fecha fin segun el _id del doc pausaActiva
    docPausaActiva = buscarCacheDocumento(db, idPausaActiva)
    docPausaActiva["fechaFin"]  = horaRegistradaPosicion
    actualizarCacheDocumentos(idPausaActiva, docPausaActiva, True)
    # docPausaActiva              = db[idPausaActiva]
    # docPausaActiva["fechaFin"]  = horaRegistradaPosicion
    # db.save(docPausaActiva)
    #asigna infraccion
    #obtiene _id del doc seguimientoPausaActiva segun el idVehiculo ojo
    # idSeguimiento              = docSeguimientoPausaActiva.get('_id')
    # docSeguimientoPausaActiva  =  buscarCacheDocSeguimientoPausaActiva(db, idSeguimiento, idVehiculo)
    # docSeguimientoPausaActiva["fechaHoraResetPausa"]        = horaRegistradaPosicion
    # docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = fechaHoraReset
    # actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, True)
    # idSeguimiento              = docSeguimientoPausaActiva.get('_id')
    # docSeguimientoPausaActiva  = db[idSeguimiento]
    # docSeguimientoPausaActiva["fechaHoraResetPausa"]        = fechaHoraReset
    # docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
    # db.save(docSeguimientoPausaActiva)
    print "actualiza infraccion"


def crearAsignarInfraccion(db, horaRegistradaPosicion, fechaHoraReset, docSeguimientoPausaActiva, idVehiculo):
    #creo doc pausaActiva y el _i generado lo actualizo al docSeguimientoPausaActiva
    fechaHoraUltimoEncendido = docSeguimientoPausaActiva["fechaHoraResetPausa"]
    #fechaHoraUltimoEncendido = docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]
    if db == None:
        return { 'success' : False }
    #crea infraccion
    try: 
        idConductor = consultarIdConductorVehiculo(db, idVehiculo)
        doc_id, doc_rev = db.save({
            "tipoDato"              : "pausaActiva",
            "creadoEn"              : datetime.now().isoformat(),
            "fechaInfraccion"       : horaRegistradaPosicion,  
            "fechaFin"              : horaRegistradaPosicion,
            "conduceDesde"          : fechaHoraUltimoEncendido,
            "idVehiculo"            : idVehiculo,
            "idConductor"           : idConductor,
            "activo"                : True 
        })

        actualizarCacheDocumentos(doc_id, db[doc_id], False)

        #asigna infraccion
        #obtiene _id del doc seguimientoPausaActiva segun el idVehiculo
        idSeguimiento              = docSeguimientoPausaActiva.get('_id')
        docSeguimientoPausaActiva  = buscarCacheDocSeguimientoPausaActiva(db, idSeguimiento, idVehiculo)
        #docSeguimientoPausaActiva["fechaHoraResetPausa"]        = fechaHoraReset
        #docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
        docSeguimientoPausaActiva["idPausaActiva"]              = doc_id
        actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, True)
        # docSeguimientoPausaActiva  = db[idSeguimiento]
        # docSeguimientoPausaActiva["fechaHoraResetPausa"]        = fechaHoraReset
        # docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
        # docSeguimientoPausaActiva["idPausaActiva"]              = doc_id
        # db.save(docSeguimientoPausaActiva)
        print "crea infraccion"
        #sys.exit(1)
    except ValueError:
        pass


def procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA):
    existeIdPausa       = False
    fechaHoraReset      = docSeguimientoPausaActiva.get('fechaHoraResetPausa')
    #fechaHoraReset      = docSeguimientoPausaActiva.get('fechaHoraUltimoEncendido')
    # se busca el tiempo de conduccion en el doc
    tiempoConduccion    = int(PAUSAACTIVATIEMPOCONDUCCION)# horas
    idPausaActiva       = docSeguimientoPausaActiva.get('idPausaActiva')                     
    if not(idPausaActiva == ""):
        existeIdPausa = True    
    horaRegistradaPosicion      = parser.parse(horaRegistradaPosicion)
    fechaHoraReset              = parser.parse(fechaHoraReset)
    diferencia                  = horaRegistradaPosicion - fechaHoraReset
    segundosDiferencias         = diferencia.total_seconds()
    horaRegistradaPosicion      = horaRegistradaPosicion.isoformat()
    fechaHoraReset              = fechaHoraReset.isoformat()
    # cambiar tiempoConduccion horas por tiempoConduccion segundos
    tiempoConduccionSegundos    = tiempoConduccion * 3600
    # cambiar PAUSAACTIVATIEMPOTOLERANCIA  en minutos por tiempoTolerancia segundos
    tiempoToleranciaSegundos                    =   PAUSAACTIVATIEMPOTOLERANCIA * 60
    desfacePermitidoTiempoConduccionSegundos    = abs(tiempoConduccionSegundos) + abs(tiempoToleranciaSegundos)
    if abs(segundosDiferencias) > abs(desfacePermitidoTiempoConduccionSegundos):
        if existeIdPausa:
            #Actualizar la fechaFin
            actualizarFechaFinDocPausaActiva(db, horaRegistradaPosicion, idPausaActiva, docSeguimientoPausaActiva, fechaHoraReset, idVehiculo) 
        else:
            #print "CREAR Y ASIGNAR INFRACCION"
            #crear y asignar infraccion
            crearAsignarInfraccion(db, horaRegistradaPosicion, fechaHoraReset, docSeguimientoPausaActiva, idVehiculo)
    # else:
    #     #actualizo ultimo encendido
    #     #asigna infraccion
    #     #obtiene _id del doc seguimientoPausaActiva segun el idVehiculo
    #     idSeguimiento              = docSeguimientoPausaActiva.get('_id')
    #     docSeguimientoPausaActiva     = buscarCacheDocSeguimientoPausaActiva(db, idSeguimiento, idVehiculo)
    #     docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]  = horaRegistradaPosicion
    #     actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, True)


        # idSeguimiento              = docSeguimientoPausaActiva.get('_id')
        # docSeguimientoPausaActiva  = db[idSeguimiento]
        # docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
        # db.save(docSeguimientoPausaActiva)



def actualizarFechaHoraReset(db, horaRegistradaPosicion, idseguimientoPausaActiva, idVehiculo):
    #actualiza el doc seguimientoPausaActiva la fechaHoraResetPausa
    docSeguimientoPausaActiva = buscarCacheDocSeguimientoPausaActiva(db, idseguimientoPausaActiva, idVehiculo)
    docSeguimientoPausaActiva["fechaHoraResetPausa"]    = horaRegistradaPosicion
    docSeguimientoPausaActiva["idPausaActiva"]          = ""
    actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, True)


    # docSeguimientoPausaActiva  = db[idseguimientoPausaActiva]
    # docSeguimientoPausaActiva["fechaHoraResetPausa"]    = horaRegistradaPosicion
    # docSeguimientoPausaActiva["idPausaActiva"]          = ""
    # db.save(docSeguimientoPausaActiva)


def procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA):
    # print "hora registaradaklll--------------"
    # print horaRegistradaPosicion
    tiempoPausaActiva           = int(PAUSAACTIVATIEMPOPAUSAACTIVA)
    fechaHoraUltimoEncendido    = docSeguimientoPausaActiva.get('fechaHoraUltimoEncendido')
    if not(fechaHoraUltimoEncendido == ""):
        print "{}----{}".format("Fecha hora ultimo encendido-----------",fechaHoraUltimoEncendido)
        fechaHoraUltimoEncendido    = parser.parse(fechaHoraUltimoEncendido)
        horaRegistradaPosicion      = parser.parse(horaRegistradaPosicion)
        diferencia                  = horaRegistradaPosicion - fechaHoraUltimoEncendido
        segundosDiferencias         = diferencia.total_seconds()
        horaRegistradaPosicion      = horaRegistradaPosicion.isoformat()
        fechaHoraUltimoEncendido    = fechaHoraUltimoEncendido.isoformat()
        # cambiar tiempoPausaActiva en minutos a tiempoPausaActivaSegundos
        tiempoPausaActivaSegundos   = tiempoPausaActiva * 60
        if segundosDiferencias >= tiempoPausaActivaSegundos:
            #Actualizar fechaHoraReset y asignar idPausaActiva = ""
            idSeguimientoPausaActiva = docSeguimientoPausaActiva.get('_id')   
            idPausaActiva       = docSeguimientoPausaActiva.get('idPausaActiva')
            actualizarFechaHoraReset(db, horaRegistradaPosicion, idSeguimientoPausaActiva, idVehiculo)
            docPausaActiva      = buscarCacheDocumento(db, idPausaActiva)
            # docPausaActiva["fechaFin"]  = horaRegistradaPosicion
            # actualizarCacheDocumentos(idPausaActiva, docPausaActiva, True)
            #actualiza la fecha fin segun el _id del doc pausaActiva
            # docPausaActiva              = db[idPausaActiva]
            # #docPausaActiva["fechaHoraUltimoEncendido"]  = fechaHoraUltimoEncendido #ojo
            # docPausaActiva["fechaFin"]  = horaRegistradaPosicion
            # db.save(docPausaActiva)
            #sys.exit(1)



def actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion):
    #actualiza el doc fechasRevision con la fecha actual
    docFechasRevision                           = db[idDocUltimaRevision]
    docFechasRevision["fechaHoraRegistrada"]    = horaRegistradaPosicion
    db.save(docFechasRevision)


#-------------------------------------Inicio funcion original-----------------------------------

def procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA):
    print "**********************************"
    print idVehiculo
    print "**********************************"
    horaRegistradaPosicion          = None
    actualizoFechaHoraRegistrada    = False
    docSeguimientoPausaActiva       = None
    existenPuntosRestantes          = True
    if ultimaFechaRevision["idDocUltimaRevision"] == "":
        # se revisa el vehiculo por primera vez el encendido y apagado y se guarda el documento
        ultimaRevision = "0"
        #guarda por primera vez el documento de revision con la fecha actual
        idDocUltimaRevision = guardarDocRevisionVehiculo(db, idVehiculo)
    else:
        idDocUltimaRevision = ultimaFechaRevision["idDocUltimaRevision"]
        ultimaRevision      = ultimaFechaRevision["fechaHoraRegistrada"]
        actualizoFechaHoraRegistrada = True
        docSeguimientoPausaActiva       = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
        actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, False)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        idSeguimiento = ""
        # docSeguimientoPausaActiva       = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
        while existenPuntosRestantes:
            if idVehiculo in datosEventosVehiculoTemp:
                for doc in datosEventosVehiculoTemp[idVehiculo]:
                    existenPuntosRestantes          = True
                    actualizoFechaHoraRegistrada    = True
                    estaEncendidoMotor              = doc.get('estaEncendidoMotor', False)
                    idDocPosicion                   = doc.get('_id')
                    horaRegistradaPosicion          = doc.get('horaRegistrada')
                    ultimaRevision              = horaRegistradaPosicion                
                    #Inicio encendido motor puntos antiguos prueba
                    velocidad = doc.get('velocidad', 0)
                    if velocidad < 1:
                        estaEncendidoMotor = False
                    else:
                        estaEncendidoMotor = True
                    #Inicio encendido motor puntos antiguos prueba
                    if docSeguimientoPausaActiva == None:
                        idSeguimiento = guardarDocSeguimientoPausaActiva(db, horaRegistradaPosicion, idVehiculo, estaEncendidoMotor)
                        docSeguimientoPausaActiva   = buscarCacheDocSeguimientoPausaActiva(db, idSeguimiento, idVehiculo)
                        #ya esta registrado un seguimientoPausaActiva entonces se valida el algoritmo decision 
                        #si esta encendido o apagado
                        if estaEncendidoMotor:
                            #valida el algoritmo cuando el vehiculo esta encendido
                            procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA)
                        else:
                            #valida el algoritmo cuando el vehiculo esta apagado
                            #if not(docSeguimientoPausaActiva.get("idPausaActiva")) == "":
                            procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)
                    else:
                        docSeguimientoPausaActiva   = buscarCacheDocSeguimientoPausaActiva(db, idSeguimiento, idVehiculo)
                        #ya esta registrado un seguimientoPausaActiva entonces se valida el algoritmo decision 
                        #si esta encendido o apagado
                        if estaEncendidoMotor:
                            #valida el algoritmo cuando el vehiculo esta encendido
                            procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA)
                        else:
                            #valida el algoritmo cuando el vehiculo esta apagado
                            #if not(docSeguimientoPausaActiva.get("idPausaActiva")) == "":
                            procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)
                #-----------------------------
                if actualizoFechaHoraRegistrada:
                    if not(horaRegistradaPosicion == None):
                        actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion)
                        guardarCacheDocSeguimientoPausaActivaDB(db)
                        guardarCacheDocumentosBD(db)
                    actualizoFechaHoraRegistrada = False
                sys.exit(1)
                existenPuntosRestantes = False
            else: #pruebas
                existenPuntosRestantes = False
                sys.exit(1)
    except ValueError:
        pass

#-------------------------------------Fin funcion original-----------------------------------


def guardarCacheDocSeguimientoPausaActivaDB(db):
    global cacheDocSeguimientoPausaActiva
    #guarda los caches cacheDocSeguimientoConduccionContinua
    for key, value in cacheDocSeguimientoPausaActiva.iteritems():
        if value["actualizar"]:
            db.save(value["doc"])
            identificador = value["doc"]["_id"]
            value["doc"] = db[identificador]
    cacheDocSeguimientoPausaActiva = {}


def guardarCacheDocumentosBD(db):
    global cacheDocumentos
    #print len(cacheDocumentos.keys())            
    #guarda los caches documentos
    for key, value in cacheDocumentos.iteritems():
        if value["actualizar"]:          
            db.save(value["doc"])
            identificador = value["doc"]["_id"]
            value["doc"] = db[identificador]
    cacheDocumentos = {}


def actualizarCacheDocSeguimientoPausaActiva(idVehiculo, doc, actualiza):
    # print doc
    cacheDocSeguimientoPausaActiva[idVehiculo] = {
        "doc"           : doc,
        "actualizar"    : actualiza
    }

def buscarCacheDocSeguimientoPausaActiva(db, idDoc, idVehiculo):
    if idVehiculo in cacheDocSeguimientoPausaActiva:
        doc = cacheDocSeguimientoPausaActiva[idVehiculo]["doc"]
    else:
        doc = db[idDoc]
        actualizarCacheDocSeguimientoPausaActiva(idVehiculo, doc, False)    
    return doc



def guardarDocSeguimientoPausaActiva(db, horaRegistradaPosicion, idVehiculo, estaEncendidoMotor):
    #Guarda el doc seguimientoPausaActiva
    #si en el punto estaEncendidoMotor entonces en el doc seguimientoPausaActiva 
    #se guarda la horaRegistradaPosicion
    if estaEncendidoMotor:
        fechaHoraUltimoEncendido = horaRegistradaPosicion
    else:
        fechaHoraUltimoEncendido = "1991-09-09T10:13:36.540564"
    #guarda la fechasRevision de la pausaActiva
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"                  : "seguimientoPausaActiva",    
            "fechaHoraResetPausa"       : horaRegistradaPosicion,
            "fechaHoraUltimoEncendido"  : fechaHoraUltimoEncendido,
            "idVehiculo"                : idVehiculo,
            "idPausaActiva"             : "",
            "activo"                    : True
        })
        return doc_id
    except ValueError:
        pass


def guardarDocRevisionVehiculo(db, idVehiculo):
    #guarda la fechasRevision de la pausaActiva
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"              : "fechasRevision",
            "tipoRevision"          : "pausaActiva",
            "fechaHoraRegistrada"   : "",  
            "idVehiculo"            : idVehiculo,
            "activo"                : True 
        })
        return doc_id
    except ValueError:
        pass

 
def buscarTenants():
    #funcion que busca los tenants en la bd fleetbi
    dbFleet = conexion.getConexionFleet()
    listaTenants = []
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view('_design/tenant/_view/visualizarTenants',
                    include_docs  = True)
        for fila in filas:
            key                     = fila.key
            value                   = fila.value
            doc                     = fila.doc
            urlTenant               = doc.get('urlTenant')      
            listaTenants.append(urlTenant)
        return listaTenants
    except ValueError:
        pass



def obtenerValorPausaActivaTiempoConduccion(db):  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["PAUSAACTIVATIEMPOCONDUCCION"],
            limit = 1,
            include_docs    = False)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value   
        return value
    except ValueError:
        pass



def obtenerValorPausaActivaTiempoPausaActiva(db):  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["PAUSAACTIVATIEMPOPAUSAACTIVA"],
            limit           = 1,
            include_docs    = False)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value   
        return value
    except ValueError:
        pass


def obtenerValorPausaActivaTiempoTolerancia(db):  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["PAUSAACTIVATIEMPOTOLERANCIA"],
            limit           = 1,
            include_docs    = False)
        for fila in filas:
            key   = fila.key
            value = fila.value   
        return value
    except ValueError:
        pass



def consultarIdConductorVehiculo(db, idVehiculo):
    idConductor = ""  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/detalleVehiculo/_view/detalleVehiculo',
            startkey             = [idVehiculo, 0],
            endkey               = [idVehiculo, {}],   
            limit           = 1,
            include_docs    = True)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            idConductor  = doc.get('conductor')                          
        return idConductor
    except ValueError:
        pass


def actualizarCacheDocumentos(idDoc, doc, actualiza):
    cacheDocumentos[idDoc] = {
        "doc"           : doc,
        "actualizar"    : actualiza
        }


def buscarCacheDocumento(db, idDoc):
    if idDoc in cacheDocumentos:
        doc = cacheDocumentos[idDoc]["doc"]
    else:
        doc = db[idDoc]
        actualizarCacheDocumentos(idDoc, doc, False)
    return doc


