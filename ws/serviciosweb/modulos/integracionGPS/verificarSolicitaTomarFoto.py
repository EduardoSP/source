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

#==============================================================
#Verifica tomar fotos Zonas Alarmas
def buscarCantidadCapturasZonaAlarmasPendientes(idVehiculo, idzonaAlarma ):
	#funcion para buscar las imagenes pendientes segun la zonaAlarma
	#bd fleetbi
	dbFleet = conexion.getConexionFleet()
	cantFotosPendientesNoDirectas = 0
	if dbFleet == None:
		return { 'success' : False, 'mensaje': "existe el bd" }
	try:
		dataRaw = {}
		filas = dbFleet.view('_design/inspeccionGPS/_view/imagenesNoDirectasPendientesVehiculo',
		            include_docs  = True,
		            key = [idVehiculo])
		for fila in filas:
			key 					= fila.key
			value 					= fila.value
			doc 					= fila.doc
			idZonasDoc 				= doc.get('idZona')
			for idZonaDoc in idZonasDoc:
				if idZonaDoc == idzonaAlarma:
					#FALTA si la foto esta en el rago de un 10 minutos contar como pendiente si no no contar
					cantFotosPendientesNoDirectas += 1
		return cantFotosPendientesNoDirectas
	except ValueError:
		pass


def buscarCantidadCapturasZonaAlarmaTomadas(peticion, idVehiculo, idzonaAlarma):
	autenticacion = peticion['autenticacion']
	datos         = peticion['data']
	usuario       = autenticacion['usuario']
	tenant      = autenticacion['tenant']
	db = conexion.getConexionTenant(tenant)
	cantFotosTomadas = 0
	if db == None:
		return { 'success' : False, 'mensaje': "existe el bd" }
	try:
		dataRaw = {}
		filas = db.view('_design/vigilancias/_view/imagenesZonaAlarmaPorVehiculo',
		            include_docs  = True,
		            key = [idVehiculo])
		for fila in filas:
			key 					= fila.key
			value 					= fila.value
			doc 					= fila.doc
			idZonasDoc 				= doc.get('zonaAlarmas')
			for idZonaDoc in idZonasDoc:
				if idZonaDoc == idzonaAlarma:
					cantFotosTomadas += 1
		return cantFotosTomadas
	except ValueError:
		pass
#==============================================================


#===============================================================
#Verifica tomar fotos Programacion vigilancia
def buscarCantidadCapturasPVPendientes(idVehiculo, idProgramacionVigilancia ):
	#funcion para buscar las imagenes pendientes segun la zonaAlarma
	#bd fleetbi
	dbFleet = conexion.getConexionFleet()
	cantFotosPendientesNoDirectas = 0
	if dbFleet == None:
		return { 'success' : False, 'mensaje': "existe el bd" }
	try:
		dataRaw = {}
		filas = dbFleet.view('_design/inspeccionGPS/_view/imagenesNoDirectasPendientesVehiculo',
		            include_docs  = True,
		            key = [idVehiculo])
		for fila in filas:
			key 					= fila.key
			value 					= fila.value
			doc 					= fila.doc
			idPVSDoc 				= doc.get('idVigilancia')
			for idPVDoc in idPVSDoc:
				if idPVDoc == idProgramacionVigilancia:
					cantFotosPendientesNoDirectas += 1
		return cantFotosPendientesNoDirectas
	except ValueError:
		pass


def buscarCantidadCapturasPVTomadas(peticion, idVehiculo, idProgramacionVigilancia):
	autenticacion = peticion['autenticacion']
	datos         = peticion['data']
	usuario       = autenticacion['usuario']
	tenant      = autenticacion['tenant']
	db = conexion.getConexionTenant(tenant)
	cantFotosTomadas = 0
	if db == None:
		return { 'success' : False, 'mensaje': "existe el bd" }
	try:
		dataRaw = {}
		filas = db.view('_design/vigilancias/_view/imagenesProgramacionVigilanciaPorVehiculo',
		            include_docs  = True,
		            key = [idVehiculo])
		for fila in filas:
			key 							= fila.key
			value 							= fila.value
			doc 							= fila.doc
			idProgramacionVigilanciasDoc	= doc.get('idProgramacion')
			for idPVDoc in idProgramacionVigilanciasDoc:
				if idPVDoc == idProgramacionVigilancia:
					cantFotosTomadas += 1
		return cantFotosTomadas
	except ValueError:
		pass		

#===============================================================


def solicitaTomarFotoZonaAlarma(peticion, idVehiculo, identificadorGPS,zonaAlarmas):
	#Listo
	respuesta			= False
	cantFotosPendientes = 0
	cantFotosTomadas	= 0
	numeroCapturasMax	= 0
	#algoritmo
	#1. traer numeroCapturasMax del doc monitoreoZonas
	autenticacion   = peticion['autenticacion']
	usuario         = autenticacion['usuario']
	tenant          = autenticacion['tenant']
	db              = conexion.getConexionTenant(tenant)
	#valida si el vehiculo tiene el permiso 13 "Imagen zona alarma" para tomar foto
	permisoTomarFotoZA = validaPermisoTomarFotoZA(db, idVehiculo)
	if permisoTomarFotoZA:
		for idzonaAlarma in zonaAlarmas:
			docZonaAlarma			= db[idzonaAlarma]
			idMonitoreoZona			= docZonaAlarma["idZona"]
			docMonitoreoZonas		= db[idMonitoreoZona]
			if docMonitoreoZonas["numeroCapturasMax"] !="":
				numeroCapturasMax		+= int(docMonitoreoZonas["numeroCapturasMax"])
			#2. traer las capturas pendientes del vehiculo y verificarlo si hace parte del monitoreo zonas y llevar un conteo
			cantFotosPendientes 	+= buscarCantidadCapturasZonaAlarmasPendientes(idVehiculo, idzonaAlarma)
			# numeroCapturasMax del documento monitoreo zonas	
			cantFotosTomadas 		+= buscarCantidadCapturasZonaAlarmaTomadas(peticion, idVehiculo, idzonaAlarma)
		totalSolicitudes = cantFotosPendientes + cantFotosTomadas
		if totalSolicitudes < numeroCapturasMax:
			respuesta = True 
	return respuesta
	
	

def solicitaTomarFotoProgramacionVigilancia(peticion, idVehiculo, identificadorGPS, programacionVigilancias):
	#Editando
	respuesta			= False
	cantFotosPendientes = 0
	cantFotosTomadas	= 0
	numeroCapturasMax	= 0
	#algoritmo
	#1. traer numeroCapturasMax del doc monitoreoZonas
	autenticacion   = peticion['autenticacion']
	usuario         = autenticacion['usuario']
	tenant          = autenticacion['tenant']
	db              = conexion.getConexionTenant(tenant)
	for idProgramacionVigilancia in programacionVigilancias:
		docPV			= db[idProgramacionVigilancia]
		if docPV["capturasMax"]!="":
			numeroCapturasMax		+= int(docPV["capturasMax"])
		#2. traer las capturas pendientes del vehiculo y verificarlo si hace parte del pv y llevar un conteo
		cantFotosPendientes 	+= buscarCantidadCapturasPVPendientes(idVehiculo, idProgramacionVigilancia)
		# numeroCapturasMax del documento programacion vigilancia	
		cantFotosTomadas 		+= buscarCantidadCapturasPVTomadas(peticion, idVehiculo, idProgramacionVigilancia)
	print "fotos tomadasssssssss"
	print cantFotosTomadas
	print "fotos pendientessssssss"
	print cantFotosPendientes
	print "num capturas maxxxx"
	print numeroCapturasMax
	totalSolicitudes = cantFotosPendientes + cantFotosTomadas
	if totalSolicitudes < numeroCapturasMax:
	   	respuesta = True 
	print "respuesta esssssss"
	print respuesta   	
	return respuesta


#valida si el vehiculo tiene el permiso 13 Imagen zona alarma para tomar foto
def validaPermisoTomarFotoZA(db, idVehiculo):
	numPermiso = "13" #captura imagen za
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

