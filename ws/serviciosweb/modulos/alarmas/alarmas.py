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
import time
from ..vehiculos.vehiculos    import traerNumeroSimCardVehiculo

def listarAlarmas(peticion):
    #editando
    autenticacion  = peticion['autenticacion']
    datos          = peticion['data']
    usuario        = autenticacion['usuario']
    tenant         = autenticacion['tenant']

    fechaInicio  = datos['fechaInicio']
    fechaFin     = datos['fechaFin']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/alarmas/_view/alarmasRangoFecha',
            startkey      = [fechaFin,    {}],
            endkey        = [fechaInicio, 0],
            descending    = True,
            include_docs  = True)
        for fila in filas:
          key = fila.key          
          doc = fila.doc
          idAlarma       = doc.get('_id')
          tipoAlarma     = doc.get('tipoDato')
          idDocumento    = ""
          horaRegistrada = ""
          idVehiculo     = ""
          placa          = ""
          latitud        = ""
          longitud        = ""

          if doc.get('tipoDato') == 'alarmasBotonPanico':
              docVehiculo    = db[doc.get('idVehiculo', '')]              
              tipoAlarma     = doc.get('tipoDato', '')
      	      idDocumento    = doc.get('_id', '')
      	      horaRegistrada = doc.get('horaRegistrada', '')
      	      idVehiculo     = doc.get('idVehiculo', '')
      	      placa          = docVehiculo.get('placa', '')
      	      latitud        = doc.get('latitud', '')
      	      longitud        = doc.get('longitud', '')
              dataRaw.append({
                "tipoAlarma"    : tipoAlarma,
                "id"            : idDocumento,
                "horaRegistrada": horaRegistrada,
                "idVehiculo"    : idVehiculo,
                "placa"         : placa,
                "latitud"       : latitud,
                "longitud"      : longitud,
                "idAlarma"      : idAlarma
                })               
              
          if doc.get('tipoDato') == 'zonaAlarma':
              docVehiculo     = db[doc.get('idVehiculo', '')]
              docPosicion = buscarPrimeraPosicionZonaAlarma(doc.get('_id', ''), db)
              if docPosicion != None:
                tipoAlarma     = doc.get('tipoDato', '')
                idDocumento    = doc.get('_id', '')
                horaRegistrada = doc.get('horaInicio', '')
                idVehiculo     = doc.get('idVehiculo', '')
                placa          = docVehiculo.get('placa', '')
                latitud        = docPosicion.get('latitud', '')
                longitud        = docPosicion.get('longitud', '')
                dataRaw.append({
                  "tipoAlarma"    : tipoAlarma,
                  "id"            : idDocumento,
                  "horaRegistrada": horaRegistrada,
                  "idVehiculo"    : idVehiculo,
                  "placa"         : placa,
                  "latitud"       : latitud,
                  "longitud"      : longitud,
                  "idAlarma"	    : idAlarma
                  })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False,
             'data'      : dataRaw
        }



#-------------------------------------------------------------
def listarUltimasAlarmas(peticion):
    #editando
    autenticacion  = peticion['autenticacion']
    datos          = peticion['data']
    usuario        = autenticacion['usuario']
    tenant         = autenticacion['tenant']

    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/alarmas/_view/alarmasRangoFecha',
            startkey      = [{}, {}],
            endkey        = [ 0,  0],
            descending    = True,
            include_docs  = True,
            limit         = 100
        )
        
        for fila in filas:
          key = fila.key          
          doc = fila.doc
          idAlarma       = doc.get('_id')
          tipoAlarma     = doc.get('tipoDato')
          idDocumento    = ""
          horaRegistrada = ""
          idVehiculo     = ""
          placa          = ""
          latitud        = ""
          longitud       = ""

          if doc.get('tipoDato') == 'alarmasBotonPanico':
              docVehiculo    = db[doc.get('idVehiculo', '')]              
              tipoAlarma     = doc.get('tipoDato', '')
      	      idDocumento    = doc.get('_id', '')
      	      horaRegistrada = doc.get('horaRegistrada', '')
      	      idVehiculo     = doc.get('idVehiculo', '')
      	      placa          = docVehiculo.get('placa', '')
      	      latitud        = doc.get('latitud', '')
      	      longitud        = doc.get('longitud', '')
              dataRaw.append({
                "tipoAlarma"    : tipoAlarma,
                "id"            : idDocumento,
                "horaRegistrada": horaRegistrada,
                "idVehiculo"    : idVehiculo,
                "placa"         : placa,
                "latitud"       : latitud,
                "longitud"      : longitud,
                "idAlarma"      : idAlarma
                })               
              
          if doc.get('tipoDato') == 'zonaAlarma':
              docVehiculo     = db[doc.get('idVehiculo', '')]
              docPosicion = buscarPrimeraPosicionZonaAlarma(doc.get('_id', ''), db)
              if docPosicion != None:
                tipoAlarma     = doc.get('tipoDato', '')
                idDocumento    = doc.get('_id', '')
                horaRegistrada = doc.get('horaInicio', '')
                idVehiculo     = doc.get('idVehiculo', '')
                placa          = docVehiculo.get('placa', '')
                latitud        = docPosicion.get('latitud', '')
                longitud        = docPosicion.get('longitud', '')
                dataRaw.append({
                  "tipoAlarma"      : tipoAlarma,
                  "id"              : idDocumento,
                  "horaRegistrada"  : horaRegistrada,
                  "idVehiculo"      : idVehiculo,
                  "placa"           : placa,
                  "latitud"         : latitud,
                  "longitud"        : longitud,
                    "idAlarma"	    : idAlarma,
                    "nombre"        : ""
                  })

                # #TODO Remover 
                # dataRaw.append({
                #     "tipoAlarma"    : "velocidadAlarma",
                #     "id"            : "",
                #     "horaRegistrada": horaRegistrada,
                #     "idVehiculo"    : idVehiculo,
                #     "placa"         : placa,
                #     "latitud"       : latitud,
                #     "longitud"      : longitud,
                #     "idAlarma"	    : "",
                #     "velocidad"     : 99.35
                    
                #   })
                # dataRaw.append({
                #     "tipoAlarma"    : "alarmasBotonPanico",

                #     "id"            : "",
                #     "horaRegistrada": horaRegistrada,
                #     "idVehiculo"    : idVehiculo,
                #     "placa"         : placa,
                #     "latitud"       : latitud,
                #     "longitud"      : longitud
                                                            
                #   })

                
                #Fin remover -----------------------------
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False,
             'data'      : dataRaw
        }

#-------------------------------------------------------------


def listarAlarmasPorVehiculo(peticion):
    autenticacion  = peticion['autenticacion']
    datos          = peticion['data']
    usuario        = autenticacion['usuario']
    tenant         = autenticacion['tenant']

    fechaInicio  = datos['fechaInicio']
    fechaFin     = datos['fechaFin']
    idVehiculo   = datos['id']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/alarmas/_view/alarmasRangoFechaPorVehiculo',
            startkey      = [idVehiculo, fechaFin],
            endkey        = [idVehiculo,fechaInicio ],
            descending    = True,
            include_docs  = True)
        for fila in filas:
          key = fila.key          
          doc = fila.doc

          idAlarma       = doc.get('_id')
          tipoAlarma     = doc.get('tipoDato')
          idDocumento    = ""
          horaRegistrada = ""
          idVehiculo     = ""
          placa          = ""
          latitud        = ""
          longitud        = ""

          if doc.get('tipoDato') == 'alarmasBotonPanico':           
              tipoAlarma     = doc.get('tipoDato', '')
              idDocumento    = doc.get('_id', '')
              horaRegistrada = doc.get('horaRegistrada', '')
              idVehiculo     = doc.get('idVehiculo', '')
              latitud        = doc.get('latitud', '')
              longitud        = doc.get('longitud', '')
              dataRaw.append({
              "tipoAlarma"    : tipoAlarma,
              "id"            : idDocumento,
              "horaRegistrada": horaRegistrada,
              "latitud"       : latitud,
              "longitud"      : longitud,
              "idAlarma"      : idAlarma,
              'idVehiculo'    : idVehiculo
              }) 
              
          if doc.get('tipoDato') == 'zonaAlarma':
              docPosicion = buscarPrimeraPosicionZonaAlarma(doc.get('_id', ''), db)
              if docPosicion != None:
                tipoAlarma     = doc.get('tipoDato', '')
                idDocumento    = doc.get('_id', '')
                horaRegistrada = doc.get('horaInicio', '')
                idVehiculo     = doc.get('idVehiculo', '')
                latitud        = docPosicion.get('latitud', '')
                longitud        = docPosicion.get('longitud', '')              
                dataRaw.append({
                "tipoAlarma"    : tipoAlarma,
                "id"            : idDocumento,
                "horaRegistrada": horaRegistrada,
                "latitud"       : latitud,
                "longitud"      : longitud,
                "idAlarma"      : idAlarma,
                'idVehiculo'    : idVehiculo
                })
           
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False,
             'data'      : dataRaw
        }

#-------------------------------------------------------------




#-------------------------------------------------------------

def listarDetalleAlarmaPanico(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idAlarmaPanico    = datos['id']
        docAlarmaPanico   = db[idAlarmaPanico]
        docVehiculo = db[docAlarmaPanico.get("idVehiculo")]
        dataRaw ={
            'placa' : docVehiculo.get("placa", ""),
            'marca' : docVehiculo.get("marca", ""),
            'modelo' : docVehiculo.get("modelo", ""),                
            'imeiGps' : docVehiculo.get("imeiGps", ""),
            'numSimCard' : traerNumeroSimCardVehiculo(docVehiculo.get("_id", "")),
            'tipoGps' : docVehiculo.get("tipoGps", ""),
            'latitud' : docAlarmaPanico.get("latitud", ""),
            'longitud': docAlarmaPanico.get("longitud", ""),
            'horaRegistrada': docAlarmaPanico.get("horaRegistrada", ""),
            'opcionesAdicionalesPlataforma': docVehiculo.get('opcionesAdicionalesPlataforma', None)
            }       
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False,
}

#-------------------------------------------------------------

#-------------------------------------------------------------

def listarCapturaImagenesPanico(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idAlarmaPanico   = datos['id']

        filas = db.view('_design/alarmas/_view/capturaImagenesAlarmaPanico',
                    include_docs    = True, 
                    startkey        = [idAlarmaPanico,0],
                    endkey          = [idAlarmaPanico,{}])

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

def listarCapturaAudiosPanico(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idAlarmaPanico    = datos['id']

        filas = db.view('_design/alarmas/_view/capturaAudioAlarmaPanico',
                    include_docs    = True, 
                    startkey        = [idAlarmaPanico,0],
                    endkey          = [idAlarmaPanico,{}])

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


#Auxiliares ==================================================

def buscarPrimeraPosicionZonaAlarma(idZonaAlarma, db):

    resultado = None
    
    filas = db.view(
        '_design/posicionVehiculos/_view/poscionVehiculoPorZonaAlarma',
        startkey      = [idZonaAlarma,    0],
        endkey        = [idZonaAlarma,   {}],
        include_docs  = True,
        limit         = 1
    )

    for fila in filas :
      resultado = fila.doc        

    return resultado
#===============================================================
    
def actualizarIngresoAlarmasUsuario(peticion):
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    key=[usuario])
        for fila in filas:
          key                 = fila.key
          value               = fila.value
          doc                 = fila.doc
          idDocumentoUsuario  = doc['_id']
        doc = db[idDocumentoUsuario]
        doc["ultimoIngresoAlarmas"] = time.time()  
        db.save(doc)            
        return {
            'success' : True, 
            'data'    : idDocumentoUsuario
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------
    
def actualizarIngresoAlarmasUsuarioGeneradorCarga(peticion):
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant        = settings.TENANT_GENERADOR_CARGA
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        doc = db[usuario]
        doc["ultimoIngresoAlarmas"] = time.time()  
        db.save(doc)            
        return {
            'success' : True, 
            'data'    : usuario
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------


#funcion auxiliar para traer el timeStamp del usuario que esta logueado
def traerTimeStampUsuario(peticion):
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    timeStampUsuario = 0
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    key=[usuario])
        for fila in filas:
          key                 = fila.key
          value               = fila.value
          doc                 = fila.doc
          timeStampUsuario  = doc['ultimoIngresoAlarmas']
        return timeStampUsuario
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

  
def contarCantidadNotificacionesAlarmas(peticion, timeStampUsuario):
    #revisar funcion ojoooooooooooooooo
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    cont = 0 # variable temporal implementar reduce
    print "############################"
    print time.time()
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/alarmas/_view/alarmasTimestamp',
            startkey        = [timeStampUsuario],
            reduce        = True,
            group_level   = 0
            )
        value = 0
        for fila in filas:
          key                 = fila.key
          value               = fila.value 
          #doc                 = fila.doc
          #cont += 1 # temporal implementar reduce 
        return value
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#funcion principal para mostrar 
#la cantidad de alarmas contadas. Este metodo lo invoca baseAdminTenant.html
def mostrarAlarmasNoVistasUsuario(peticion):
  timeStampUsuario = traerTimeStampUsuario(peticion)
  if  timeStampUsuario != 0:
    cantidadNotifNoVistas = contarCantidadNotificacionesAlarmas(peticion, timeStampUsuario)
    return { 'success' : True, 'mensaje':cantidadNotifNoVistas }
  else:
    return { 'success' : False, 'mensaje':"" }


  
