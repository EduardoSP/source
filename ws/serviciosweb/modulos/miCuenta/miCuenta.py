import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
import hashlib

def consultarDatosUsuario(db, usuario):
    dataRaw = None
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    key=[usuario])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          dataRaw.append({
            'nombres'  : doc['nombres'],
            'identificacion': doc['identificacion'],
            'correo': doc['correo'],
            'telefono': doc['telefono'],
            'loginUsuario': doc['loginUsuario']     
            })            
        return dataRaw
    except ValueError:
        pass




def detalleClienteTenant(peticion):
    autenticacion   = peticion['autenticacion']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    dataRaw       = None

    if tenant == settings.TENANT_ADMINISTRACION:
        dbFleetbi = conexion.getConexionFleet()
        dataRaw = consultarDatosUsuario(dbFleetbi, usuario)
    else:
        dbTenant    = conexion.getConexionTenant(tenant)
        dataRaw   = consultarDatosUsuario(dbTenant, usuario)
    if not dataRaw == None:   
        return {
            'success' : True, 
            'data'    : dataRaw
        }
    else:   
        return {
            'success' : False, 
            'error'    : "Error al actualizar"
        }

        
def actualizarDocUsuario(db, usuario, datos):
    resultado = False
    if db == None:
        return { 'success' : False }

    try:
        md5Salada = ""
        m = hashlib.md5()
        idDoc                   = buscarIdDocumentoUsuario(usuario, db) 
        doc = db[idDoc]
        doc["modificadoEn"]     = datetime.now().isoformat()
        doc["modificadoPor"]    = usuario
        doc["nombres"]          = datos["nombres"]
        doc["identificacion"]   = datos["identificacion"]
        doc["correo"]           = datos["correo"]
        doc["telefono"]         = datos["telefono"]
        if datos["contrasena"] != "":
            md5Salada = salarConMd5(datos["contrasena"])
            doc["contrasena"] =  md5Salada  
        db.save(doc)
        resultado = True
        return resultado
    except ValueError:
        pass



def actualizarDatosCuenta(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    resultado       = False

    if tenant == settings.TENANT_ADMINISTRACION:
        dbFleetbi = conexion.getConexionFleet()
        resultado = actualizarDocUsuario(dbFleetbi, usuario, datos)
    else:
        dbTenant    = conexion.getConexionTenant(tenant)
        resultado   = actualizarDocUsuario(dbTenant, usuario, datos)
    if resultado:
        return { 'success' : True }
    else:
        return { 'success' : False}


#funciones auxiliares
def buscarIdDocumentoUsuario(usuario, db):
    idDoc 			= ""

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    key=[usuario])
        for fila in filas:
          key 		= fila.key
          value 	= fila.value
          doc 		= fila.doc
          idDoc 	= doc['_id']
        
        return idDoc   
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

def salarConMd5(texto):
    texto = texto+"cualquiercosa"
    m = hashlib.md5()
    m.update(texto.encode('utf8'))
    return m.hexdigest()