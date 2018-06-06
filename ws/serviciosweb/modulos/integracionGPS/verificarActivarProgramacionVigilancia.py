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
#from ..integracionGPS.integracionGPS		  import evaluarHora
import integracionGPS

def buscarDocProgramacionVigilanciaEjecutadas(peticion, idVehiculo,fecha, hora, idProgramacion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    encontroVigilanciaEjecutada = False
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        filas = db.view('_design/consultarRangoProgramacionVigilanciaEjecutadas/_view/consultarRangoProgramacionVigilanciaEjecutadas',
                    include_docs  = True,
                    key=[fecha ,idVehiculo, idProgramacion])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print "entro"
          horaInicio                    =   doc.get('horaInicio')
          horaFin                       =   doc.get('horaFin')
          horaEncontrada                =   integracionGPS.evaluarHora(horaInicio, horaFin, hora)
          if horaEncontrada:
          	encontroVigilanciaEjecutada	= True
        return encontroVigilanciaEjecutada
    except ValueError:
        pass
    return { 'success' : False}



def puedoUsarPV(peticion, idVehiculo, horaRegistrada, programacionVigilancia):
	#retorna true o false si se activa la programacion vigilancia segun la hora registrada
	fecha       =	horaRegistrada[0:10]
	fecha = fecha.split("-")
	#fecha 		= "2016-11-2"
	fechaFormateada =	str(int(fecha[0]))+"-"+str(int(fecha[1]))+"-"+str(int(fecha[2]))
	hora		=	horaRegistrada[11:16]
	encontroVigilanciaEjecutada = buscarDocProgramacionVigilanciaEjecutadas(peticion,idVehiculo, fechaFormateada, hora, programacionVigilancia)
	return encontroVigilanciaEjecutada


#=======================================================================================================

def guardarCadaDocProgramacionVigilancia(peticion, programacionVigilancia, idVehiculo, fechaInicio, fechaFin,horaInicio, horaFin):
    #funcion que guarda el documento en la bd
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:        
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        logging.warning("GOOD!!")
        doc_id, doc_rev = db.save({
            "tipoDato"                  :   "programacionVigilanciaEjecutadas",
            "creadoEn"                  :   datetime.now().isoformat(), 
            "idVehiculo"    : idVehiculo ,
            "fechaInicio" : fechaInicio,
            "fechaFin"    : fechaFin,
            "horaInicio"  : horaInicio,
            "horaFin"     : horaFin,
            "idProgramacion" : programacionVigilancia,
            "activo"	: True

        })
        return doc_id
    except ValueError:
        logging.warning("GOOD!")
        pass


def conultarHorariosProgramacionVigilancia(peticion, idProgramacion):
    autenticacion   	= peticion['autenticacion']
    usuario         	= autenticacion['usuario']
    tenant          	= autenticacion['tenant']
    db              	= conexion.getConexionTenant(tenant)
    horariosPV = {}
    horariosPV["fechaInicio"] 	= ""
    horariosPV["fechaFin"] 		= ""
    horariosPV["horaInicio"] 	= ""
    horariosPV["horaFin"] 		= ""
    docProgramacionVigilancia 	= db[idProgramacion]
    horariosPV["fechaInicio"] 	= docProgramacionVigilancia["fechaInicio"]
    horariosPV["fechaFin"] 		= docProgramacionVigilancia["fechaFin"]
    horariosPV["horaInicio"] 	= docProgramacionVigilancia["horaInicio"]
    horariosPV["horaFin"] 		= docProgramacionVigilancia["horaFin"]
    return horariosPV


def guardarProgramacionVigilanciaComoEjecutada(peticion, horaRegistrada, programacionVigilancia, idVehiculo):
	fecha = horaRegistrada[0:10]
	for idProgramacion in programacionVigilancia:
		horariosPV = conultarHorariosProgramacionVigilancia(peticion, idProgramacion)
		guardarCadaDocProgramacionVigilancia(peticion, programacionVigilancia, idVehiculo, fecha, fecha, horariosPV["horaInicio"], horariosPV["horaFin"])


#=======================================================================================================    