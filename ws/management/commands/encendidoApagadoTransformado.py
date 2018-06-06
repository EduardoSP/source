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

#===============================================================================================
cantidadPuntosDetenido          = 100 #variable que se usa debido a que no se esta recibiendo el valor de encendido o apagado
rutaArchivoJournal      = '/home/eduardo/Escritorio/dataJournalEncendidoApagado/dataJournal'
rutaArchivoJournalCopia = '/home/eduardo/Escritorio/dataJournalEncendidoApagado/dataJournalCopia' 

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        tenants = buscarTenants()
        for tenant in tenants:
            print "==================================="
            print tenant
            #por cada tenant se procesara la informacion
            procesarEvaluacionEncendidoApagado(tenant)
        #actualizarEstadoRevisado(ultimaFechaRevision["idUltimaPosicionRevisada"])


def actualizarDocFechaHoraRegistrada(db, idDocUltimaRevision, fechaHoraRegistrada):
    docUltimaRevision = db[idDocUltimaRevision]
    docUltimaRevision["fechaHoraRegistrada"] = fechaHoraRegistrada
    db.save(docUltimaRevision)


def obtenerUltimaRevisionEncendidoApagado(db, idVehiculo):
    ultimaRevision      = {}
    ultimaRevision["fechaHoraRegistrada"]       = ""
    ultimaRevision["idUltimaPosicionRevisada"]  = ""
    #ultimaRevision["revisado"]                  = ""    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/seguridadVial/_view/listarFechasRevision',
            key             = ["encendidoApagado", idVehiculo],
            include_docs    = True)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value
            doc                             = fila.doc
            ultimaRevision["fechaHoraRegistrada"]       = doc.get('fechaHoraRegistrada')
            ultimaRevision["idUltimaPosicionRevisada"]  = doc.get('_id')
            #ultimaRevision["revisado"]                  = doc.get('revisado')
        return ultimaRevision
    except ValueError:
        pass

def procesarEvaluacionEncendidoApagado(tenant):
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
        for fila in filas:
            key                     = fila.key
            value                   = fila.value
            doc                     = fila.doc
            #Obtiene el identficador de cada vehiculo
            idVehiculo           = doc.get('_id')
            ultimaFechaRevision = obtenerUltimaRevisionEncendidoApagado(db, idVehiculo)       
            procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, tenant)
        #actualizo la ultima revision en el documento
    except ValueError:
        pass

def buscarRegistroActualMotor(db, idVehiculo):
    # funcion que retorna si el registro en la bd es encendido(True) o apagado(False)
    #y retorna si el registro de la bd esta EnCurso
    registroActualMotor = {}
    registroActualMotor["evento"] = ""
    registroActualMotor["idDocRegistroActual"] = 0
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []
        filas = db.view('_design/seguridadVial/_view/listarEncendidoApagadoPorVehiculo',
                    startkey = [idVehiculo, {}],
                    endkey  = [idVehiculo,0],
                    descending    = True,
                    include_docs  = True,
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            estaEncendido     = doc.get('evento', '')
            registroActualMotor["idDocRegistroActual"]  = doc.get('_id', '') 
            if estaEncendido == "Encendido":
                registroActualMotor["evento"]   = True
            else:
                registroActualMotor["evento"]   = False
        return registroActualMotor   
    except ValueError:
        pass


def procesarPosicionesVehiculosFechaCreacion(db, idVehiculo, ultimaFechaRevision, tenant):    
    print "**********************************"
    print idVehiculo
    print "**********************************"
    global cantidadPuntosDetenido
    revisoPuntos    = False
    if ultimaFechaRevision["idUltimaPosicionRevisada"] == "":
        # se revisa el vehiculo por primera vez el encendido y apagado y se guarda el documento
        ultimaRevision = "0"
        #guarda por primerza vez el documento de revision con la fecha actual
        idDocUltimaRevision = guardarDocRevisionVehiculo(db, idVehiculo)
    else:
        idDocUltimaRevision = ultimaFechaRevision["idUltimaPosicionRevisada"]
        ultimaRevision      = ultimaFechaRevision["fechaHoraRegistrada"]
        if ultimaRevision == "":
            #el vehiculo no tiene fecha hora registrada en el documento revision, entonces se busca el journal
            consultaDataJournal             = obtenerValoresDataJournal(idVehiculo)
            ultimaRevision                  = consultaDataJournal["ultimaFechaRevisada"]
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        contadorIteracion = 2000
        contadorCantidadPuntosDetenido  = 0
        while contadorIteracion == 2000:
            contadorIteracion = 0
            filas = db.view('_design/posicionVehiculos/_view/posicionFechaCreacion',
                startkey             = [idVehiculo, ultimaRevision+"Z"],
                endkey               = [idVehiculo, {}],  
                include_docs    = True,
                limit = 2000)
            #funcion que obtiene el estadoActual del motor y si el registro esta En Curso
            registroActualMotor         =  buscarRegistroActualMotor(db, idVehiculo)
            estadoActualEncendido       =  registroActualMotor["evento"]
            idDocRegistroActual         =  registroActualMotor["idDocRegistroActual"]
            for fila in filas:
                contadorIteracion       += 1
                key                     = fila.key
                value                   = fila.value
                doc                     = fila.doc
                estaEncendidoMotor      = doc.get('estaEncendidoMotor', False)             
                idDocPosicion               = doc.get('_id')
                revisoPuntos = True
                #print idDocPosicion
                horaRegistradaPosicion      = doc.get('horaRegistrada')
                ultimaRevision                  = horaRegistradaPosicion 
                print horaRegistradaPosicion
                #Inicio encendido motor puntos antiguos prueba
                velocidad = doc.get('velocidad', 0.0)
                if velocidad < 1:
                    estaEncendidoMotor              = False
                    contadorCantidadPuntosDetenido += 1
                else:
                    estaEncendidoMotor = True
                    contadorCantidadPuntosDetenido = 0
                if estadoActualEncendido == "":
                    # no hay eventos de encendido y apagado en la base de datos
                    #creo por primera vez y actualizo el estadoActualEncendido
                    idDocRegistroActual     = creoNuevoEvento(horaRegistradaPosicion, estaEncendidoMotor, idVehiculo, db)
                    estadoActualEncendido   = estaEncendidoMotor
                else:
                    if estadoActualEncendido:
                        if estadoActualEncendido == estaEncendidoMotor:
                            actualizoEventoAnterior(False, idDocRegistroActual, horaRegistradaPosicion, db)
                            estadoActualEncendido = True
                        else:
                            if contadorCantidadPuntosDetenido == cantidadPuntosDetenido:# if provisional ya que no se recibe los datos del motor
                                actualizoEventoAnterior(True, idDocRegistroActual, horaRegistradaPosicion,db)
                                estadoActualEncendido = False
                                idDocRegistroActual = creoNuevoEvento(horaRegistradaPosicion, estadoActualEncendido, idVehiculo, db)
                                contadorCantidadPuntosDetenido = 0 #linea provisional ya que no se recibe los datos del motor
                    else:
                        if estadoActualEncendido == estaEncendidoMotor:
                            if contadorCantidadPuntosDetenido == cantidadPuntosDetenido:# if provisional ya que no se recibe los datos del motor
                                actualizoEventoAnterior(False, idDocRegistroActual, horaRegistradaPosicion, db)
                                estadoActualEncendido = False
                        else:            
                            actualizoEventoAnterior(True, idDocRegistroActual, horaRegistradaPosicion, db)
                            estadoActualEncendido = True
                            idDocRegistroActual = creoNuevoEvento(horaRegistradaPosicion, estadoActualEncendido, idVehiculo, db)
                            contadorCantidadPuntosDetenido = 0 #linea provisional ya que no se recibe los datos del motor
                #guarda en el journal la fecha hora registrada y los datos que lleva hasta el momento
                guardarDataJournal(db, idVehiculo, horaRegistradaPosicion, tenant)
        if revisoPuntos:
            #registra la ultima hora de la ultima posicion en el documento encendidoApagado 
            actualizarDocFechaHoraRegistrada(db, idDocUltimaRevision, horaRegistradaPosicion)
    except ValueError:
        pass


def actualizoEventoAnterior(actualizoAnterior, idDocRegistroActual, horaRegistradaPosicion, db):
    if actualizoAnterior:
        print "actualizo fecha fin anterior"
        actualizarUltimaFechaEncendidoApagado(idDocRegistroActual, horaRegistradaPosicion, db)   

def creoNuevoEvento(horaRegistradaPosicion, estadoActualEncendido, idVehiculo, db):
    if db == None:
        return { 'success' : False }
    if estadoActualEncendido:
        textoEvento = "Encendido"
    else:
        textoEvento = "Apagado"
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"      : "encendidoApagado",
            "creadoEn"      : datetime.now().isoformat(),  
            "evento"        : textoEvento,
            "horaInicio"    : horaRegistradaPosicion,
            "horaFin"       : "",
            "idVehiculo"    : idVehiculo,
            "activo"        : True 
        })
        return doc_id
        print "creo nuevo evento"
    except ValueError:
        pass
    
def actualizarUltimaFechaEncendidoApagado(idDocRegistroActual, horaRegistradaPosicion, db):
    docEncendidoApagado = db[idDocRegistroActual]
    #actualizo la hora Fin
    docEncendidoApagado["horaFin"] = horaRegistradaPosicion
    db.save(docEncendidoApagado) 


def guardarDocRevisionVehiculo(db, idVehiculo):
    #guarda la fechasRevisio de encendidoApagado
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"              : "fechasRevision",
            "tipoRevision"          : "encendidoApagado",
            "fechaHoraRegistrada"   : "",  
            "idVehiculo"            : idVehiculo,
            "activo"                : True 
        })
        return doc_id
        print "creo nuevo evento"
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


def guardarDataJournal(db, idVehiculo, horaRegistradaPosicion, tenant):
    global rutaArchivoJournal
    global rutaArchivoJournalCopia
    dataJournal = {
        idVehiculo : {
            'ultimaFechaRevisada'               :  horaRegistradaPosicion,
            'tenant'                            :  tenant
            }
    }
    # Writing JSON data 
    # escribe en un archivo copia
    with open(rutaArchivoJournalCopia+idVehiculo+'.json', 'w') as f:
        json.dump(dataJournal, f)
    # copia el contenido del archivo copia al original
    copyfile(rutaArchivoJournalCopia+idVehiculo+'.json', rutaArchivoJournal+idVehiculo+'.json')


def obtenerValoresDataJournal(idVehiculo):
    global rutaArchivoJournal
    # Reading data back
    with open(rutaArchivoJournal+idVehiculo+'.json', 'r') as f:
        data = json.load(f)     
    return data[idVehiculo]  
