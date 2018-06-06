# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from jsonschema               import validate, ValidationError
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
from ws.serviciosweb.modulos.integracionGPS.funcionesTwilio import crearLlamada
import time
from twilio.rest import TwilioRestClient
import random
from ..geocoderFleet          import geocoderFleet
from ..cadenaFrio                 import cadenaFrio

#-------------------------------------------------------------
# def listarMapaVehiculos( peticion ):
#     autenticacion = peticion['autenticacion']
#     datos         = peticion['data']
#     usuario       = autenticacion['usuario']
#     tenant      = autenticacion['tenant']
    
#     db = conexion.getConexionTenant(tenant)

#     if db == None:
#         return { 'success' : False, 'mensaje': "existe el tenant" }

#     try:
#         dataRaw = []
#         filas = db.view('_design/posicionVehiculos/_view/posicionVehiculosUltimaPosicion',
#                     include_docs  = True,
#                     startkey      = [True, 0],
#                     endkey        = [True, {}] )
#         for fila in filas:
#           key   = fila.key
#           value = fila.value
#           doc   = fila.doc
#           #logging.warning(fila)
#           dataRaw.append({
#           	'idVehiculo' : doc['_id'],
#           	'placa'      : doc['placa'],
#           	'latitud'    : value['latitud'],
#           	'longitud'   : value['longitud'],
#           	'estado'     : value['estado']
#           	})            
#         return {
#             'success' : True,
#             'data'    : dataRaw
#         }
#     except ValueError:
#         pass

#     return { 'success' : False, 'mensaje':"error desconocido" }

def listarMapaVehiculos( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs  = True,            
        )
        for fila in filas:
          key   = fila.key
          value = fila.value
          doc   = fila.doc
          #logging.warning(fila)

          docPosicion = {}
          filasPosicion = db.view(
              '_design/posicionVehiculos/_view/posicionFechaCreacion',
              include_docs  = True,
              limit         = 1,
              descending    = True,
              startkey      = [doc["_id"], {}],
              endkey        = [doc["_id"], 0]
          )
          
          for filaPosicion in filasPosicion:
              docPosicion = filaPosicion.doc

          #TODO FABIO QUITAR!!!!!!!!!!
          if docPosicion.get('latitud') == None or docPosicion.get('longitud') == None:
              continue
          #busca las n posiciones anteriores a la actual. Si en todas las posiciones 
          #su velocidad es 0 el vehiculo esta detenido (movimiento = False) si no el
          # vehiculo esta en movimiento (movimiento = True)
          movimiento, velocidadReportada = buscarVelocidadActualVehiculo(db, doc['_id'])

          itemVehiculo = {
              'idVehiculo' : doc['_id'],
              'placa'      : doc['placa'],
              'latitud'    : float(docPosicion.get('latitud')),
              'longitud'   : float(docPosicion.get('longitud')),
              'estado'     : docPosicion.get('estado'),
              'movimiento' : movimiento,
              'velocidad'  : velocidadReportada,
              'opcionesAdicionalesPlataforma' : doc.get('opcionesAdicionalesPlataforma', None),              
                            
          }

          if doc['_id'] == "a6a9368d6c64bb1cdbab24cd05bec5ed":
              #TODO FABIO DUMMIE
              itemVehiculo["estaAlarmaCadenaFrioActivada"] = doc.get("estaAlarmaCadenaFrioActivada", False)
              itemVehiculo["tempLimSuperior"] = doc.get("tempLimSuperior", 0)              
              itemVehiculo["tempLimInferior"] = doc.get("tempLimInferior", 0)
              itemVehiculo["temperatura"]     = cadenaFrio.getTemperaturaVehiculo(db, doc['_id'])
          
          dataRaw.append(itemVehiculo)            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensa  #e':"error desconocido" }


#----------------------------------------------------


def obtenerEstadoVehiculo(peticion, idVehiculo):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    estado        = ""
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/posicionVehiculos/_view/posicionVehiculosUltimaPosicion',
                    include_docs  = True,
                    key      = [True, idVehiculo],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            estado = value.get('estado',"")          
        return estado
    except ValueError:
        pass


def listarVehiculos(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    incluirDireccion = datos.get("incluirDireccion",False)
    
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw     = []
        conductor   = ""
        filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
        for fila in filas:
          key   = fila.key
          value = fila.value
          doc   = fila.doc

          idVehiculo = doc.get('_id')

          docUltimaPosicionVehiculo = getDocUltimaPosicionVehiculo(db,idVehiculo)
          idConductor = doc.get('conductor')
          if not(idConductor == ""):
            docConductor    = db[idConductor]
            conductor       = u"{}-{} {}".format(docConductor['cedula'], docConductor['nombres'], docConductor['apellidos'])

          direccion = ""
          if incluirDireccion:
              direccion = geocoderFleet.getDireccion(
                  docUltimaPosicionVehiculo.get("latitud", ""),
                  docUltimaPosicionVehiculo.get("longitud","")
              );
              
          dataRaw.append({
              'idVehiculo'     : idVehiculo,
              'placa'          : doc.get('placa'),
              'marca'          : doc.get('marca'),
              'modelo'         : doc.get('modelo'),
              'imeiGps'        : traerImeiGpsVehiculo(idVehiculo),
              'numSimCard'     : traerNumeroSimCardVehiculo(idVehiculo),
              'tipoGps'        : traerTipoGPSVehiculo(idVehiculo),
              'estado'         : obtenerEstadoVehiculo(peticion, idVehiculo),              
              'conductor'      : conductor,
              'ultimaPosicion' : {
                  'latitud'        : docUltimaPosicionVehiculo.get("latitud",""),
                  'longitud'       : docUltimaPosicionVehiculo.get("longitud",""),
                  'horaRecibida'   : docUltimaPosicionVehiculo.get("horaRecibida",""),
                  'horaRegistrada' : docUltimaPosicionVehiculo.get("horaRegistrada",""),
                  'velocidad'      : docUltimaPosicionVehiculo.get("velocidad",""),
              },
              "direccion" : direccion,
              'opcionesAdicionalesPlataforma' : doc.get('opcionesAdicionalesPlataforma', None)
            })
          conductor = ""
          
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

def listarDetalleVehiculo(peticion):

    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idVehiculo    = datos['id']

        filas = db.view('_design/detalleVehiculo/_view/detalleVehiculo',
                    include_docs  = True, 
                    startkey = [idVehiculo,0],
                    endkey = [idVehiculo,{}])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          idVehiculo = doc.get('_id')
          dataRaw = {
              'idVehiculo' : doc.get('_id'),
              'placa' : doc.get('placa'),
              'marca' : doc.get('marca'),
              'modelo' : doc.get('modelo'),
              'imeiGps' : traerImeiGpsVehiculo(idVehiculo),
              'numSimCard' : traerNumeroSimCardVehiculo(idVehiculo),
              'tipoGps'    : traerTipoGPSVehiculo(idVehiculo),
              'conductor': doc.get('conductor'),
              'cargado'  : doc.get('cargado'),
              'opcionesAdicionalesPlataforma': doc.get('opcionesAdicionalesPlataforma', None),
              'estaAlarmaCadenaFrioActivada' : doc.get('estaAlarmaCadenaFrioActivada',False),
              "tempLimSuperior" : doc.get('tempLimSuperior',0),
              "tempLimInferior" : doc.get('tempLimInferior',0),
				
              
            }            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False}

#-------------------------------------------------------------


def posicionVehiculoRangoFecha(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        fechaInicio  = datos['fechaInicio']
        fechaFin     = datos['fechaFin']
        idVehiculo   = datos['id']

        intercalarDatos         = datos.get( "intercalarDatos", False)
        numeroDatosIntercalados = datos.get( "numeroDatosIntercalados", 1000)
        
        filas = db.view(
            '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
            include_docs = True ,
            #descending  = True,
            startkey     = [idVehiculo, fechaInicio],
            endkey       = [idVehiculo, fechaFin]                        
        )
        
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'idVehiculo'        : doc.get('_id'),
            'horaRegistrada'    : doc.get('horaRegistrada'),
            'horaRecibida'      : doc.get('horaRecibida'),
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'velocidad'         : doc.get('velocidad'),
            'idFragmentoParada' : doc.get('idFragmentoParada')
            })

        
        if intercalarDatos:
            dataRawIntercalado = [ ]
            salto              = int( round( 1.0 * len(dataRaw) / numeroDatosIntercalados ) )
            print u"Salto {}".format(salto)
            contador           = 0
            for dato in dataRaw:
                if contador == 0 or salto == 0:
                    dataRawIntercalado.append(dato)
                    contador += 1
                elif contador >= salto :                    
                    contador = 0
                else:
                    contador += 1
                    

            dataRaw = dataRawIntercalado
          
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}


#-------------------------------------------------------------


def vehiculoRangoFechaCapturaImagen(peticion):
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
        idVehiculo      = datos['id']
###
        filas = db.view('_design/posicionVehiculoRangoFecha/_view/capturaImagenes',
                    include_docs  = True ,
                    startkey = [idVehiculo , fechaFin],
                    endkey = [idVehiculo, fechaInicio],
                    descending    = True)

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'idVehiculo' : doc.get('_id'),
            'horaRegistrada' : doc.get('horaRegistrada'),
            'latitud' : doc.get('latitud'),
            'longitud' : doc.get('longitud'),
            'idImagen': doc.get('idImagen',""),
            'urlImagen' : settings.NISABU_IMAGE_URL+doc.get('idImagen', "")
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}


#-------------------------------------------------------------


def vehiculoRangoFechaCapturaAudio(peticion):
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
        idVehiculo      = datos['id']
###
        filas = db.view('_design/posicionVehiculoRangoFecha/_view/capturaAudio',
                    include_docs  = True ,
                    startkey = [idVehiculo, fechaFin],
                    endkey = [idVehiculo, fechaInicio],
                    descending    = True)

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'idVehiculo' : doc.get('_id'),
            'horaRegistrada' : doc.get('horaRegistrada'),
            'latitud' : doc.get('latitud'),
            'longitud' : doc.get('longitud'),
            'duracion' : doc.get('duracion'),
            'urlAudio' : doc.get('urlAudio')
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}


#-------------------------------------------------------------

def vehiculoRangoFechaAlarma(peticion):
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
        idVehiculo  = datos['id']
###
        filas = db.view('_design/posicionVehiculoRangoFecha/_view/capturaAlarmas',
                    include_docs  = True ,
                    startkey = [idVehiculo,fechaFin],
                    endkey = [idVehiculo, fechaInicio],
                    descending    = True)

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          tipoCaptura = doc.get('tipoCaptura')
          if tipoCaptura == "imagen":
            urlCaptura = settings.NISABU_IMAGE_URL
          else:
            urlCaptura = settings.NISABU_IMAGE_URL
          dataRaw.append({
            'idVehiculo' : doc['_id'],
            'horaRegistrada' : doc.get('horaRegistrada'),
            'descripcion' : doc.get('descripcion'),
            'latitud': doc.get('latitud'),
            'longitud': doc.get('longitud'),
            #'detalleImagen': doc.get('detalleImagen', doc.get('detalle_imagen', '') )#doc['detalleImagen']
            'idCaptura': doc.get('idCaptura',""),
            'urlCaptura': urlCaptura + doc.get('idCaptura', ""),
            #'urlCaptura': doc.get('urlCaptura',""),
            'tipoCaptura': doc.get('tipoCaptura'),
            'duracion' : doc.get('duracion')
            })
       
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}



#-------------------------------------------------------------

"""
def ultimaPosicionVehiculo(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idVehiculo    = datos['id']
###
        filas = db.view('_design/posicionVehiculos/_view/posicionVehiculosUltimaPosicion',
                    include_docs  = True, 
                    key = [True, idVehiculo])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw = {
            'idVehiculo' : doc['_id'],
            'horaRegistrada' : value.get('horaRegistrada'),
            'horaRecibida' : value.get('horaRecibida'),
            'latitud' : value.get('latitud'),
            'longitud': value.get('longitud')
            }            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}
"""

def ultimaPosicionVehiculo(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idVehiculo    = datos['id']
###
        filas = db.view('_design/posicionVehiculos/_view/ultimaPosicionGuardada',
                    include_docs  = True, 
                    key = [True, idVehiculo])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw = {
            'idVehiculo' : doc['_id'],
            'horaRegistrada' : doc.get('horaRegistrada'),
            'horaRecibida' : doc.get('horaRecibida'),
            'latitud' : doc.get('latitud'),
            'longitud': doc.get('longitud'),
            'estado'  : doc.get('estado')
            }            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}


#-------------------------------------------------------------
def listVehiculos(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    numeroOpcionHabilitadaPlataforma = datos.get("numeroOpcionHabilitadaPlataforma",None)
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          if not(numeroOpcionHabilitadaPlataforma == None):
            # Consulta realizada para validar si un vehiculo tiene configurada la opcion en la platafor
            opcionesAdicionalesPlataforma = doc.get("opcionesAdicionalesPlataforma", [])
            if not(opcionesAdicionalesPlataforma == None):
              if numeroOpcionHabilitadaPlataforma == U'19' and numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                # vehiculos de la cadena de frio permiso 19
                estadoPermisoCadenaFrio = doc.get('estaAlarmaCadenaFrioActivada', False)
                if estadoPermisoCadenaFrio: 
                  dataRaw.append({
                    'idVehiculo' : doc.get('_id'),
                    'placa' : doc.get('placa')
                  })
              else:
                if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                  dataRaw.append({
                    'idVehiculo' : doc.get('_id'),
                    'placa' : doc.get('placa')
                  })
          else:
            #consulta normal si no se recibe el parametro numeroOpcionHabilitadaPlataforma
            dataRaw.append({
              'idVehiculo' : doc.get('_id'),
              'placa' : doc.get('placa')
            })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except :
        pass

    return { 'success' : False}



#-------------------------------------------------------------

def listarParadaVehiculo(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        fechaInicio     = datos['fechaInicio']
        fechaFin        = datos['fechaFin']
        idVehiculo      = datos['id']
        filas = db.view('_design/posicionVehiculos/_view/paradaVehiculo',
                    include_docs  = True ,
                    startkey = [idVehiculo, fechaInicio],
                    endkey = [idVehiculo, fechaFin])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'latitud'           : doc.get('latitud'),
            'longitud'          : doc.get('longitud'),
            'fechahoraInicio'   : doc.get('fechahoraInicio'),
            'fechahoraFin'      : doc.get('fechahoraFin')
            })
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'mensaje' : 'aqui llego'}



#-------------------------------------------------------------
#funciones para las llamadas Twilio

#busca el punto anterior del vehiculo
def buscarUltimaPosicionVehiculo(peticion, idVehiculo):
    # Segun la deficnicion de la vista es la ultima 
    #posicion guardada en la base de datos
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
                    limit = 1)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc         
    except ValueError:
        pass
    return doc

#funcion para guardar el documento capturaAudio que se muestra en una tabla
def guardarDocCapturaAudio(peticion, doc_idLlamada, idVehiculo):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 

        docUltimaPosicion = buscarUltimaPosicionVehiculo(peticion, idVehiculo)
        doc_id, doc_rev = db.save({
            "tipoDato"        : "capturaAudio",
            "creadoEn"        : datetime.now().isoformat(),
            "modificadoEn"    : datetime.now().isoformat(),
            "modificadoPor"   : usuario,
            "horaRegistrada"  : datetime.now().isoformat(),
            "latitud"         : docUltimaPosicion.get('latitud'),
            "longitud"        : docUltimaPosicion.get('longitud'), 
            "duracion"        : "",  
            "idLlamada"       : doc_idLlamada,
            "idVehiculo"      : idVehiculo,
            "estado"          : "En curso", 
            "urlAudio"        : "", 
            "activo"          : True
        })
        return doc_id
    except ValueError:
        return { 'success' : False }


#funcion para guardar el documento de la llamada
def guardarDocLLamadas(peticion, idVehiculo, sid):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 

        doc_id, doc_rev = db.save({
            "tipoDato"      : "llamadas",
            "creadoEn"      : datetime.now().isoformat(), 
            "idVehiculo"    : idVehiculo, 
            "sidLlamada"    : sid,
            "estado"        : "En curso", 
            "razonLLamada"  : "usuario", 
            "idRemitente"   :  usuario,
            "limite"        : "",
            "activoPanico"  : False,
            "activo"        : True
        })
        return doc_id
    except ValueError:
        return { 'success' : False }

"""
def crearLlamada(client, destino, origen):
    call = client.calls.create(url="http://fleetbi.cloud/llamada.xml",
        to=destino,
        from_= origen, record=True)
    return call.sid
"""

def terminarLlamada(client, sid):
    call = client.calls.update(sid, status="completed")

def solicitarCapturaAudio(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    tiempoLlamada   = settings.TWILIO_TIEMPO_LLAMADA 
    numeroFLEET     = settings.TWILIO_NUMERO 
    account_sid     = settings.TWILIO_ACCOUNT_SID 
    auth_token      = settings.TWILIO_AUTH_TOKEN 

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        idVehiculo      = datos['idVehiculo']
        doc             = db[idVehiculo]
        numSimCardVehiculo      =  traerNumeroSimCardVehiculo(idVehiculo) # revisar esta linea posiblemente es con el id GPS
        client = TwilioRestClient(account_sid, auth_token)
        #DESCOMENTAR PARA QUE FUNCIONE
        sid = crearLlamada(client, numSimCardVehiculo,  numeroFLEET )
        #sid = "prueba llamada directa"
        #guardar el documento llamada con sid y el estado En curso,razonllamada:usuario
        doc_idLlamada = guardarDocLLamadas(peticion, idVehiculo, sid)
        #guardar documento capturaAudio
        doc_idCapturaAudio = guardarDocCapturaAudio(peticion, doc_idLlamada, idVehiculo)
        return {
            'success' : True,
            'sid'    : sid 
        }
    except ValueError:
        return { 'success' : False, 'mensaje' : 'Error al hacer la grabación'}

#--------------------------------------------------------------------

def listarLlamada(peticion, sid):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/llamadas/_view/llamadas',
                    include_docs  = True, 
                    startkey = [sid],
                    endkey = [sid])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
        return doc
    except :
        return { 'success' : False}

def modificarDocumentoLlamadas(peticion, idDocLlamadas):
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    docLlamadas     = db[idDocLlamadas]
    docLlamadas["estado"] = "Finalizado"
    db.save(docLlamadas) 

#Inicio funciones para modificar doc captura audio
def listarAudiosLlamadas(peticion, idDocLlamadas):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/llamadas/_view/audiosLlamadas',
                    include_docs  = True, 
                    startkey = [idDocLlamadas],
                    endkey = [idDocLlamadas])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
        return doc
    except :
        return { 'success' : False}

def modificarDocumentoCapturaAudio(peticion, idDocCapturaAudio, duracionLlamada, urlAudio):
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    docCapturaAudio             = db[idDocCapturaAudio]
    docCapturaAudio["estado"]   = "Finalizado"
    docCapturaAudio["duracion"] = duracionLlamada
    docCapturaAudio["urlAudio"] = urlAudio
    db.save(docCapturaAudio) 

def consultarDuracionLlamadaTwilio(sid, client):
    call = client.calls.get(sid)
    return call.duration

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

#Fin funciones para modificar doc captura audio

def verificarLlamadaDirecta(peticion, idDocLlamadas):
    respuesta = False
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    docLlamadas     = db[idDocLlamadas]
    if docLlamadas["razonLLamada"] == "usuario" and docLlamadas["estado"] == "En curso":
        print "entro=================================================="
        print idDocLlamadas
        respuesta = True
    return respuesta


def detenerCapturaAudio(peticion):
    datos           = peticion['data']
    account_sid     = settings.TWILIO_ACCOUNT_SID 
    auth_token      = settings.TWILIO_AUTH_TOKEN 
    try:
        client      = TwilioRestClient(account_sid, auth_token)
        sid         = datos['sid']
        #al momento de terminar la llamada modifica el documento con el estado finalizado
        docLlamadas     = listarLlamada(peticion, sid)
        idDocLlamadas   = docLlamadas["_id"]
        #Verificar si es una llamada directa si es asi de puede detener la llamada
        llamadaDirecta = verificarLlamadaDirecta(peticion, idDocLlamadas)
        if llamadaDirecta:
            #DESCOMENTAR PARA QUE FUNCIONE
            terminarLlamada(client, sid)
            modificarDocumentoLlamadas(peticion, idDocLlamadas)
            #Modidicar estado a Finalizado Doc capturaAudios, duracion llamada y url audio
            docCapturaAudio     =   listarAudiosLlamadas(peticion, idDocLlamadas)
            idDocCapturaAudio   = docCapturaAudio["_id"]
            #DESCOMENTAR PARA QUE FUNCIONE
            duracionLlamada     = consultarDuracionLlamadaTwilio(sid, client)
            #duracionLlamada      = 5
            #Url audio
            #DESCOMENTAR PARA QUE FUNCIONE
            urlAudio            = consultarUrlGrabacion(sid, client)
            #urlAudio = "url"
            modificarDocumentoCapturaAudio(peticion, idDocCapturaAudio, duracionLlamada, urlAudio)
            return {
                'success' : True,
                'respuesta': "Se detuvo la llamada del usuario" 
            }
        else:
            return {
            'success' : False,
            'respuesta': "Existe una llamada en curso automática" 
            }

    except ValueError:
        return { 'success' : False, 'mensaje' : 'Ha ocurrido un error'}
#----------------------------------------------------------------------------------------------------------

def verificarEstadoLlamada(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idVehiculo    = datos['idVehiculo']
        filas = db.view('_design/llamadas/_view/estadoLlamadas',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"],
                    limit = 1)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            dataRaw ={
                'estado'    : doc.get('estado'),
                'sidLlamada' : doc.get('sidLlamada')
                }
        return {
            'success' : True,
            'data': dataRaw 
        }

    except:
        return { 'success' : False}



def buscarLlamadaActivaDirecta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = {}
        idVehiculo    = datos['idVehiculo']
        filas = db.view('_design/llamadas/_view/estadoLlamadas',
                    include_docs  = True, 
                    key = [idVehiculo, "En curso"],
                    limit = 1)
        sid   = ""
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            if doc.get('razonLLamada') == "usuario" and not(doc.get('activoPanico')):
                sid = doc.get('sidLlamada')

                return {
                    'success' : True,
                    'sidLlamada': sid 
                }
            else:
                return { 'success' : False}
        if sid == "":
            return { 'success' : False}            

    except:
        return { 'success' : False}

    
#----------------------------------------------------------------------------------------------------------
def verificarPlaca(db, placa):
    existePlaca = False    
    try:
        filas = db.view('_design/detalleVehiculo/_view/buscarPlacaVehiculo',
                    include_docs  = True, 
                    key      = [placa])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            existePlaca = True     
        return existePlaca
    except :
        return existePlaca



#Crear vehiculo desde administrador
def crearVehiculoAdminTenant(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    tennant   = docTenant.get("urlTenant")
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    
    try: 
        idGps   =   datos["idGps"]
        print "entre al try y el idGps es: "+idGps
        
        if not idGps == "":
            print "entre al if y el idGps es: "+idGps
            filas = dbAdmin.view(
                                 '_design/GPS/_view/gpsPorId',
                                 include_docs   = True,
                                 startkey       = [idGps,0],
                                 endkey         = [idGps,{}]
            )
            totalFilas = len(filas)
            str(totalFilas)
            print "despues de consulta y el resultado es de : ",totalFilas
            idVehiculo = ""
            for fila in filas:
                key           = fila.key
                value         = fila.value
                doc           = fila.doc
                idVehiculo    = doc.get('idVehiculo', '')
                print "entre al for : "+idVehiculo

        placa = datos["placa"]
        existePlaca = verificarPlaca(db, placa)    
        if existePlaca:
            return { 'success' : False, 
                     'data'    : {
                        'existePlaca' : existePlaca
                     }
            }
        else:                        
            doc_id, doc_rev = db.save({
                "activo"        : True,
                "tipoDato"        : "vehiculos",
                "creadoEn"        : datetime.now().isoformat(),
                "modificadoEn"    : datetime.now().isoformat(),
                "modificadoPor"   : usuario,
                "placa"           : datos["placa"],
                "marca"           : datos["marca"],
                "modelo"          : datos["modelo"],
                "referencia"      : datos.get("referencia",""),
                "marcaMotor"      : datos.get("marcaMotor",""),
                "referenciaMotor" : datos.get("referenciaMotor",""),
                "consumoGalKm"    : datos.get("consumoGalKm",0),
                "conductor"       : "",
                "cargado"         : False,
                "opcionesAdicionalesPlataforma" :datos.get("opcionesAdicionalesPlataforma", None)
      
            })

            if not idGps == "":
                if not idVehiculo == "":
                        return { 'success' : False, 
                               'mensaje': "El gps ya esta asociado al vehículo: "+idVehiculo }
                        
                else:
                    docGps                  = dbAdmin[datos["idGps"]]
                    docGps['idVehiculo']    = doc_id
                    docGps['tenant']        = docTenant.get("urlTenant")
                    dbAdmin.save(docGps)
            
            return {
                'success' : True,
                'data'    : {
                    'id' : doc_id
                }            
            }
        
    except ValidationError as e:
        print "error del try "+e.message
        pass

    return { 'success' : False }

#-------------------------------------------------------------
def compararVehiculos(db, placa, idDocVehiculo):
    docsVehiculos = db[idDocVehiculo]
    if docsVehiculos["placa"] == placa:
        return True
    else:
        return False    

def buscarVehiculoRepetido(db, placa, idVehiculo):
    existeVehiculo = False
    docsVehiculos = []    
    try:
        filas = db.view('_design/detalleVehiculo/_view/buscarPlacaVehiculo',
                    include_docs  = True, 
                    key      = [placa])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            idDoc   = doc.get('_id')
            if idDoc != idVehiculo:
                docsVehiculos.append(idDoc) 
        for idDocVehiculo in docsVehiculos:
            vehiculosIguales =   compararVehiculos(db, placa, idDocVehiculo)
            if vehiculosIguales:
                return True
        return False           
    except :
        return existeVehiculo

#Editar vehiculo desde administrador
def editarVehiculoAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return {
            'success' : False,
            "mensaje" : "NO se encuentra la base de datos"
        }

    docTenant = dbAdmin[datos["idTenant"]]
    Tennant   = docTenant.get("urlTenant")
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    
    try:
        idVehiculo   = datos["idVehiculo"]
        placa           =   datos['placa']
        existePlaca   =   buscarVehiculoRepetido(db, placa, idVehiculo)
        if existePlaca:
            return { 'success' : False, 
                     'data'    : {
                        'existePlaca' : existePlaca
                     }
            }            
        else:
            idGps   =   datos["idGps"]
            idVehiculo  = datos['idVehiculo']
            print "entre al try idGps: ",idVehiculo
            
            #busco todos los gps que tengan asociado el id del vehiculo y borro todas las asociaciones 
            filas = dbAdmin.view(
                                     '_design/GPS/_view/gpsPorVehiculo',
                                     include_docs   = True,
                                     startkey       = [idVehiculo,0],
                                     endkey         = [idVehiculo,{}]
                )
            
            totalFilas = len(filas)
            str(totalFilas)
            print "despues de consulta y el resultado es de : ",totalFilas
          
            for fila in filas:
                key           = fila.key
                value         = fila.value
                docGps        = fila.doc
                idVehiculo    = docGps.get('idVehiculo', '')
                docGps['idVehiculo'] = ""
                docGps['tenant'] = ""
                dbAdmin.save(docGps)
                print "entre al for : "+idVehiculo
            
            
            doc = db[datos['idVehiculo']]
            doc['modificadoPor']    = usuario
            doc['modificadoEn']     = datetime.now().isoformat()
            doc['placa']            = datos['placa']
            doc['marca']            = datos['marca']
            doc['activo']           = datos['estado']
            doc['modelo']           = datos['modelo']
            doc['opcionesAdicionalesPlataforma']  = datos['opcionesAdicionalesPlataforma']
            
            doc["referencia"]      = datos.get("referencia","")
            doc["marcaMotor"]      = datos.get("marcaMotor","")
            doc["referenciaMotor"] = datos.get("referenciaMotor","")
            doc["consumoGalKm"]    = datos.get("consumoGalKm",0)
            
            #Guardo el idvehiculo en el Gps 
            if not idGps == "":
                print "entre al if idGps: "+idGps
                docGps                  = dbAdmin[datos["idGps"]]
                docGps['idVehiculo']    = datos['idVehiculo']
                docGps['tenant']        = docTenant.get("urlTenant")
                dbAdmin.save(docGps)

            
            db.save(doc)
            
            return {
                'success' : True,
                'data'    : {
                }            
            }
    except ValidationError as e:
        print "error del try "+e.message
        pass

    return {
        'success' : False,
        "mensaje" : "Error desconocido"
    }

#-------------------------------------------------------------

def eliminarAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    
    try:
        idEquipo    = datos['id']
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

def detalleVehiculoAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    
            
    try:
        doc            = db[datos['id']]
        filasGps       = dbAdmin.view(
                                     '_design/GPS/_view/gpsPorVehiculo',
                                     include_docs = True,
                                     startkey     = [doc['_id'],0],
                                     endkey       = [doc['_id'],{}]
                                 )
                 
        idGps            = ""
        
        if not len(filasGps) == 0:
            for filaGps in filasGps:
                docGps           = filaGps.doc
                idGps            = docGps.get("_id") 
               
        
        dataResponse = {
            'id'                    : doc['_id'],
            'activo'                : doc['activo'],
            'placa'                 : doc.get('placa', ''),
            'marca'                 : doc.get('marca', ''),
            'modelo'                : doc.get('modelo', ''),
            'idGps'                 : idGps,            
            "referencia"      : doc.get("referencia",""),
            "marcaMotor"      : doc.get("marcaMotor",""),
            "referenciaMotor" : doc.get("referenciaMotor",""),
            "consumoGalKm"    : doc.get("consumoGalKm",0),
            "opcionesAdicionalesPlataforma" : doc.get("opcionesAdicionalesPlataforma", None)
            
         }
        
        return {
            'success' : True,
            'data'    : dataResponse 
        }    
    except:
        pass

    return { 'success' : False }

#-------------------------------------------------------------

def pickerVehiculos(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    numeroOpcionHabilitadaPlataforma = datos.get("numeroOpcionHabilitadaPlataforma",None)
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs  = True
        )
        
        for fila in filas:
          key               = fila.key
          value             = fila.value
          doc               = fila.doc
          eliminado         = doc.get('eliminado','')
          activo            = doc.get('activo','')
          if not(eliminado) and activo:

              idConductor  = doc.get("conductor", "")
              docConductor = {}

              if not idConductor == "":
                  docConductor = db[idConductor]

              nombreConductor = u"{} {}".format(
                  docConductor.get("nombres", ""),
                  docConductor.get("apellidos", "")
              )

              nombre = u"{} - {}".format(
                  doc.get("placa",""),
                  nombreConductor
                  
              )
              if not(numeroOpcionHabilitadaPlataforma == None):
                # Consulta realizada para validar si un vehiculo tiene configurada la opcion en la plataforma
                opcionesAdicionalesPlataforma = doc.get("opcionesAdicionalesPlataforma", [])
                if not(opcionesAdicionalesPlataforma == None):
                  if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                    dataRaw.append({
                        'id'     : doc.get('_id',''),
                        'nombre' : nombre,
                        'conductor' : {
                            'nombres'   : docConductor.get("nombres", ""),
                            'apellidos' : docConductor.get("apellidos", ""),
                            'cedula'    : docConductor.get("cedula", "")
                        },
                        'vehiculo' : {
                            "placa" : doc.get("placa", "")
                        }
                        
                    })
              else:
                #consulta normal si no se recibe el parametro numeroOpcionHabilitadaPlataforma
                dataRaw.append({
                    'id'     : doc.get('_id',''),
                    'nombre' : nombre,
                    'conductor' : {
                        'nombres'   : docConductor.get("nombres", ""),
                        'apellidos' : docConductor.get("apellidos", ""),
                        'cedula'    : docConductor.get("cedula", "")
                    },
                    'vehiculo' : {
                        "placa" : doc.get("placa", "")
                    }
                    
                })

        return {
            'success' : True,
            'data'    : dataRaw
        }
    except BufferError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#=============================================================
# Auxiliares
#=============================================================

def getDocUltimaPosicionVehiculo(db, idVehiculo):

    docPosicion = {}

    filas = db.view(
        '_design/posicionVehiculos/_view/posicionFechaCreacion',
        include_docs  = True,   
        startkey      = [idVehiculo,{}],
        endkey        = [idVehiculo, 0],
        limit         = 1,
        descending    = True
    )

    for fila in filas:
        docPosicion = fila.doc
        
    return docPosicion

def traerNumeroSimCardVehiculo(idVehiculo):
    numero = ""
    dbFleet = conexion.getConexionFleet()

    filas = dbFleet.view(
        '_design/GPS/_view/gpsPorIdVehiculo',
        include_docs  = True,   
        key = [idVehiculo],
        limit = 1
    )

    for fila in filas:
        docGps = fila.doc
        numero = docGps.get("numSimCard","")
        
    return numero


def traerImeiGpsVehiculo(idVehiculo):
    numero = ""
    dbFleet = conexion.getConexionFleet()

    filas = dbFleet.view(
        '_design/GPS/_view/gpsPorIdVehiculo',
        include_docs  = True,   
        key = [idVehiculo],
        limit = 1
    )

    for fila in filas:
        docGps = fila.doc
        numero = docGps.get("imei","")
        
    return numero
    
def traerTipoGPSVehiculo(idVehiculo):
    tipo = ""
    dbFleet = conexion.getConexionFleet()

    filas = dbFleet.view(
        '_design/GPS/_view/gpsPorIdVehiculo',
        include_docs  = True,   
        key = [idVehiculo],
        limit = 1
    )

    for fila in filas:
        docGps = fila.doc
        tipo = docGps.get("tipo","")
        
    return tipo


def actualizarEstadoCarga(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['idVehiculo']]
        doc['modificadoPor']         = usuario
        doc['modificadoEn']          = datetime.now().isoformat()
        doc['cargado']               = datos.get('cargado', '')
        db.save(doc)
        return {
            'success' : True,
            'data'    : {
            }            
        }   

    except ValidationError as e:
        print "error del try "+e

    return { 'success' : False }


def buscarVelocidadActualVehiculo(db, idVehiculo):
  movimiento            = False
  velocidadReportada    = 0
  try:
    filas = db.view(
      '_design/posicionVehiculos/_view/posicionFechaCreacion',
      include_docs  = True,
      limit         = settings.CANTIDADPUNTOSMOVIMIENTO,
      descending    = True,
      startkey      = [idVehiculo, {}],
      endkey        = [idVehiculo, 0]
    )
    for fila in filas:
      key     = fila.key
      value   = fila.value
      doc     = fila.doc
      velocidad = doc.get('velocidad', 0.0)
      if float(velocidad) > 1.0:#si la velocidad es mayor a 1 el vehiculo esta en movimiento
        movimiento = True
    return movimiento, velocidad
  except ValidationError as e:
     print "error del try "+e
     return False
