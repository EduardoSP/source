# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import uuid
import logging
import urllib2
import json
import logging
import dateutil.parser
from ..conexion             import conexion
from django.db              import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core            import serializers

from decimal                import Decimal
#from ..autenticacion        import autenticacion

def detalleCuentaUsuario( peticion ):

    try:
        datosUsuario    = peticion['autenticacion']
        datosCompletos  = peticion['data']
        usuario         = datosUsuario['usuario']
        data            = None
        
        db = conexion.getConexionTenant(usuario[:3])

        if db == None:
            return { 'success' : False }
        
       
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                                        key      = [usuario], 
                                        include_docs  = True ) 
                        
        for fila in filas:                
            doc                 = fila.doc
            data = {
                'nombres'               : doc.get('nombres', ''),
                'identificacion'        : doc.get('identificacion', ''),
                'titulo'                : doc.get('titulo', ''),
                'correo'                : doc.get('correo', ''),
                'telefono'              : doc.get('telefono', ''),
                'loginUsuario'          : (doc.get('loginUsuario', '')[3:]),
            }

        return { 'success'  : True,
                 'data'     : data  }

    except ValueError as e:
        return {
            'success' : False,
            'error'   : "Error desconocido-CU003"+e[0]
        }


def actualizarCuentaUsuario( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    Tennant       = usuario[:3]
    
    db = conexion.getConexionTenant(usuario[:3])

    if db == None:
        return { 'success' : False }

    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                                        key      = [usuario], 
                                        include_docs  = True ) 
                        
        for fila in filas:                
            doc                 = fila.doc
            doc['modificadoPor'] = usuario
            doc['modificadoEn']  = datetime.now().isoformat()
    
            doc['nombres']          = datos['nombres']
            doc['identificacion']   = datos['identificacion']
            doc['titulo']           = datos['titulo']
            doc['correo']           = datos['correo']
            doc['telefono']         = datos['telefono']
            doc['loginUsuario']     = Tennant+datos['loginUsuario']
            doc['contrasena']       = moduloAutenticacion.salarConMd5( datos['contrasena'] ) if not datos.get('contrasena',None) == None else doc['contrasena'] 
            
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }