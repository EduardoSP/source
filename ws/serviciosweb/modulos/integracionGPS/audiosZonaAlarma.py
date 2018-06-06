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
            "razonLLamada"  : "zonaAlarma", 
            "idRemitente"   :  "GPS",
            "limite"        : str(tiempoMaxGrabAudio),
            "activoPanico"  : False,
            "activo"        : True
        })
        return doc_id
    except ValueError:
        return { 'success' : False }

def actualizarDuracionCapturaAudioZonaAlarma(peticion, idLlamada, tiempoMaxGrabAudio):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/llamadacapturaAudioZA',
                    include_docs  = True, 
                    key = [idLlamada, "En curso"],
                    limit = 1)
        for fila in filas:
            key 	= fila.key
            value 	= fila.value
            doc 	= fila.doc
            idCapturaAudioZonaAlarma  = doc.get('_id')
            docCapturaAudioZonaAlarma = db[idCapturaAudioZonaAlarma]
            docCapturaAudioZonaAlarma["duracion"] = str(tiempoMaxGrabAudio)
            db.save(docCapturaAudioZonaAlarma)
    except ValueError:
        return { 'success' : False}


def actualizarLimiteLlamada(peticion, idLlamada, tiempoMaxGrabAudio):
	#Funcion que usa el idLlamada para buscar los documentos llamadas 
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    docLlamadas     = db[idLlamada]
    docLlamadas["limite"] = str(tiempoMaxGrabAudio)
    db.save(docLlamadas)

   
def obtenerLimiteLlamada(peticion, idZonaAudio):
	#funcion auxiliar de verificarLlamadaEnCurso y obtenerTiempoMaxZonaAlarma
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    docZonaAlarmas		= db[idZonaAudio]
    docMonitoreoZonas	= db[docZonaAlarmas["idZona"]]
    return docMonitoreoZonas["tiempoMaxGrabAudio"]


def verificarRegistraAudioZA(peticion, idZonaAlarma):
    #editando
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    registraAudio   = False
    docZonaAlarmas      = db[idZonaAlarma]
    docMonitoreoZonas   = db[docZonaAlarmas["idZona"]]
    if docMonitoreoZonas["registrarAudio"]:
        registraAudio   = True
    return registraAudio


def obtenerTiempoMaxZonaAlarma(peticion, zonaAlarmas):
	#por cada zona alarma obtengo el tiempoMaxGrabAudio y retorno el mayor, tener en
	#cuenta que toca pasar por el doc zonaAlarma y luego monitoreoZonas donde esta el valor
	mayor = 0
	for zonaAlarma in zonaAlarmas:
		tiempoMax = obtenerLimiteLlamada(peticion, zonaAlarma)
        registraAudio = verificarRegistraAudioZA(peticion, zonaAlarma)
        if registraAudio:
            if mayor < float(tiempoMax):
                mayor = float(tiempoMax)
	return mayor


def verificarLlamadaEnCurso(peticion, zonaAlarmas, idVehiculo):
	#Se busca en el doc capturaAudioZonaAlarma las que se encuentran en curso
	#y se obtiene el campo zonaAlarmas 
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
        filas = db.view('_design/llamadas/_view/zonaAlarmasEnCurso',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"])
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            if doc.get('estado') == "En curso":
            	doc.get('zonaAlarmas', [])
            	for zonaAlarma in zonaAlarmas:
            		for idZonaAudio in doc.get('zonaAlarmas', []):
            			if zonaAlarma == idZonaAudio:
            				llamadaEnCurso["EnCurso"] 	= True
            				llamadaEnCurso["limite"] 	= obtenerLimiteLlamada(peticion, idZonaAudio)
            				llamadaEnCurso["idLlamada"]	= doc.get('idLlamada')
        return llamadaEnCurso
    except ValueError:
        return { 'success' : False}

def ejecutarAudioZonaAlarma(peticion, latitud, longitud, horaRegistrada, idVehiculo, zonaAlarmas):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    tiempoLlamada   = settings.TWILIO_TIEMPO_LLAMADA  
    account_sid     = settings.TWILIO_ACCOUNT_SID 
    auth_token      = settings.TWILIO_AUTH_TOKEN 
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc            		= db[idVehiculo]
        #valida si el vehiculo tiene el permiso 14 "Audio zona alarma" para tomar foto
        permisoTomarAudioZA = validaPermisoAudioZA(db, idVehiculo) 
        if permisoTomarAudioZA:
            numSimCardVehiculo	= traerNumeroSimCardVehiculo(idVehiculo)
            numeroFLEET     	= settings.TWILIO_NUMERO
            #verificar si la llamada esta en curso = llamadaEnCurso["EnCurso"], limite =llamadaEnCurso["limite"], 
            # llamadaEnCurso["idLlamada"] en curso retorna un booleano
            llamadaEnCurso = verificarLlamadaEnCurso(peticion, zonaAlarmas, idVehiculo)
            #funcion para obtener el tiempoMaxGrabAudio de la zona monitoreada
            tiempoMaxGrabAudioZA = obtenerTiempoMaxZonaAlarma(peticion, zonaAlarmas)
            #print "llamada en curso True o False"
            #print llamadaEnCurso["EnCurso"]
            if llamadaEnCurso["EnCurso"]:
                #verificar el limite de la llamada en curso con el limite 
                #del tiempoMaxGrabAudio
                if float(llamadaEnCurso["limite"]) < tiempoMaxGrabAudioZA:
                    #funcion para actualizar el limite de la llamada doc llamadas y el doc capturaAudioZonaAlarma
                    print "entro a dos zonas"
                    actualizarLimiteLlamada(peticion,llamadaEnCurso["idLlamada"], tiempoMaxGrabAudioZA)
                    #funcion para modificar la duracion del doc capturaAudioZonaAlarma 
                    actualizarDuracionCapturaAudioZonaAlarma(peticion, llamadaEnCurso["idLlamada"], tiempoMaxGrabAudioZA)
            else:
                #No hay llamada en zona Alarma se creara
                client = TwilioRestClient(account_sid, auth_token)
                #DESCOMENTAR PARA QUE FUNCIONE
                sid = crearLlamada(client, numSimCardVehiculo,  numeroFLEET )
                doc_idLlamada = guardarDocLLamadas(peticion, idVehiculo, sid, tiempoMaxGrabAudioZA)
                doc_idCapturaAudioZA = guardarcapturaAudioZonaAlarma(peticion, latitud, longitud, tiempoMaxGrabAudioZA, doc_idLlamada, idVehiculo, zonaAlarmas)
                #sid = crearLlamada(client, numSimCardVehiculo,  numeroFLEET )
                #guardar el documento llamada con sid y el estado En curso,razonllamada:usuario
        
                #guardar documento capturaAudio
	        
    except ValueError:
        return { 'success' : False, 'mensaje' : 'aqui llego'}

#puntos para hacer pruebas
#Lat : 3.5833 Long: -76.25 Palmira - Valle del Cauca Longitud
#Latitud: 3.26389  Longitud: -76.5444 Jamundi
#Se encuentra en dos zonas alaramas 3.359153, -76.539222



#=============Inicio Terminar llamada sale de zona alarma============

def verificarLlamadaEnCursoZA(peticion, idVehiculo):
	# Se verifica el estado En curso en el documento capturaAudioZonaAlarma
	#y se retorna un booleano
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    datosCapturaAudioZA= {}
    datosCapturaAudioZA["estado"] 	= False
    datosCapturaAudioZA["idCapturaAudioZA"] = None
    datosCapturaAudioZA["idLlamada"] 		= None
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/llamadas/_view/zonaAlarmasEnCurso',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            datosCapturaAudioZA["estado"] 	= True
            datosCapturaAudioZA["idCapturaAudioZA"]	= doc.get('_id')
            datosCapturaAudioZA["idLlamada"]		= doc.get('idLlamada')
     	return datosCapturaAudioZA
    except ValueError:
        return { 'success' : False}

def terminarLlamadaSaleZonaAlarma(peticion, idVehiculo, llamadaEnCurso):
	#Se actualiza el estado a finalizado en el documento capturaAudioZonaAlarma y en el documento llamadas
	#modificar estado a finalizado del documento capturaAudioZonaAlarma
    autenticacion   					= peticion['autenticacion']
    usuario         					= autenticacion['usuario']
    tenant          					= autenticacion['tenant']
    db              					= conexion.getConexionTenant(tenant)
    docCapturaAudioZA					= db[llamadaEnCurso["idCapturaAudioZA"]]
    docLlamadas 						= db[llamadaEnCurso["idLlamada"]]
    account_sid     = settings.TWILIO_ACCOUNT_SID 
    auth_token      = settings.TWILIO_AUTH_TOKEN
    #Obtiene el sidLlamada
    sidLlamada 							= docLlamadas["sidLlamada"] 
    client      = TwilioRestClient(account_sid, auth_token)
    terminarLlamada(client, sidLlamada)
    docCapturaAudioZA["estado"] 		= "Finalizado"
    #Url audio
    urlAudio            = consultarUrlGrabacion(sidLlamada, client)
    docCapturaAudioZA["urlAudio"]		= urlAudio
    db.save(docCapturaAudioZA)
    docLlamadas["estado"]				= "Finalizado"
    db.save(docLlamadas)
    #print urlAudio
#=============Fin Terminar llamada sale de zona alarma============


#=============================================================================================
#Verificar llamadas ejecutadas en la zona alarmas
def verificarLlamadaZAEjecutada(peticion, idVehiculo, zonaAlarmas):
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
        filas = db.view('_design/llamadas/_view/llamadasRealizadasZA',
                    include_docs  = True, 
                    key = [idVehiculo, zonaAlarmas],
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


def actualizarLimiteLlamadaZAEnCurso(peticion, idVehiculo, llamadaEnCurso, zonaAlarmas):
    #    llamadaEnCurso["idCapturaAudioZA"] 
    #    llamadaEnCurso["idLlamada"]
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    docLlamadas     = db[llamadaEnCurso["idLlamada"]]
    limite = str(docLlamadas["limite"])
    db.save(docLlamadas)


#===================================================================
def verificarReingresoZona(peticion, idVehiculo, zonaAlarmas):
    pass


#valida si el vehiculo tiene el permiso 14 audio zona alarma para tomar foto
def validaPermisoAudioZA(db, idVehiculo):
	numPermiso = "14" #captura audio za
	respuesta = False
	if db == None:
		return { 'success' : False }
	try:
		doc = db[idVehiculo]
		opcionesAdicionalesPlataforma = doc.get("opcionesAdicionalesPlataforma", None)
		if not(opcionesAdicionalesPlataforma == None):
			if numPermiso in opcionesAdicionalesPlataforma:
				respuesta = True
		return respuesta
	except:
		print "error del try "

