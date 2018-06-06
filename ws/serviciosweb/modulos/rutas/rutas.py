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
from ..autenticacion          import autenticacion as moduloAutenticacion
from django.db                import IntegrityError, transaction
import time
import geocoder


def crearRuta(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        puntosRuta          = datos["puntosRuta"]
        idDocPuntosRutaDefinida = crearDocPuntosDefinicionRuta(db, usuario, puntosRuta)
        doc_id, doc_rev = db.save({
            "tipoDato"        	    : "rutas",
            "creadoEn"        	    : datetime.now().isoformat(),
            "modificadoEn"    	    : datetime.now().isoformat(),
            "modificadoPor"   	    : usuario,
            "nombreRuta"            : datos["nombreRuta"],
            "origen"		    : datos["origen"],
            "destino"               : datos["destino"],
            "direccionOrigen"       : datos["direccionOrigen"],
            "direccionDestino"      : datos["direccionDestino"],
            "idPuntosRutaDefinida"  : idDocPuntosRutaDefinida,
            "puntosParadas"         : datos["puntosParadas"],
            # "zoom"              : datos.get("zoom",4), # datos["zoom"],
            "waypointsmaps"         : datos.get ("waypointsmaps", []),
            "activo"          	    : True,
            "eliminado"             : False,
            "creadoPor"             : usuario
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

def editarRuta(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc = db[datos['id']]

        doc['modificadoPor']        = usuario
        doc['modificadoEn']         = datetime.now().isoformat()

        doc['nombreRuta']           = datos.get('nombreRuta',       doc['nombreRuta'])
        doc['origen']               = datos.get('origen',           doc['origen'])
        doc['destino']              = datos.get('destino',          doc['destino'])
        doc['direccionOrigen']      = datos.get('direccionOrigen',  doc['direccionOrigen'])
        doc['direccionDestino']     = datos.get('direccionDestino', doc['direccionDestino'])
        #doc['idPuntosRutaDefinida'] = datos.get('null', doc['idPuntosRutaDefinida'])
        doc['puntosParadas']        = datos.get('puntosParadas',    doc['puntosParadas'])
        doc['waypointsmaps']        = datos.get('waypointsmaps',    doc['waypointsmaps'])
        #doc['activo']               = datos.get('activo',           doc['activo'])
        #doc['eliminado']            = datos.get('eliminado',        doc['eliminado'])
        idPuntosRutaDefinida        = datos.get('idPuntosRutaDefinida', doc['idPuntosRutaDefinida'])
        db.save(doc)

        puntosRuta = datos["puntosRuta"]
        idDocPuntosRutaDefinida = editarDocPuntosDefinicionRuta(db, usuario, puntosRuta, idPuntosRutaDefinida)

        return {
            'success'               : True,
            'success_rutadefinida'  : idDocPuntosRutaDefinida["success"],
            #'idDocPuntosDefinicionRuta'    : idDocPuntosRutaDefinida
        }

    except ValueError:
        return { 'success' : False, 'error' : 'error en db.save()' }

def editarPuntosControlRuta(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc = db[datos['id']]

        doc['modificadoPor']        = usuario
        doc['modificadoEn']         = datetime.now().isoformat()
        doc['puntosControl']        = datos.get('puntosControl',       doc['puntosControl'])
        db.save(doc)

        return {
            'success'               : True
        }

    except ValueError:
        return { 'success' : False, 'error' : 'error en db.save()' }

def editarPuntosVelocidadRuta(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc = db[datos['id']]

        doc['modificadoPor']        = usuario
        doc['modificadoEn']         = datetime.now().isoformat()
        doc['puntosVelocidad']      = datos.get('puntosVelocidad',       doc['puntosVelocidad'])
        db.save(doc)

        return {
            'success'               : True
        }

    except ValueError:
        return { 'success' : False, 'error' : 'error en db.save()' }

def editarPuntosInteresRuta(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc = db[datos['id']]

        doc['modificadoPor']        = usuario
        doc['modificadoEn']         = datetime.now().isoformat()
        doc['puntosInteres']        = datos.get('puntosInteres',       doc['puntosInteres'])
        db.save(doc)

        return {
            'success'               : True
        }

    except ValueError:
        return { 'success' : False, 'error' : 'error en db.save()' }

def editarDocPuntosDefinicionRuta(db, usuario, puntosRuta, idPuntosRutaDefinida):

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc = db[idPuntosRutaDefinida]

        doc['modificadoPor']        = usuario
        doc['modificadoEn']         = datetime.now().isoformat()
        doc['puntosRuta']           = puntosRuta
        db.save(doc)
        return {
            'success' : True
        }

    except ValueError:
        return { 'success' : False, 'error' : 'error en db.save()' }

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
                'eliminado'         : doc['eliminado'],
                'creadoPor'         : doc.get('creadoPor','')
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
    db              = conexion.getConexionTenant(tenant)


    retornarPuntosRutaDefinida = datos.get("retornarPuntosRutaDefinida", False)
    
    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]

        puntosRutaDefinida = []
        if retornarPuntosRutaDefinida:
            if not doc.get("idPuntosRutaDefinida", "") == "":
                puntosRutaDefinida =  db[doc.get("idPuntosRutaDefinida", "")].get("puntosRuta",[])
        
        data= {
            "nombreRuta"            : doc["nombreRuta"],
            "origen"                : doc["origen"],
            "destino"               : doc["destino"],
            "direccionOrigen"       : doc["direccionOrigen"],
            "direccionDestino"      : doc["direccionDestino"],
            "idPuntosRutaDefinida"  : doc["idPuntosRutaDefinida"], # detallePuntosRutaDefinida (db, doc["idPuntosRutaDefinida"]),
            "puntosParadas"         : doc["puntosParadas"],
            "zoom"                  : doc.get("zoom",5), # doc["zoom"],
            "waypointsmaps"         : doc.get ("waypointsmaps", []),
            "activo"                : doc["activo"],   
            "eliminado"             : doc["eliminado"],
            "puntosRutaDefinida"    : puntosRutaDefinida
        }          
        return {
            'success' : True,
            'data'    : data         
        }
    except ValueError:
        pass
    return { 'success' : False }

def detallePuntoControlPorRuta ( peticion ):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    token           = autenticacion['token']
    db              = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "error" : "no existe db"}

    filas = db.view(
            '_design/rutas/_view/recuperarPuntoControlPorIdRuta',
            include_docs  = True,
            key           = [datos['id']],
            limit         = 1)

    # print (peticion)
    """
    valida que el documento existe en la db, si existe continua normalmente, en el
    caso de no ser asi, se crea un nuevo documento y se accede a este. """
    if (filas.__len__() == 0):
        """
        Si entra aqui significa que la busqueda no encontro
        elemeno, una de las razones puede ser porque el usuario,
        al crear una ruta, no siguio la secuencia normal de eventos
        y por esta razon no se creo este documento"""
        peticion_temp = {
            "autenticacion" : {
                "usuario"   : usuario,
                "token"     : token,
                "tenant"    : tenant
            },
            "data" : {
                'idRuta'            : datos['idRuta'],
                'idPuntosRuta'      : datos['idPuntosRuta'],
                'puntosControl'     : datos['puntosControl']
            }
        }
        respuesta_temp =  crearPuntosControl(peticion_temp) # { "success" : False}
        if (respuesta_temp["success"]):
            filas = db.view(
                        '_design/rutas/_view/recuperarPuntoControlPorIdRuta',
                        include_docs=True,
                        key=[datos['id']],
                        limit=1)
            print  ("No se encontro el documento, pero se creo uno nuevo (control)")
        else:
            print  ("No se encontro el documento, y tampoco se pudo crear uno nuevo (control)")
            return {'success': False,
                    "error": "No se encontro el documento, y tampoco se pudo crear uno nuevo (control)"
                    }
    else:
        pass

    #resultado = []
    resultado = {}
    for fila in filas:
        doc   = fila.doc
        item = {
            "id"             : doc.get("_id",""),
            "tipoDato"       : doc.get("tipoDato",""),
            "idPuntosRuta"   : doc.get("idPuntosRuta",""),
            "puntosControl"  : doc.get("puntosControl",[]),
            "idRuta"         : doc.get("idRuta","")
        }
        #resultado.append(item)
        resultado = item
    return { "success"        : True, 
             "data"           : resultado }

def detallePuntoVelocidadPorRuta ( peticion ):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    token           = autenticacion['token']
    db              = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "error" : "no existe db"}

    filas = db.view(
            '_design/rutas/_view/recuperarPuntosVelocidadPorIdRuta',
            include_docs  = True,
            key           = [datos['id']],
            limit         = 1)

    # print (peticion)
    """
    valida que el documento existaen la db, si existe continua normalmente, en el
    caso de no ser asi, se crea un nuevo documento y se accede a este. """
    if (filas.__len__() == 0):
        """
        Si entra aqui significa que la busqueda no encontro
        elemeno, una de las razones puede ser porque el usuario,
        al crear una ruta, no siguio la secuencia normal de eventos
        y por esta razon no se creo este documento"""
        peticion_temp = {
            "autenticacion" : {
                "usuario"   : usuario,
                "token"     : token,
                "tenant"    : tenant
            },
            "data" : {
                'idRuta'            : datos['idRuta'],
                'idPuntosRuta'      : datos['idPuntosRuta'],
                'puntosVelocidad'   : datos['puntosVelocidad']
            }
        }
        respuesta_temp = crearPuntosVelocidad(peticion_temp)
        if (respuesta_temp["success"]):
            filas = db.view(
                        '_design/rutas/_view/recuperarPuntosVelocidadPorIdRuta',
                        include_docs=True,
                        key=[datos['id']],
                        limit=1)
            print  ("No se encontro el documento, pero se creo uno nuevo (velocidad)")
        else:
            print  ("No se encontro el documento, y tampoco se pudo crear uno nuevo (velocidad)")
            return {'success': False,
                    "error": "No se encontro el documento, y tampoco se pudo crear uno nuevo (velocidad)"
                    }
    else:
        pass

    #resultado = []
    resultado = {}
    for fila in filas:
        doc   = fila.doc
        item = {
            "id"                : doc.get("_id",""),
            "tipoDato"          : doc.get("tipoDato",""),
            "idPuntosRuta"      : doc.get("idPuntosRuta",""),
            "puntosVelocidad"   : doc.get("puntosVelocidad",[]),
            "idRuta"            : doc.get("idRuta","")
        }
        #resultado.append(item)
        resultado = item
    return { "success"        : True, 
             "data"           : resultado }

def detallePuntoInteresPorRuta ( peticion ):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    token           = autenticacion['token']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "error" : "no existe db"}

    filas = db.view(
            '_design/rutas/_view/recuperarPuntosInteresPorIdRuta',
            include_docs  = True,
            key           = [datos['id']],
            limit         = 1)

    # print (peticion)
    """
    valida que el documento existe en la db, si existe continua normalmente, en el
    caso de no ser asi, se crea un nuevo documento y se accede a este. """
    if (filas.__len__() == 0):
        """
        Si entra aqui significa que la busqueda no encontro
        elemeno, una de las razones puede ser porque el usuario,
        al crear una ruta, no siguio la secuencia normal de eventos
        y por esta razon no se creo este documento"""
        peticion_temp = {
            "autenticacion" : {
                "usuario"   : usuario,
                "token"     : token,
                "tenant"    : tenant
            },
            "data" : {
                'idRuta'            : datos['idRuta'],
                'idPuntosRuta'      : datos['idPuntosRuta'],
                'puntosInteres'     : datos['puntosInteres']
            }
        }
        respuesta_temp =  crearPuntosInteres(peticion_temp) # { "success" : False}
        if (respuesta_temp["success"]):
            filas = db.view(
                        '_design/rutas/_view/recuperarPuntosInteresPorIdRuta',
                        include_docs=True,
                        key=[datos['id']],
                        limit=1)
            print  ("No se encontro el documento, pero se creo uno nuevo (Interes)")
        else:
            print  ("No se encontro el documento, y tampoco se pudo crear uno nuevo (Interes)")
            return {'success': False,
                    "error": "No se encontro el documento, y tampoco se pudo crear uno nuevo (Interes)"
                    }
    else:
        pass

    #resultado = []
    resultado = {}
    for fila in filas:
        doc   = fila.doc
        item = {
            "id"                : doc.get("_id",""),
            "tipoDato"          : doc.get("tipoDato",""),
            "idPuntosRuta"      : doc.get("idPuntosRuta",""),
            "puntosInteres"     : doc.get("puntosInteres",[]),
            "idRuta"            : doc.get("idRuta","")
        }
        #resultado.append(item)
        resultado = item
    return { "success"        : True, 
             "data"           : resultado }

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
    tenant        = autenticacion['tenant']
    
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


#-------------------------------------------------------------

def pickerRutas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
            '_design/rutas/_view/listarRutas',
            include_docs  = True
        )
        
        for fila in filas:
          key               = fila.key
          value             = fila.value
          doc               = fila.doc
          eliminado         = doc.get('eliminado','')
          activo            = doc.get('activo','')
          if not(eliminado) and activo:

              dataRaw.append({
                  'id'     : doc.get('_id',''),
                  'nombre' : doc.get('nombreRuta', '')
              })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except BufferError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }



