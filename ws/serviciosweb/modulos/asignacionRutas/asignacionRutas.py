# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.http              import HttpResponse
from jsonschema               import validate, ValidationError
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from django.db                import IntegrityError, transaction
import time
import geocoder


def listarAsignacionesRutas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:

        dataRaw = []

        cacheRutas       = {}
        cacheVehiculos   = {}
        cacheConductores = {}
        
        filas   = db.view(
            '_design/asignacionRuta/_view/asignacionRuta',
            include_docs =  True,            
        )
    
        for fila in filas:
            doc = fila.doc

            idAsignacion           = doc["_id"]
            idRuta                 = doc.get("idRuta", "")
            idVehiculo             = doc.get("idVehiculo", "")
            idConductor            = doc.get("idConductor", "")
            fechaInicioProgramada  = doc.get("fechaInicioProgramada", "")
            fechaFinProgramada     = doc.get("fechaFinProgramada", "") 
            fechaInicioReal        = doc.get("fechaInicioReal", "")
            fechaFinReal           = doc.get("fechaFinReal", "")
            estado                 = doc.get("estado", "")
            puntosDeControlVirtual = doc.get("puntosDeControlVirtual", [])
            creadoPor              = doc.get('creadoPor','') 

            #Ruta --------------------------------------------------------
            docRuta = {}
            if idRuta in cacheRutas:
                docRuta = cacheRutas[idRuta]
            else:
                docRuta            = db[idRuta]
                cacheRutas[idRuta] = docRuta
 
            origen  = {
                "latitud"   : docRuta.get("origen" , ["",""])[0],
		"longitud"  : docRuta.get("origen" , ["",""])[0],
		"direccion" : docRuta.get("direccionOrigen" , "")
            }
            destino  = {
                "latitud"   : docRuta.get("destino" , ["",""])[0],
		"longitud"  : docRuta.get("destino" , ["",""])[0],
		"direccion" : docRuta.get("direccionDestino" , "")
            }
            
            ruta = {
                "nombreRuta" : docRuta.get("nombreRuta", ""),
                "origen"     : origen,
                "destino"    : destino
            }
            #-----------------------------------------------------------------
            #Vehículo --------------------------------------------------------
            docVehiculo = {}
            if idVehiculo in cacheVehiculos:
                docVehiculo = cacheVehiculos[idVehiculo]
            else:
                docVehiculo = db[idVehiculo]
                cacheVehiculos[idVehiculo] = docVehiculo

            vehiculo = {
                "placa" : docVehiculo.get("placa" , "")
            }
            #------------------------------------------------------------------
            #Conductor --------------------------------------------------------
            docConductor = {}
            if idConductor in cacheConductores:
                docConductor = cacheConductores[idConductor]
            else:
                docConductor = db[idConductor]
                cacheConductores[idConductor] = docConductor

            conductor = {
                "nombres"   : docConductor.get("nombres",   ""),
		"apellidos" : docConductor.get("apellidos", ""),
		"celular"   : docConductor.get("celular",   ""),
		"cedula"    : docConductor.get("cedula",    ""),
            }
            #-------------------------------------------------------------    
            
            dataRaw.append({
                "id"                     : idAsignacion,
	        "idRuta"                 : idRuta,
	        "idVehiculo"             : idVehiculo,
	        "idConductor"            : idConductor,
	        "fechaInicioProgramada"  : fechaInicioProgramada,
	        "fechaFinProgramada"     : fechaFinProgramada,
	        "fechaInicioReal"        : fechaInicioReal,
	        "fechaFinReal"           : fechaFinReal,
	        "estado"                 : estado,
	        "puntosDeControlVirtual" : puntosDeControlVirtual,
	        "ruta"                   : ruta,
	        "vehiculo"               : vehiculo,
	        "conductor"              : conductor,
            "creadoPor"              : creadoPor
            })
            
    
        # dataRaw.append({
	#     "id"              : "1920120129012901",
	#     "idRuta"          : "44444654454555412",
	#     "idVehiculo"      : "18291829192812892",
	#     "idConductor"     : "18291820ihaj81298",
	#     "fechaInicioProgramada" : "2016-03-12T08:07:19Z",
	#     "fechaFinProgramada"    : "2016-03-12T08:07:19Z",
	#     "fechaInicioReal"       : "2016-03-12T08:07:19Z",
	#     "fechaFinReal"          : "2016-03-12T08:07:19Z",
	#     "estado"                 : "programada",
	#     "puntosDeControlVirtual" : [
	# 	{
	# 	    "latitud"                  : "16.909009090",
	# 	    "longitud"                 : "-70.12819281",
	# 	    "direccion"                : "Av 123 # 678",
	# 	    "fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
	# 	    "fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z"
	# 	}		
	#     ],
	#     "ruta" : {
	# 	"nombreRuta" : "ruta cavasa",
	# 	"origen": {
	# 	    "latitud"   : 3.5266987,
	# 	    "longitud"  : -76.32760560000003,
	# 	    "direccion" : "Cra 123 # 23-45"
	# 	},
	# 	"destino": {
	# 	    "latitud"   : 3.5266987,
	# 	    "longitud"  : -76.32760560000003,
	# 	    "direccion" : "Cra 123 # 23-45"
	# 	}
	#     },
	#     "vehiculo" : {
	# 	"placa" : "18218291"				
	#     },
	#     "conductor" : {
	# 	"nombres"   : "Hector",
	# 	"apellidos" : "Machuca",
	# 	"celular"   : "5555",
	# 	"cedula"    : "12345"
	#     }
	    
	# })
        
        
        # filas   = db.view(
        #     '_design/asignacionRuta/_view/asignacionRuta',
        #     include_docs = True
        # )
        
        # for fila in filas:
        #   key   = fila.key
        #   value = fila.value
        #   doc   = fila.doc

        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }

def crearAsignacionRuta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:

        idRuta                 = datos.get("idRuta", "")
        idVehiculo             = datos.get("idVehiculo" , "")
        idConductor            = datos.get("idConductor" , "")
        fechaInicioProgramada  = datos.get("fechaInicioProgramada" , "")
        fechaFinProgramada     = datos.get("fechaFinProgramada" , "")
        puntosDeControlVirtual = datos.get("puntosDeControlVirtual" , "")

        ruta = {
        }

        puntosParadas = []
        if not idRuta == "":
            docRuta = db[idRuta]
            listaPuntosParadas = docRuta.get("puntosParadas",[])
            for puntoParada in listaPuntosParadas:
                puntosParadas.append({
                    "latitud"   : puntoParada[0],
		    "longitud"  : puntoParada[1],
		    "direccion" : "",
		    "tipo"      : puntoParada[2],
		    "fechaHoraInicioParada" : "",
		    "fechaHoraFinParada"    : ""
                })

            ruta = {
                "origen": {
		    "latitud"   : docRuta.get("origen",[0,0])[0],
		    "longitud"  : docRuta.get("origen",[0,0])[1],
		    "direccion" : docRuta.get("direccionOrigen",""),
		    "velocidad" : 0
	        },
	        "destino": {
                    "latitud"   : docRuta.get("destino",[0,0])[0],
		    "longitud"  : docRuta.get("destino",[0,0])[1],
		    "direccion" : docRuta.get("direccionDestino",""),
		    "velocidad" : 0
	        }
            }
            

        limitesDeVelocidad = []
        if not idRuta == "":            
            docPuntosVelocidad = getPuntosVelocidadDeRuta(db, idRuta)
            puntosVelocidad = docPuntosVelocidad.get("puntosVelocidad", [])
            for puntoVelocidad in puntosVelocidad:
                
                limitesDeVelocidad.append({
	            "latitud"          : puntoVelocidad[0],
	            "longitud"         : puntoVelocidad[1],
	            "direccion"        : puntoVelocidad[2],
	            "limiteCargado"    : puntoVelocidad[3],
	            "limiteDescargado" : puntoVelocidad[4],
	            "estado"           : "vigilando",
	            "infracciones"     : []
	        })
        
        #Validar que no existan registros en horas diferentes 
        esFechaValida = not existeAsignacionEnRangoFechas(
            db             = db,
            idProgramacion = "",
            idVehiculo     = idVehiculo,
            fechaInicio    = fechaInicioProgramada,
            fechaFin       = fechaFinProgramada
        )

        
        
        docAsignacion = {
            "tipoDato"      : "asignacionRuta",
            "creadoEn"      : datetime.now().isoformat(),
            "modificadoEn"  : datetime.now().isoformat(),
            "modificadoPor" : usuario,
            "creadoPor"     : usuario,
            "activo"        : True,
            "eliminado"     : False,

            "estado"                 : "programada",
            "idRuta"                 : idRuta,
            "idVehiculo"             : idVehiculo,
	    "idConductor"            : idConductor,
            "ruta"                   : ruta,
            "fechaInicioReal"        : "",
	    "fechaFinReal"           : "",
	    "fechaInicioProgramada"  : fechaInicioProgramada,
	    "fechaFinProgramada"     : fechaFinProgramada,
	    "puntosDeControlVirtual" : puntosDeControlVirtual,
            "puntosParadas"          : puntosParadas,
            "limitesDeVelocidad"     : limitesDeVelocidad
        }

        doc_id, doc_rev = db.save( docAsignacion )
        #doc_id="1"

        print doc_id
        
        dataRaw = {
	    "id" : doc_id
	}
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
    
    except ValueError:
        return { 'success' : False }

def editarAsignacionRuta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        idAsignacionRuta = datos.get("idAsignacionRuta","")

        docAsignacion = db[idAsignacionRuta]

        idConductor           = datos.get("idConductor",           docAsignacion.get("idConductor",""))
        fechaInicioProgramada = datos.get("fechaInicioProgramada", docAsignacion.get("fechaInicioProgramada",""))
        fechaFinProgramada    = datos.get("fechaFinProgramada",    docAsignacion.get("fechaFinProgramada",""))
        
        puntosDeControlVirtual = docAsignacion.get("puntosDeControlVirtual", [])
        for i, puntoNuevo in enumerate(datos.get("puntosDeControlVirtual",[])):
            if i < len(puntosDeControlVirtual):
                docPunto = puntosDeControlVirtual[i]
                docPunto["fechaHoraCruceProgramada"] = puntoNuevo.get("fechaHoraCruceProgramada", docPunto.get("fechaHoraCruceProgramada", ""))

                docPunto["minutosTolerancia"]        = puntoNuevo.get("minutosTolerancia", docPunto.get("minutosTolerancia", ""))
                puntosDeControlVirtual[i]            = docPunto                
                                
                #docPunto["minutosTolerancia"] = puntoNuevo.get("minutosTolerancia", docPunto.get("minutosTolerancia", ""))
                #puntosDeControlVirtual[i] = docPunto                

        
        docAsignacion["idConductor"]            = idConductor
        docAsignacion["fechaInicioProgramada"]  = fechaInicioProgramada
        docAsignacion["fechaFinProgramada"]     = fechaFinProgramada
        docAsignacion["puntosDeControlVirtual"] = puntosDeControlVirtual
                           
        db.save(docAsignacion)
                  	
        dataRaw = {
	    "id" : docAsignacion["_id"]
	}
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
    
    except ValueError:
        return { 'success' : False }

def eliminarAsignacionRuta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        idAsignacionRuta = datos.get("idAsignacionRuta","")

        docAsignacion = db[idAsignacionRuta]

        docAsignacion["activo"] = False
                                       
        db.save(docAsignacion)
                                       
        
        	
        dataRaw = {
	    "id" : docAsignacion["_id"]
	}
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
    
    except ValueError:
        return { 'success' : False }


def abortarAsignacionRuta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:

        idAsignacionRuta = datos.get("idAsignacionRuta","")

        docAsignacion = db[idAsignacionRuta]

        docAsignacion["estado"] = "abortada"
                                       
        db.save(docAsignacion)
                                               	
        dataRaw = {
	    "id" : docAsignacion["_id"]
	}
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
    
    except ValueError:
        return { 'success' : False }



def detalleAsignacionRuta( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    # dbAdmin = conexion.getConexionTenant(tenant)

    # if dbAdmin == None:
    #     return { 'success' : False }


    db = conexion.getConexionTenant(tenant)
    
            
    try:
        doc            = db[datos['idAsignacionRuta']]
        
        idAsignacion           = doc["_id"]
        idRuta                 = doc.get("idRuta", "")
        idVehiculo             = doc.get("idVehiculo", "")
        idConductor            = doc.get("idConductor", "")
        fechaInicioProgramada  = doc.get("fechaInicioProgramada", "")
        fechaFinProgramada     = doc.get("fechaFinProgramada", "") 
        fechaInicioReal        = doc.get("fechaInicioReal", "")
        fechaFinReal           = doc.get("fechaFinReal", "")
        estado                 = doc.get("estado", "")
        puntosDeControlVirtual = doc.get("puntosDeControlVirtual", []) 

        #Ruta --------------------------------------------------------
        docRuta            = db[idRuta]
        
        origen  = {
            "latitud"   : docRuta.get("origen" , ["",""])[0],
            "longitud"  : docRuta.get("origen" , ["",""])[0],
            "direccion" : docRuta.get("direccionOrigen" , "")
        }
        
        destino  = {
            "latitud"   : docRuta.get("destino" , ["",""])[0],
            "longitud"  : docRuta.get("destino" , ["",""])[0],
            "direccion" : docRuta.get("direccionDestino" , "")
        }

        ruta = {
            "nombreRuta" : docRuta.get("nombreRuta", ""),
            "origen"     : origen,
            "destino"    : destino
        }
        #-----------------------------------------------------------------
        #Vehículo --------------------------------------------------------
        docVehiculo = db[idVehiculo]

        vehiculo = {
            "placa" : docVehiculo.get("placa" , "")
        }
        #------------------------------------------------------------------
        #Conductor --------------------------------------------------------
        docConductor = db[idConductor]
        
        conductor = {
            "nombres"   : docConductor.get("nombres",   ""),
            "apellidos" : docConductor.get("apellidos", ""),
            "celular"   : docConductor.get("celular",   ""),
            "cedula"    : docConductor.get("cedula",    ""),
        }
        #-------------------------------------------------------------    

        dataResponse = {
            "id"                     : idAsignacion,
            "idRuta"                 : idRuta,
            "idVehiculo"             : idVehiculo,
            "idConductor"            : idConductor,
            "fechaInicioProgramada"  : fechaInicioProgramada,
            "fechaFinProgramada"     : fechaFinProgramada,
            "fechaInicioReal"        : fechaInicioReal,
            "fechaFinReal"           : fechaFinReal,
            "estado"                 : estado,
            "puntosDeControlVirtual" : puntosDeControlVirtual,
            "ruta"                   : ruta,
            "vehiculo"               : vehiculo,
            "conductor"              : conductor
        }

        
        # dataResponse = {
        #     "id"                     : "1920120129012901",
	#     "idRuta"                 : "44444654454555412",
	#     "idVehiculo"             : "18291829192812892",
	#     "idConductor"            : "18291820ihaj81298",
	#     "fechaInicioProgramada"  : "2016-03-12T08:07:19Z",
	#     "fechaFinProgramada"     : "2016-03-12T08:07:19Z",
	#     "fechaInicioReal"        : "2016-03-12T08:07:19Z",
	#     "fechaFinReal"           : "2016-03-12T08:07:19Z",
	#     "estado"                 : "programada",
	#     "puntosDeControlVirtual" : [
	# 	{
	# 	    "latitud"                  : "16.909009090",
	# 	    "longitud"                 : "-70.12819281",
	# 	    "direccion"                : "Av 123 # 678",
	# 	    "fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
	# 	    "fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z",
	# 	    "minutosTolerancia"        : 30
	# 	}		
	#     ],
	#     "ruta" : {
	# 	"nombreRuta" : "ruta cavasa"
	#     },
	#     "vehiculo" : {
	# 	"placa" : "18218291"				
	#     },
	#     "conductor" : {
	# 	"nombres"   : "Hector",
	# 	"apellidos" : "Machuca",
	# 	"celular"   : "5555",
	# 	"cedula"    : "12345"
	#     }
        # }
            
        return {
            'success' : True,
            'data'    : dataResponse 
        }    
    except ValueError:
        pass

    return { 'success' : False }

    
#Auxiliares ---------------------------------

def getPuntosVelocidadDeRuta(db, idRuta):

    doc = {}
    filas   = db.view(
        '_design/rutas/_view/recuperarPuntosVelocidadPorIdRuta',
        include_docs =  True,
        key          = [idRuta]
    )
    
    for fila in filas:
        doc = fila.doc


    return doc


#idASignacion sirve para verificar que el id de la programacion no exista
def existeAsignacionEnRangoFechas(db, idProgramacion, idVehiculo, fechaInicio, fechaFin):    
    existeAsignacion = False

    #-------------------------------------
    filas   = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoVehiculoFechaInicio',
        include_docs =  True,
        startkey = ['programada', idVehiculo, fechaInicio],
        endkey   = ['programada', idVehiculo, fechaFin]        
    )
    
    for fila in filas:
        doc = fila.doc
        if not doc["_id"] == idProgramacion:
            existeAsignacion = True
            return True
    #--------------------------------------

    #-------------------------------------
    filas   = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoVehiculoFechaInicio',
        include_docs =  True,
        startkey = ['finalizada', idVehiculo, fechaInicio],
        endkey   = ['finalizada', idVehiculo, fechaFin]        
    )
    
    for fila in filas:
        doc = fila.doc
        if not doc["_id"] == idProgramacion:
            existeAsignacion = True
            return True
    #--------------------------------------


    #-------------------------------------
    filas   = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoVehiculoFechaFin',
        include_docs =  True,
        startkey = ['programada', idVehiculo, fechaInicio],
        endkey   = ['programada', idVehiculo, fechaFin]        
    )
    
    for fila in filas:
        doc = fila.doc
        if not doc["_id"] == idProgramacion:
            existeAsignacion = True
            return True
    #--------------------------------------

    #-------------------------------------
    filas   = db.view(
        '_design/asignacionRuta/_view/asignacionPorEstadoVehiculoFechaFin',
        include_docs =  True,
        startkey = ['finalizada', idVehiculo, fechaInicio],
        endkey   = ['finalizada', idVehiculo, fechaFin]        
    )
    
    for fila in filas:
        doc = fila.doc
        if not doc["_id"] == idProgramacion:
            existeAsignacion = True
            return True
    #--------------------------------------

    
    
    return existeAsignacion