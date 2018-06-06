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
from ..integracionGPS.funcionesTwilio          import crearLlamada, terminarLlamada, consultarUrlGrabacion
from ..vehiculos.vehiculos    import traerNumeroSimCardVehiculo
from twilio.rest import TwilioRestClient


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
            "razonLLamada"  : "botonPanico", 
            "idRemitente"   :  "GPS",
            "limite"        : str(tiempoMaxGrabAudio),
            "activoPanico"  : True, # campo para saber si en algun momento activo el boton de panico
            "activo"        : True
        })
        return doc_id
    except ValueError:
        return { 'success' : False }


def guardarcapturaAudioBotonPanico(peticion, horaRegistrada, latitud, longitud, tiempoMaxGrabAudio, idLlamada, idVehiculo, idPanico):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 

        doc_id, doc_rev = db.save({
            "tipoDato"      		: "capturaAudioBotonPanico",
            "creadoEn"      		: datetime.now().isoformat(), 
            "horaRegistrada"    	: horaRegistrada, 
            "latitud"				: latitud,
            "longitud"				: longitud,
            "duracion"				: tiempoMaxGrabAudio,
            "idLlamada"				: idLlamada,
            "idVehiculo"			: idVehiculo,
            "estado"				: "En curso",
            "idAlarmaBotonPanico"	: idPanico,
            "activo"        		: True
        })
        return doc_id
    except ValueError:
        return { 'success' : False }


def obtenerLlamadaEnCurso(peticion, idVehiculo):
	#Se busca el limite de la llamada en curso
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    llamadaEnCurso = {}
    llamadaEnCurso["_id"] 				= 0
    llamadaEnCurso["limiteLlamada"] 	= 0
    llamadaEnCurso["EnCurso"] 			= False
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/llamadaEnCursoVehiculo',
                    include_docs  = True, 
                    key = [idVehiculo])
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            llamadaEnCurso["_id"] 			= doc.get('_id', "")
            llamadaEnCurso["limiteLlamada"] = doc.get('limite', "")
            llamadaEnCurso["EnCurso"] 		= True
        return llamadaEnCurso
    except ValueError:
        return { 'success' : False}


def actualizaDocLlamadasActivaPanico(peticion, idLlamada):
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    docLlamadas = db[idLlamada]
    docLlamadas["activoPanico"] = True
    db.save(docLlamadas) 


def actualizaDocLlamadasDuracion(peticion, idLlamada, limite):
    autenticacion 	= peticion['autenticacion']
    usuario       	= autenticacion['usuario']
    tenant      	= autenticacion['tenant']
    db 				= conexion.getConexionTenant(tenant)
    docLlamadas 	= db[idLlamada]
    docLlamadas["limite"] = limite
    db.save(docLlamadas) 


def ejecutarGuardarAudioBotonPanico(peticion, latitud, longitud, horaRegistrada, idVehiculo, idPanico):
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client 				= TwilioRestClient(account_sid, auth_token)
	numSimCardVehiculo	= traerNumeroSimCardVehiculo(idVehiculo)
	numeroFLEET     	= settings.TWILIO_NUMERO
	tiempoMaxGrabAudio  = settings.TIEMPO_MAX_GRAB_AUDIO_PANICO
	#buscar llamada en curso 
	llamadaEnCurso  	= obtenerLlamadaEnCurso(peticion, idVehiculo) 
	if llamadaEnCurso["EnCurso"]:
		doc_idLlamada 	   		= llamadaEnCurso["_id"]
		#actualizar en el documento llamadas que activo el boton de panico
		actualizaDocLlamadasActivaPanico(peticion, doc_idLlamada)
		#si la llamada esta en curso. si el limite del doc buscado es mayor asignarlo al tiempoMaxGrabAudio
		if float(llamadaEnCurso["limiteLlamada"]) >= float(tiempoMaxGrabAudio):
			tiempoMaxGrabAudio 	= llamadaEnCurso["limiteLlamada"]
		else:
			#La duracion del boton de panico es la mayor
			actualizaDocLlamadasDuracion(peticion, doc_idLlamada, str(tiempoMaxGrabAudio))
				
	else:
		#crear llamada si no existe ninguna donde
        #DESCOMENTAR PARA QUE FUNCIONE
		sid 					= crearLlamada(client, numSimCardVehiculo,  numeroFLEET )
		#sid 					= "SID DE PRUEBA"
		doc_idLlamada			= guardarDocLLamadas(peticion, idVehiculo, sid, tiempoMaxGrabAudio)
	doc_idcapturaPanico 		= guardarcapturaAudioBotonPanico(peticion, horaRegistrada, latitud, longitud, tiempoMaxGrabAudio, doc_idLlamada, idVehiculo, idPanico)

