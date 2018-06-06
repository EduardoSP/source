# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from ..autenticacion          import autenticacion as moduloAutenticacion
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from twilio.rest import TwilioRestClient
from dateutil import parser
from datetime import datetime
import time
from motionless import CenterMap
from motionless import DecoratedMap, AddressMarker
from audioBotonPanico import ejecutarGuardarAudioBotonPanico
import locale
import geocoder
import requests
import json
from dateutil import parser
import pytz
import requests
import json
import pytz
from  ws.serviciosweb.modulos.notificaciones.notificaciones import notificarTenant
#locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

def enviarSMS(client, destino, origen, texto):
	try:
		mensaje = client.messages.create(to = destino, from_= origen,
	                                 body = texto)                         
	except Exception, e:
		raise e


def obtenerinfoVehiculo(identificadorGPS):
    #obtiene el id de vehiculo segun el numero del identificador del GPS"[idVehiculo, tenant]"
    infoVehiculo = [0,0]
    infoVehiculo[0] = ""
    dbFleet = conexion.getConexionFleet()
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view('_design/GPS/_view/idVehiculoGPS',
                    include_docs  = True, 
                    startkey = [identificadorGPS, 0],
                    endkey = [identificadorGPS, {}])

        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            infoVehiculo[0] = doc.get('idVehiculo')
            infoVehiculo[1] = doc.get('tenant')
        return infoVehiculo
    except :
        pass

def buscarCelEmergenciaCorreoTenant(nombreTenant):
    dbFleet = conexion.getConexionFleet()
    infoContacto = [0,0]
    celularEmergencia = ""
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view('_design/tenantPorTenant/_view/tenantPorTenant',
                    include_docs  = True, 
                    key = [nombreTenant])

        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            infoContacto[0] 	= doc.get('celularEmergencia')
            infoContacto[1]		= doc.get('correo')    
        return infoContacto

    except :
        pass

    return { 'success' : False}


def envioGodaddy(correo, mensaje, asunto, remitente):
    correoRemitente = remitente

    fromaddr = correoRemitente
    toaddrs  = correo
    message  = u"""From: <%s>                                                                                                                              
To: <%s>                                                                                                                                                   
MIME-Version: 1.0                                                                                                                                          
Content-type: text/html; charset=UTF-8                                                                                                                     
Subject: %s                                                                                                                                                
%s                                                                                                                                                         
""" % (fromaddr, toaddrs, asunto, mensaje)
    username = settings.CORREO_USUARIO
    password = settings.CORREO_CONTRASENA
    #server = smtplib.SMTP('smtp.gmail.com:587')                                                                                                           
    #server = servers.get(username)
    
    #    print "repitiendo3"
    server = smtplib.SMTP_SSL(settings.CORREO_SMTP, settings.CORREO_PUERTO)
    server.login(username,password)
    #servers[username] = server
    #server.sendmail(fromaddr, toaddrs, msg)                                                                                                               
    server.sendmail(fromaddr, toaddrs, message.encode('utf8'))
    #server.quit()                                                                                                                                         


def enviarLlamadaConVoz(client, destino, origen, placa, nombreTenant):
    pass
    call = client.calls.create(url="{}/webfleetbigui/{}/llamada/{}".format(settings.RUTA_BASE_FLEETBI, str(nombreTenant), str(placa)),
        to=destino,
        from_= origen, record=True)
    return call.sid


#==================================================
def solicitarTomarFoto(idFoto, rutaFoto, idGps):
    # se solicita la toma de la captura al GPS
    try:
        peticion = {
            "autenticacion" : {  
                "usuario" : "gps",     "token"   : "123456"  
            }, 
            "data" : {  
                "idFoto"   : idFoto,       
                "rutaFoto" : rutaFoto,       
                "idGps"    : idGps   
            } 

        } 

        datos ={"request": json.dumps(peticion) }

        cabeceras = {
           "Content-Type" : "application/x-www-form-urlencoded"
            }
        url = settings.URL_SOLICITAR_FOTO
        response = requests.post(url, data=datos, headers=cabeceras)
        print response.text
    except requests.exceptions.RequestException as e:
        print e


def wslistadoGPS(idVehiculo):
    datosGPS = ["",""]
    dbFleet = conexion.getConexionFleet()
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view('_design/GPS/_view/GPS',
                    include_docs  = True, 
                    startkey = [idVehiculo, 0],
                    endkey = [idVehiculo, {}])

        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            identificadorGPS = doc.get('identificadorGPS') 
            datosGPS[0] = doc.get('identificadorGPS') 
            datosGPS[1] = doc.get('tenant')      
        return datosGPS

    except :
        pass

    return { 'success' : False}


def tomarCapturasfotoBotonPanico(peticion, idVehiculo, idPanico):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    dbFleet = conexion.getConexionFleet()

    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:     
        #consulta vista para extraer el identificador del GPS
        datosGPS    =   wslistadoGPS(idVehiculo)
        if datosGPS[0] != "" and datosGPS[1] != "":     
            doc_id, doc_rev = dbFleet.save({
                "tipoDato"              :   "inspeccionImagen",
                "fechaHoraSolicitud"    :   datetime.now().isoformat(),  
                "estado"                :   "pendiente",
                "identificadorGPS"      :   datosGPS[0],
                "idVehiculo"            :   idVehiculo,
                "esDirecta"             :   False,
                "esPanico"           	: 	True, 
                "idZona"                :   [],
                "idVigilancia"          :   [],
                "idPanico"              :   idPanico,
                "tenant"                :   datosGPS[1],
                "activo"                :   True
            })

            #crear el documento inspeccionImagen
            #Se llama a la funcion de node para que me genere la imagen el GPS
            idFoto = doc_id
            #Llamar a ws para que el GPS tome la foto
            rutaCreacion = settings.GPS_RUTA_FOTO
            solicitarTomarFoto(idFoto, rutaCreacion, datosGPS[0]) 
        else:
            doc_id = "El vehiculo no tiene un GPS asociado"           
        return {
            'success' : True, 
            'data'    : {
                'id' : doc_id
            }              
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


def registrarDocalarmasBotonPanico(peticion, latitud, longitud, idVehiculo):
    #funcion que guarda el documento en la bd boton de panico
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:        
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        #logging.warning("GOOD!!")
        doc_id, doc_rev = db.save({
            "tipoDato"              : "alarmasBotonPanico",
            "creadoEn"              : datetime.now().isoformat(),  
            "modificadoEn"          : "",
            "modificadoPor"         : "",
            "horaRegistrada"        : datetime.now().isoformat(),
            "latitud"               : latitud,
            "longitud"              : longitud,
            "idVehiculo"            : idVehiculo,
            "activo"                : True,
            "timeStamp"             : time.time()      
        })
        docVehiculo = db[idVehiculo]
        placa       = docVehiculo["placa"]         
        notificarTenant(tenant, "alarma", u"El vehículo {} activó el botón de pánico".format(placa))
        return doc_id
    except ValueError:
        logging.warning("GOOD!")
        pass


#==================================================


def registrarBotonPanicoGPS(peticion):
    autenticacion 		= peticion['autenticacion']
    datos         		= peticion['data']
    usuario       		= autenticacion['usuario']
    tenant      		= autenticacion['tenant']
    db 					= conexion.getConexionTenant(tenant)  
    account_sid     = settings.TWILIO_ACCOUNT_SID 
    auth_token      = settings.TWILIO_AUTH_TOKEN
    identificadorGPS	= datos['identificadorGPS']
    #se consulta el id del vehiculo
    infoVehiculo        = obtenerinfoVehiculo(identificadorGPS)
    idVehiculo		= infoVehiculo[0]
    tenantVehiculo      = infoVehiculo[1]
    db                  = conexion.getConexionTenant(tenantVehiculo)  
    docUltimaPosicion   = getUltimaPosicionVehiculo(idVehiculo, db)
    peticion['autenticacion']["tenant"] = tenantVehiculo
    if idVehiculo != "":
        nombreTenant		= infoVehiculo[1]
        docVehiculo  		= db[idVehiculo]
        placaVehiculo           = docVehiculo["placa"]
        
        # latitud			= datos['latitud']
        # longitud		= datos['longitud']
        # horaRegistrada		= datos['horaRegistrada']
        # velocidad		= datos['velocidad']

        latitud			= docUltimaPosicion.get("latitud", 0)
        longitud		= docUltimaPosicion.get("longitud", 0)
        horaRegistrada		= docUltimaPosicion.get("horaRegistrada", "")
        velocidad		= docUltimaPosicion.get("velocidad", 0)
        
        
        #fechaParse 			= parser.parse(horaRegistrada).astimezone(settings.EST).strftime("%A %d de %B %Y %I:%M %p")
        fechaParse 			= parser.parse(horaRegistrada).strftime("%A %d de %B %Y %I:%M %p")
        g 					= geocoder.google([float(latitud), float(longitud)], method='reverse')

        direccionCaptada 	= g.address
        infoContacto		= buscarCelEmergenciaCorreoTenant(nombreTenant)
        celularEmergencia 	= infoContacto[0]
        correoTenant        = infoContacto[1]
        #Permiso 17 llamada automatica boton de panico
        llamadaAutomaticaBotonPanico = evaluarPermisosFleetBi(docVehiculo, "17")
        #Permiso 18 Mensaje automatico SMS botón de panico
        enviaSmsAutomatico           = evaluarPermisosFleetBi(docVehiculo, "18")
        if llamadaAutomaticaBotonPanico or enviaSmsAutomatico:
            client = TwilioRestClient(account_sid, auth_token)
        if enviaSmsAutomatico:
            mensajeTexto		= settings.MENSAJE_TEXTO_PARTE_UNO+str(placaVehiculo)+settings.MENSAJE_TEXTO_PARTE_DOS+"Latitud: "+str(latitud)+" y Longitud: "+str(longitud)+". "+str(fechaParse).decode("utf8")
            enviarSMS(client, celularEmergencia,  settings.NUM_TWILIO_SMS, mensajeTexto)
        asuntoCorreo 	= settings.CORREO_ASUNTO+str(placaVehiculo)+" "+ fechaParse.decode("utf8")
        mensajeCorreo 	= u"<h2>{}  Latitud {}  y Longitud {}, direccion {}</h2>".format(settings.CORREO_MENSAJE,str(latitud),str(longitud), u"{}".format(direccionCaptada))
        #DESCOMENTAR PARA ENVIAR EMAIL
        #envioGodaddy(correoTenant, mensajeCorreo, asuntoCorreo, settings.CORREO_USUARIO)	
        #DESCOMENTAR PARA HACER LLAMADA BOTON DE PANICO
        if llamadaAutomaticaBotonPanico:
            placa = str(placaVehiculo).lower() #Twilio reconoce el audio solo en minusculas
            enviarLlamadaConVoz(client, celularEmergencia, settings.TWILIO_NUMERO, placa , nombreTenant)
        #linea para solicitar la captura de una foto
        #================================================================
        #toma captura audio
        idPanico = registrarDocalarmasBotonPanico(peticion, latitud, longitud, idVehiculo)
        for i in range(settings.CANT_FOTOS_A_TOMAR):
            #DESCOMENTAR PARA QUE FUNCIONE
            #Permiso 11 tomar foto boton de panico
            tomaFotos = evaluarPermisosFleetBi(docVehiculo, "11")
            if tomaFotos:
                tomarCapturasfotoBotonPanico(peticion, idVehiculo, idPanico)
        #================================================================
        #permiso 12 grabar audio boton de panico
        grabaAudio = evaluarPermisosFleetBi(docVehiculo, "12")
        if grabaAudio:
            ejecutarGuardarAudioBotonPanico(peticion, latitud, longitud, horaRegistrada, idVehiculo, idPanico)
        return {
        	'success' : True, 
        	'data'    : {
        			'id' : "enviado"
        	}              
        }


def getUltimaPosicionVehiculo(idVehiculo, dbTenant):

    resultado = None
    
    filas = dbTenant.view(
        '_design/posicionVehiculos/_view/posicionFechaCreacion',
        startkey      = [idVehiculo, {}],
        endkey        = [idVehiculo, 0],
        include_docs  = True,
        descending    = True,
        limit         = 1

    )
    for fila in filas:
        resultado = fila.doc

    return resultado
    
#valida si el vehiculo tiene el permiso 11 tomar foto boton panico y 12 grabar audio boton panico, 17 llamada automatica y 18 mensaje automatico
def evaluarPermisosFleetBi(docVehiculo, numPermiso):
    respuesta = False
    try:
        opcionesAdicionalesPlataforma = docVehiculo.get("opcionesAdicionalesPlataforma", None)
        if not(opcionesAdicionalesPlataforma == None):
			if numPermiso in opcionesAdicionalesPlataforma:
				respuesta = True
        return respuesta
    except:
        print "error del try "

