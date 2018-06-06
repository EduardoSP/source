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
from django.conf            import settings
from decimal                import Decimal
#from ..autenticacion        import autenticacion

def listarConfiguraciones( peticion ):

    try:
        datosUsuario    = peticion['autenticacion']
        datosCompletos  = peticion['data']
        usuario         = datosUsuario['usuario']
        tenant          = datosUsuario['tenant']
        data            = None
        
        db              = conexion.getConexionTenant(tenant)

        if db == None:
            return { 'success' : False }
               
        filas = db.view(
            '_design/configuracion/_view/configuraciones', 
            include_docs  = False
        ) 

        data = {}
        
        for fila in filas:                
            key       = fila.key
            value     = fila.value
            data[key[0]] = value

        #Limite de velocidad
        if not "LIMITEDEVELOCIDAD" in data:
            data["LIMITEDEVELOCIDAD"] = settings.LIMITE_VELOCIDAD_DEFECTO

        if not "PENALIZACIONACELERACIONES" in data:
            data["PENALIZACIONACELERACIONES"]       = settings.PENALIZACION_ACELERACIONES_DEFECTO
            
        if not "PENALIZACIONFRENADAS" in data:
            data["PENALIZACIONFRENADAS"]            = settings.PENALIZACION_FRENADAS_DEFECTO
            
        if not "PENALIZACIONMOVIMIENTOSABRUPTOS" in data:
            data["PENALIZACIONMOVIMIENTOSABRUPTOS"] = settings.PENALIZACION_MOVIMIENTO_ABRUPTOS_DEFECTO
            
        if not "PENALIZACIONEXCESOSVELOCIDAD" in data:
            data["PENALIZACIONEXCESOSVELOCIDAD"]    = settings.PENALIZACION_EXCESOS_VELOCIDAD_DEFECTO

        if not "CONFIGURACIONGENERADORCARGA" in data:
            data["CONFIGURACIONGENERADORCARGA"]     = settings.CONFIGURACIONGENERADORCARGA    

        return { 'success'  : True,
                 'data'     : data  }

    except ValueError as e:
        return {
            'success' : False,
            'error'   : "Error desconocido-CU003"+e[0]
        }


def actualizarConfiguracion( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
                
        for key in datos:

            valor = datos[key]
        
            filas = db.view(
                '_design/configuracion/_view/configuraciones',
                key      = [key], 
                include_docs  = True
            ) 

            docConfiguracion = None
            
            for fila in filas:                
                docConfiguracion = fila.doc

            if key in ["LIMITEDEVELOCIDAD", "PAUSAACTIVATIEMPOCONDUCCION", "PAUSAACTIVATIEMPOPAUSAACTIVA", "PAUSAACTIVATIEMPOTOLERANCIA", "CONDUCCIONCONTINUATIEMPOMAXCONDUCCION", "CONDUCCIONCONTINUATIEMPONOCONDUCCION", "CONDUCCIONCONTINUATIEMPOTOLERANCIA", "PENALIZACIONACELERACIONES", "PENALIZACIONFRENADAS", "PENALIZACIONMOVIMIENTOSABRUPTOS", "PENALIZACIONEXCESOSVELOCIDAD", "CONFIGURACIONGENERADORCARGA" ] :
                if docConfiguracion == None:
                    docConfiguracion = {
                        "tipoDato"        : "configuracion",
                        "creadoEn"        : datetime.now().isoformat(),
                        "horaRegistrada"  : datetime.now().isoformat(),
    	                "activo"          : True,
    	            
    	                "codigo" : key,
    	                "valor"  : valor
                    }

                docConfiguracion["valor"] = valor
                db.save(docConfiguracion)

                

        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except ValueError:
        pass

    return { 'success' : False }


def getTodaConfiguracion(db):
    if db == None:
        return { 'success' : False }
               
    filas = db.view(
        '_design/configuracion/_view/configuraciones', 
        include_docs  = False
    ) 

    data = {}
    
    for fila in filas:                
        key       = fila.key
        value     = fila.value
        data[key[0]] = value


    if not "LIMITEDEVELOCIDAD" in data:
            data["LIMITEDEVELOCIDAD"] = settings.LIMITE_VELOCIDAD_DEFECTO

    if not "PENALIZACIONACELERACIONES" in data:
        data["PENALIZACIONACELERACIONES"]       = settings.PENALIZACION_ACELERACIONES_DEFECTO

    if not "PENALIZACIONFRENADAS" in data:
        data["PENALIZACIONFRENADAS"]            = settings.PENALIZACION_FRENADAS_DEFECTO

    if not "PENALIZACIONMOVIMIENTOSABRUPTOS" in data:
        data["PENALIZACIONMOVIMIENTOSABRUPTOS"] = settings.PENALIZACION_MOVIMIENTO_ABRUPTOS_DEFECTO

    if not "PENALIZACIONEXCESOSVELOCIDAD" in data:
        data["PENALIZACIONEXCESOSVELOCIDAD"]    = settings.PENALIZACION_EXCESOS_VELOCIDAD_DEFECTO

    return data
