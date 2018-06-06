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


def colgarLlamadasEnCurso(tenant):
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	db = conexion.getConexionTenant(tenant)
	idLlamada  = ""
	sidLlamada = ""
	estado = ""
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
    			docLlamada             = db[idLlamada]
    			docLlamada["estado"]   = "Finalizado"
    			db.save(docLlamada) 
    			print "termina llamada"
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
