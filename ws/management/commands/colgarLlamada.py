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
    	#Nota: No se ha hecho una prueba con una llamada Real
		#Buscar documento colgar 
    	#llamada si se encuentran las llamadas en curso
    	#Extraer el limite y el campo creadoEn del doc llamadas
    	# el limite debe estar en minutos
		tenants = buscarTenants()
		for tenant in tenants:
			colgarLlamadaEnCurso(tenant)


def colgarLlamadaEnCurso(tenant):
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	db = conexion.getConexionTenant(tenant)
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
		    activoPanico  	= doc.get('activoPanico') # si en algun momento se activo boton de panico
		    if razonLLamada == "zonaAlarma":
		    	if activoPanico:
		    		examinarLlamadaBotonPanico(idLlamada, limite, creadoEn, sidLlamada, db)
		    		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		    		#urlAudio			= "URL AUDIO"
		    		actualizarEstadocapturaAudioZonaAlarma(idLlamada, urlAudio, limite, db)
		    	else:	
		    		#cuelga la llamada de zonaAlarma si ya cumplio el limite
		    		examinarLlamadaZonaAlarma(idLlamada, limite, creadoEn, sidLlamada, db)
		    if razonLLamada == "programacionVigilancia":
		    	if activoPanico:
		    		examinarLlamadaBotonPanico(idLlamada, limite, creadoEn, sidLlamada, db)
		    		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		    		#urlAudio			= "URL AUDIO"
		    		actualizarEstadocapturaAudioProgramacionVigilancia(idLlamada, urlAudio, limite, db)
		    	else:	
		    		#cuelga la llamada de la profamacion vigilancia si ya cumplio el limite
		    		examinarLlamadaProgramacionVigilancia(idLlamada, limite, creadoEn, sidLlamada, db)
		    if razonLLamada == "zonaAlarmaProgramacionVigilancia":
		    	if activoPanico:
		    		examinarLlamadaBotonPanico(idLlamada, limite, creadoEn, sidLlamada, db)
		    		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		    		#urlAudio			= "URL AUDIO"
		    		actualizarEstadocapturaAudioZonaAlarma(idLlamada, urlAudio, limite, db)
		    		actualizarEstadocapturaAudioProgramacionVigilancia(idLlamada,urlAudio, limite, db)		    		
		    	else:	
		    		examinarLlamadaZAPVSimultanea(idLlamada, limite, creadoEn, sidLlamada, db)
		    if razonLLamada == "botonPanico":
		    	#si la llamada solo corresponde al boton de panico
		    	examinarLlamadaBotonPanico(idLlamada, limite, creadoEn, sidLlamada, db)	
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


def actualizarEstadoDocLlamadas(idLlamada, db):
	docLlamadas 			= db[idLlamada]
	docLlamadas["estado"]	= "Finalizado"
	db.save(docLlamadas) 

def actualizarEstadocapturaAudioZonaAlarma(idLlamada, urlAudio, limite, db):
    try:
        filas = db.view('_design/llamadas/_view/llamadacapturaAudioZA',
                    include_docs  = True, 
                    key = [idLlamada, "En curso"],
                    limit = 1)
        for fila in filas:
            key 	= fila.key
            value 	= fila.value
            docCapturaAudioZonaAlarma 	= fila.doc
            docCapturaAudioZonaAlarma["estado"]   	= "Finalizado"
            docCapturaAudioZonaAlarma["urlAudio"] 	= urlAudio
            docCapturaAudioZonaAlarma["duracion"] 	= limite
            db.save(docCapturaAudioZonaAlarma)
    except ValueError:
        return { 'success' : False}


def verificarLimiteLlamada(creadoEn, limite):
	#funcioque verifica si se paso o no el limite de la llamada para 
	#poderla colgar
	pasaLimite = False
	fechaHoraActual = datetime.now()
	horaRegistrada	= datetime.strptime(creadoEn, '%Y-%m-%dT%H:%M:%S.%f')
	#paso el valor del limite de minutos a segundos
	limiteSegundos 	= limite * 60
	restaHoras 		= fechaHoraActual - horaRegistrada
	if limiteSegundos <= restaHoras.seconds:
		pasaLimite	= True
	return pasaLimite


def examinarLlamadaZonaAlarma(idLlamada, limite, creadoEn, sidLlamada, db):
    #-- Inicio Twilio--
    #DESCOMENTAR
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	#-- Fin Twilio--
	pasaLimite = verificarLimiteLlamada(creadoEn, float(limite))
	if pasaLimite:
		#colgar llamada ZonaAlarma
		#cambia el estado a Finalizado del doc llamadas y del doc 
		#capturaAudioZonaAlarma usando el idLlamada
		#DESCOMENTAR
		terminarLlamada(client, sidLlamada) # Terminar llamada Twilio
		#Espera 15 segundos para que cargue por completo el archivo twilio y asi generar la url
		actualizarEstadoDocLlamadas(idLlamada, db)
		time.sleep(15)
		#DESCOMENTAR
		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		actualizarEstadocapturaAudioZonaAlarma(idLlamada, urlAudio, limite, db)
		print "Termina llamada"
		print idLlamada
		print "Url audio"
		#print urlAudio

	

def actualizarEstadocapturaAudioProgramacionVigilancia(idLlamada, urlAudio, limite, db):
    try:
        filas = db.view('_design/llamadas/_view/llamadacapturaAudioPV',
                    include_docs  = True, 
                    key = [idLlamada, "En curso"],
                    limit = 1)
        for fila in filas:
            key 	= fila.key
            value 	= fila.value
            docCapturaAudioProgramacionVigilancia 	= fila.doc
            docCapturaAudioProgramacionVigilancia["estado"] = "Finalizado"
            docCapturaAudioProgramacionVigilancia["urlAudio"] = urlAudio
            docCapturaAudioProgramacionVigilancia["duracion"] = limite
            db.save(docCapturaAudioProgramacionVigilancia)
    except ValueError:
    	return "Problemas para actualizar "


def examinarLlamadaProgramacionVigilancia(idLlamada, limite, creadoEn, sidLlamada, db):
    #-- Inicio Twilio--
    #DESCOMENTAR
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	#-- Fin Twilio--
	pasaLimite = verificarLimiteLlamada(creadoEn, float(limite))
	if pasaLimite:
		#colgar llamada Programacion vigilancia
		#cambia el estado a Finalizado del doc llamadas y del doc 
		#audioProgramacionVigilancia usando el idLlamada
		#DESCOMENTAR
		terminarLlamada(client, sidLlamada) # Terminar llamada Twilio 
		time.sleep( 15 )
		actualizarEstadoDocLlamadas(idLlamada, db)
		#Espera 15 segundos para que cargue por completo el archivo twilio y asi generar la url
		time.sleep(15)
		#DESCOMENTAR
		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		actualizarEstadocapturaAudioProgramacionVigilancia(idLlamada, urlAudio, limite, db)
		print "Termina llamada"
		print idLlamada
		print "Url audio"
		#print urlAudio

def terminarLlamada(client, sid):
    call = client.calls.update(sid, status="completed")

#Obtiene la url del audio
def consultarUrlGrabacion(callSid, client):
    call = client.calls.get(callSid)
    accountSid = call.account_sid
    if len(call.recordings.list()) > 0:
        recording = call.recordings.list()[0]
        recording = client.recordings.get(sid = recording.sid)
        return "https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Recordings/{RecordingSid}".format(AccountSid = accountSid, RecordingSid = recording.sid)
    else:
        return ""



def examinarLlamadaZAPVSimultanea(idLlamada, limite, creadoEn, sidLlamada, db):
    #-- Inicio Twilio--
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	#-- Fin Twilio--
	pasaLimite = verificarLimiteLlamada(creadoEn, float(limite))
	if pasaLimite:
		#colgar llamada ZonaAlarma
		#cambia el estado a Finalizado del doc llamadas y del doc 
		#capturaAudioZonaAlarma usando el idLlamada
		#DESCOMENTAR PARA QUE FUNCIONE
		terminarLlamada(client, sidLlamada) # Terminar llamada Twilio
		#Espera 15 segundos para que cargue por completo el archivo twilio y asi generar la url
		actualizarEstadoDocLlamadas(idLlamada, db)
		time.sleep(15)
		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		actualizarEstadocapturaAudioZonaAlarma(idLlamada, urlAudio, limite, db)
		actualizarEstadocapturaAudioProgramacionVigilancia(idLlamada,urlAudio, limite, db)
		print "Termina llamada"
		print idLlamada
		print "Url audio"
		print urlAudio

def actualizarEstadocapturaAudioBotonPanico(idLlamada, urlAudio, db):
    try:
        filas = db.view('_design/llamadas/_view/llamadacapturaBotonPanico',
                    include_docs  = True, 
                    key = [idLlamada, "En curso"])
        for fila in filas:
            key 	= fila.key
            value 	= fila.value
            docCapturaAudioBotonPanico 	= fila.doc
            docCapturaAudioBotonPanico["estado"] = "Finalizado"
            docCapturaAudioBotonPanico["urlAudio"] = urlAudio
            db.save(docCapturaAudioBotonPanico)
    except ValueError:
    	return "Problemas para actualizar "



def examinarLlamadaBotonPanico(idLlamada, limite, creadoEn, sidLlamada, db):
    #-- Inicio Twilio--
	account_sid     = settings.TWILIO_ACCOUNT_SID 
	auth_token      = settings.TWILIO_AUTH_TOKEN 
	client      = TwilioRestClient(account_sid, auth_token)
	#-- Fin Twilio--
	pasaLimite = verificarLimiteLlamada(creadoEn, float(limite))
	if pasaLimite:
		#colgar llamada ZonaAlarma
		#cambia el estado a Finalizado del doc llamadas y del doc 
		#capturaAudioZonaAlarma usando el idLlamada
		#DESCOMENTAR PARA QUE FUNCIONE
		terminarLlamada(client, sidLlamada) # Terminar llamada Twilio
		#Espera 15 segundos para que cargue por completo el archivo twilio y asi generar la url
		actualizarEstadoDocLlamadas(idLlamada, db)
		#time.sleep(15)
		urlAudio            = consultarUrlGrabacion(sidLlamada, client)
		#urlAudio			= "URL AUDIO"
		actualizarEstadocapturaAudioBotonPanico(idLlamada, urlAudio, db)
		print "Termina llamada"
		print idLlamada
		print "Url audio"
		print urlAudio