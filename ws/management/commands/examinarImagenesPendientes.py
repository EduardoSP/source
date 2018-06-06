# -*- encoding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf                 import settings
#from webbiodws.models            import *
from django.conf                 import settings
import urllib2
import logging
import couchdb
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ws.serviciosweb.modulos.conexion import conexion
from datetime                 import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
import os
import json
from ws import nisabuUtils
import os.path 
from dateutil import parser
import pytz

#==========================================================================
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
		dbFleet = conexion.getConexionFleet()
		if dbFleet == None:
			return { 'success' : False, 'mensaje': "existe el bd" }
		try:
			dataRaw = {}
			filas = dbFleet.view('_design/inspeccionGPS/_view/inspeccionImagen',
			            include_docs  = True)
			for fila in filas:
				key 					= fila.key
				value 					= fila.value
				doc 					= fila.doc
				identificadorSolicitud	= doc.get('_id') 
				idVehiculo				= doc.get('idVehiculo')
				tenant					= doc.get('tenant')
				esDirecta 				= doc.get('esDirecta')
				esPanico				= doc.get('esPanico')
				idZona					= doc.get('idZona')
				idVigilancia			= doc.get('idVigilancia')
				idAlarmaBotonPanico		= doc.get('idPanico')
				datosJson = leerArchivoJsonData(identificadorSolicitud)
				identificadorImagenIsabu = leerArchivoImagen(identificadorSolicitud)
				idDoc = False
				if datosJson != False and identificadorImagenIsabu != False:
					datosJson[0] = parser.parse(datosJson[0]).astimezone(settings.EST).isoformat()[0:19] 
					#Funcion que busca la ultima posicion del vehiculo segun la fecha de creacion del json
					posicion = posicionImagenTomada(datosJson[0], idVehiculo)
					if esDirecta:
						#si se toma directamente la imagen desde el boton capturarImagen   
						#guarda el documento capturaImagenes segun el tenant
						print "Guarda imagen directa"
						idDoc = guardarDocumentoCapturaImagenes(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu) 
                                                print "este es el ide del doc"
                                                print idDoc
                                                #Modifica el estado de pendiente a entregado
                                                if idDoc != False:
                                                    modificarEstadoDocumentoInspeccionImagen(identificadorSolicitud)
                                                    idDoc = False
					else:
						if esPanico:
							#guarda la imagen de un boton de panico
							idDoc = guardarDocumentoCapturaImagenesBotonPanico(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu, idAlarmaBotonPanico) 
							print idDoc
						else:
							# se Modifica el estado de pendiente a entregado y se 
							#guarda en el documento capturaImagenesZonaAlarma 
							#y tambien se guarda el idZona completo 
							# se Modifica el estado de pendiente a entregado y se 
							#guarda en el documento imagenesProgramacionVigilancia 
							#y tambien se guarda el programacionVigilancia=[] completo
							if idZona!=[]:
								print "Guarda imagen de zonas"
								idDoc = guardarDocumentoCapturaImagenesZonaAlarma(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu, idZona) 
								print idDoc
							if idVigilancia!=[]:
								print "Guarda imagen programacion vigilancia"
								idDoc = guardarDocumentoImagenesProgramacionVigilancia(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu, idVigilancia)
								print idDoc               
						#Modifica el estado de pendiente a entregado
						if idDoc != False:
							modificarEstadoDocumentoInspeccionImagen(identificadorSolicitud)
							idDoc = False
				else:
					print "El GPS no ha generado la solicitud " + identificadorSolicitud
		except ValueError:
			pass

def posicionImagenTomada(fechaCreacion, idVehiculo):
	posicion = {}
	fechaHoraActual = datetime.now().isoformat()
	tenants = buscarTenants()
	for tenant in tenants:
		posicion = buscarVehiculoRangoFechas1(tenant,fechaCreacion, fechaHoraActual, idVehiculo)
                if posicion["latitud"] == "" and posicion["longitud"] == "":
                    posicion = buscarVehiculoRangoFechas2(tenant,fechaCreacion, fechaHoraActual, idVehiculo)
	return posicion

def buscarVehiculoRangoFechas1(tenant,fechaCreacion, fechaHoraActual, idVehiculo):
	print "-----------------------------------"
	print tenant
	print fechaCreacion
	print fechaHoraActual
	print idVehiculo
	db = conexion.getConexionTenant(tenant)
	posicion = {}
	#fechaCreacion 	= parser.parse(fechaCreacion).astimezone(settings.EST).isoformat()
	#fechaCreacion  	= fechaCreacion[0:19]
	fechaHoraActual	= fechaHoraActual[0:19]
	posicion["latitud"]  = ""
	posicion["longitud"] = ""
	if db == None:
		print "No existe bd"
	try:
		logging.warning("BUscando {} {} fecha actual {}".format(fechaCreacion, idVehiculo, fechaHoraActual))
		filas = db.view('_design/posicionVehiculos/_view/posicionFechaCreacion',
                    include_docs  = True, 
                    startkey = [idVehiculo, fechaCreacion],
                    		limit = 1)
		for fila in filas:
		    key 					= 	fila.key
		    value 					= 	fila.value
		    doc 					= 	fila.doc
		    posicion["latitud"]		= 	doc.get('latitud',"")
		    posicion["longitud"]	=	doc.get('longitud',"")
		return posicion
	except ValueError:
		print "error"


def buscarVehiculoRangoFechas2(tenant,fechaCreacion, fechaHoraActual, idVehiculo):
	db = conexion.getConexionTenant(tenant)
	posicion = {}
	#fechaCreacion 	= parser.parse(fechaCreacion).astimezone(settings.EST).isoformat()
	#fechaCreacion  	= fechaCreacion[0:19]
	fechaHoraActual	= fechaHoraActual[0:19]
        posicion["latitud"]  = ""
        posicion["longitud"] = ""
	if db == None:
		print "No existe bd"
	try:
		logging.warning("BUscando {} {} fecha actual {}".format(fechaCreacion, idVehiculo, fechaHoraActual))
		filas = db.view('_design/posicionVehiculos/_view/posicionFechaCreacion',
                    include_docs  = True, 
                    startkey = [idVehiculo, fechaCreacion],
                    		limit = 1,
                    		descending    = True)
		for fila in filas:
		    key 					= 	fila.key
		    value 					= 	fila.value
		    doc 					= 	fila.doc
		    posicion["latitud"]		= 	doc.get('latitud',"")
		    posicion["longitud"]	=	doc.get('longitud',"")
		return posicion
	except ValueError:
		print "error"
                

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
			key 					= fila.key
			value 					= fila.value
			doc 					= fila.doc
			urlTenant 				= doc.get('urlTenant')		
			listaTenants.append(urlTenant)
		return listaTenants
	except ValueError:
		pass


def leerArchivoJsonData(identificadorSolicitud):
	datosJson = [0,0,0]
	#rutaJson	= "/home/eduardo/Documentos/fleetbiImagenesGPS/{}.json".format(str(identificadorSolicitud))
	rutaJson	= settings.RUTA_ARCHIVO_JSON.format(str(identificadorSolicitud))
	print rutaJson
	print os.path.exists(rutaJson)
	if os.path.exists(rutaJson):
		#file      = open(u"/home/eduardo/Documentos/fleetbiImagenesGPS/{}.json".format(str(identificadorSolicitud)), 'r')
		file      = open(u""+settings.RUTA_ARCHIVO_JSON.format(str(identificadorSolicitud)), 'r')
		contenido = file.read()
		marc      = json.loads(contenido)
		dataMarc  = marc.get("capturaImagen",[])
		for item in dataMarc:
			creadoEn = item.get("creadoEn")
			latitud = item.get("latitud")
			longitud = item.get("longitud")
		datosJson[0] = creadoEn 
		print datosJson
		return datosJson
	else:
		return False

def leerArchivoImagen(identificadorSolicitud):
	#rutaImagen	= "/home/eduardo/Documentos/fleetbiImagenesGPS/{}.jpg".format(str(identificadorSolicitud))
	rutaImagen	= settings.RUTA_ARCHIVO_JPG.format(str(identificadorSolicitud))
	if os.path.exists(rutaImagen):
		#file = open(u"/home/eduardo/Documentos/fleetbiImagenesGPS/{}.jpg".format(str(identificadorSolicitud)), 'r')
		file = open(u""+settings.RUTA_ARCHIVO_JPG.format(str(identificadorSolicitud)), 'r')
		return nisabuUtils.guardarImagenFile(file)
	else:
		return False 

def guardarDocumentoCapturaImagenes(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu):
	db = conexion.getConexionTenant(tenant)
	if db == None:
		#return { 'success' : False, 'mensaje': "existe el bd" }	
		return False
	doc_id, doc_rev = db.save({
		"tipoDato"			: "capturaImagenes",
		"creadoEn"			: datosJson[0],  
		"modificadoEn"		: datetime.now().isoformat(),
		"modificadoPor"		: "",
		"horaRegistrada"	: datetime.now().isoformat(),
		"latitud" 			: posicion["latitud"],
		"longitud"			: posicion["longitud"],
		"idVehiculo"		: idVehiculo,
		"idImagen"			: identificadorImagenIsabu,
		#"urlImagen"			: "http://localhost/nisabu/image/{}".format(str(identificadorImagenIsabu)),
		"urlImagen"			: settings.RUTA_ARCHIVO_NISABU.format(str(identificadorImagenIsabu)),
		"activo"			: True
    })
    
	return doc_id


def guardarDocumentoCapturaImagenesBotonPanico(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu, idAlarmaBotonPanico):
	db = conexion.getConexionTenant(tenant)
	if db == None:
		#return { 'success' : False, 'mensaje': "existe el bd" }	
		return False
	doc_id, doc_rev = db.save({
		"tipoDato"				: "capturaImagenesBotonPanico",
		"creadoEn"				: datosJson[0],  
		"modificadoEn"			: datetime.now().isoformat(),
		"modificadoPor"			: "",
		"horaRegistrada"		: datetime.now().isoformat(),
		"latitud" 				: posicion["latitud"],
		"longitud"				: posicion["longitud"],
		"idVehiculo"			: idVehiculo,
		"idImagen"				: identificadorImagenIsabu,
		"idAlarmaBotonPanico"	: idAlarmaBotonPanico,
		"activo"				: True
    })
    
	return doc_id


 
def guardarDocumentoCapturaImagenesZonaAlarma(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu, idZona):
	db = conexion.getConexionTenant(tenant)
	if db == None:
		#return { 'success' : False, 'mensaje': "existe el bd" }
		return False	
	doc_id, doc_rev = db.save({
		"tipoDato"			: "capturaImagenesZonaAlarma",
		"creadoEn"			: datosJson[0],  
		"horaRegistrada"	: datetime.now().isoformat(),
		"latitud" 			: posicion["latitud"],
		"longitud"			: posicion["longitud"],
		"idVehiculo"		: idVehiculo,
		"idImagen"			: identificadorImagenIsabu,
		"urlImagen"			: settings.RUTA_ARCHIVO_NISABU.format(str(identificadorImagenIsabu)),
		"activo"			: True,
		"zonaAlarmas"		: idZona
    })
    
	return doc_id
 
def guardarDocumentoImagenesProgramacionVigilancia(tenant, idVehiculo, datosJson, posicion, identificadorImagenIsabu, idVigilancia):
	db = conexion.getConexionTenant(tenant)
	if db == None:
		return { 'success' : False, 'mensaje': "existe el bd" }	
	doc_id, doc_rev = db.save({
		"tipoDato"			: "imagenesProgramacionVigilancia",
		"creadoEn"			: datosJson[0],  
		"horaRegistrada"	: datetime.now().isoformat(),
		"latitud" 			: posicion["latitud"],
		"longitud"			: posicion["longitud"],
		"idVehiculo"		: idVehiculo,
		"idImagen"			: identificadorImagenIsabu,
		"urlImagen"			: settings.RUTA_ARCHIVO_NISABU.format(str(identificadorImagenIsabu)),
		"activo"			: True,
		"idProgramacion"	: idVigilancia
    })
    
	return doc_id


def modificarEstadoDocumentoInspeccionImagen(idInspeccionImagen):
	dbFleet = conexion.getConexionFleet()
	docInspeccionImagen = dbFleet[idInspeccionImagen]
	docInspeccionImagen["estado"]	= "Entregado"
	#dbFleet[docInspeccionImagen.get("estado")] = "Entregado"
	dbFleet.save(docInspeccionImagen)
	print "modifica pendiente"


#==========================================================================

