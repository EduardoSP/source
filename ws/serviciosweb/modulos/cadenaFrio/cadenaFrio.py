# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from jsonschema               import validate, ValidationError
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
import time
import random

def listadoAlarmasCadenaFrio( peticion ):

    #import pdb; pdb.set_trace()
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    fechaInicio   = datos.get("fechaInicio")
    fechaFin      = datos.get("fechaFin")
    idVehiculo    = datos.get("idVehiculo")
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        dataRaw = []

        filasPosicion = db.view(
            '_design/cadenaFrio/_view/alarmasCadenaFrio',
            include_docs  = True,
            #limit         = 1,
            descending    = False,
            startkey      = [idVehiculo, fechaInicio],
            endkey        = [idVehiculo, fechaFin],
            reduce        = False
        )
        
        for filaPosicion in filasPosicion:
            docPosicion = filaPosicion.doc
            dataRaw.append({
                "idAlarmaCadenaFrio" : docPosicion["_id"],
		"fechahoraInicio"    : docPosicion.get("fechahoraInicio"),
		"fechahoraFin"       : docPosicion.get("fechahoraFin"),
                "estado"             : docPosicion.get("estado"),
                "tempMaxima"         : docPosicion.get("tempMaxima"),
                "tempMinima"         : docPosicion.get("tempMinima"),
                "tempLimSuperior"    : docPosicion.get("tempLimSuperior"),
                "tempLimInferior"    : docPosicion.get("tempLimInferior"),
                "tipoAlarma"         : docPosicion.get("tipoAlarma"),
            })
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
        
        #dataRaw = []

        # filas = db.view(
        #     '_design/vehiculos/_view/vehiculos',
        #     include_docs  = True,            
        # )
        # for fila in filas:
        #   key   = fila.key
        #   value = fila.value
        #   doc   = fila.doc
                     
        # return {
        #     'success' : True,
        #     'data'    : dataRaw
        # }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

def listadoPuntosCadenaFrio( peticion ):

    #import pdb; pdb.set_trace()
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    fechaInicio   = datos.get("fechaInicio")
    fechaFin      = datos.get("fechaFin")
    idVehiculo    = datos.get("idVehiculo")
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        dataRaw = {}
        temperaturas = []

        filasPosicion = db.view(
            '_design/cadenaFrio/_view/puntoCadenaFrio',
            include_docs  = True,
            #limit         = 1,
            descending    = False,
            startkey      = [idVehiculo, fechaInicio],
            endkey        = [idVehiculo, fechaFin],
            reduce        = False
        )

        tempMaxima = 0
        tempMinima = 100
        for filaPosicion in filasPosicion:
            docPosicion    = filaPosicion.doc
            horaRegistrada = docPosicion.get("horaRegistrada")
            temperatura    = docPosicion.get("temperatura")
            if temperatura < tempMinima:
                tempMinima = temperatura

            if temperatura > tempMaxima:
                tempMaxima = temperatura
            
            temperaturas.append({
                "fechahora"       : horaRegistrada,
                "temperatura"     : temperatura,
            })
        dataRaw = {
            "tempMaxima"   : tempMaxima,
            "tempMinima"   : tempMinima,
            "temperaturas" : temperaturas
        }
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
        
        #dataRaw = []

        # filas = db.view(
        #     '_design/vehiculos/_view/vehiculos',
        #     include_docs  = True,            
        # )
        # for fila in filas:
        #   key   = fila.key
        #   value = fila.value
        #   doc   = fila.doc
                     
        # return {
        #     'success' : True,
        #     'data'    : dataRaw
        # }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

def actualizarAlarmaCadenaFrio( peticion ):

    #import pdb; pdb.set_trace()
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    idVehiculo                   = datos.get("idVehiculo")
    estaAlarmaCadenaFrioActivada = datos.get("estaAlarmaCadenaFrioActivada")
    tempLimSuperior              = datos.get("tempLimSuperior")
    tempLimInferior              = datos.get("tempLimInferior")
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        dataRaw     = {}
        docVehiculo = db[idVehiculo]

        docVehiculo["estaAlarmaCadenaFrioActivada"] = estaAlarmaCadenaFrioActivada
        docVehiculo["tempLimInferior"]              = tempLimInferior
        docVehiculo["tempLimSuperior"]              = tempLimSuperior

        db.save(docVehiculo)
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
        
        #dataRaw = []

        # filas = db.view(
        #     '_design/vehiculos/_view/vehiculos',
        #     include_docs  = True,            
        # )
        # for fila in filas:
        #   key   = fila.key
        #   value = fila.value
        #   doc   = fila.doc
                     
        # return {
        #     'success' : True,
        #     'data'    : dataRaw
        # }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

def listadoVehiculosCadenaFrio( peticion ):

    #import pdb; pdb.set_trace()
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        dataRaw = []
        for i in range(10):
            dataRaw.append({
                "idVehiculo"                   : "129018201829102",
                "placaVehiculo"                : "TTY123",
                "latitud"                      : 4.696926666666666,
                "longitud"                     : -74.17124833333334,
		"fechaHora"                    : "2017-12-18T12:03:28",
                "estaAlarmaCadenaFrioActivada" : random.choice([True, False]),
                "temperatura"                  : random.randint(10, 30),
                "tempLimSuperior"              : random.randint(10, 30),
                "tempLimInferior"              : random.randint(10, 30)                
            })
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
        
        #dataRaw = []

        # filas = db.view(
        #     '_design/vehiculos/_view/vehiculos',
        #     include_docs  = True,            
        # )
        # for fila in filas:
        #   key   = fila.key
        #   value = fila.value
        #   doc   = fila.doc
                     
        # return {
        #     'success' : True,
        #     'data'    : dataRaw
        # }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

def reporteTemperaturaVehiculos( peticion ):

    #import pdb; pdb.set_trace()
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        dataRaw = []
        for i in range(10):
            dataRaw.append({
                "idVehiculo"                   : "129018201829102",
                "placaVehiculo"                : "TTY123",
                "latitud"                      : 4.696926666666666,
                "longitud"                     : -74.17124833333334,
		"fechaHora"                    : "2017-12-18T12:03:28",
                "estaAlarmaCadenaFrioActivada" : random.choice([True,False]),
                "temperatura"                  : random.randint(10, 30),
                "tempLimSuperior"              : random.randint(10, 30),
                "tempLimInferior"              : random.randint(10, 30),
            })
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
        
        #dataRaw = []

        # filas = db.view(
        #     '_design/vehiculos/_view/vehiculos',
        #     include_docs  = True,            
        # )
        # for fila in filas:
        #   key   = fila.key
        #   value = fila.value
        #   doc   = fila.doc
                     
        # return {
        #     'success' : True,
        #     'data'    : dataRaw
        # }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

def getTemperaturaVehiculo(db, idVehiculo):
    docPosicion = {}
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
                
    return docPosicion.get("temperatura",0)


def listarVehiculosCadenaFrio(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)
    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw     = []
        conductor   = ""
        filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
        for fila in filas:
            key   = fila.key
            value = fila.value
            doc   = fila.doc
            idVehiculo = doc.get('_id')
            idConductor = doc.get('conductor',"")
            if not(idConductor == ""):
                docConductor    = db[idConductor]
                conductor       = u"{}-{} {}".format(docConductor['cedula'], docConductor['nombres'], docConductor['apellidos'])              
            opcionesAdicionalesPlataforma   = doc.get('opcionesAdicionalesPlataforma', None)
            tieneCadenaFrio                 = evaluarVehiculoCadenaFrio(opcionesAdicionalesPlataforma)
            if tieneCadenaFrio:
                dataRaw.append({
                    'idVehiculo'                : idVehiculo,
                    'placa'                     : doc.get('placa'),
                    'marca'                     : doc.get('marca'),
                    'modelo'                    : doc.get('modelo'),        
                    'conductor'                 : conductor,
                    'estadoPermisoCadenaFrio'   : doc.get('estaAlarmaCadenaFrioActivada', False)
                    })
            conductor = ""
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False,
             'data'      : dataRaw
        }


def evaluarVehiculoCadenaFrio(opcionesAdicionalesPlataforma):
    #permiso 19 (cadena de frio)
    permiso = u'19'
    if not(opcionesAdicionalesPlataforma == None):
        if permiso in opcionesAdicionalesPlataforma:
            return True
        else:
            return False
    else:
        return False


def activarDesactivarCadenaFrioVehiculos(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        listaIdVehiculos    = datos.get("listaIdVehiculos", [])
        activar             = datos.get("activaCadenaFrio", False)
        for idVehiculo in listaIdVehiculos:
            print idVehiculo
            docVehiculo = db[idVehiculo]
            docVehiculo['estaAlarmaCadenaFrioActivada'] = activar
            db.save(docVehiculo)
        return {
            'success' : True 
        }    
    except ValueError as e:
        print e
    return { 'success' : False }