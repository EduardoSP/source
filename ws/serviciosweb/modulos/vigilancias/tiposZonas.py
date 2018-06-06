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
#-------------------------------------------------------------

def listarTiposZonas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return {
            'success' : False,
            'mensaje' : "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/tipoZona/_view/listarTipoZona',
                    include_docs  = True)
        
        for fila in filas:
          key   = fila.key
          value = fila.value
          doc   = fila.doc
          
          dataRaw.append({
              'id'          : doc['_id'],
              'nombre'      : doc.get('nombre',''),
              'descripcion' : doc.get('descripcion',''),
              'activo'      : doc.get('activo',False),
              'creadoPor'   : doc.get('creadoPor','')
          })            
        return {
            'success' : True, 
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

#-------------------------------------------------------------


def crearTipoZona( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try: 
        doc_id, doc_rev = db.save({
	    "tipoDato"      : "tipoZona",
	    "creadoEn"      : datetime.now().isoformat(),  
	    "modificadoEn"  : datetime.now().isoformat(),
	    "modificadoPor" : usuario,
	    "nombre"        : datos.get("nombre",""),
	    "descripcion"   : datos.get("descripcion",""),
	    "activo"	    : True,
        "eliminado"     : False,
        "creadoPor"     : usuario
        })
        print "---------------------------------------"
        print doc_id
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


def editarTipoZona( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    idDoc         = datos["id"]
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try: 
        doc = db[idDoc]
        
        doc["modificadoEn"]  = datetime.now().isoformat()
        doc["modificadoPor"] = usuario
        doc["nombre"]        = datos.get("nombre", doc.get("nombre",""))
        # doc["descripcion"]   = datos.get("descripcion", doc.get("descripcion",""))
        # doc["activo"]        = datos.get("activo", doc.get("activo",False))
        
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
def eliminarTipoZona( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db            = conexion.getConexionTenant(tenant)

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

#-------------------------------------------------------------

def detalleTipoZona( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db            = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]
        dataRaw = {
            "id"          : doc["_id"],
            "nombre"      : doc.get("nombre",""),
            #"descripcion" : datos.get("descripcion",""),
            #"activo"      : datos.get("activo",False),
            
        }
        
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except:
        pass

    return { 'success' : False, 'error': 'Error al traer datos' }

#-------------------------------------------------------------

