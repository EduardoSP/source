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
from ..geocoderFleet          import geocoderFleet


def detalleSeguimientoAsignacionRuta( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    # dbAdmin = conexion.getConexionTenant(tenant)

    # if dbAdmin == None:
    #     return { 'success' : False }

    db = conexion.getConexionTenant(tenant)
    
            
    try:
        docAsignacion            = db[datos['idAsignacionRuta']]
        docSeguimiento           = getSeguimientoAsignacion(db, docAsignacion, False)
        if docSeguimiento == None:
            docSeguimiento = {}
    
        ruta = {	
            "fechaInicioReal"       : docAsignacion.get("fechaInicioReal",""),
	    "fechaFinReal"          : docAsignacion.get("fechaFinReal",""),
	    "fechaInicioProgramada" : docAsignacion.get("fechaInicioProgramada",""),
	    "fechaFinProgramada"    : docAsignacion.get("fechaFinProgramada",""),
	    "origen": {
		"latitud"   : docAsignacion.get("ruta").get("origen",{}).get("latitud", ""),
		"longitud"  : docAsignacion.get("ruta").get("origen",{}).get("longitud", ""),
		"direccion" : docAsignacion.get("ruta").get("origen",{}).get("direccion", ""),
		"velocidad" : docAsignacion.get("ruta").get("origen",{}).get("velocidad", 0),
	    },
	    "destino": {
		"latitud"   : docAsignacion.get("ruta").get("destino",{}).get("latitud",   ""),
		"longitud"  : docAsignacion.get("ruta").get("destino",{}).get("longitud",  ""),
		"direccion" : docAsignacion.get("ruta").get("destino",{}).get("direccion", ""),
		"velocidad" : docAsignacion.get("ruta").get("destino",{}).get("velocidad", 0),
	    }
	}

        seguimientoAsignacionRuta = {
	    "fechaHoraInicioSeguimiento" : docSeguimiento.get("fechaHoraInicioSeguimiento",""),
	    "fechaHoraFinSeguimiento"    : docSeguimiento.get("fechaHoraFinSeguimiento",""),
	    "fechaHoraUltimaRevision"    : docSeguimiento.get("fechaHoraUltimaRevision",""),
	    "estado"                     : docSeguimiento.get("estado","")
	}

        puntosDeControl    = docAsignacion.get("puntosDeControlVirtual", [])
        paradas            = docAsignacion.get("puntosParadas", [])
        limitesDeVelocidad = docAsignacion.get("limitesDeVelocidad", [])
        
        #limitesDeVelocidad = []
        for limiteDeVelocidad in limitesDeVelocidad:
            if limiteDeVelocidad.get("direccion", "") == "":
                limiteDeVelocidad["direccion"] = geocoderFleet.getDireccion(
                    latitud  = limiteDeVelocidad.get("latitud", "0"),
                    longitud = limiteDeVelocidad.get("longitud", "0")                    
                )
            for infraccion in limiteDeVelocidad.get("infracciones", []):
                if infraccion.get("direccion", "") == "":
                    infraccion["direccion"] = geocoderFleet.getDireccion(
                    latitud  = infraccion.get("latitud",  "0"),
                    longitud = infraccion.get("longitud", "0")                    
                )
        #----------------------------------------------------------------

        
        dataResponse  = {
            "ruta"                      : ruta,
            "seguimientoAsignacionRuta" : seguimientoAsignacionRuta,
	    "puntosDeControl"           : puntosDeControl,
	    "paradas"                   : paradas,
	    "limitesDeVelocidad"        : limitesDeVelocidad
        }
            
        return {
            'success' : True,
            'data'    : dataResponse 
        }    
    except ValueError:
        pass

    return { 'success' : False }

    
#Auxiliares ---------------------------------

#crearSeguimiento  crea un seguimiento vacio si no existe.
def getSeguimientoAsignacion(db, docAsignacion, crearSeguimiento=True):

    docSeguimiento    = None
    
    filas = db.view(
        '_design/seguimientoAsignacionRuta/_view/seguimientoAsignacionRutaPorAsignacionRuta',
        include_docs = True,
        key          = [ docAsignacion["_id"] ],
        limit        = 1
    )

    for fila in filas:
        docSeguimiento    = fila.doc
        
    if docSeguimiento == None:
        docSeguimiento = {
            "tipoDato"        : "seguimientoAsignacionRuta",
	    
            "creadoEn"        : datetime.now().isoformat()[:19],
            "modificadoEn"    : datetime.now().isoformat()[:19],
            "modificadoPor"   : "",
            "activo"          : True,
            "eliminado"       : False,
	    
	    "idAsignacionRuta"           : docAsignacion["_id"],
	    "fechaHoraInicioSeguimiento" : "",
	    "fechaHoraFinSeguimiento"    : "",
	    "fechaHoraUltimaRevision"    : "",
            "estado"                     : "noiniciada"
        }
        db.save(docSeguimiento)

    return docSeguimiento
