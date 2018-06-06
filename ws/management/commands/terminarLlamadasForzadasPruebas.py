from django.core.management.base import NoArgsCommand
from django.conf              import settings
from ws.serviciosweb.modulos.conexion import conexion
from datetime                 import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
from twilio.rest import TwilioRestClient
import time
# -*- encoding: utf-8 -*- 
#==========================================================================
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
		tenants = buscarTenants()
		for tenant in tenants:
			colgarLlamadasEnCurso(tenant)

def evaluarLimiteForzado(creadoEn, tiempoForzado):
	colgarLlamada = False
	horaActual = datetime.now()
	horaRegistradaLlamada = datetime.strptime(creadoEn, '%Y-%m-%dT%H:%M:%S.%f')
	horaRegistradaActual  = datetime.strptime(str(horaActual), '%Y-%m-%d %H:%M:%S.%f')
	#diferenciaHoras 		= horaRegistradaActual - horaRegistradaLlamada	
	diferenciaHoras = horaRegistradaActual - horaRegistradaLlamada
	diferenciaHorasS = str(diferenciaHoras)
	splitDiferenciaHoras = diferenciaHorasS.split(":")
	if int(splitDiferenciaHoras[1]) == 0 or int(splitDiferenciaHoras[1]) >= tiempoForzado: #minutos es mayor que el tiempo forzado 
		colgarLlamada = True
	return colgarLlamada


def colgarLlamadasEnCurso(tenant):
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	db = conexion.getConexionTenant(tenant)
	idLlamada  = ""
	sidLlamada = ""
	estado = ""
	tiempoForzado = 2 # limite para terminar la llamada forzada version pruebas
	if db == None:
		print "No existe bd"
	try:
		filas = db.view('_design/llamadas/_view/llamadasEnCurso',
		            include_docs  = True, 
                    key      = ["En curso"])
		for fila in filas:
		    key 			= fila.key
		    value 			= fila.value
		    doc 			= fila.doc
		    idLlamada 		= doc.get('_id')
		    razonLLamada	= doc.get('razonLLamada')
		    limite			= doc.get('limite')
		    creadoEn		= doc.get('creadoEn')
		    sidLlamada		= doc.get('sidLlamada')
		    estado			= doc.get('estado')
    		if estado == "En curso":
    			colgarLlamada = evaluarLimiteForzado(creadoEn, tiempoForzado)
    			if colgarLlamada:
    				print "cuelga llamada"
	    			docLlamada             = db[idLlamada]
	    			docLlamada["estado"]   = "Finalizado Forzado pruebas paso limite definido"
	    			db.save(docLlamada) 
	    			print "termina llamada forzado paso limite definido"
	    			print sidLlamada	    
	    			terminarLlamada(client, sidLlamada) # Terminar llamada Twilio
	except ValueError as err:
		print err


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

def terminarLlamada(client, sid):
    call = client.calls.update(sid, status="completed")
