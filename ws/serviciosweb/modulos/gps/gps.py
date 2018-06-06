# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from jsonschema               import validate, ValidationError
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
from ..autenticacion          import autenticacion as moduloAutenticacion
#-------------------------------------------------------------

def listarGps( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    placa         = ""  
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:

        filas = db.view(
            '_design/GPS/_view/listadoGPS',
            include_docs = True
        )
    
        dataRaw = []
        for fila in filas:
            doc         = fila.doc  
            
            vehiculo = {}
            idVehiculo = doc.get("idVehiculo","")
           
            if not idVehiculo == "":
                tenant = doc.get("tenant")
                if not tenant == "":
                    try:
                        dbTenant = conexion.getConexionTenant(doc.get("tenant"))
                        vehiculo = dbTenant[idVehiculo]
                        placa    = vehiculo.get("placa","")
                    except:
                        vehiculo = ""  
                        placa = "Vehículo eliminado"                 
                   
            dataRaw.append(
                {
                    "id"               : doc['_id'],
                    "activo"           : doc.get("activo",""),
                    "observaciones"    : doc.get("observaciones",""),
                    "imei"             : doc.get("imei",""),
                    "identificadorGPS" : doc.get("identificadorGPS",""),
                    "numSimCard"       : doc.get("numSimCard",""),
                    "tipoGps"          : doc.get("tipo",""),
                    "tenant"           : doc.get("tenant",""),
                    "idVehiculo"       : doc.get("idVehiculo",""),
                    "placaVehiculo"    : placa,
                  }
            )        
            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    
    except ValidationError as e:
        respuesta['mensaje'] = e.message
        print "error del try "+e
        #pass

    return { 'success' : False }


def verificarIdentificadorGPS(db, identificadorGPS):
    existeIdentificador = False    
    try:
        filas = db.view('_design/GPS/_view/listadoGPS',
                    include_docs  = True, 
                    startkey = [identificadorGPS, 0],
                    endkey = [identificadorGPS, {}])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            existeIdentificador = True     
        return existeIdentificador
    except :
        return existeIdentificador

def verificarNumSimcard(db, numSimCard):
    existeNumSimCard = False    
    try:
        filas = db.view('_design/GPS/_view/gpsPorNumSimCard',
                    include_docs  = True, 
                    key = [numSimCard])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            existeNumSimCard = True     
        return existeNumSimCard
    except :
        return existeNumSimCard


def verificarImei(db, imei):
    existeImei = False    
    try:
        filas = db.view('_design/GPS/_view/gpsPorImei',
                    include_docs  = True, 
                    key = [imei])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            existeImei = True     
        return existeImei
    except :
        return existeImei


def crearGps(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db    = conexion.getConexionTenant(tenant)
    couch = conexion.getCouch()
    
    if db == None:
        return { 'success' : False, 'mensaje': "no existe el tenant" }

    try:

        identificadorGPS    = datos.get("identificadorGPS","")
        numSimCard          = datos.get("numSimCard","")
        imei                = datos.get("imei","")
        existeIdentificador = verificarIdentificadorGPS(db, identificadorGPS)
        existeNumSimCard    = verificarNumSimcard(db, numSimCard)
        existeImei          = verificarImei(db, imei)
        if existeIdentificador or existeNumSimCard or existeImei:
            return { 'success' : False, 
                     'data'    : {
                        'existeIdentificador' : existeIdentificador,
                        'existeNumSimCard'    : existeNumSimCard,
                        'existeImei'          : existeImei  
                     }
            }            
        else:
            doc = {
                "tipoDato"              : "GPS",
                "activo"                : True,
                "identificadorGPS"      : datos.get("identificadorGPS",""),
        	    "numSimCard"            : datos.get("numSimCard",""),
        	    "tipo"                  : datos.get("tipo",""),
        	    "imei"                  : datos.get("imei",""),
        	    "observaciones"         : datos.get("observaciones",""),
        	    "tenant"                : "",
                "idVehiculo"            : "",          
                "creadoEn"              : datetime.now().isoformat(),
                "modificadoPor"         : usuario,
                "modificadoEn"          : datetime.now().isoformat()

            }

            db.save(doc)
            #crearNuevaBaseDatos(nuevaBaseDatos, couch)
            
            return {
                'success' : True,
                'data'    : {}
            }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


def compararGPS(db, identificadorGPS, idDocGps):
    docsGPS = db[idDocGps]
    if docsGPS["identificadorGPS"] == identificadorGPS:
        return True
    else:
        return False    

def buscarIdentificadorGPSRepetido(db, identificadorGPS, idGPS):
    existeGPS = False
    docsGPS = []    
    try:
        filas = db.view('_design/GPS/_view/listadoGPS',
                    include_docs  = True, 
                    startkey = [identificadorGPS, 0],
                    endkey = [identificadorGPS, {}])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            idDoc   = doc.get('_id')
            if idDoc != idGPS:
                docsGPS.append(idDoc) 
        for idDocGps in docsGPS:
            gpsIguales =   compararGPS(db, identificadorGPS, idDocGps)
            if gpsIguales:
                return True
        return False           
    except :
        return existeGPS

def compararNumSimcard(db, numSimCard, idDocGps):
    docsGPS = db[idDocGps]
    if docsGPS["numSimCard"] == numSimCard:
        return True
    else:
        return False   

def buscarNumSimcardGPSRepetido(db, numSimCard, idGPS):
    existeNumSimCard = False
    docsGPS = []    
    try:
        filas = db.view('_design/GPS/_view/gpsPorNumSimCard',
                    include_docs  = True, 
                    key = [numSimCard])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            idDoc   = doc.get('_id')
            if idDoc != idGPS:
                docsGPS.append(idDoc) 
        for idDocGps in docsGPS:
            gpsIguales =   compararNumSimcard(db, numSimCard, idDocGps)
            if gpsIguales:
                return True
        return False           
    except :
        return existeNumSimCard


def compararImei(db, imei, idDocGps):
    docsGPS = db[idDocGps]
    if docsGPS["imei"] == imei:
        return True
    else:
        return False   


def buscarImeiGPSRepetido(db, imei, idGPS):
    existeImei = False
    docsGPS = []    
    try:
        filas = db.view('_design/GPS/_view/gpsPorImei',
                    include_docs  = True, 
                    key = [imei])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            idDoc   = doc.get('_id')
            if idDoc != idGPS:
                docsGPS.append(idDoc) 
        for idDocGps in docsGPS:
            gpsIguales =   compararImei(db, imei, idDocGps)
            if gpsIguales:
                return True
        return False           
    except :
        return existeImei


def editarGps( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)
    print "despues de conectar tenant"+datos['id']

    if db == None:
        print "no encuentro db"
        return { 'success' : False }

    try:
        idGPS               = datos["id"]
        identificadorGPS    = datos["identificadorGPS"]
        numSimCard          = datos["numSimCard"]
        imei                = datos["imei"]
        existeIdentificador =   buscarIdentificadorGPSRepetido(db, identificadorGPS, idGPS) 
        existeNumSimCard    =   buscarNumSimcardGPSRepetido(db, numSimCard, idGPS)  
        existeImei          =   buscarImeiGPSRepetido(db, imei, idGPS)    
        if existeIdentificador or existeNumSimCard or existeImei:
            return { 'success' : False, 
                     'data'    : {
                        'existeIdentificador' : existeIdentificador,
                        'existeNumSimCard'    : existeNumSimCard,
                        'existeImei'          : existeImei  
                     }
            }        
        
        else:
            doc = db[datos['id']]
            print "traje  documento:"
            
            doc['modificadoPor']         = usuario
            doc['modificadoEn']          = datetime.now().isoformat()
            doc['activo']                = datos.get('activo',   doc['activo'])
            doc['observaciones']         = datos.get('observaciones',    doc['observaciones'])
            doc['imei']                  = datos.get('imei',    doc['imei'])
            doc['identificadorGPS']      = datos.get('identificadorGPS', doc['identificadorGPS'])
            doc['numSimCard']            = datos.get('numSimCard', doc['numSimCard'])
            doc['tipo']                  = datos.get('tipo',       doc['tipo'])
       
            db.save(doc)
           
            return {
                'success' : True,
                'data'    : {
                }            
            }
    except ValidationError as e:
        respuesta['mensaje'] = e.message
        print "error del try "+e

    return { 'success' : False }

# #-------------------------------------------------------------

def eliminarTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    
    db = conexion.getConexionTenant(usuario[:3])

    if db == None:
        return { 'success' : False }

    try:
        idEquipo    = datos['id']
        doc = db[datos['id']]
        doc['modificadoPor'] = usuario
        doc['modificadoEn']  = datetime.now().isoformat()

        doc['estado']        = "inactivo"
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }

# #-------------------------------------------------------------

def detalleGps( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]

        vehiculo = {}
        idVehiculo = doc.get("idVehiculo","")
        print "idvehiculo: "+idVehiculo
        if not idVehiculo == "":
            dbTenant = conexion.getConexionTenant(doc.get("tenant"))
            vehiculo = dbTenant[idVehiculo]

        dataResponse = {
            'id'                   : doc['_id'],
            'activo'               : doc.get('activo', ''),
            'observaciones'        : doc.get('observaciones', ''),
            'imei'                 : doc.get('imei', ''),
            'identificadorGPS'     : doc.get('identificadorGPS', ''),
            'numSimCard'           : doc.get('numSimCard', ''),
            'tipoGps'              : doc.get('tipo',''),
            'tenant'               : doc.get('tenant', ''),
            "idVehiculo"           : doc.get('idVehiculo',''),
            "placaVehiculo"        : vehiculo.get('placa',''),     
            
             
        }
        return {
            'success' : True,
            'data'    : dataResponse 
        }    
    except ValidationError as e:
        print "error del try "+e.message
        pass

    return { 'success' : False }


def pickerGps(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
                        '_design/GPS/_view/listadoGPS',
                        include_docs  = True
                        )
        
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          idVehiculo    = doc.get('idVehiculo', '')
          
          if idVehiculo == "":
              dataRaw.append(
                  {
                    'id'                   : doc.get('_id',''),
                    'identificadorGps'     : doc.get('identificadorGPS', ''),
                    'imei'                 : doc.get('imei', ''),
                    'numSimCard'           : doc.get('numSimCard', ''),
                    'tipoGps'              : doc.get('tipo',''),
                  }
              )            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

