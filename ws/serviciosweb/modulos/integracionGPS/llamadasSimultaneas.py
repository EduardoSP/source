# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion


def obtenerLimiteLlamada(peticion, idProgramacion):
	#funcion auxiliar de verificarLlamadaEnCurso y obtenerTiempoMaxZonaAlarma
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    docProgramacionVigilancia = db[idProgramacion]
    return docProgramacionVigilancia["tiempoMaxGrabAudio"]



def verificarLlamadaProgramacionVigilancia(peticion, idVehiculo):
	#Se busca en el doc audioProgramacionVigilancia las que se encuentran en curso
	#y se obtiene el campo idProgramacion 
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    llamadaEnCurso = {}
    llamadaEnCurso["EnCurso"] 	= False
    db = conexion.getConexionTenant(tenant)
    mayor = 0
    limite = 0
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/programacionVigilanciaEnCurso',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"])
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            if doc.get('estado') == "En curso":
            	llamadaEnCurso['_id'] = doc.get('_id') 
            	llamadaEnCurso["EnCurso"] 	= True
            	llamadaEnCurso["idLlamada"]	= doc.get('idLlamada')
            	for idProgramacion in doc.get('idProgramacion', []):
            		limite	= obtenerLimiteLlamada(peticion, idProgramacion)
            		if int(limite) > mayor:
						mayor = int(limite)					
        llamadaEnCurso["limite"] = mayor
        return llamadaEnCurso
    except ValueError:
    	return { 'success' : False}

#funcion para guardar el documento capturaAudioZonaAlarma
def guardarcapturaAudioZonaAlarma(peticion, latitud, longitud, tiempoMaxGrabAudioZA, doc_idLlamada, idVehiculo, zonaAlarmas):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"        : "capturaAudioZonaAlarma",
            "creadoEn"        : datetime.now().isoformat(),
            "horaRegistrada"  : datetime.now().isoformat(),
            "latitud"         : latitud,
            "longitud"        : longitud, 
            "duracion"        : tiempoMaxGrabAudioZA,  
            "idLlamada"       : doc_idLlamada,
            "idVehiculo"      : idVehiculo,
            "estado"          : "En curso", 
            "urlAudio"        : "", 
            "activo"          : True,
            "zonaAlarmas"	  : zonaAlarmas
        })
        return doc_id
    except ValueError:
        return { 'success' : False }



def guardarLlamadaSimultaneaZA(peticion,llamadaPV, idVehiculo, latitud, longitud, zonaAlarmas, limiteMayor):
	guardarcapturaAudioZonaAlarma(peticion, latitud, longitud, limiteMayor, llamadaPV["idLlamada"], idVehiculo, zonaAlarmas)



def verificarDoccapturaAudioZonaAlarmaCreada(peticion, idVehiculo, idLlamada):
	#Se busca en el doc audioProgramacionVigilancia las que se encuentran en curso
	#y se obtiene el campo idProgramacion 
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    respuesta = False
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        filas = db.view('_design/llamadas/_view/llamadasZAVehiculoLlamada',
                    include_docs  = True, 
                    key = [idVehiculo, idLlamada],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            respuesta = True
    	return respuesta 
    except ValueError:
    	return { 'success' : False}


#=========================================================================================
#audios programacion vigilancia
def verificarLlamadaZonaAlarma(peticion, idVehiculo):
	#Se busca en el doc audioProgramacionVigilancia las que se encuentran en curso
	#y se obtiene el campo idProgramacion 
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    llamadaEnCurso = {}
    llamadaEnCurso["EnCurso"] 	= False
    db = conexion.getConexionTenant(tenant)
    limite = 0
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/zonaAlarmasEnCurso',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"])
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            if doc.get('estado') == "En curso":
            	llamadaEnCurso['_id'] = doc.get('_id') 
            	llamadaEnCurso["EnCurso"] 	= True
            	llamadaEnCurso["idLlamada"]	= doc.get('idLlamada')
            	limite = int(doc.get('duracion'))   	
        llamadaEnCurso["limite"] = limite
        return llamadaEnCurso
    except ValueError:
    	return { 'success' : False}


def verificarDocaudioProgramacionVigilancia(peticion, idVehiculo, idLlamada):
	#Se busca en el doc audioProgramacionVigilancia las que se encuentran en curso
	#y se obtiene el campo idProgramacion 
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    respuesta = False
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        filas = db.view('_design/llamadas/_view/llamadasPVVehiculoLlamada',
                    include_docs  = True, 
                    key = [idVehiculo, idLlamada],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            respuesta = True
    	return respuesta 
    except ValueError:
    	return { 'success' : False}


#funcion para guardar el documento capturaAudioZonaAlarma
def guardarcapturaAudioPV(peticion, latitud, longitud, tiempoMaxGrabAudioPV, doc_idLlamada, idVehiculo, programacionesVigilancia):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"        	: "audioProgramacionVigilancia",
            "creadoEn"        	: datetime.now().isoformat(),
            "horaRegistrada"  	: datetime.now().isoformat(),
            "latitud"         	: latitud,
            "longitud"        	: longitud, 
            "duracion"        	: str(tiempoMaxGrabAudioPV),  
            "idLlamada"       	: doc_idLlamada,
            "idVehiculo"      	: idVehiculo,
            "estado"          	: "En curso", 
            "urlAudio"        	: "", 
            "activo"          	: True,
            "idProgramacion"	: programacionesVigilancia
        })
        return doc_id
    except ValueError:
        return { 'success' : False }


def guardarLlamadaSimultaneaPV(peticion,llamadaZA, idVehiculo, latitud, longitud, programacionVigilancia, limiteMayor):
		guardarcapturaAudioPV(peticion, latitud, longitud, limiteMayor, llamadaZA["idLlamada"], idVehiculo, programacionVigilancia)

#==============================================================================
def obteneridMonitoreoZona(peticion, idZonaAlarma):
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    docZonaAlarma = db[idZonaAlarma]
    return docZonaAlarma["idZona"]


def obtenerTiempoMaxGrabAudioDocMonitoreoZona(peticion, idMonitoreoZona):
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    docMonitoreoZona = db[idMonitoreoZona]
    return docMonitoreoZona["tiempoMaxGrabAudio"]



def obtenerLimiteMayorZonaAlarmas(peticion,zonaAlarmas, limitePV):
	#editando
	mayor = 0
	tiempoMaxGrabAudio = 0
	limiteMayor = 0
	for idZonaAlarma in zonaAlarmas:
		idMonitoreoZona = obteneridMonitoreoZona(peticion, idZonaAlarma)
		tiempoMaxGrabAudio = obtenerTiempoMaxGrabAudioDocMonitoreoZona(peticion, idMonitoreoZona)
		if int(tiempoMaxGrabAudio) > mayor:
			mayor = int(tiempoMaxGrabAudio)	
	if limitePV > mayor:
		limiteMayor = limitePV
	else:
		limiteMayor = mayor
	return limiteMayor




#==============================================================================

def obtenerTiempoMaxGrabAudioDocPV(peticion, idVigilancia, idVehiculo):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    tiempoMaxGrabAudio = 0
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        filas = db.view('_design/vigilancias/_view/programacionVigilancia',
                    include_docs  = True, 
                    key = [idVigilancia, idVehiculo],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            tiempoMaxGrabAudio = doc.get('tiempoMaxGrabAudio')
    	return tiempoMaxGrabAudio 
    except ValueError:
    	return { 'success' : False}


def obtenerLimiteMayorProgramacion(peticion,programacionVigilancias, idVehiculo, limiteZA):
	mayor = 0
	tiempoMaxGrabAudio = 0
	limiteMayor = 0
	for idVigilancia in programacionVigilancias:
		tiempoMaxGrabAudio = obtenerTiempoMaxGrabAudioDocPV(peticion, idVigilancia, idVehiculo)
		if int(tiempoMaxGrabAudio) > mayor:
			mayor = int(tiempoMaxGrabAudio)	
	if limiteZA > mayor:
		limiteMayor = limiteZA
	else:
		limiteMayor = mayor
	return limiteMayor

def actualizarDocLLamadasRazonLimite(peticion, llamada, limite):
	#funcion que modifica el limite y la razon de la llamada=zonaAlarmaProgramacionVigilancia
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    docLlamadas 		= db[llamada["idLlamada"]]
    print "------------------------------------------------"
    print llamada["idLlamada"]
    docLlamadas["limite"]	= limite
    docLlamadas["razonLLamada"]	= "zonaAlarmaProgramacionVigilancia"
    db.save(docLlamadas) 
