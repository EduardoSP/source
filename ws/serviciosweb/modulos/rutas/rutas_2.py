# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.http                import HttpResponse
from jsonschema               import validate, ValidationError
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
from django.db              import IntegrityError, transaction
import time
import geocoder


def crearRuta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        puntosRuta          = datos["puntosRuta"]
        idDocPuntosRutaDefinida = crearDocPuntosDefinicionRuta(db, usuario, puntosRuta)
        doc_id, doc_rev = db.save({
            "tipoDato"        	: "rutas",
            "creadoEn"        	: datetime.now().isoformat(),
            "modificadoEn"    	: datetime.now().isoformat(),
            "modificadoPor"   	: usuario,
            "nombreRuta"		: datos["nombreRuta"],
            "origen"			: datos["origen"],
            "destino"           : datos["destino"],
            "direccionOrigen"   : datos["direccionOrigen"],
            "direccionDestino"  : datos["direccionDestino"], 
            "idPuntosRutaDefinida"  : idDocPuntosRutaDefinida,
            "puntosParadas"     : datos["puntosParadas"],
            "zoom"              : datos.get("zoom",4), # datos["zoom"],
            "activo"          	: True,
            "eliminado"         : False
        })
        return {
            'success' : True,
            'idDocRuta'  : doc_id,
            'idDocPuntosDefinicionRuta'    : idDocPuntosRutaDefinida
        }

    except ValueError:
        return { 'success' : False }


def crearDocPuntosDefinicionRuta(db, usuario, puntosRuta):

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"          : "puntosRutaDefinida",
            "creadoEn"          : datetime.now().isoformat(),
            "modificadoEn"      : datetime.now().isoformat(),
            "modificadoPor"     : usuario,
            "puntosRuta"        : puntosRuta,
            "activo"            : True,
            "eliminado"         : False
        })
        return doc_id

    except ValueError:
        return { 'success' : False }


def listarRutas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/rutas/_view/listarRutas',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          if not(doc['eliminado']):
              puntosParadas         = doc['puntosParadas']
              cantidadCargaDescarga = obtenerCantidadCargaDescarga(puntosParadas)
              dataRaw.append({
                'id'                : doc['_id'],
                'nombreRuta'        : doc['nombreRuta'],
                'latitudOrigen'     : doc['origen'][0],
                'longitudOrigen'    : doc['origen'][1],
                'latitudDestino'    : doc['destino'][0],
                'longitudDestino'   : doc['destino'][1],
                'direccionOrigen'   : doc['direccionOrigen'],
                'direccionDestino'  : doc['direccionDestino'],
                'cantidadCarga'     : cantidadCargaDescarga["Carga"],
                'cantidadDescarga'  : cantidadCargaDescarga["Descarga"],  
                'activo'            : doc['activo'],
                'eliminado'         : doc['eliminado']
                })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


def buscarDireccion(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)
    direccion = obtenerDireccionGeocoder(db, datos["latitud"], datos["longitud"])
    return {
        'success' : True,
        'direccion'    : direccion }

    # if db == None:
    #     return { 'success' : False, 'mensaje': "existe el tenant" }
    # try:
    #     nombreGeoposicion = ""
    #     filas = db.view('_design/geoposiciones/_view/geoposicionesPrecalculadas',
    #                 key         = [datos["latitud"], datos["longitud"]],
    #                 include_docs  = True,
    #                 limit         = 1
    #     )
    #     for fila in filas:
    #       key = fila.key
    #       value = fila.value
    #       doc = fila.doc
    #       nombreGeoposicion = doc.get("nombreGeoposicion", "")
    #       direccion         = nombreGeoposicion

    #     if nombreGeoposicion == "":
    #         g = geocoder.google([datos["latitud"], datos["longitud"]], method='reverse')
    #         direccion = g.address
    #         guardarPosicionesGeocoder(db, datos["latitud"], datos["longitud"], direccion)

    #     return {
    #         'success' : True,
    #         'direccion'    : direccion }

    # except ValueError:
    #     return { 'success' : False }


def detalleRuta(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]
        data= {
            "nombreRuta"            : doc["nombreRuta"],
            "origen"                : doc["origen"],
            "destino"               : doc["destino"],
            "direccionOrigen"       : doc["direccionOrigen"],
            "direccionDestino"      : doc["direccionDestino"],
            "idPuntosRutaDefinida"  : detallePuntosRutaDefinida (db, doc["idPuntosRutaDefinida"]), # doc["idPuntosRutaDefinida"],
            "puntosParadas"         : doc["puntosParadas"],
            "zoom"                  : doc.get("zoom",5), # doc["zoom"],
            "activo"                : doc["activo"],   
            "eliminado"             : doc["eliminado"],            
        }          
        return {
            'success' : True,
            'data'    : data         
        }
    except:
        pass
    return { 'success' : False }




#=======================================================================================
#Funciones auxiliares
def detallePuntosRutaDefinida(db, id_puntos_ruta):
    #autenticacion   = peticion['autenticacion']
    #datos           = peticion['data']
    #usuario         = autenticacion['usuario']
    #tenant          = autenticacion['tenant']
    # db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc         = db[id_puntos_ruta]
        puntosRuta  = doc["puntosRuta"]            
        return puntosRuta
    except:
        pass
    return False  


def obtenerCantidadCargaDescarga(puntosParadas):
    cantidadCargaDescarga = {}
    cantCarga       = 0
    cantDescarga    = 0
    for puntoParada in puntosParadas:
        if puntoParada[2] == "Carga":
            cantCarga += 1
        else:
            cantDescarga += 1
    cantidadCargaDescarga["Carga"]    = cantCarga
    cantidadCargaDescarga["Descarga"] = cantDescarga
    return cantidadCargaDescarga


def guardarPosicionesGeocoder(db, latitud, longitud, direccion):
    print "----------------------------Guardo-------------------------"
    #funcion para guardar la geoposición en el documento posicionesGeocoder
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"          : "posicionesGeocoder",
            "latitud"           : latitud,
            "longitud"          : longitud,
            "nombreGeoposicion" : direccion,
            "activo"            : True
        })
        print doc_id

    except ValueError:
        return { 'success' : False }


def obtenerDireccionGeocoder(db, latitud, longitud):
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        nombreGeoposicion = ""
        filas = db.view('_design/geoposiciones/_view/geoposicionesPrecalculadas',
                    key         = [latitud, longitud],
                    include_docs  = True,
                    limit         = 1
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          nombreGeoposicion = doc.get("nombreGeoposicion", "")
          direccion         = nombreGeoposicion

        if nombreGeoposicion == "":
            g = geocoder.google([latitud, longitud], method='reverse')
            direccion = g.address
            guardarPosicionesGeocoder(db, latitud, longitud, direccion)
        return direccion

    except ValueError:
        return { 'success' : False }


def eliminarRuta(peticion):
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
        doc['eliminado']     = True
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }


def crearPuntosControl(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"          : "puntosControl",
            "creadoEn"          : datetime.now().isoformat(),
            "modificadoEn"      : datetime.now().isoformat(),
            "modificadoPor"     : usuario,
            "idRuta"            : datos["idRuta"],
            "idPuntosRuta"      : datos["idPuntosRuta"],
            "puntosControl"     : datos["puntosControl"],
            "activo"            : True,
            "eliminado"         : False
        })
        return {
            'success' : True,
            'idDocPuntosControl'  : doc_id,
        }

    except ValueError:
        return { 'success' : False }

def crearPuntosVelocidad(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"          : "puntosVelocidad",
            "creadoEn"          : datetime.now().isoformat(),
            "modificadoEn"      : datetime.now().isoformat(),
            "modificadoPor"     : usuario,
            "idRuta"            : datos["idRuta"],
            "idPuntosRuta"      : datos["idPuntosRuta"],
            "puntosVelocidad"   : datos["puntosVelocidad"],
            "activo"            : True,
            "eliminado"         : False
        })
        return {
            'success' : True,
            'idDocPuntosVelocidad'  : doc_id,
        }

    except ValueError:
        return { 'success' : False }

def crearPuntosInteres(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        doc_id, doc_rev = db.save({
            "tipoDato"          : "puntosInteres",
            "creadoEn"          : datetime.now().isoformat(),
            "modificadoEn"      : datetime.now().isoformat(),
            "modificadoPor"     : usuario,
            "idRuta"            : datos["idRuta"],
            "idPuntosRuta"      : datos["idPuntosRuta"],
            "puntosInteres"     : datos["puntosInteres"],
            "activo"            : True,
            "eliminado"         : False
        })
        return {
            'success' : True,
            'idDocPuntosInteres'  : doc_id,
        }

    except ValueError:
        return { 'success' : False }





