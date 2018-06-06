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

cacheDocumentos = {} #diccionario que almacenara en cache los documentos para guardarlos posteriormente

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        tenants = buscarTenants()
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


def actualizarFechaFinDocPausaActiva(db, horaRegistradaPosicion, idPausaActiva, docSeguimientoPausaActiva, fechaHoraReset):
    #actualizar fechafin
    #actualiza la fecha fin segun el _id del doc pausaActiva
    docPausaActiva              = db[idPausaActiva]
    docPausaActiva["fechaFin"]  = horaRegistradaPosicion
    db.save(docPausaActiva)
    #asigna infraccion
    #obtiene _id del doc seguimientoPausaActiva segun el idVehiculo
    idSeguimiento              = docSeguimientoPausaActiva.get('_id')
    docSeguimientoPausaActiva  = db[idSeguimiento]
    docSeguimientoPausaActiva["fechaHoraResetPausa"]        = fechaHoraReset
    docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
    db.save(docSeguimientoPausaActiva)
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
            "fechaFin"              : "",
            "conduceDesde"          : fechaHoraUltimoEncendido,
            "idVehiculo"            : idVehiculo,
            "idConductor"           : idConductor,
            "activo"                : True 
        }) 
        #asigna infraccion
        #obtiene _id del doc seguimientoPausaActiva segun el idVehiculo
        idSeguimiento              = docSeguimientoPausaActiva.get('_id')
        docSeguimientoPausaActiva  = db[idSeguimiento]
        docSeguimientoPausaActiva["fechaHoraResetPausa"]        = fechaHoraReset
        docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
        docSeguimientoPausaActiva["idPausaActiva"]              = doc_id
        db.save(docSeguimientoPausaActiva)
        print "crea infraccion"
    except ValueError:
        pass


def procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA):
    existeIdPausa       = False
    fechaHoraReset      = docSeguimientoPausaActiva.get('fechaHoraResetPausa')
    # se busca el tiempo de conduccion en el doc
    tiempoConduccion    = int(PAUSAACTIVATIEMPOCONDUCCION)# horas
    idPausaActiva       = docSeguimientoPausaActiva.get('idPausaActiva')
    if idPausaActiva != "":
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
            actualizarFechaFinDocPausaActiva(db, horaRegistradaPosicion, idPausaActiva, docSeguimientoPausaActiva, fechaHoraReset) 
        else:
            #print "CREAR Y ASIGNAR INFRACCION"
            #crear y asignar infraccion
            crearAsignarInfraccion(db, horaRegistradaPosicion, fechaHoraReset, docSeguimientoPausaActiva, idVehiculo)
    else:
        #actualizo ultimo encendido
        #asigna infraccion
        #obtiene _id del doc seguimientoPausaActiva segun el idVehiculo
        idSeguimiento              = docSeguimientoPausaActiva.get('_id')
        docSeguimientoPausaActiva  = db[idSeguimiento]
        docSeguimientoPausaActiva["fechaHoraUltimoEncendido"]   = horaRegistradaPosicion
        db.save(docSeguimientoPausaActiva)



def actualizarFechaHoraReset(db, horaRegistradaPosicion, idseguimientoPausaActiva):
    #actualiza el doc seguimientoPausaActiva la fechaHoraResetPausa
    docSeguimientoPausaActiva  = db[idseguimientoPausaActiva]
    docSeguimientoPausaActiva["fechaHoraResetPausa"]    = horaRegistradaPosicion
    docSeguimientoPausaActiva["idPausaActiva"]          = ""
    db.save(docSeguimientoPausaActiva)


def procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA):
    tiempoPausaActiva           = int(PAUSAACTIVATIEMPOPAUSAACTIVA)
    fechaHoraUltimoEncendido    = docSeguimientoPausaActiva.get('fechaHoraUltimoEncendido')
    if fechaHoraUltimoEncendido != "":
        fechaHoraUltimoEncendido    = parser.parse(fechaHoraUltimoEncendido )
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
            actualizarFechaHoraReset(db, horaRegistradaPosicion, idSeguimientoPausaActiva)

            idPausaActiva       = docSeguimientoPausaActiva.get('idPausaActiva')
            #actualiza la fecha fin segun el _id del doc pausaActiva
            docPausaActiva              = db[idPausaActiva]
            docPausaActiva["fechaFin"]  = horaRegistradaPosicion
            db.save(docPausaActiva)




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
    # fechaActual     = datetime.now().isoformat()
    # if ultimaFechaRevision["fechaHoraRegistrada"] == "":
    #     # se revisa el vehiculo por primera vez el encendido y apagado y se guarda el documento
    #     ultimaRevision = fechaActual
    #     #guarda por primera vez el documento de revision con la fecha actual
    #     idDocUltimaRevision = guardarDocRevisionVehiculo(db, idVehiculo, ultimaRevision)
    # else:
    #     idDocUltimaRevision = ultimaFechaRevision["idDocUltimaRevision"]
    #     ultimaRevision      = ultimaFechaRevision["fechaHoraRegistrada"]
    #     actualizoFechaHoraRegistrada = True
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        print "entro 0"
        while existenPuntosRestantes:
            print "entro"
            filas = db.view('_design/posicionVehiculos/_view/posicionFechaCreacion',
                startkey             = [idVehiculo, ultimaRevision+"Z"],
                endkey               = [idVehiculo, {}],  
                include_docs    = True,
                limit = 1000
                )
            print "hola"
            existenPuntosRestantes = False
            for fila in filas:
                existenPuntosRestantes          = True
                actualizoFechaHoraRegistrada    = True
                key                             = fila.key
                value                           = fila.value
                doc                             = fila.doc
                estaEncendidoMotor              = doc.get('estaEncendidoMotor', False)
                idDocPosicion                   = doc.get('_id')
                horaRegistradaPosicion          = doc.get('horaRegistrada')
                ultimaRevision              = horaRegistradaPosicion                
                print horaRegistradaPosicion
                #Inicio encendido motor puntos antiguos prueba
                velocidad = doc.get('velocidad', 0)
                print velocidad
                if velocidad < 1:
                    estaEncendidoMotor = False
                else:
                    estaEncendidoMotor = True
                #Inicio encendido motor puntos antiguos prueba
                print estaEncendidoMotor
                docSeguimientoPausaActiva       = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
                if docSeguimientoPausaActiva == None:
                    guardarDocSeguimientoPausaActiva(db, horaRegistradaPosicion, idVehiculo, estaEncendidoMotor)
                    docSeguimientoPausaActiva   = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
                    #ya esta registrado un seguimientoPausaActiva entonces se valida el algoritmo decision 
                    #si esta encendido o apagado
                    if estaEncendidoMotor:
                        #valida el algoritmo cuando el vehiculo esta encendido
                        procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA)
                    else:
                        #valida el algoritmo cuando el vehiculo esta apagado
                        procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)
                else:
                    #ya esta registrado un seguimientoPausaActiva entonces se valida el algoritmo decision 
                    #si esta encendido o apagado
                    if estaEncendidoMotor:
                        #valida el algoritmo cuando el vehiculo esta encendido
                        procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA)
                    else:
                        #valida el algoritmo cuando el vehiculo esta apagado
                        procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicion, docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)
            #-----------------------------
        if actualizoFechaHoraRegistrada:
            if horaRegistradaPosicion != None:
                actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion)
            actualizoFechaHoraRegistrada = False
    except ValueError:
        pass

#-------------------------------------Fin funcion original-----------------------------------



# #--------------------------funcion prueba----------------------------------


# def procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA):
#     print "**********************************"
#     print idVehiculo
#     print "**********************************"
#     horaRegistradaPosicion          = None
#     actualizoFechaHoraRegistrada    = False
#     docSeguimientoPausaActiva       = None
#     #----------------------------------------------
#     #PRUEBA
#     i = 0
#     # horaRegistradaPosicionPrueba    = ["2017-08-21T17:47:19", "2017-08-21T17:50:19", "2017-08-21T19:47:19", 
#     #  "2017-08-21T20:47:19","2017-08-21T21:47:19", "2017-08-21T22:50:19", "2017-08-21T23:47:19"]
#     # estaEncendidoMotorPrueba        = [False, True, True, False, False, True, True]
#     # horaRegistradaPosicionPrueba    = ["2017-08-21T17:47:19", "2017-08-21T17:50:19", "2017-08-21T19:47:19", 
#     # "2017-08-21T20:47:19","2017-08-21T21:47:19", "2017-08-21T22:50:19", "2017-08-21T23:47:19"]
#     # estaEncendidoMotorPrueba        = [True, True, True, True, True, True, True]
#     # horaRegistradaPosicionPrueba    = ["2017-08-21T17:47:19", "2017-08-21T17:50:19", "2017-08-21T19:47:19", 
#     # "2017-08-21T20:47:19","2017-08-21T21:47:19", "2017-08-21T22:50:19", "2017-08-21T23:47:19"]
#     # estaEncendidoMotorPrueba        = [False, False, False, False, False, False, True]
#     horaRegistradaPosicionPrueba    = ["2017-08-21T17:47:19", "2017-08-21T17:50:19", "2017-08-21T19:47:19", 
#      "2017-08-21T20:47:19","2017-08-21T21:47:19", "2017-08-21T22:50:19", "2017-08-21T23:47:19"]
#     estaEncendidoMotorPrueba        = [True, False, True, False, True, False, True]
#     #----------------------------------------------
#     fechaActual     = datetime.now().isoformat()
#     if ultimaFechaRevision["fechaHoraRegistrada"] == "":
#         # se revisa el vehiculo por primera vez el encendido y apagado y se guarda el documento
#         ultimaRevision = fechaActual
#         #guarda por primera vez el documento de revision con la fecha actual
#         #DESCOMENTAR
#         idDocUltimaRevision = guardarDocRevisionVehiculo(db, idVehiculo, ultimaRevision)
#     else:
#         idDocUltimaRevision = ultimaFechaRevision["idDocUltimaRevision"]
#         ultimaRevision      = ultimaFechaRevision["fechaHoraRegistrada"]
#         actualizoFechaHoraRegistrada = True
#     if db == None:
#         return { 'success' : False, 'mensaje': "existe el bd" }
#     try:
#         filas = db.view('_design/posicionVehiculos/_view/posicionFechaCreacion',
#             startkey             = [idVehiculo, ultimaRevision],
#             endkey               = [idVehiculo, fechaActual],  
#             include_docs    = True
#             )

#         for fila in filas:
#             key                         = fila.key
#             value                       = fila.value
#             doc                         = fila.doc
#             estaEncendidoMotor          = doc.get('estaEncendidoMotor', False)
#             #estaEncendidoMotor          = False
#             idDocPosicion               = doc.get('_id')
#             horaRegistradaPosicion      = doc.get('horaRegistrada')
#             docSeguimientoPausaActiva   = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
#             print horaRegistradaPosicion
#             print estaEncendidoMotor
#             if docSeguimientoPausaActiva == None:
#                 #Guardo por primera vez el documento de seguimientoPausaActiva del vehiculo
#                 #Con la fechaHoraResetPausa = horaRegistradaPosicion
#                 #Prueba
#                 guardarDocSeguimientoPausaActiva(db, horaRegistradaPosicionPrueba[0], idVehiculo, estaEncendidoMotor)
#                 docSeguimientoPausaActiva   = obtenerDocSeguimientoPausaActiva(db, idVehiculo)
#                 if estaEncendidoMotorPrueba[i]:
#                     #valida el algoritmo cuando el vehiculo esta encendido
#                     print "ESTA ENCENDIDO"
#                     print i
#                     #DESCOMENTAR
#                     procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicionPrueba[i], docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA)
#                 else:
#                     print "ESTA APAGADO"
#                     print i
#                     #valida el algoritmo cuando el vehiculo esta apagado
#                     #DESCOMENTAR
#                     procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicionPrueba[i], docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)  
#             else:
#                 # #PRUEBA
#                 #ya esta registrado un seguimientoPausaActiva entonces se valida el algoritmo decision 
#                 #si esta encendido o apagado
#                 print estaEncendidoMotorPrueba[i]
#                 if estaEncendidoMotorPrueba[i]:
#                     #valida el algoritmo cuando el vehiculo esta encendido
#                     print "ESTA ENCENDIDO"
#                     print i
#                     #DESCOMENTAR
#                     procesarPausaActivaVehiculoEncendido(db, horaRegistradaPosicionPrueba[i], docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOCONDUCCION, PAUSAACTIVATIEMPOTOLERANCIA)
#                 else:
#                     print "ESTA APAGADO"
#                     print i
#                     #valida el algoritmo cuando el vehiculo esta apagado
#                     #DESCOMENTAR
#                     print docSeguimientoPausaActiva
#                     procesarPausaActivaVehiculoApagado(db, horaRegistradaPosicionPrueba[i], docSeguimientoPausaActiva, idVehiculo, PAUSAACTIVATIEMPOPAUSAACTIVA, PAUSAACTIVATIEMPOTOLERANCIA)    
#             i = i + 1 
#             # #-----------------------------
#             #-----------------------------
#         # if actualizoFechaHoraRegistrada:
#         #     if horaRegistradaPosicion != None:
#         #         actualizarFechaHoraRegistradaDocFechasRevision(db, idDocUltimaRevision, horaRegistradaPosicion)
#         #     actualizoFechaHoraRegistrada = False
#     except ValueError:
#         pass


#--------------------------fin funcion prueba----------------------------------

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


def guardarCacheDocumentosBD(db):
    #guarda los caches documentos
    for key, value in pendientes:
        if value["actualizar"]:
            db.save(value["doc"])
    cacheDocumentos = {}


