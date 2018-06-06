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
from funcionesTwilio          import crearLlamada, terminarLlamada, consultarUrlGrabacion
from ..vehiculos.vehiculos    import traerNumeroSimCardVehiculo
from twilio.rest import TwilioRestClient

def obtenerLimiteLlamada(peticion, idProgramacion):
	#funcion auxiliar de verificarLlamadaEnCurso y obtenerTiempoMaxZonaAlarma
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    docProgramacionVigilancia = db[idProgramacion]
    return docProgramacionVigilancia["tiempoMaxGrabAudio"]


def actualizarLimiteLlamada(peticion, idLlamada, tiempoMaxGrabAudio):
	#Funcion que usa el idLlamada para buscar los documentos llamadas 
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    docLlamadas     = db[idLlamada]
    docLlamadas["limite"] = str(tiempoMaxGrabAudio)
    db.save(docLlamadas)

def verificarLlamadaEnCurso(peticion, programacionesVigilancia, idVehiculo):
	#Se busca en el doc audioProgramacionVigilancia las que se encuentran en curso
	#y se obtiene el campo idProgramacion 
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    llamadaEnCurso = {}
    llamadaEnCurso["EnCurso"] 	= False
    db = conexion.getConexionTenant(tenant)
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
            	for programacionVigilancia in programacionesVigilancia:
            		for idProgramacion in doc.get('idProgramacion', []):
            			if programacionVigilancia == idProgramacion:
            				llamadaEnCurso["EnCurso"] 	= True
            				llamadaEnCurso["limite"] 	= obtenerLimiteLlamada(peticion, idProgramacion)
            				llamadaEnCurso["idLlamada"]	= doc.get('idLlamada')

        return llamadaEnCurso
    except ValueError:
        return { 'success' : False}


def verificarRegistraAudioPV(peticion, idProgramacion):
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    registraAudio 	= False
    docProgramacionVigilancia     = db[idProgramacion]
    if docProgramacionVigilancia["registrarAudio"]:
    	registraAudio =	True
    return registraAudio

def obtenerTiempoMaxPV(peticion, programacionesVigilancia):
	#por cada zona alarma obtengo el tiempoMaxGrabAudio y retorno el mayor, tener en
	mayor = 0
	for programaciionVigilancia in programacionesVigilancia:
		tiempoMax = obtenerLimiteLlamada(peticion, programaciionVigilancia)
		registraAudio = verificarRegistraAudioPV(peticion, programaciionVigilancia)
		if registraAudio:
			if mayor < float(tiempoMax):
				mayor = float(tiempoMax)
	return mayor


def actualizarDuracionAudioProgramacionVigilancia(peticion, idLlamada, tiempoMaxGrabAudio):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/llamadacapturaAudioPV',
                    include_docs  = True, 
                    key = [idLlamada, "En curso"],
                    limit = 1)
        for fila in filas:
            key 	= fila.key
            value 	= fila.value
            doc 	= fila.doc
            idCapturaAudioPV  = doc.get('_id')
            docCapturaAudioPV = db[idCapturaAudioPV]
            docCapturaAudioPV["duracion"] = str(tiempoMaxGrabAudio)
            db.save(docCapturaAudioPV)
    except ValueError:
        return { 'success' : False}

#funcion para guardar el documento de la llamada
def guardarDocLLamadas(peticion, idVehiculo, sid, tiempoMaxGrabAudio):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 

        doc_id, doc_rev = db.save({
            "tipoDato"      : "llamadas",
            "creadoEn"      : datetime.now().isoformat(), 
            "idVehiculo"    : idVehiculo, 
            "sidLlamada"    : sid,
            "estado"        : "En curso", 
            "razonLLamada"  : "programacionVigilancia", 
            "idRemitente"   :  "GPS",
            "limite"        : tiempoMaxGrabAudio,
            "activoPanico"  : False,
            "activo"        : True
        })
        return doc_id
    except ValueError:
        return { 'success' : False }

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


def ejecutarAudioProgramacionVigilancia(peticion, latitud, longitud, horaRegistrada, idVehiculo, programacionesVigilancia):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant'] 
    account_sid     = settings.TWILIO_ACCOUNT_SID 
    auth_token      = settings.TWILIO_AUTH_TOKEN 
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
		doc            		= db[idVehiculo]
		numSimCardVehiculo  = traerNumeroSimCardVehiculo(idVehiculo)
		numeroFLEET     	= settings.TWILIO_NUMERO
		#verificar si la llamada esta en curso = llamadaEnCurso["EnCurso"], limite =llamadaEnCurso["limite"], 
		# llamadaEnCurso["idLlamada"] en curso retorna un booleano
		llamadaEnCurso = verificarLlamadaEnCurso(peticion, programacionesVigilancia, idVehiculo)
		#funcion para obtener el tiempoMaxGrabAudio de la programacion vigilancia
		tiempoMaxGrabAudioPV = obtenerTiempoMaxPV(peticion, programacionesVigilancia)
		#print tiempoMaxGrabAudioPV
		if llamadaEnCurso["EnCurso"]:
			#verificar el limite de la llamada en curso con el limite 
			#del tiempoMaxGrabAudio
			if float(llamadaEnCurso["limite"]) < tiempoMaxGrabAudioPV:
				#funcion para actualizar el limite de la llamada doc llamadas y el doc audioProgramacionVigilancia
				print "entro a dos programaciones vigilancia"
				actualizarLimiteLlamada(peticion,llamadaEnCurso["idLlamada"], tiempoMaxGrabAudioPV)
				#funcion para modificar la duracion del doc audioProgramacionVigilancia 
				actualizarDuracionAudioProgramacionVigilancia(peticion, llamadaEnCurso["idLlamada"], tiempoMaxGrabAudioPV)
		else:
			#No hay llamada en la programacion vigilancia se creara
			client = TwilioRestClient(account_sid, auth_token)
            #DESCOMENTAR PARA QUE FUNCIONE
			sid = crearLlamada(client, numSimCardVehiculo,  numeroFLEET )
			doc_idLlamada = guardarDocLLamadas(peticion, idVehiculo, sid, tiempoMaxGrabAudioPV)
			doc_idCapturaAudioPV = guardarcapturaAudioPV(peticion, latitud, longitud, tiempoMaxGrabAudioPV, doc_idLlamada, idVehiculo, programacionesVigilancia)
    except ValueError:
        return { 'success' : False, 'mensaje' : 'aqui llego'}


def verificarLlamadaPVEjecutada(peticion, idVehiculo, programacionVigilancia):
    # Se verifica el estado En curso en el documento capturaAudioZonaAlarma
    #y se retorna un booleano
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    respuesta = False
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        filas = db.view('_design/llamadas/_view/llamadasRealizadasPV',
                    include_docs  = True, 
                    key = [idVehiculo, programacionVigilancia],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            estado  = doc.get('estado')
            if estado == "Finalizado":
                respuesta = True
        return respuesta
    except ValueError:
        return { 'success' : False}

#=============================================================================================



def verificarLlamadaEnCursoPV(peticion, idVehiculo):
    # Se verifica el estado En curso en el documento capturaAudioZonaAlarma
    #y se retorna un booleano
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    datosCapturaAudioZA= {}
    datosCapturaAudioZA["estado"]   = False
    datosCapturaAudioZA["idCapturaAudioPV"] = None
    datosCapturaAudioZA["idLlamada"]        = None
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/programacionVigilanciaEnCurso',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            datosCapturaAudioZA["estado"]   = True
            datosCapturaAudioZA["idCapturaAudioPV"] = doc.get('_id')
            datosCapturaAudioZA["idLlamada"]        = doc.get('idLlamada')
        return datosCapturaAudioZA
    except ValueError:
        return { 'success' : False}
