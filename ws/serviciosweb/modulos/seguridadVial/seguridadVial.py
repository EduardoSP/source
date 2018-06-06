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
from dateutil import parser
from  ws.serviciosweb.modulos.botonPanicoGPS.botonPanicoGPS import obtenerinfoVehiculo, getUltimaPosicionVehiculo, buscarCelEmergenciaCorreoTenant, envioGodaddy

def contarRegistrosVista(db, identificador, fechaInicio, fechaFin, vista):
        cantidad = 0 
        try:
                filas = db.view(vista,
            startkey      = [identificador, fechaInicio],
            endkey        = [identificador,fechaFin],
            include_docs  = True)
                for fila in filas:
                        key = fila.key          
                        doc = fila.doc
                        cantidad = cantidad + 1
                return cantidad
        except ValueError:
                pass


def obtenerInformacion(db, fechaInicio, fechaFin, tipoConsulta, numeroOpcionHabilitadaPlataforma):
        #si tipoConsulta es igual a cero entonces la consulta es por vehiculo
        #si tipoConsulta es igual a 1 es por conductor
        vistaAceleracionVehiculo                        = '_design/seguridadVial/_view/listarAceleracionPorVehiculo'
        vistaFrenadasVehiculo                           = '_design/seguridadVial/_view/listarFrenadasPorVehiculo'
        vistaMovimientoAbruptoVehiculo          = '_design/seguridadVial/_view/listarMovimientoAbruptoPorVehiculo'
        vistaExcesoVelocidadVehiculo            = '_design/seguridadVial/_view/listarExcesoVelocidadPorVehiculo'
        
        vistaAceleracionConductor                       = '_design/seguridadVial/_view/listarAceleracionPorConductor'
        vistaFrenadasConductor                          = '_design/seguridadVial/_view/listarFrenadasPorConductor'
        vistaMovimientoAbruptoConductor     = '_design/seguridadVial/_view/listarMovimientoAbruptoConductor'
        vistaExcesoVelocidadConductor           = '_design/seguridadVial/_view/listarExcesoVelocidadPorConductor'
        
        cantidadAceleracion             = 0
        cantidadFrenadas                        = 0
        cantidadMovimientoAbrupto       = 0
        cantidadExcesoVelocidad         = 0

        dataRaw     = []
        listaResultado = []
        # si la peticuion es por vehiculo
        if tipoConsulta == "0":
                filas = db.view('_design/vehiculos/_view/vehiculos',
                    include_docs  = True)
                for fila in filas:
                    key   = fila.key
                    value = fila.value
                    doc   = fila.doc
                    idVehiculo = doc.get('_id')
                    placa          = doc.get('placa')
                    cantidadAceleracion                 = contarRegistrosVista(db, idVehiculo, fechaInicio, fechaFin, vistaAceleracionVehiculo)
                    cantidadFrenadas                    = contarRegistrosVista(db, idVehiculo, fechaInicio, fechaFin, vistaFrenadasVehiculo)
                    cantidadMovimientoAbrupto   = contarRegistrosVista(db, idVehiculo, fechaInicio, fechaFin, vistaMovimientoAbruptoVehiculo)
                    cantidadExcesoVelocidad     = contarRegistrosVista(db, idVehiculo, fechaInicio, fechaFin, vistaExcesoVelocidadVehiculo)
                    listaResultado.append([placa, cantidadAceleracion, cantidadFrenadas, cantidadMovimientoAbrupto, cantidadExcesoVelocidad])
                    if not(numeroOpcionHabilitadaPlataforma == None):
                        opcionesAdicionalesPlataforma = doc.get("opcionesAdicionalesPlataforma", [])
                        if not(opcionesAdicionalesPlataforma == None):
                            if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:  
                                dataRaw.append({
                                    'id'                                        : idVehiculo,
                                    'nombre'                            : placa,
                                    'aceleracion'                       : str(cantidadAceleracion),
                                    'frenadas'                          : str(cantidadFrenadas),
                                    'movimientosAbruptos'       : str(cantidadMovimientoAbrupto),
                                    'excesosVelocidad'          : str(cantidadExcesoVelocidad),
                                    'tipoConsulta'                      : "Vehiculo"
                                    })
                    else:  
                        dataRaw.append({
                            'id'                                        : idVehiculo,
                            'nombre'                            : placa,
                            'aceleracion'                       : str(cantidadAceleracion),
                            'frenadas'                          : str(cantidadFrenadas),
                            'movimientosAbruptos'       : str(cantidadMovimientoAbrupto),
                            'excesosVelocidad'          : str(cantidadExcesoVelocidad),
                            'tipoConsulta'                      : "Vehiculo"
                            })
        else:
                print "Hola"
                filas = db.view('_design/conductores/_view/listarConductores',
                    include_docs  = True)
                for fila in filas:
                        key   = fila.key
                        value = fila.value
                        doc   = fila.doc
                        idConductor = doc.get('_id')
                        nombreConductor = doc.get('nombres')+" "+doc.get('apellidos')
                        cantidadAceleracion             = contarRegistrosVista(db, idConductor, fechaInicio, fechaFin, vistaAceleracionConductor)
                        cantidadFrenadas                        = contarRegistrosVista(db, idConductor, fechaInicio, fechaFin, vistaFrenadasConductor)
                        cantidadMovimientoAbrupto       = contarRegistrosVista(db, idConductor, fechaInicio, fechaFin, vistaMovimientoAbruptoConductor)
                        cantidadExcesoVelocidad         = contarRegistrosVista(db, idConductor, fechaInicio, fechaFin, vistaExcesoVelocidadConductor)
                        if not(numeroOpcionHabilitadaPlataforma == None):
                            estaConductor = validarConductorPermisoHabilitado(db, idConductor, numeroOpcionHabilitadaPlataforma)
                            if estaConductor:
                                dataRaw.append({
                                        'id'                                    : idConductor,
                                'nombre'                        : nombreConductor,
                                'aceleracion'                   : str(cantidadAceleracion),
                                'frenadas'                              : str(cantidadFrenadas),
                                'movimientosAbruptos'   : str(cantidadMovimientoAbrupto),
                                'excesosVelocidad'              : str(cantidadExcesoVelocidad),
                                'tipoConsulta'                  : "Conductor"
                                })
                        else:
                            dataRaw.append({
                                    'id'                                    : idConductor,
                            'nombre'                        : nombreConductor,
                            'aceleracion'                   : str(cantidadAceleracion),
                            'frenadas'                              : str(cantidadFrenadas),
                            'movimientosAbruptos'   : str(cantidadMovimientoAbrupto),
                            'excesosVelocidad'              : str(cantidadExcesoVelocidad),
                            'tipoConsulta'                  : "Conductor"
                            })
        return dataRaw


def consultarConduccionAgresiva(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    numeroOpcionHabilitadaPlataforma = datos.get("numeroOpcionHabilitadaPlataforma",None)
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        tipoConsulta            =       datos["posicionConduccionAgresiva"]
        listaResultado          = obtenerInformacion(db, fechaInicio, fechaFin, tipoConsulta, numeroOpcionHabilitadaPlataforma)
        #print listaResultado
        return {
            'success'           : True,
            'data'                      : listaResultado,
            'tipoConsulta'      : tipoConsulta          
        }
    except ValueError:
        return { 'success' : False }

def consultarPlacaVehiculo(db, idVehiculo):
    docVehiculo = db[idVehiculo]
    placa               =       docVehiculo["placa"]  
    return placa

def consultarNombresConductor(db, idConductor):
    docConductor                = db[idConductor]
    nombresConductor    = docConductor["nombres"] + " "+docConductor["apellidos"]  
    return nombresConductor


def consultarDetalleAceleracion(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    vistaAceleracionVehiculo                    = '_design/seguridadVial/_view/listarAceleracionPorVehiculo'
    vistaAceleracionConductor                   = '_design/seguridadVial/_view/listarAceleracionPorConductor'

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        identificador           =       datos["id"]
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        tipoConsulta            =   datos["tipoConsulta"]
        if tipoConsulta == "0":
                vista = vistaAceleracionVehiculo
        else:
                vista = vistaAceleracionConductor

        dataRaw = []
        filas = db.view(vista,
            startkey      = [identificador, fechaFin],
            endkey        = [identificador,fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
                        key = fila.key          
                        doc = fila.doc
                        horaRegistrada  = doc.get('horaRegistrada')
                        ubicacion               = doc.get('ubicacion')
                        if tipoConsulta == "0":
                                #consulta condcutor
                                idTipoUsuario   = doc.get('idConductor')
                                tipoUsuario     = consultarNombresConductor(db, idTipoUsuario)

                        else:
                                idTipoUsuario   = doc.get('idVehiculo')
                                tipoUsuario     = consultarPlacaVehiculo(db, idTipoUsuario)
                        dataRaw.append({
                        "horaRegistrada"    : horaRegistrada,
                    "ubicacion"         : ubicacion,
                    "tipoUsuario"               : tipoUsuario
                    })
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }



def consultarDetalleFrenadas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    vistaFrenadaVehiculo                        = '_design/seguridadVial/_view/listarFrenadasPorVehiculo'
    vistaFrenadaConductor                       = '_design/seguridadVial/_view/listarFrenadasPorConductor'

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        identificador           =       datos["id"]
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        tipoConsulta            =   datos["tipoConsulta"]
        if tipoConsulta == "0":
                vista = vistaFrenadaVehiculo
        else:
                vista = vistaFrenadaConductor

        dataRaw = []
        filas = db.view(vista,
            startkey      = [identificador, fechaFin],
            endkey        = [identificador,fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
                        key = fila.key          
                        doc = fila.doc
                        horaRegistrada  = doc.get('horaRegistrada')
                        ubicacion               = doc.get('ubicacion')
                        if tipoConsulta == "0":
                                #consulta condcutor
                                idTipoUsuario   = doc.get('idConductor')
                                tipoUsuario     = consultarNombresConductor(db, idTipoUsuario)

                        else:
                                idTipoUsuario   = doc.get('idVehiculo')
                                tipoUsuario     = consultarPlacaVehiculo(db, idTipoUsuario)
                        dataRaw.append({
                        "horaRegistrada"    : horaRegistrada,
                    "ubicacion"         : ubicacion,
                    "tipoUsuario"               : tipoUsuario
                    })
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }



def consultarDetalleMovimientosAbruptos(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    vistaMovimientosAbruptosVehiculo                    = '_design/seguridadVial/_view/listarMovimientoAbruptoPorVehiculo'
    vistaMovimientosAbruptosConductor                   = '_design/seguridadVial/_view/listarMovimientoAbruptoConductor'

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        identificador           =       datos["id"]
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        tipoConsulta            =   datos["tipoConsulta"]
        if tipoConsulta == "0":
                vista = vistaMovimientosAbruptosVehiculo
        else:
                vista = vistaMovimientosAbruptosConductor

        dataRaw = []
        filas = db.view(vista,
            startkey      = [identificador, fechaFin],
            endkey        = [identificador,fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
                        key = fila.key          
                        doc = fila.doc
                        horaRegistrada  = doc.get('horaRegistrada')
                        ubicacion               = doc.get('ubicacion')
                        if tipoConsulta == "0":
                                #consulta condcutor
                                idTipoUsuario   = doc.get('idConductor')
                                tipoUsuario     = consultarNombresConductor(db, idTipoUsuario)

                        else:
                                idTipoUsuario   = doc.get('idVehiculo')
                                tipoUsuario     = consultarPlacaVehiculo(db, idTipoUsuario)
                        dataRaw.append({
                        "horaRegistrada"    : horaRegistrada,
                    "ubicacion"         : ubicacion,
                    "tipoUsuario"               : tipoUsuario
                    })
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }



def consultarDetalleExcesosVelocidad(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    vistaExcesoVelocidadVehiculo                        = '_design/seguridadVial/_view/listarExcesoVelocidadPorVehiculo'
    vistaExcesoVelocidadConductor                       = '_design/seguridadVial/_view/listarExcesoVelocidadPorConductor'

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        identificador           =       datos["id"]
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        tipoConsulta            =   datos["tipoConsulta"]
        if tipoConsulta == "0":
                vista = vistaExcesoVelocidadVehiculo
        else:
                vista = vistaExcesoVelocidadConductor

        dataRaw = []
        filas = db.view(vista,
            startkey      = [identificador, fechaFin],
            endkey        = [identificador,fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
                        key = fila.key          
                        doc = fila.doc
                        horaRegistrada  = doc.get('horaRegistrada')
                        ubicacion               = doc.get('ubicacion')
                        if tipoConsulta == "0":
                                #consulta condcutor
                                idTipoUsuario   = doc.get('idConductor')
                                tipoUsuario     = consultarNombresConductor(db, idTipoUsuario)

                        else:
                                idTipoUsuario   = doc.get('idVehiculo')
                                tipoUsuario     = consultarPlacaVehiculo(db, idTipoUsuario)
                        dataRaw.append({
                        "horaRegistrada"    : horaRegistrada,
                    "ubicacion"         : ubicacion,
                    "tipoUsuario"               : tipoUsuario
                    })
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }



def consultarEncendidoApagado(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        idVehiculo                      =   datos["posicionEncendidoApagado"]
        dataRaw = []
        filas = db.view('_design/seguridadVial/_view/listarEncendidoApagadoPorVehiculo',
            startkey      = [idVehiculo, fechaFin],
            endkey        = [idVehiculo,fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
            key = fila.key
            doc = fila.doc
            evento              = doc.get('evento')
            inicio              = doc.get('horaInicio')
            fin                 = doc.get('horaFin')
            if fin == "":
                duracion = "En curso"
            else:
                fecha1                          = parser.parse(inicio)
                fecha2                          = parser.parse(fin)
                diferencia          = fecha2 - fecha1
                segundosDiferencias = diferencia.total_seconds()
                cantidadHoras           = segundosDiferencias / (60*60)
                horasMinutos        = int(cantidadHoras) * 60
                cantidadMinutos     = (segundosDiferencias / 60) - horasMinutos
                if not (cantidadMinutos == 0):     
                    duracion    = "{} horas {} minutos".format(int(cantidadHoras) , int(cantidadMinutos))
                else:
                    duracion    = "{} horas".format(int(cantidadHoras))
            dataRaw.append({
                        "evento"    : evento,
                    "inicio"    : inicio,
                    "fin"               : fin,
                    "duracion"  : duracion
                    })
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }



def consultarPausaActiva(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    numeroOpcionHabilitadaPlataforma = datos.get("numeroOpcionHabilitadaPlataforma",None)
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        dataRaw = []
        filas = db.view('_design/seguridadVial/_view/listarPausaActiva',
            startkey      = [fechaFin],
            endkey        = [fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
            key = fila.key          
            doc = fila.doc
            fechaInfraccion     = doc.get('fechaInfraccion')
            conduceDesde                = doc.get('conduceDesde',"")
            conduceHasta        = doc.get('fechaFin',"")
            idVehiculo                  = doc.get('idVehiculo')
            idConductor                 = doc.get('idConductor')
            vehiculo                    = consultarPlacaVehiculo(db, idVehiculo)
            if not(idConductor == ""):
                conductor                       = consultarNombresConductor(db, idConductor)
            else:
                conductor           = ""
            if not conduceHasta == "" and not conduceHasta == None:
                fecha1                          = parser.parse(conduceHasta)
                fecha2                          = parser.parse(conduceDesde)
                diferencia                      = fecha1 - fecha2
                segundosDiferencias = diferencia.total_seconds()
                cantidadHoras           = segundosDiferencias / (60*60)
                horasMinutos        = int(cantidadHoras) * 60
                cantidadMinutos     = (segundosDiferencias / 60) - horasMinutos
                if cantidadMinutos != 0:     
                    tiempoConduccion    = "{} horas {} minutos".format(int(cantidadHoras) , int(cantidadMinutos))
                else:
                    tiempoConduccion    = "{} horas".format(int(cantidadHoras))
            else:
                conduceHasta        = ""
                tiempoConduccion    = ""
            if not(conduceDesde == "1991-09-09T10:13:36.540564"):
                if not(numeroOpcionHabilitadaPlataforma == None):
                    opcionesAdicionalesPlataforma = buscarOpcionesAdicionalesPlataforma(db, idVehiculo)
                    if not(opcionesAdicionalesPlataforma == None):
                        if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                            dataRaw.append({
                                "fechaInfraccion"   : fechaInfraccion,
                                "conduceDesde"      : conduceDesde,
                                "conduceHasta"      : conduceHasta,    
                                "tiempoConduccion"  : tiempoConduccion,
                                "vehiculo"                  : vehiculo,
                                "conductor"                 : conductor,
                                "idVehiculo"                : idVehiculo,
                                "idConductor"               : idConductor
                                })
                else:
                    dataRaw.append({
                        "fechaInfraccion"   : fechaInfraccion,
                        "conduceDesde"      : conduceDesde,
                        "conduceHasta"      : conduceHasta,    
                        "tiempoConduccion"  : tiempoConduccion,
                        "vehiculo"                  : vehiculo,
                        "conductor"                 : conductor,
                        "idVehiculo"                : idVehiculo,
                        "idConductor"               : idConductor
                        })
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }



def consultarConduccionContinua(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    numeroOpcionHabilitadaPlataforma = datos.get("numeroOpcionHabilitadaPlataforma",None)
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        fechaInicio             =       datos["fechaInicio"]
        fechaFin                        =       datos["fechaFin"]
        dataRaw = []
        filas = db.view('_design/seguridadVial/_view/listarConduccionContinua',
            startkey      = [fechaFin],
            endkey        = [fechaInicio],
            descending    = True,
            include_docs  = True)
        for fila in filas:
            key = fila.key          
            doc = fila.doc
            fechaInfraccion     = doc.get('fechaInfraccion')
            conduceDesde                = doc.get('conduceDesde')
            conduceHasta        = doc.get('fechaFin')
            idVehiculo                  = doc.get('idVehiculo')
            idConductor                 = doc.get('idConductor')
            vehiculo                    = consultarPlacaVehiculo(db, idVehiculo)
            if not(idConductor == ""):
                conductor           = consultarNombresConductor(db, idConductor)
            else:
                conductor           = ""
            if not conduceHasta == "" and not conduceHasta == None:
                fecha1              = parser.parse(conduceHasta)
                fecha2              = parser.parse(conduceDesde)
                diferencia          = fecha1 - fecha2
                segundosDiferencias = diferencia.total_seconds()
                cantidadHoras       = segundosDiferencias / (60*60)
                horasMinutos        = int(cantidadHoras) * 60
                cantidadMinutos     = (segundosDiferencias / 60) - horasMinutos
                if cantidadMinutos != 0:     
                    tiempoConduccion    = "{} horas {} minutos".format(int(cantidadHoras) , int(cantidadMinutos))
                else:
                    tiempoConduccion    = "{} horas".format(int(cantidadHoras))
            else:
                conduceHasta        = ""
                tiempoConduccion    = ""
            if not(numeroOpcionHabilitadaPlataforma == None):
                opcionesAdicionalesPlataforma = buscarOpcionesAdicionalesPlataforma(db, idVehiculo)
                if not(opcionesAdicionalesPlataforma == None):
                    if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                        dataRaw.append({
                                "fechaInfraccion"   : fechaInfraccion,
                                "conduceDesde"      : conduceDesde,
                                "conduceHasta"      : conduceHasta,
                                "tiempoConduccion"  : tiempoConduccion,
                                "vehiculo"                  : vehiculo,
                                "conductor"                 : conductor,
                                "idVehiculo"                : idVehiculo,
                                "idConductor"               : idConductor
                                })
            else:
                dataRaw.append({
                        "fechaInfraccion"   : fechaInfraccion,
                        "conduceDesde"      : conduceDesde,
                        "conduceHasta"      : conduceHasta,
                        "tiempoConduccion"  : tiempoConduccion,
                        "vehiculo"                  : vehiculo,
                        "conductor"                 : conductor,
                        "idVehiculo"                : idVehiculo,
                        "idConductor"               : idConductor
                        })
                
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        return { 'success' : False }


def validarDatosGPS(placaVehiculo, latitud, longitud, horaRegistrada, idVehiculo, db):
    datosEntrada = {}
    if placaVehiculo != "" and latitud != "" and longitud != "" and horaRegistrada != "":
        datosEntrada["placa"]           = placaVehiculo
        datosEntrada["latitud"]         = latitud
        datosEntrada["longitud"]        = longitud
        datosEntrada["horaRegistrada"]  = horaRegistrada
    else:  
        docUltimaPosicion               = getUltimaPosicionVehiculo(idVehiculo, db)
        datosEntrada["placa"]           = placaVehiculo
        datosEntrada["latitud"]         = docUltimaPosicion.get("latitud", 0)
        datosEntrada["longitud"]        = docUltimaPosicion.get("longitud", 0)
        datosEntrada["horaRegistrada"]  = docUltimaPosicion.get("horaRegistrada", "")
    return datosEntrada


def guardarDocAceleracion(db, horaRegistrada, ubicacion, idConductor, idVehiculo):
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        doc_id, doc_rev = db.save({
            "tipoDato"                  :   "aceleracion",
            "creadoEn"                  :   datetime.now().isoformat(), 
            "horaRegistrada"            :   horaRegistrada,
            "ubicacion"                 :   ubicacion,
            "idConductor"               :   idConductor,
            "idVehiculo"                :   idVehiculo,
            "activo"                    :   True
        })
        return True
    except ValueError:
        return False


def registrarAceleracionVehiculoGPS(peticion):
    #registra las aceleraciones de un vehiculo
    autenticacion       = peticion['autenticacion']
    datos               = peticion['data']
    usuario             = autenticacion['usuario']
    tenant              = autenticacion['tenant']
    db                  = conexion.getConexionTenant(tenant)  
    identificadorGPS    = datos['identificadorGPS']
    #se consulta el id del vehiculo
    infoVehiculo        = obtenerinfoVehiculo(identificadorGPS)
    idVehiculo          = infoVehiculo[0]
    tenantVehiculo      = infoVehiculo[1]
    db                  = conexion.getConexionTenant(tenantVehiculo)
    peticion['autenticacion']["tenant"] = tenantVehiculo
    if idVehiculo != "":
        nombreTenant        = infoVehiculo[1]
        docVehiculo         = db[idVehiculo]
        placaVehiculo       = docVehiculo["placa"]
        idConductor         = docVehiculo["conductor"]
        latitud             = datos['latitud']
        longitud            = datos['longitud']
        horaRegistrada      = datos['horaRegistrada']
        datosEntrada        = validarDatosGPS(placaVehiculo, latitud, longitud, horaRegistrada, idVehiculo, db)
        #fechaParse             = parser.parse(horaRegistrada).astimezone(settings.EST).strftime("%A %d de %B %Y %I:%M %p")
        fechaParse          = parser.parse(horaRegistrada).strftime("%A %d de %B %Y %I:%M %p")
        direccionCaptada    = obtenerDireccionGeocoder(db, str(datosEntrada["latitud"]), str(datosEntrada["longitud"]))    
        infoContacto        = buscarCelEmergenciaCorreoTenant(nombreTenant)
        correoTenant        = infoContacto[1]
        asuntoCorreo        = settings.CORREO_ASUNTO_ACELERACION+str(placaVehiculo)+" "+ fechaParse.decode("utf8")
        mensajeCorreo       = u"<h2>{}  Latitud {}  y Longitud {}, direccion {}</h2>".format(settings.CORREO_MENSAJE_ACELERACION,str(datosEntrada["latitud"]),str(datosEntrada["longitud"]), str(direccionCaptada))
        horaRegistradaFormato      = parser.parse(datosEntrada["horaRegistrada"]).astimezone(settings.EST).isoformat()
        guardo = guardarDocAceleracion(db, horaRegistradaFormato, str(direccionCaptada), idConductor, idVehiculo)
        #DESCOMENTAR PARA ENVIAR EMAIL
        if guardo:
            envioGodaddy(correoTenant, mensajeCorreo, asuntoCorreo, settings.CORREO_USUARIO)   
        return {
            'success' : True, 
            'data'    : {
                    'id' : "enviado"
            }              
        }


def guardarDocFrenadas(db, horaRegistrada, ubicacion, idConductor, idVehiculo, intensidadFrenada):
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        doc_id, doc_rev = db.save({
            "tipoDato"                  :   "frenadas",
            "creadoEn"                  :   datetime.now().isoformat(), 
            "horaRegistrada"            :   horaRegistrada,
            "ubicacion"                 :   ubicacion,
            "idConductor"               :   idConductor,
            "idVehiculo"                :   idVehiculo,
            "intensidadFrenada"         :   intensidadFrenada,
            "activo"                    :   True
        })
        return True
    except ValueError:
        return False


def registrarFrenadasVehiculoGPS(peticion):
    #registra las frenadas abruptas de un vehiculo
    autenticacion       = peticion['autenticacion']
    datos               = peticion['data']
    usuario             = autenticacion['usuario']
    tenant              = autenticacion['tenant']
    db                  = conexion.getConexionTenant(tenant)  
    identificadorGPS    = datos['identificadorGPS']
    #se consulta el id del vehiculo
    infoVehiculo        = obtenerinfoVehiculo(identificadorGPS)
    idVehiculo          = infoVehiculo[0]
    tenantVehiculo      = infoVehiculo[1]
    db                  = conexion.getConexionTenant(tenantVehiculo)
    peticion['autenticacion']["tenant"] = tenantVehiculo
    if idVehiculo != "":
        nombreTenant        = infoVehiculo[1]
        docVehiculo         = db[idVehiculo]
        placaVehiculo       = docVehiculo["placa"]
        idConductor         = docVehiculo["conductor"]
        latitud             = datos['latitud']
        longitud            = datos['longitud']
        horaRegistrada      = datos['horaRegistrada']
        intensidadFrenada   = datos['intensidadFrenada']
        datosEntrada        = validarDatosGPS(placaVehiculo, latitud, longitud, horaRegistrada, idVehiculo, db)
        fechaParse          = parser.parse(horaRegistrada).strftime("%A %d de %B %Y %I:%M %p")
        direccionCaptada    = obtenerDireccionGeocoder(db, str(datosEntrada["latitud"]), str(datosEntrada["longitud"]))      
        infoContacto        = buscarCelEmergenciaCorreoTenant(nombreTenant)
        correoTenant        = infoContacto[1]
        asuntoCorreo        = settings.CORREO_ASUNTO_FRENADA+str(placaVehiculo)+" "+ fechaParse.decode("utf8")
        mensajeCorreo       = u"<h2>{}  Latitud {}  y Longitud {}, direccion {}</h2>".format(settings.CORREO_MENSAJE_FRENADA,str(datosEntrada["latitud"]),str(datosEntrada["longitud"]), str(direccionCaptada))
        horaRegistradaFormato      = parser.parse(datosEntrada["horaRegistrada"]).astimezone(settings.EST).isoformat()
        guardo = guardarDocFrenadas(db, horaRegistradaFormato, str(direccionCaptada), idConductor, idVehiculo, intensidadFrenada)
        if guardo:
            envioGodaddy(correoTenant, mensajeCorreo, asuntoCorreo, settings.CORREO_USUARIO)   
        return {
            'success' : True, 
            'data'    : {
                    'id' : "enviado"
            }              
        }


def guardarDocMovimientoAbrupto(db, horaRegistrada, ubicacion, idConductor, idVehiculo, intensidadMovimiento):
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        doc_id, doc_rev = db.save({
            "tipoDato"                  :   "movimientoAbrupto",
            "creadoEn"                  :   datetime.now().isoformat(), 
            "horaRegistrada"            :   horaRegistrada,
            "ubicacion"                 :   ubicacion,
            "idConductor"               :   idConductor,
            "idVehiculo"                :   idVehiculo,
            "intensidadMovimiento"      :   intensidadMovimiento,
            "activo"                    :   True
        })
        return True
    except ValueError:
        return False


def registrarMovimientosAbruptosVehiculoGPS(peticion):
    #registra las frenadas abruptas de un vehiculo
    autenticacion       = peticion['autenticacion']
    datos               = peticion['data']
    usuario             = autenticacion['usuario']
    tenant              = autenticacion['tenant']
    db                  = conexion.getConexionTenant(tenant)  
    identificadorGPS    = datos['identificadorGPS']
    #se consulta el id del vehiculo
    infoVehiculo        = obtenerinfoVehiculo(identificadorGPS)
    idVehiculo          = infoVehiculo[0]
    tenantVehiculo      = infoVehiculo[1]
    db                  = conexion.getConexionTenant(tenantVehiculo)
    peticion['autenticacion']["tenant"] = tenantVehiculo
    if idVehiculo != "":
        nombreTenant            = infoVehiculo[1]
        docVehiculo             = db[idVehiculo]
        placaVehiculo           = docVehiculo["placa"]
        idConductor             = docVehiculo["conductor"]
        latitud                 = datos['latitud']
        longitud                = datos['longitud']
        horaRegistrada          = datos['horaRegistrada']
        intensidadMovimiento    = datos['intensidadMovimiento']
        datosEntrada        = validarDatosGPS(placaVehiculo, latitud, longitud, horaRegistrada, idVehiculo, db)
        fechaParse          = parser.parse(horaRegistrada).strftime("%A %d de %B %Y %I:%M %p")
        direccionCaptada    = obtenerDireccionGeocoder(db, str(datosEntrada["latitud"]), str(datosEntrada["longitud"]))  
        infoContacto        = buscarCelEmergenciaCorreoTenant(nombreTenant)
        correoTenant        = infoContacto[1]
        asuntoCorreo        = settings.CORREO_ASUNTO_MOVIMIENTOABRUPTO+str(placaVehiculo)+" "+ fechaParse.decode("utf8")
        mensajeCorreo       = u"<h2>{}  Latitud {}  y Longitud {}, direccion {}</h2>".format(settings.CORREO_MENSAJE_MOVIMIENTOABRUPTO,str(datosEntrada["latitud"]),str(datosEntrada["longitud"]), str(direccionCaptada)) 
        horaRegistradaFormato      = parser.parse(datosEntrada["horaRegistrada"]).astimezone(settings.EST).isoformat()
        guardo = guardarDocMovimientoAbrupto(db, horaRegistradaFormato, str(direccionCaptada), idConductor, idVehiculo, intensidadMovimiento)
        if guardo:
            envioGodaddy(correoTenant, mensajeCorreo, asuntoCorreo, settings.CORREO_USUARIO)   
        return {
            'success' : True, 
            'data'    : {
                    'id' : "enviado"
            }              
        }



def obtenerDireccionGeocoder(db, latitud, longitud):
    latitud  = str(latitud)
    longitud = str(longitud)
    lat1 = latitud.split(".")[0]
    lat2 = latitud.split(".")[1]
    lng1 = longitud.split(".")[0]
    lng2 = longitud.split(".")[1]
    nuevaLatitud    = lat1+"."+lat2[0:3]
    nuevaLongitud   = lng1+"."+lng2[0:3]

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        nombreGeoposicion = ""
        filas = db.view('_design/geoposiciones/_view/geoposicionesPrecalculadas',
                    key         = [nuevaLatitud, nuevaLongitud],
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
            time.sleep(5)
            g         = geocoder.google([nuevaLatitud, nuevaLongitud], method='reverse')
            direccion = g.address
            if not direccion == None:
                guardarPosicionesGeocoder(db, nuevaLatitud, nuevaLongitud, direccion)
            else:
                return ""
        return direccion

    except ArithmeticError:
        return "ERROR!!!"


def guardarPosicionesGeocoder(db, latitud, longitud, direccion):
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



def validarConductorPermisoHabilitado(db, idConductor, numeroOpcionHabilitadaPlataforma):    
    try:
        filas = db.view('_design/conductores/_view/listarVehiculosPorConductor',
                    include_docs  = True,
                    key      = [idConductor])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          opcionesAdicionalesPlataforma = doc.get("opcionesAdicionalesPlataforma", [])
          if not(opcionesAdicionalesPlataforma == None):
              if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                return True
              else:
                return False
    except ValueError:
        pass



def buscarOpcionesAdicionalesPlataforma(db, idVehiculo):
    docVehiculo = db[idVehiculo]
    opcionesAdicionalesPlataforma  =  docVehiculo.get("opcionesAdicionalesPlataforma",[]) 
    return opcionesAdicionalesPlataforma
