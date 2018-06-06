# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
import dateutil
from ..autenticacion          import autenticacion as moduloAutenticacion
from geopy.distance import vincenty

#busca el punto anterior del vehiculo
def traerPuntoAnterior(peticion, idVehiculo, limite):
    contador = 1
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    doc = None
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []
        filas = db.view('_design/posicionVehiculos/_view/anteriorPosicionVehiculo',
                    include_docs  = True,
                    startkey = [idVehiculo,{}],
                    endkey = [idVehiculo,0],
                    descending = True,
                    limit = limite)
        for fila in filas:
          key = fila.key
          value = fila.value
          if contador == limite:
          	doc = fila.doc
          contador += 1        
    except ValueError:
        pass
    return doc

def estanCercaLosPuntos(docPuntoAnterior, latitud, longitud, horaRegistrada):
	#Revisar si estan cerca
	nMetrosPorSegundo 		= settings.DISTANCIA_METROS #constante cambiara segun la necesidad

	metrosPorSegundo 		= 0
	latitudPAnterior  		= docPuntoAnterior.get('latitud')
	longitudPAnterior 		= docPuntoAnterior.get('longitud')
	horaRegistradaPAnterior = docPuntoAnterior.get('horaRegistrada')
	puntoInicial    		= (float(latitudPAnterior), float(longitudPAnterior))
	puntoFinal      		= (float(latitud), float(longitud))
	distanciaMetros 		=  vincenty(puntoInicial, puntoFinal).meters
	horaRegistradaPAnterior = horaRegistradaPAnterior[:16]+"Z"
	horaRegistrada 			= horaRegistrada[:16]+"Z"
	#horaRegistrada 			= horaRegistrada[:17] 
	horaRegistradaPAnterior = datetime.strptime(horaRegistradaPAnterior, '%Y-%m-%dT%H:%MZ')
	horaRegistrada 			= datetime.strptime(horaRegistrada, '%Y-%m-%dT%H:%MZ')
	diferenciaHoras 		= horaRegistrada - horaRegistradaPAnterior
	dias 	= diferenciaHoras.days
	minutos = diferenciaHoras.seconds / 60
	if minutos != 0:
		metrosPorSegundo = distanciaMetros / minutos 
	if dias == 0 and metrosPorSegundo <= nMetrosPorSegundo:
		return True #Estan cerca
	else:
		return False #Estan lejos

def tieneFragmentoParada(peticion, docPuntoAnterior):
	if docPuntoAnterior.get('idFragmentoParada') == "":
		return False
	else:
		return True


def juntarNamigos(peticion, idVehiculo, docPuntoAnterior, nAmigos):
	limite = 2
	amigosUnidos = []
	nAmigos -= 1
	amigosUnidos.append(docPuntoAnterior)
	docPuntoActual = docPuntoAnterior
	print "######################"
	print docPuntoActual.get("horaRegistrada")
	print"#######################"
	for i in range(nAmigos):
		docPuntoAnterior = traerPuntoAnterior(peticion, idVehiculo, limite)
		if docPuntoAnterior != None:
			estanCerca = estanCercaLosPuntos(docPuntoAnterior, docPuntoActual.get('latitud'), docPuntoActual.get('longitud'), docPuntoActual.get('horaRegistrada'))
			if estanCerca:
				resultFragmentoParada = tieneFragmentoParada(peticion, docPuntoAnterior)
				if not(resultFragmentoParada):		
					amigosUnidos.append(docPuntoAnterior)
					docPuntoActual = docPuntoAnterior
					limite += 1  
				else:
					break
	return amigosUnidos

def crearFragmentoParada(peticion, idVehiculo, amigosUnidos):
	latitudPromedio  	= 0
	longitudPromedio 	= 0
	latitudSuma 		= 0
	longitudSuma 		= 0
	for i in range(len(amigosUnidos)):
		docAmigo = amigosUnidos[i]
		latitudSuma  += float(docAmigo.get('latitud'))
		longitudSuma += float(docAmigo.get('longitud'))
	if len(amigosUnidos) != 0:
		latitudPromedio 	= latitudSuma /	len(amigosUnidos)
		longitudPromedio 	= longitudSuma / len(amigosUnidos)
	autenticacion = peticion['autenticacion']
	datos         = peticion['data']
	usuario       = autenticacion['usuario']
	tenant      = autenticacion['tenant']
	db = conexion.getConexionTenant(tenant)
	if db == None:
	    return { 'success' : False }
	try: 

	    doc_id, doc_rev = db.save({
	        "tipoDato"      	: "fragmentoParada",
	        "latitud"			: str(latitudPromedio),
	        "longitud"			: str(longitudPromedio),
	        "fechaHoraRegistro"	: datetime.now().isoformat(),
	        "idVehiculo"		: idVehiculo,
	        "idParada"			: "",  
	        "activo"        : True
	    })

	except ValueError:
	    pass
	return doc_id


def asignarFragmentoParada(peticion, amigosUnidos, doc_idFragmento):
	# se le asigna el identificador del fragmento a los amigos
	autenticacion = peticion['autenticacion']
	usuario       = autenticacion['usuario']
	tenant      = autenticacion['tenant']
	db = conexion.getConexionTenant(tenant)
	for i in range(len(amigosUnidos)):
		docAmigo = amigosUnidos[i]
		docIdAmigo = docAmigo.get('_id')
		docPosicionVehiculos = db[docIdAmigo]
		docPosicionVehiculos["idFragmentoParada"] = doc_idFragmento
		db.save(docPosicionVehiculos)


def evaluarParadaPuntoLast(docPuntoLast):
	if docPuntoLast.get('idParada') != "":
		return docPuntoLast.get('idParada') # si tiene parada el punto Last
	else:
		return ""


def asignarParadaTodosLosAmigos(peticion, doc_idParada, amigosUnidos, horaRegistradaUltimo):
	# se le asigna el identificador del fragmento a los amigos
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    idParada  	  =""
    db = conexion.getConexionTenant(tenant)
    for i in range(len(amigosUnidos)):
    	docAmigo = amigosUnidos[i]
    	docIdAmigo = docAmigo.get('_id')
    	docPosicionVehiculos = db[docIdAmigo]
    	docPosicionVehiculos["idParada"] = doc_idParada
    	idParada 	= doc_idParada
    	db.save(docPosicionVehiculos)
	#modifica la fecha fin cuando hay otra parada igual
	docParadas 					= db[doc_idParada]
	docParadas["fechahoraFin"]	= horaRegistradaUltimo
	db.save(docParadas)
	

def crearParada(peticion, fechahoraInicio ,fechahoraFin, latitud, longitud, idVehiculo):
	autenticacion = peticion['autenticacion']
	datos         = peticion['data']
	usuario       = autenticacion['usuario']
	tenant      = autenticacion['tenant']
	db = conexion.getConexionTenant(tenant)
	if db == None:
	    return { 'success' : False }
	try:
		fechahoraInicioFormateada = fechahoraInicio[:19]
		fechahoraFinFormateada    = fechahoraFin[:19]		
		fechahoraInicioDateTime = dateutil.parser.parse(fechahoraInicioFormateada)
		fechahoraFinDateTime    = dateutil.parser.parse(fechahoraFinFormateada)
		diferencia = (fechahoraFinDateTime-fechahoraInicioDateTime).total_seconds()
		doc_id, doc_rev = db.save({
	        "tipoDato"      	: "paradaVehiculo",
	        "latitud"			: latitud,
	        "longitud"			: longitud,
	        "fechahoraInicio"	: fechahoraInicio,
	        "fechahoraFin"		: fechahoraFin,
	        "idVehiculo"		: idVehiculo,
	        "duracionParadaSegundos":diferencia,
	        "activo"        : True
	    })
	      
	except ValueError:
	    pass
	return doc_id

def actualizarPosicionVehiculoParadas(peticion, doc_idPosicionVehiculo, idFragmentoParada, idParada):
    autenticacion 	= peticion['autenticacion']
    usuario       	= autenticacion['usuario']
    tenant      	= autenticacion['tenant']
    db 				= conexion.getConexionTenant(tenant)
    docPosicionVehiculos = db[doc_idPosicionVehiculo]
    docPosicionVehiculos["idParada"] 			= idParada
    docPosicionVehiculos["idFragmentoParada"]	= idFragmentoParada
    db.save(docPosicionVehiculos) 


#funcion principal
def evaluarParadas(peticion, latitud, longitud, idVehiculo, horaRegistrada):
	#nAmigos = 3 #esta constante se define deacuerdo a la necesidad nAmigos >=2
	nAmigos = settings.CANTIDAD_PUNTOS_UNIR #esta constante se define deacuerdo a la necesidad nAmigos >=2
	estanCerca = False
	doc_idFragmento = ""
	doc_idParada	= ""
	paradaPuntoLast = ""
	datos = [0,0]
	docPuntoAnterior = traerPuntoAnterior(peticion, idVehiculo, 1) #trae el ultimo punto anterior que esta guardado en la base de datos
	if docPuntoAnterior != None:
		#evaluo si el punto anterior esta cerca del que se va a guardar
		estanCerca = estanCercaLosPuntos(docPuntoAnterior, latitud, longitud, horaRegistrada)
		if estanCerca:
			resultFragmentoParada = tieneFragmentoParada(peticion, docPuntoAnterior)
			if not(resultFragmentoParada):
				amigosUnidos = juntarNamigos(peticion, idVehiculo, docPuntoAnterior,nAmigos)
				# si se juntaron los amigos
				#print "amigos"
				#print nAmigos
				#print len(amigosUnidos) -1 
				if nAmigos == (len(amigosUnidos) + 1 ):
					doc_idFragmento = crearFragmentoParada(peticion, idVehiculo, amigosUnidos)
					#asigno el id todos los amigos al fragmento parada
					asignarFragmentoParada(peticion, amigosUnidos, doc_idFragmento)
					docUltimoAmigo = amigosUnidos[len(amigosUnidos) -1]
					# busca el punto Last despues de crear los fragmentos para saber si pertenece a la misma parada
					docPuntoLast = traerPuntoAnterior(peticion, idVehiculo, nAmigos)
					if docPuntoLast != None:
						paradaPuntoLast = evaluarParadaPuntoLast(docPuntoLast)
						doc_idParada = paradaPuntoLast
						estanCerca  = estanCercaLosPuntos(docPuntoLast, docUltimoAmigo.get('latitud'), docUltimoAmigo.get('longitud'), docUltimoAmigo.get('horaRegistrada') )
						if estanCerca and (paradaPuntoLast != "" or paradaPuntoLast != None):
							asignarParadaTodosLosAmigos(peticion, doc_idParada, amigosUnidos, horaRegistrada)
						else:
							primerAmigo 	= amigosUnidos[0] # trae el documento del primer amigo
							#ultimoAmigo 	= amigosUnidos[len(amigosUnidos) - 1]
							#doc_idParada = crearParada(peticion, primerAmigo.get('horaRegistrada'),ultimoAmigo.get('horaRegistrada'), primerAmigo.get('latitud'), primerAmigo.get('longitud'), idVehiculo)
							doc_idParada = crearParada(peticion, primerAmigo.get('horaRegistrada'),horaRegistrada, primerAmigo.get('latitud'), primerAmigo.get('longitud'), idVehiculo)
							asignarParadaTodosLosAmigos(peticion, doc_idParada, amigosUnidos,horaRegistrada)
					else:
						primerAmigo 	= amigosUnidos[0] # trae el documento del primer amigo
						#ultimoAmigo 	= amigosUnidos[len(amigosUnidos) - 1]
						#doc_idParada = crearParada(peticion, primerAmigo.get('horaRegistrada'),ultimoAmigo.get('horaRegistrada'), primerAmigo.get('latitud'), primerAmigo.get('longitud'), idVehiculo)
						doc_idParada = crearParada(peticion, primerAmigo.get('horaRegistrada'),horaRegistrada, primerAmigo.get('latitud'), primerAmigo.get('longitud'), idVehiculo)
						asignarParadaTodosLosAmigos(peticion, doc_idParada, amigosUnidos,horaRegistrada)
	#datos para que se le asignen al punto que no se ha guardado el fragmento y la parada					
	datos[0] 	= doc_idFragmento
	datos[1]	= doc_idParada					
	return datos