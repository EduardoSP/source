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
from ..vehiculos.vehiculos    import traerNumeroSimCardVehiculo
#-------------------------------------------------------------

def listarMonitoreoZonas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/vigilancias/_view/monitoreoZonas',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'id'  : doc['_id'],
          	'nombre' : doc.get('nombre'),
          	'latitud': doc.get('latitud'),
            'longitud': doc.get('longitud'),
          	'radio': doc.get('radio'),
          	'registrarAudio': doc.get('registrarAudio'),
            'registrarImagen': doc.get('registrarImagen'),
            'creadoPor'  : doc.get('creadoPor','')   
          	})            
        return {
            'success' : True, 
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------

def listarVigilancias( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/vigilancias/_view/programacionVigilancia',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
          	'idVehiculo' : doc.get('idVehiculo'),
          	'fechaInicio': doc.get('fechaInicio'),
          	'fechaFin': doc.get('fechaFin'),
          	'horaInicio': doc.get('horaInicio'),
          	'horaFin': doc.get('horaFin'),
          	'registrarAudio': doc.get('registrarAudio'),
          	'registrarImagen': doc.get('registrarImagen'),
            'estadoProgramacion': doc.get('estadoProgramacion')

          	})            
        return {
            'success' : True, 
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }



#-------------------------------------------------------------


def crearZonas( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try: 

        doc_id, doc_rev = db.save({
	     	"tipoDato"            : "monitoreoZonas",
	        "creadoEn"		: datetime.now().isoformat(),  
	        "modificadoEn"	: datetime.now().isoformat(),
	        "modificadoPor"	: usuario,
	    	"nombre" : datos["nombre"],
			"descripcion" : datos["descripcion"],
			"registrarAudio" : datos["registrarAudio"],
			"registrarImagen" : datos["registrarImagen"],
			"tiempoMaxGrabAudio"  : datos["tiempoMaxGrabAudio"],
			"numeroCapturasMax"   : datos["numeroCapturasMax"],
            "latitud"             : datos["latitud"],	
	    	"longitud"            : datos["longitud"],
	  		"radio"               : datos["radio"],
            "tipoZona"            : datos["tipoZona"],
	        "activo"		      : True,
            "creadoPor"           : usuario
        })
        return {
            'success' : True,
            'data'    : {
                'id' : doc_id
            }            
        }
    except ValueError:
        pass

    return { 'success' : False }


#-------------------------------------------------------------


def editarZonas( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    idDoc          = datos["id"]
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try: 
        doc = db[idDoc]
        doc["modificadoEn"] = datetime.now().isoformat()
        doc["modificadoPor"] = usuario
        doc["nombre"] = datos["nombre"]
        doc["descripcion"] = datos["descripcion"]
        doc["registrarAudio"] = datos["registrarAudio"]
        doc["registrarImagen"] = datos["registrarImagen"]
        doc["tiempoMaxGrabAudio"] = datos["tiempoMaxGrabAudio"]
        doc["numeroCapturasMax"] = datos["numeroCapturasMax"]
        doc["latitud"] = datos["latitud"]
        doc["longitud"] = datos["longitud"]
        doc["radio"] = datos["radio"]
        doc["tipoZona"] = datos["tipoZona"]
        db.save(doc)

        return {
            'success' : True,
            'data'    : {
                'id' : doc["_id"]
            }            
        }
    except ValueError:
        pass

    return { 'success' : False }

#-------------------------------------------------------------


def eliminarZonas( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]
        doc['modificadoPor'] = usuario
        doc['modificadoEn']  = datetime.now().isoformat()

        doc['activo']        = False
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }

#-------------------------------------------------------------

def zonaAlarmas( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idZona    = datos['id']
        filas = db.view('_design/posicionVehiculos/_view/poscionVehiculoPorZonaAlarma',
                    include_docs  = True,
                    startkey = [idZona,0],
                    endkey = [idZona,{}])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'idVehiculo' : doc.get('idVehiculo')

            })            
        return {
            'success' : True, 
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

#-------------------------------------------------------------

#-------------------------------------------------------------

def crearProgramacion( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)


    if db == None:
        return { 'success' : False }

    try: 
        doc_id, doc_rev = db.save({
	     	"tipoDato"            : "programacionVigilancia",
	        "creadoEn"		: datetime.now().isoformat(),  
	        "modificadoEn"	: datetime.now().isoformat(),
	        "modificadoPor"	: usuario,
	    	"idVehiculo" : datos["idVehiculo"],
	    	"registrarAudio" : datos["registrarAudio"],
	    	"registrarImagen" : datos["registrarImagen"],
	    	"fechaInicio" : datos["fechaInicio"],
	    	"fechaFin" : datos["fechaFin"],
			"horaInicio" : datos["horaInicio"],
			"horaFin" : datos["horaFin"],
	        "activo"		: True
        })
        return {
            'success' : True,
            'data'    : {
                'id' : doc_id
            }            
        }
    except ValueError:
        pass

    return { 'success' : False }

#-------------------------------------------------------------


#-------------------------------------------------------------

def eliminarProgramacionVigilancia( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]
        doc['modificadoPor'] = usuario
        doc['modificadoEn']  = datetime.now().isoformat()

        doc['activo']        = False
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }

#-------------------------------------------------------------

#-------------------------------------------------------------

def listarDetalleZona(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idZona    = datos['id']

        filas = db.view('_design/detalleZona/_view/detalleZona',
                    include_docs  = True, 
                    startkey = [idZona,0],
                    endkey = [idZona,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw = {
            'idZona' : doc.get('_id'),
            'nombre' : doc.get('nombre'),
            'descripcion' : doc.get('descripcion'),
            'registrarAudio' : doc.get('registrarAudio'),
            'registrarImagen' : doc.get('registrarImagen'),
            'tiempoMaxGrabAudio' : doc.get('tiempoMaxGrabAudio'),
            'numeroCapturasMax' : doc.get('numeroCapturasMax'),
            'latitud' : doc.get('latitud'),
            'longitud' : doc.get('longitud'),
            'tipoZona' : doc.get('tipoZona', "n/a"),
            'radio' : doc.get('radio')
            }            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False}

#-------------------------------------------------------------

#-------------------------------------------------------------

def listarDetalleZonaAlarma(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idZona    = datos['id']

        filas = db.view('_design/vigilancias/_view/zonaAlarma',
                    include_docs  = True, 
                    startkey = [idZona, 0],
                    endkey = [idZona, {}])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          placaVehiculo = ""

          #Sacar placa vehiculo
          docVehiculo = db[doc.get('idVehiculo')]
          placaVehiculo = docVehiculo.get("placa", "")
          #--------------------------------------------

          dataRaw.append( {
            'idZonaAlarma' : doc.get('_id'),
            'fecha' : doc.get('fecha'),
            'horaInicio' : doc.get('horaInicio'),
            'horaFin' : doc.get('horaFin'),
            'estado' : doc.get('estado'),
            'idVehiculo' : doc.get('idVehiculo'),
            'placaVehiculo' : placaVehiculo,
            'idZona' : doc.get('idZona')
            })       
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False}

#-------------------------------------------------------------

#-------------------------------------------------------------

def listarDetalleVehiculoZonaAlarma(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idZonaAlarma    = datos['id']
        docZonaAlarma = db[idZonaAlarma]
        docVehiculo = db[docZonaAlarma.get("idVehiculo")]
        docMonitoreoZona = db[docZonaAlarma.get("idZona")]
        dataRaw ={
            'placa' : docVehiculo.get("placa", ""),
            'marca' : docVehiculo.get("marca", ""),
            'modelo' : docVehiculo.get("modelo", ""),                
            'imeiGps' : docVehiculo.get("imeiGps", ""),
            'numSimCard' : traerNumeroSimCardVehiculo(docVehiculo.get("_id", "")),
            'tipoGps' : docVehiculo.get("tipoGps", ""),
            'radioMonitoreoZona' : docMonitoreoZona.get("radio", ""),
            'latitudMonitoreoZona' : docMonitoreoZona.get("latitud", ""),
            'longitudMonitoreoZona' : docMonitoreoZona.get("longitud", "")
            }       
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False}

#-------------------------------------------------------------


#-------------------------------------------------------------

def listarPosicionZonaAlarma(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idZonaAlarma    = datos['id']

        filas = db.view('_design/posicionVehiculos/_view/poscionVehiculoPorZonaAlarma',
                    include_docs  = True, 
                    startkey = [idZonaAlarma,0],
                    endkey = [idZonaAlarma,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append( {
            'horaRegistrada' : doc.get('horaRegistrada'),
            'horaRecibida' : doc.get('horaRecibida'),
            'latitud' : doc.get('latitud'),
            'longitud' : doc.get('longitud'),
            'velocidad' : doc.get('velocidad')
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False}

#-------------------------------------------------------------


#-------------------------------------------------------------

def listarCapturaImagenesZonaAlarma(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idZonaAlarma    = datos['id']

        filas = db.view('_design/vigilancias/_view/capturaImagenesZonaAlarma',
                    include_docs    = True, 
                    startkey        = [idZonaAlarma,0],
                    endkey          = [idZonaAlarma,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append( {
            'horaRegistrada'    : doc.get('horaRegistrada'),
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'idImagen'          : doc.get('idImagen',""),
            'urlImagen'         : settings.NISABU_IMAGE_URL+doc.get('idImagen', "")
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False}

#-------------------------------------------------------------

#-------------------------------------------------------------

def listarCapturaAudiosZonaAlarma(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idZonaAlarma    = datos['id']

        filas = db.view('_design/vigilancias/_view/capturaAudioZonaAlarma',
                    include_docs    = True, 
                    startkey        = [idZonaAlarma,0],
                    endkey          = [idZonaAlarma,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append( {
            'horaRegistrada'    : doc.get('horaRegistrada'),
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'idAudio'           : doc.get('idAudio',""),
            'urlAudio'          : doc.get('urlAudio',""),
            'duracion'          : doc.get('duracion',"")
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False}

#-------------------------------------------------------------


def listarProgramacionVigilancia(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/vigilancias/_view/programacionVigilancia',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          placaVehiculo = ""
          #Sacar placa vehiculo
          docVehiculo = db[doc.get('idVehiculo')]
          placaVehiculo = docVehiculo.get("placa", "")
          dataRaw.append({
            'idProgramacion'    : doc.get('_id'),
            'idVehiculo'        : doc.get('idVehiculo'),
            'placa'             : placaVehiculo,
            'fechaInicio'       : doc.get('fechaInicio'),
            'fechaFin'          : doc.get('fechaFin'),
            'horaInicio'        : doc.get('horaInicio'),
            'horaFin'           : doc.get('horaFin'),
            'registrarAudio'    : doc.get('registrarAudio'),
            'registrarImagen'   : doc.get('registrarImagen'),
            'estadoProgramacion': doc.get('estadoProgramacion'),
            'activo'            : doc.get('activo'),
            'creadoPor'         : doc.get('creadoPor') 

            })            
        return {
            'success' : True, 
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

#-------------------------------------------------------------

def crearProgramacionVigilancia(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db            = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try: 

        doc_id, doc_rev = db.save({
            "tipoDato"              : "programacionVigilancia",
            "creadoEn"              : datetime.now().isoformat(),  
            "modificadoEn"          : datetime.now().isoformat(),
            "modificadoPor"         : usuario,
            "idVehiculo"            : datos["idVehiculo"],
            "registrarAudio"        : datos["registrarAudio"],
            "registrarImagen"       : datos["registrarImagen"],
            "capturasMax"           : datos["capturasMax"],
            "tiempoMaxGrabAudio"    : datos["grabMax"],      
            "fechaInicio"           : datos["fechaInicio"],
            "fechaFin"              : datos["fechaFin"],
            "horaInicio"            : datos["horaInicio"],   
            "horaFin"               : datos["horaFin"],
            "estadoProgramacion"    : "Iniciado",
            "activo"                : True,
            "creadoPor"             : usuario
        })
        return {
            'success' : True,
            'data'    : {
                'id' : doc_id
            }            
        }
    except ValueError:
        pass

    return { 'success' : False }

#-------------------------------------------------------------


def listarPosicionesVehiculoVigilancia(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idProgramacionVigilancia    = datos['id']

        filas = db.view('_design/vigilancias/_view/vehiculosPosicion',
                    include_docs    = True, 
                    startkey        = [idProgramacionVigilancia, 0],
                    endkey          = [idProgramacionVigilancia, {}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append( {
            'horaRegistrada'    : doc.get('horaRegistrada'),
            'horaRecibida'      : doc.get('horaRecibida'),
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'velocidad'         : doc.get('velocidad')
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False}

#-------------------------------------------------------------

def listarDetalleVehiculoProgramacionVigilancia(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idProgramacionVigilancia    = datos['id']
        docProgramacionVigilancia = db[idProgramacionVigilancia]
        docVehiculo = db[docProgramacionVigilancia.get("idVehiculo")]
        dataRaw ={
            'placa' : docVehiculo.get("placa", ""),
            'marca' : docVehiculo.get("marca", ""),
            'modelo' : docVehiculo.get("modelo", ""),                
            'imeiGps' : docVehiculo.get("imeiGps", ""),
            'numSimCard' : traerNumeroSimCardVehiculo(docVehiculo.get("_id", "")),
            'tipoGps' : docVehiculo.get("tipoGps", ""),
            'opcionesAdicionalesPlataforma': docVehiculo.get('opcionesAdicionalesPlataforma', None)
            }       
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False}

#-------------------------------------------------------------

#-------------------------------------------------------------

def listarImagenesProgramacionVigilancia(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idProgramacionVigilancia    = datos['id']

        filas = db.view('_design/vigilancias/_view/listarImagenesProgramacionVigilancia',
                    include_docs    = True, 
                    startkey        = [idProgramacionVigilancia,0],
                    endkey          = [idProgramacionVigilancia,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append( {
            'horaRegistrada'    : doc.get('horaRegistrada'),
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'idImagen'          : doc.get('idImagen',""),
            'urlImagen'         : settings.NISABU_IMAGE_URL+doc.get('idImagen', "")
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False}

#-------------------------------------------------------------

def listarAudiosProgramacionVigilancia(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idProgramacionVigilancia    = datos['id']
        print idProgramacionVigilancia

        filas = db.view('_design/vigilancias/_view/listadoAudiosProgramacionVigilancia',
                    include_docs    = True, 
                    startkey        = [idProgramacionVigilancia,0],
                    endkey          = [idProgramacionVigilancia,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append( {
            'horaRegistrada'    : doc.get('horaRegistrada'),
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'duracion'          : doc.get('duracion'),
            "urlAudio"          : doc.get('urlAudio')
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False}

#-------------------------------------------------------------


def paradaPorRangoFecha(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        fechaInicio  = datos['fechaInicio']
        fechaFin = datos['fechaFin']

        filas = db.view('_design/vigilancias/_view/fragmentoParada',
                    include_docs    = True ,
                    startkey        = [fechaInicio],
                    endkey          = [fechaFin])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'latitud' : doc.get('latitud'),
            'longitud' : doc.get('longitud')
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}


#-------------------------------------------------------------


def validarAudioImagenVehiculo(peticion): 
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    mostrarAudio  = False
    mostrarImagen = False
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    
    try:
        dataRaw = []
        idVehiculo  = datos['idVehiculo']
        filas = db.view('_design/detalleVehiculo/_view/detalleVehiculo',
                    include_docs  = True,
                    startkey = [idVehiculo,0],
                    endkey = [idVehiculo,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          opcionesAdicionalesPlataforma = doc.get("opcionesAdicionalesPlataforma", [])
          if not(opcionesAdicionalesPlataforma == None):
            if "15" in opcionesAdicionalesPlataforma:
                #permiso 15 imagen programacion vigilancia
                mostrarImagen = True
            if "16" in opcionesAdicionalesPlataforma:
                #permiso 16 audio programacion vigilancia
                mostrarAudio  = True
        return {
            'success' : True,
            'mostrarImagen'    : mostrarImagen,
            'mostrarAudio'     : mostrarAudio 
        }     
    except ValueError:
        pass