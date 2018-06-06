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
import json
import sys
from shutil import copyfile
from django.conf              import settings


cacheDocumentos = {} #diccionario que almacenara en cache los documentos para guardarlos posteriormente
cacheDocSeguimientoConduccionContinua = {}
rutaArchivoJournal      = settings.RUTA_CARPETA_CONDUCCION_CONTINUA+'dataJournal'
rutaArchivoJournalCopia = settings.RUTA_CARPETA_CONDUCCION_CONTINUA+'dataJournalCopia' 

# cacheDocumentos[idConduccionContinua] = {
#     "doc"           : DOCOBJETO.
#     "actualizar"    : False # PARA QUE NO GUARDE EN LA BD SOLO BUSCAR
# }

 
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        tenants = buscarTenants()
        for tenant in tenants:
            cacheDocumentos = {}
            cacheDocSeguimientoConduccionContinua = {}
            print "==================================="
            print tenant
            #por cada tenant se procesara la informacion
            procesarEvaluacionConduccionContinua(tenant)


def procesarEvaluacionConduccionContinua(tenant):
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        CONDUCCIONCONTINUATIEMPOMAXCONDUCCION  = obtenerValorConduccionContinuaTiempoMaxConduccion(db)
        CONDUCCIONCONTINUATIEMPONOCONDUCCION   = obtenerValorConduccionContinuaTiempoNoConduccion(db)
        CONDUCCIONCONTINUATIEMPOTOLERANCIA     = obtenerValorConduccionContinuaTiempoTolerancia(db)
        filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
        for fila in filas:
            key                     = fila.key
            value                   = fila.value
            doc                     = fila.doc
            #Obtiene el identficador de cada vehiculo
            idVehiculo           = doc.get('_id')
            ultimaFechaRevision = obtenerUltimaRevisionConduccionContinua(db, idVehiculo)
            procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, CONDUCCIONCONTINUATIEMPOMAXCONDUCCION, CONDUCCIONCONTINUATIEMPONOCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA, tenant)
    except ValueError:
        pass


def procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, CONDUCCIONCONTINUATIEMPOMAXCONDUCCION, CONDUCCIONCONTINUATIEMPONOCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA, tenant):
    print "**********************************"
    print idVehiculo
    print "**********************************"
    horaRegistradaPosicion          	= None
    actualizoFechaHoraRegistrada    	= False
    docSeguimientoConduccionContinua  	= None
    existenPuntosRestantes              = True
    if ultimaFechaRevision["idDocUltimaRevision"] == "":
        # se revisa el vehiculo por primera vez el encendido y apagado y se guarda el documento
        ultimaRevision = "0"
        #guarda por primera vez el documento de revision con la fecha actual
        idDocUltimaRevision = guardarDocRevisionVehiculo(db, idVehiculo)
    else:
        idDocUltimaRevision = ultimaFechaRevision["idDocUltimaRevision"]
        ultimaRevision      = ultimaFechaRevision["fechaHoraRegistrada"]
        if ultimaRevision == "":
            consultaDataJournal                     = obtenerValoresDataJournal(idVehiculo)
            ultimaRevision                          = consultaDataJournal["ultimaFechaRevisada"]
            cacheDocumentos                         = consultaDataJournal["cacheDocumentos"]
            cacheDocSeguimientoConduccionContinua   = consultaDataJournal["cacheDocSeguimientoConduccionContinua"]
            actualizarCacheDocumentos(idVehiculo, cacheDocumentos , False)
            actualizarCacheDocSeguimientoConduccionContinua(idVehiculo,cacheDocSeguimientoConduccionContinua[idVehiculo]["doc"],False)
            docSeguimientoConduccionContinua        = cacheDocSeguimientoConduccionContinua[idVehiculo]["doc"]
        else:
            docSeguimientoConduccionContinua       = obtenerDocSeguimientoConduccionContinua(db, idVehiculo)
            actualizarCacheDocSeguimientoConduccionContinua(idVehiculo,docSeguimientoConduccionContinua,False)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        idSeguimiento = ""
        #docSeguimientoConduccionContinua   = obtenerDocSeguimientoConduccionContinua(db, idVehiculo)
        contadorIteracion = 2000
        while contadorIteracion == 2000:
            contadorIteracion = 0
            filas = db.view('_design/posicionVehiculos/_view/posicionFechaCreacion',
                startkey             = [idVehiculo, ultimaRevision+"Z"],
                endkey               = [idVehiculo, {}],  
                include_docs    = True,
                limit = 2000
                )
            #existenPuntosRestantes = False
            for fila in filas:
                contadorIteracion        += 1
                #existenPuntosRestantes       = True
                actualizoFechaHoraRegistrada = True
                key                         = fila.key
                value                       = fila.value
                doc                         = fila.doc
                estaEncendidoMotor          = doc.get('estaEncendidoMotor', False)
                idDocPosicion               = doc.get('_id')
                horaRegistradaPosicion      = doc.get('horaRegistrada')
                ultimaRevision              = horaRegistradaPosicion
                print horaRegistradaPosicion
                #Inicio encendido motor puntos antiguos prueba
                velocidad = doc.get('velocidad', 0.0)
                if velocidad < 1:
                    estaEncendidoMotor = False
                else:
                    estaEncendidoMotor = True
                #Inicio encendido motor puntos antiguos prueba
                #print estaEncendidoMotor
                if docSeguimientoConduccionContinua == None:
                    idSeguimiento = guardarDocSeguimientoConduccionContinua(db, horaRegistradaPosicion, idVehiculo, estaEncendidoMotor)
                    docSeguimientoConduccionContinua = buscarCacheDocSeguimientoConduccionContinua(db, idSeguimiento, idVehiculo)
                    #docSeguimientoConduccionContinua   = obtenerDocSeguimientoConduccionContinua(db, idVehiculo)
                    #ya esta registrado un seguimientoConduccionContinua entonces se valida el algoritmo decision 
                    #si esta encendido o apagado
                    if estaEncendidoMotor:
                        #valida el algoritmo cuando el vehiculo esta encendido
                        procesarConduccionContinuaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoConduccionContinua, idVehiculo, CONDUCCIONCONTINUATIEMPOMAXCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA)
                    else:
                        #valida el algoritmo cuando el vehiculo esta apagado
                        procesarConduccionContinuaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoConduccionContinua, idVehiculo, CONDUCCIONCONTINUATIEMPONOCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA)
                else:
                    docSeguimientoConduccionContinua = buscarCacheDocSeguimientoConduccionContinua(db, idSeguimiento, idVehiculo)
                    #ya esta registrado un seguimientoConduccionContinua entonces se valida el algoritmo decision 
                    #si esta encendido o apagado
                    if estaEncendidoMotor:
                        #valida el algoritmo cuando el vehiculo esta encendido
                        procesarConduccionContinuaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoConduccionContinua, idVehiculo, CONDUCCIONCONTINUATIEMPOMAXCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA)
                    else:
                        #valida el algoritmo cuando el vehiculo esta apagado
                        procesarConduccionContinuaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoConduccionContinua, idVehiculo, CONDUCCIONCONTINUATIEMPONOCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA)
                #guarda en el journal la fecha hora registrada y los datos que lleva hasta el momento
                guardarDataJournal(db, idVehiculo, horaRegistradaPosicion, tenant)
                #-----------------------------
        if actualizoFechaHoraRegistrada:
            if horaRegistradaPosicion != None:
                actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion)  
                guardarCacheDocSeguimientoConduccionContinuaDB(db)
                guardarCacheDocumentosBD(db)
            actualizoFechaHoraRegistrada = False
    except ValueError:
        pass


#-------------------------------------Fin funcion original---------------------------------------

def actualizarCacheDocSeguimientoConduccionContinua(idVehiculo, doc, actualiza):
    cacheDocSeguimientoConduccionContinua[idVehiculo] = {
        "doc"           : doc,
        "actualizar"    : actualiza
    }

def buscarCacheDocSeguimientoConduccionContinua(db, idDoc, idVehiculo):
    if idVehiculo in cacheDocSeguimientoConduccionContinua:
        doc = cacheDocSeguimientoConduccionContinua[idVehiculo]["doc"]
    else:
        doc = db[idDoc]
        actualizarCacheDocSeguimientoConduccionContinua(idVehiculo, doc, False)    
    return doc


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


def guardarCacheDocumentosBD(db):
    global cacheDocumentos          
    #guarda los caches documentos
    for key, value in cacheDocumentos.iteritems():
        if value["actualizar"]:
            db.save(value["doc"])
            identificador = value["doc"]["_id"]
            value["doc"] = db[identificador]
    cacheDocumentos = {}

def guardarCacheDocSeguimientoConduccionContinuaDB(db):
    global cacheDocSeguimientoConduccionContinua
    #guarda los caches cacheDocSeguimientoConduccionContinua
    for key, value in cacheDocSeguimientoConduccionContinua.iteritems():
        if value["actualizar"]:
            db.save(value["doc"])
            identificador = value["doc"]["_id"]
            value["doc"] = db[identificador]
    cacheDocSeguimientoConduccionContinua = {}


def procesarConduccionContinuaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoConduccionContinua, idVehiculo, CONDUCCIONCONTINUATIEMPONOCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA):
    tiempoNoConduccion              = int(CONDUCCIONCONTINUATIEMPONOCONDUCCION)
    fechaHoraUltimoEncendido        = docSeguimientoConduccionContinua.get('fechaHoraUltimoEncendido')
    if not(fechaHoraUltimoEncendido == ""):
        fechaHoraUltimoEncendido    = parser.parse(fechaHoraUltimoEncendido )
        horaRegistradaPosicion      = parser.parse(horaRegistradaPosicion)
        diferencia                  = horaRegistradaPosicion - fechaHoraUltimoEncendido
        segundosDiferencias         = diferencia.total_seconds()
        horaRegistradaPosicion      = horaRegistradaPosicion.isoformat()
        fechaHoraUltimoEncendido    = fechaHoraUltimoEncendido.isoformat()
        # cambiar tiempoNoConduccion en horas a tiempoNoConduccionSegundos
        tiempoNoConduccionContinuaHoras  = tiempoNoConduccion * 3600
        if segundosDiferencias >= tiempoNoConduccionContinuaHoras:
            #Actualizar fechaHoraReset y asignar idConduccionContinua = ""
            idSeguimientoConduccionContinua = docSeguimientoConduccionContinua.get('_id')
            actualizarFechaHoraReset(db, horaRegistradaPosicion, idSeguimientoConduccionContinua, idVehiculo)


def actualizarFechaHoraReset(db, horaRegistradaPosicion, idSeguimientoConduccionContinua, idVehiculo):
    #actualiza el doc seguimientoConduccionContinua la fechaHoraResetPausa
    #docSeguimientoConduccionContinua = buscarCacheDocumento(db, idSeguimientoConduccionContinua)
    docSeguimientoConduccionContinua = buscarCacheDocSeguimientoConduccionContinua(db, idSeguimientoConduccionContinua, idVehiculo)
    docSeguimientoConduccionContinua["fechaHoraResetPausa"]    = horaRegistradaPosicion
    docSeguimientoConduccionContinua["idConduccionContinua"]   = ""
    actualizarCacheDocSeguimientoConduccionContinua(idVehiculo, docSeguimientoConduccionContinua, True)

def procesarConduccionContinuaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoConduccionContinua, idVehiculo, CONDUCCIONCONTINUATIEMPOMAXCONDUCCION, CONDUCCIONCONTINUATIEMPOTOLERANCIA):
    existeIdConduccion       = False
    fechaHoraReset      = docSeguimientoConduccionContinua.get('fechaHoraResetPausa')
    # se busca el tiempo de conduccion en el doc
    tiempoConduccion    = int(CONDUCCIONCONTINUATIEMPOMAXCONDUCCION)# horas
    idConduccionContinua       = docSeguimientoConduccionContinua.get('idConduccionContinua')
    if not(idConduccionContinua == ""):
        existeIdConduccion = True    
    horaRegistradaPosicion      = parser.parse(horaRegistradaPosicion)
    fechaHoraReset              = parser.parse(fechaHoraReset)
    diferencia                  = horaRegistradaPosicion - fechaHoraReset
    segundosDiferencias         = diferencia.total_seconds()
    horaRegistradaPosicion      = horaRegistradaPosicion.isoformat()
    fechaHoraReset              = fechaHoraReset.isoformat()
    # cambiar tiempoConduccion horas por tiempoConduccion segundos
    tiempoConduccionSegundos    = tiempoConduccion * 3600
    # cambiar CONDUCCIONCONTINUATIEMPOTOLERANCIA  en minutos por tiempoTolerancia segundos
    tiempoToleranciaSegundos                    =   CONDUCCIONCONTINUATIEMPOTOLERANCIA * 60
    desfacePermitidoTiempoConduccionSegundos    = abs(tiempoConduccionSegundos) + abs(tiempoToleranciaSegundos)
    if abs(segundosDiferencias) > abs(desfacePermitidoTiempoConduccionSegundos):
        if existeIdConduccion:
            #Actualizar la fechaFin
            actualizarFechaFinDocConduccionContinua(db, horaRegistradaPosicion, idConduccionContinua, docSeguimientoConduccionContinua, fechaHoraReset, idVehiculo) 
        else:
            #print "CREAR Y ASIGNAR INFRACCION"
            #crear y asignar infraccion
            crearAsignarInfraccion(db, horaRegistradaPosicion, fechaHoraReset, docSeguimientoConduccionContinua, idVehiculo)


def crearAsignarInfraccion(db, horaRegistradaPosicion, fechaHoraReset, docSeguimientoConduccionContinua, idVehiculo):
    #creo doc conduccionContinua y el _i generado lo actualizo al docSeguimientoConduccionContinua
    fechaHoraUltimoEncendido = docSeguimientoConduccionContinua["fechaHoraResetPausa"]
    if db == None:
        return { 'success' : False }
    #crea infraccion
    try: 
        idConductor = consultarIdConductorVehiculo(db, idVehiculo)
        doc_id, doc_rev = db.save({
            "tipoDato"              : "conduccionContinua",
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
        #obtiene _id del doc seguimientoConduccionContinua segun el idVehiculo
        idSeguimiento                       = docSeguimientoConduccionContinua.get('_id')
        docSeguimientoConduccionContinua    = buscarCacheDocSeguimientoConduccionContinua(db, idSeguimiento, idVehiculo)
        docSeguimientoConduccionContinua["idConduccionContinua"]       = doc_id
        actualizarCacheDocSeguimientoConduccionContinua(idVehiculo, docSeguimientoConduccionContinua, True)
        print "crea infraccion"
    except ValueError:
        pass


def actualizarFechaFinDocConduccionContinua(db, horaRegistradaPosicion, idConduccionContinua, docSeguimientoConduccionContinua, fechaHoraReset, idVehiculo):
    #actualizar fechafin
    #actualiza la fecha fin segun el _id del doc conduccionContinua
    docConduccionContinua = buscarCacheDocumento(db, idConduccionContinua)
    docConduccionContinua["fechaFin"]  = horaRegistradaPosicion
    actualizarCacheDocumentos(idConduccionContinua, docConduccionContinua, True)
    print "Crea infraccion"


def obtenerDocSeguimientoConduccionContinua(db, idVehiculo):
    doc = None    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/seguridadVial/_view/listarSeguimientoConduccionContinua',
            key             = [idVehiculo],
            include_docs    = True)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value
            doc                             = fila.doc
        return doc
    except ValueError:
        pass


def guardarDocSeguimientoConduccionContinua(db, horaRegistradaPosicion, idVehiculo, estaEncendidoMotor):
    #Guarda el doc seguimientoConduccionContinua
    #si en el punto estaEncendidoMotor entonces en el doc seguimientoConduccionContinua 
    #se guarda la horaRegistradaPosicion
    if estaEncendidoMotor:
        fechaHoraUltimoEncendido = horaRegistradaPosicion
    else:
        fechaHoraUltimoEncendido = "1991-09-09T10:13:36.540564"
    #guarda la fechasRevision de la conduccionContinua
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"                  : "seguimientoConduccionContinua",    
            "fechaHoraResetPausa"       : horaRegistradaPosicion,
            "fechaHoraUltimoEncendido"  : fechaHoraUltimoEncendido,
            "idVehiculo"                : idVehiculo,
            "idConduccionContinua"      : "",
            "activo"                    : True
        })
        return doc_id
    except ValueError:
        pass


def guardarDocRevisionVehiculo(db, idVehiculo):
    #guarda la fechasRevision de la conduccionContinua
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"              : "fechasRevision",
            "tipoRevision"          : "conduccionContinua",
            "fechaHoraRegistrada"   : "",  
            "idVehiculo"            : idVehiculo,
            "activo"                : True 
        })
        #actualizarCacheDocumentos(doc_id, db[doc_id], False)
        return doc_id
    except ValueError:
        pass

def actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion):
    #actualiza el doc fechasRevision con la fecha actual
    docFechasRevision                           = db[idDocUltimaRevision]
    docFechasRevision["fechaHoraRegistrada"]    = horaRegistradaPosicion
    db.save(docFechasRevision)


def obtenerUltimaRevisionConduccionContinua(db, idVehiculo):
    ultimaRevision      = {}
    ultimaRevision["fechaHoraRegistrada"]       = ""
    ultimaRevision["idDocUltimaRevision"]       = ""
    #ultimaRevision["revisado"]                  = ""    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/seguridadVial/_view/listarFechasRevision',
            key             = ["conduccionContinua", idVehiculo],
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



def obtenerValorConduccionContinuaTiempoMaxConduccion(db):  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["CONDUCCIONCONTINUATIEMPOMAXCONDUCCION"],
            limit = 1,
            include_docs    = False)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value   
        return value
    except ValueError:
        pass


def obtenerValorConduccionContinuaTiempoNoConduccion(db):  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["CONDUCCIONCONTINUATIEMPONOCONDUCCION"],
            limit           = 1,
            include_docs    = False)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value   
        return value
    except ValueError:
        pass


def obtenerValorConduccionContinuaTiempoTolerancia(db):  
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["CONDUCCIONCONTINUATIEMPOTOLERANCIA"],
            limit           = 1,
            include_docs    = False)
        for fila in filas:
            key   = fila.key
            value = fila.value   
        return value
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


def guardarDataJournal(db, idVehiculo, horaRegistradaPosicion, tenant):
    global cacheDocumentos
    global cacheDocSeguimientoConduccionContinua
    global rutaArchivoJournal
    global rutaArchivoJournalCopia
    dataJournal = {
        idVehiculo : {
            'ultimaFechaRevisada'                       :  horaRegistradaPosicion,
            'tenant'                                    :  tenant,
            'cacheDocumentos'                           :  cacheDocumentos,
            'cacheDocSeguimientoConduccionContinua'     :  cacheDocSeguimientoConduccionContinua
            }
    }
    # Writing JSON data 
    # escribe en un archivo copia
    with open(rutaArchivoJournalCopia+idVehiculo+'.json', 'w') as f:
        json.dump(dataJournal, f)
    # copia el contenido del archivo copia al original
    copyfile(rutaArchivoJournalCopia+idVehiculo+'.json', rutaArchivoJournal+idVehiculo+'.json')

def borrarDataJournal(idVehiculo):
    global rutaArchivoJournal
    dataJournal = {
        "" : {
            'ultimaFechaRevisada'               :  '',
            'cacheDocumentos'                   :  '',
            'cacheDocSeguimientoConduccionContinua'    :  ''
            }
    }
    # Writing JSON data
    with open(rutaArchivoJournal+idVehiculo+'.json', 'w') as f:
        json.dump(dataJournal, f)


def obtenerValoresDataJournal(idVehiculo):
    global rutaArchivoJournal
    # Reading data back
    with open(rutaArchivoJournal+idVehiculo+'.json', 'r') as f:
        data = json.load(f)     
    return data[idVehiculo]  
