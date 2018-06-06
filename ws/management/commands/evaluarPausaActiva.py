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
cacheDocSeguimientoPausaActiva = {}
rutaArchivoJournal      = settings.RUTA_CARPETA_PAUSA_ACTIVA+'dataJournal'
rutaArchivoJournalCopia = settings.RUTA_CARPETA_PAUSA_ACTIVA+'dataJournalCopia' 
# rutaArchivoJournal      = '/home/eduardo/Escritorio/dataJournalPausaActiva/dataJournal'
# rutaArchivoJournalCopia = '/home/eduardo/Escritorio/dataJournalPausaActiva/dataJournalCopia' 

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        tenants = buscarTenants()
        for tenant in tenants:
            cacheDocumentos = {}
            cacheDocSeguimientoPausaActiva = {}
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
            procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA, tenant)
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
    print "actualiza infraccion"


def crearAsignarInfraccion(db, horaRegistradaPosicion, fechaHoraReset, docSeguimientoPausaActiva, idVehiculo):
    #creo doc pausaActiva y el _i generado lo actualizo al docSeguimientoPausaActiva
    fechaHoraUltimoEncendido = docSeguimientoPausaActiva["fechaHoraResetPausa"]
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
        # asigna infraccion
        # obtiene _id del doc seguimientoPausaActiva segun el idVehiculo
        idSeguimiento              = docSeguimientoPausaActiva.get('_id')
        docSeguimientoPausaActiva  = buscarCacheDocSeguimientoPausaActiva(db, idSeguimiento, idVehiculo)
        docSeguimientoPausaActiva["idPausaActiva"]              = doc_id
        actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, True)
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



def actualizarFechaHoraReset(db, horaRegistradaPosicion, idseguimientoPausaActiva, idVehiculo):
    #actualiza el doc seguimientoPausaActiva la fechaHoraResetPausa
    docSeguimientoPausaActiva = buscarCacheDocSeguimientoPausaActiva(db, idseguimientoPausaActiva, idVehiculo)
    docSeguimientoPausaActiva["fechaHoraResetPausa"]    = horaRegistradaPosicion
    docSeguimientoPausaActiva["idPausaActiva"]          = ""
    actualizarCacheDocSeguimientoPausaActiva(idVehiculo, docSeguimientoPausaActiva, True)


def procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA):
    tiempoPausaActiva           = int(PAUSAACTIVATIEMPOPAUSAACTIVA)
    fechaHoraUltimoEncendido    = docSeguimientoPausaActiva.get('fechaHoraUltimoEncendido')
    if not(fechaHoraUltimoEncendido == ""):
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
            #idPausaActiva       = docSeguimientoPausaActiva.get('idPausaActiva')
            actualizarFechaHoraReset(db, horaRegistradaPosicion, idSeguimientoPausaActiva, idVehiculo)
            #docPausaActiva      = buscarCacheDocumento(db, idPausaActiva)
            #sys.exit(1)



def actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion):
    #actualiza el doc fechasRevision con la fecha actual
    docFechasRevision                           = db[idDocUltimaRevision]
    docFechasRevision["fechaHoraRegistrada"]    = horaRegistradaPosicion
    db.save(docFechasRevision)


#-------------------------------------Inicio funcion original-----------------------------------
def procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA, tenant):
    print "**********************************"
    print idVehiculo
    print "**********************************"
    horaRegistradaPosicion          = None
    actualizoFechaHoraRegistrada    = False
    docSeguimientoPausaActiva       = None
    existenPuntosRestantes          = True
    if ultimaFechaRevision["idDocUltimaRevision"] == "":
        # se revisa el vehiculo por primera vez el encendido y apagado y se guarda el documento
        ultimaRevision = "0" #DESCOMENTAR
        #ultimaRevision  ="2017-11-20T06:17:38"
        #guarda por primera vez el documento de revision con la fecha actual
        idDocUltimaRevision = guardarDocRevisionVehiculo(db, idVehiculo)
    else:
        idDocUltimaRevision = ultimaFechaRevision["idDocUltimaRevision"]
        ultimaRevision      = ultimaFechaRevision["fechaHoraRegistrada"] #DESCOMENTAR
        # Tener en cuenta que se estan haciendo consultas de a 1000
        if ultimaRevision == "":
            # no se ha registrado ultima revision ojo cambiar por el journal busco en el journal ojo 
            # y obtengo los datos del journal para guardarlos en las caches
            # ultimaRevision                  = obtenerFechaInfraccionPausaActivaPorVehiculo(db, idVehiculo)#cambiar con el journal
            consultaDataJournal             = obtenerValoresDataJournal(idVehiculo)
            ultimaRevision                  = consultaDataJournal["ultimaFechaRevisada"]
            cacheDocumentos                 = consultaDataJournal["cacheDocumentos"]
            cacheDocSeguimientoPausaActiva  = consultaDataJournal["cacheDocSeguimientoPausaActiva"]
            actualizarCacheDocumentos(idVehiculo, cacheDocumentos , False)
            actualizarCacheDocSeguimientoPausaActiva(idVehiculo,cacheDocSeguimientoPausaActiva[idVehiculo]["doc"],False)
            docSeguimientoPausaActiva       = cacheDocSeguimientoPausaActiva[idVehiculo]["doc"]
        else:
            docSeguimientoPausaActiva       = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
            actualizarCacheDocSeguimientoPausaActiva(idVehiculo,docSeguimientoPausaActiva,False)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        idSeguimiento = ""
        #docSeguimientoPausaActiva       = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
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
                #existenPuntosRestantes          = True
                actualizoFechaHoraRegistrada    = True
                key                             = fila.key
                value                           = fila.value
                doc                             = fila.doc
                estaEncendidoMotor              = doc.get('estaEncendidoMotor', False)
                idDocPosicion                   = doc.get('_id')
                horaRegistradaPosicion          = doc.get('horaRegistrada')
                ultimaRevision                  = horaRegistradaPosicion                
                print horaRegistradaPosicion
                #Inicio encendido motor puntos antiguos prueba
                velocidad = doc.get('velocidad', 0.0)
                if velocidad < 1:
                    estaEncendidoMotor = False
                else:
                    estaEncendidoMotor = True
                #Inicio encendido motor puntos antiguos prueba
                #print estaEncendidoMotor
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
                        procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)
                #guarda en el journal la fecha hora registrada y los datos que lleva hasta el momento
                guardarDataJournal(db, idVehiculo, horaRegistradaPosicion, tenant)
            #-----------------------------
        #Actualiza la revision del vehiculo del tenant
        if actualizoFechaHoraRegistrada:
            if horaRegistradaPosicion != None:
                actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion)
                guardarCacheDocSeguimientoPausaActivaDB(db)
                guardarCacheDocumentosBD(db)
                #borra dataJournal
                #borrarDataJournal(idVehiculo)
            actualizoFechaHoraRegistrada = False
        #existenPuntosRestantes = False
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


def obtenerFechaInfraccionPausaActivaPorVehiculo(db, idVehiculo):
    #obtiene la fecha de la infraccion de la pausa activa
    fechaInfraccion = "0"
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/seguridadVial/_view/listarPausaActivaPorVehiculo',
            startkey             = [idVehiculo, {}],
            endkey               = [idVehiculo, 0],   
            limit           = 1,
            descending    = True,
            include_docs    = True)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            fechaInfraccion  = doc.get('fechaInfraccion', "0")                          
        return fechaInfraccion
    except ValueError:
        pass



def guardarDataJournal(db, idVehiculo, horaRegistradaPosicion, tenant):
    global cacheDocumentos
    global cacheDocSeguimientoPausaActiva
    global rutaArchivoJournal
    global rutaArchivoJournalCopia
    dataJournal = {
        idVehiculo : {
            'ultimaFechaRevisada'               :  horaRegistradaPosicion,
            'tenant'                            :  tenant,
            'cacheDocumentos'                   :  cacheDocumentos,
            'cacheDocSeguimientoPausaActiva'    :  cacheDocSeguimientoPausaActiva
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
            'cacheDocSeguimientoPausaActiva'    :  ''
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
