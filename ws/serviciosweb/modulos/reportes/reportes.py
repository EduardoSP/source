# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from ..configuracion          import configuracion
import datetime
from datetime                 import timedelta
import dateutil.parser
from geopy.distance import vincenty


def wsReporteEstadiscasVehiculos( peticion ):

    resultadoData = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"]
    fechaFin    = data["fechaFin"]
    vehiculos   = data.get("vehiculos", [])

    numeroOpcionHabilitadaPlataforma = data.get("numeroOpcionHabilitadaPlataforma",None)
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    if len(vehiculos) == 0:
        filasVehiculos = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs = False
        )

        for filaVehiculo in filasVehiculos:
            key        = filaVehiculo.key
            idVehiculo = key[0]
            vehiculos.append(idVehiculo)


    for idVehiculo in vehiculos:
        filaResultado = {}
        print idVehiculo
        docVehiculo = db[idVehiculo]
        kilometrosRecorridos = calcularKilometrosRecorridos(
            db,
            idVehiculo,
            fechaInicio,            
            fechaFin
        )

        velocidadPromedio = calcularVelocidadPromedio(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin
        )

        excesosVelocidad = calcularExcesosVelocidad(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin
        )

        duracionExcesosVelocidad = calcularDuracionExcesosVelocidad(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin
        )

        velocidadMaxima = calcularVelocidadMaxima(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin
        )

        totalParadas = calcularTotalParadas(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin
        )

        paradasRangos = calcularParadasRangos(
            db,
            ["R0-60", "R60-120", "R120"],
            idVehiculo,
            fechaInicio,
            fechaFin        
        )

        tiempoEncendido = calcularTiempoEncendido(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin            
        )

        numeroPanicos = calcularNumeroPanicos(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin            
        )

        desconexionesBateria = calcularDesconexionesBateria(
            db,
            idVehiculo,
            fechaInicio,
            fechaFin            
        )

        consumoGalCombustible = kilometrosRecorridos * docVehiculo.get("consumoGalKm",0)
        
        filaResultado["idVehiculo"]           = idVehiculo
        filaResultado["placaVehiculo"]        = docVehiculo.get("placa", "")
        filaResultado["kilometrosRecorridos"] = kilometrosRecorridos
        filaResultado["velocidadPromedio"]    = velocidadPromedio
        filaResultado["excesosVelocidad"]     = excesosVelocidad
        filaResultado["duracionExcesosVelocidad"] = duracionExcesosVelocidad
        filaResultado["velocidadMaxima"]      = velocidadMaxima       
        filaResultado["totalParadas"]         = totalParadas
        filaResultado["paradasRangos"]        = paradasRangos
        filaResultado["tiempoEncendido"]      = tiempoEncendido
        filaResultado["numeroPanicos"]        = numeroPanicos
        filaResultado["desconexionesBateria"] = desconexionesBateria
        filaResultado["consumoGalCombustible"] = "{0:.2f}".format(consumoGalCombustible)
        if not(numeroOpcionHabilitadaPlataforma == None):
            # Consulta realizada para validar si un vehiculo tiene configurada la opcion en la plataforma
            opcionesAdicionalesPlataforma = docVehiculo.get("opcionesAdicionalesPlataforma", [])
            if not(opcionesAdicionalesPlataforma == None):
                if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                    resultadoData.append(filaResultado)
        else:
            resultadoData.append(filaResultado)

    return {
        "success" : True,
        "data" : resultadoData
    }


def wsReporteEstadisticasVehiculoPorDia( peticion ):

    resultadoData = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"]
    fechaFin    = data["fechaFin"]
    idVehiculo  = data["idVehiculo"]
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }


    docVehiculo = db[idVehiculo]


    fechaIteracion = dateutil.parser.parse(fechaInicio)
    fechaFin       = data["fechaFin"][:10]
    while fechaIteracion.isoformat()[:10] <= fechaFin:
        filaResultado = {}    
        fecha = fechaIteracion.isoformat()[:10]
        print fecha
        
        kilometrosRecorridos = calcularKilometrosRecorridos(
            db,
            idVehiculo,
            fecha,            
            fecha
        )

        velocidadPromedio = calcularVelocidadPromedio(
            db,
            idVehiculo,
            fecha,
            fecha
        )
    
        excesosVelocidad = calcularExcesosVelocidad(
            db,
            idVehiculo,
            fecha,
            fecha
        )
        
        duracionExcesosVelocidad = calcularDuracionExcesosVelocidad(
            db,
            idVehiculo,
            fecha,
            fecha
        )
        
        velocidadMaxima = calcularVelocidadMaxima(
            db,
            idVehiculo,
            fecha,
            fecha
        )

        totalParadas = calcularTotalParadas(
            db,
            idVehiculo,
            fecha,
            fecha
        )
        
        paradasRangos = calcularParadasRangos(
            db,
            ["R0-60", "R60-120", "R120"],
            idVehiculo,
            fecha,
            fecha       
        )

        tiempoEncendido = calcularTiempoEncendido(
            db,
            idVehiculo,
            fecha,
            fecha            
        )
        
        numeroPanicos = calcularNumeroPanicos(
            db,
            idVehiculo,
            fecha,
            fecha            
        )

        desconexionesBateria = calcularDesconexionesBateria(
            db,
            idVehiculo,
            fecha,
            fecha            
        )

        consumoGalCombustible = kilometrosRecorridos * docVehiculo.get("consumoGalKm",0)
        
        filaResultado["fecha"]                = fecha        
        filaResultado["idVehiculo"]           = idVehiculo
        filaResultado["placaVehiculo"]        = docVehiculo.get("placa", "")
        filaResultado["kilometrosRecorridos"] = kilometrosRecorridos
        filaResultado["velocidadPromedio"]    = velocidadPromedio
        filaResultado["excesosVelocidad"]     = excesosVelocidad
        filaResultado["duracionExcesosVelocidad"] = duracionExcesosVelocidad
        filaResultado["velocidadMaxima"]      = velocidadMaxima       
        filaResultado["totalParadas"]         = totalParadas
        filaResultado["paradasRangos"]        = paradasRangos
        filaResultado["tiempoEncendido"]      = tiempoEncendido
        filaResultado["numeroPanicos"]        = numeroPanicos
        filaResultado["desconexionesBateria"] = desconexionesBateria
        filaResultado["consumoGalCombustible"] = "{0:.2f}".format(consumoGalCombustible)
        
        resultadoData.append(filaResultado)

        fechaIteracion = fechaIteracion + datetime.timedelta(days=1)
        

    return {
        "success" : True,
        "data" : resultadoData
    }


def wsReporteParadasVehiculo( peticion ):

    resultadoData = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"]
    fechaFin    = data["fechaFin"]
    vehiculos   = data.get("vehiculos", [])
    duracionInicioMinutos   = data.get("duracionInicioMinutos", 0)
    duracionFinMinutos      = data.get("duracionFinMinutos",    0)

    if duracionInicioMinutos == "":
        duracionInicioMinutos = 0
    if duracionFinMinutos == "":
        duracionFinMinutos = 0
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }


    if len(vehiculos) == 0:
        filasVehiculos = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs = False
        )
        for filaVehiculo in filasVehiculos:
            vehiculos.append(filaVehiculo.key[0])


    docsVehiculos = {}
    for idVehiculo in vehiculos:
        docVehiculo = db[idVehiculo]
        docsVehiculos[idVehiculo] = docVehiculo
            

    for idVehiculo in vehiculos:

        print "BUscando vehiculo {}".format(idVehiculo)
        filasParadas = db.view(
            '_design/estadisticas/_view/paradasVehiculosPorFecha',
            include_docs = True,
            startkey     = [fechaInicio[:10]],
            endkey       = [fechaFin[:10]+"Z"]
            
        )

        for filaParada in filasParadas:
            docParada = filaParada.doc

            if docParada.get("idVehiculo", "") in docsVehiculos:
                docVehiculo = docsVehiculos[docParada.get("idVehiculo", "")]

                fechahoraInicioDateTime = dateutil.parser.parse(docParada.get("fechahoraInicio", "")[:19])
                fechahoraFinDateTime = dateutil.parser.parse(docParada.get("fechahoraFin", "")[:19])
                duracionMinutos = int((fechahoraFinDateTime - fechahoraInicioDateTime).total_seconds()/60)

                esValidoFiltroDuracionParada = True

                print "La duracion en minutos es {} y revizando contra: {}".format(duracionMinutos, duracionInicioMinutos)
                
                if duracionMinutos < duracionInicioMinutos:
                    print "Por arriba"
                    esValidoFiltroDuracionParada = False
                if duracionFinMinutos > 0 and duracionMinutos >duracionFinMinutos:
                    print "por abajo"
                    esValidoFiltroDuracionParada = False

                print "La respuesta es: {}".format(esValidoFiltroDuracionParada)
                if esValidoFiltroDuracionParada:
                    dataItem = {
                        "idVehiculo"        : docVehiculo["_id"],
		        "placaVehiculo"     : docVehiculo.get("placa",""),
		        "latitud"           : docParada.get("latitud", ""),
		        "longitud"          : docParada.get("longitud", ""),
		        "fechahoraInicio"   : docParada.get("fechahoraInicio", ""),
		        "fechahoraFin"      : docParada.get("fechahoraFin", ""),
		        "nombreGeoposicion" : docParada.get("nombreGeoposicion", ""),
                        "duracionMinutos"   : duracionMinutos
                    }
                    resultadoData.append(dataItem)
            
    return {
        "success" : True,
        "data"     : resultadoData
    }


def wsReporteGraficoVehiculosPorEstadistica(peticion):

    resultadoData = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio     = data["fechaInicio"]
    fechaFin        = data["fechaFin"]
    tipoEstadistica = data["tipoEstadistica"] 
    vehiculos       = data.get("vehiculos", [])
    numeroOpcionHabilitadaPlataforma = data.get("numeroOpcionHabilitadaPlataforma",None)
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }


    if len(vehiculos) == 0:
        filasVehiculos = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs = False
        )

        for filaVehiculo in filasVehiculos:
            key        = filaVehiculo.key
            idVehiculo = key[0]
            vehiculos.append(idVehiculo)


    for idVehiculo in vehiculos:
        filaResultado = {}
        print idVehiculo
        docVehiculo = db[idVehiculo]

        valor = 0

        if tipoEstadistica == "kilometrosRecorridos":        
            valor = calcularKilometrosRecorridos(
                db,
                idVehiculo,
                fechaInicio,            
                fechaFin
            )
        elif tipoEstadistica == "velocidadPromedio":
            valor = calcularVelocidadPromedio(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin
            )
        elif tipoEstadistica == "excesosVelocidad":
            valor = calcularExcesosVelocidad(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin
            )
        elif tipoEstadistica == "duracionExcesosVelocidad":
            valor = calcularDuracionExcesosVelocidad(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin
            )
        elif tipoEstadistica == "velocidadMaxima":
            valor = calcularVelocidadMaxima(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin
            )
        elif tipoEstadistica == "totalParadas":
            valor = calcularTotalParadas(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin
            )
        elif tipoEstadistica == "R0-15":
            valor = calcularParadasRangos(
                db,
                ["R0-15"],
                idVehiculo,
                fechaInicio,
                fechaFin        
            )[0]["valorRango"]
        elif tipoEstadistica == "R15-30":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fechaInicio,
                fechaFin        
            )[0]["valorRango"]
        elif tipoEstadistica == "R30-60":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fechaInicio,
                fechaFin        
            )[0]["valorRango"]
        elif tipoEstadistica == "R60-120":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fechaInicio,
                fechaFin        
            )[0]["valorRango"]
        elif tipoEstadistica == "R120":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fechaInicio,
                fechaFin        
            )[0]["valorRango"]
        elif tipoEstadistica == "R0-60":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fechaInicio,
                fechaFin        
            )[0]["valorRango"]
        elif tipoEstadistica == "tiempoEncedido":
            valor = calcularTiempoEncendido(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin            
            )
        elif tipoEstadistica == "numeroPanicos":
            valor = calcularNumeroPanicos(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin            
            )

        elif tipoEstadistica == "desconexionesBateria":
            desconexionesBateria = calcularDesconexionesBateria(
                db,
                idVehiculo,
                fechaInicio,
                fechaFin            
            )
        elif tipoEstadistica == "consumoGalCombustible":        
            valor = calcularKilometrosRecorridos(
                db,
                idVehiculo,
                fechaInicio,            
                fechaFin
            ) * docVehiculo.get("consumoGalKm",0)
            valor = "{0:.2f}".format(valor)

        filaResultado = {
            
	    "idVehiculo"    : idVehiculo,
	    "placaVehiculo" : docVehiculo.get("placa", "") ,
	    "valor"         : valor
	    
        }
        if not(numeroOpcionHabilitadaPlataforma == None):
            # Consulta realizada para validar si un vehiculo tiene configurada la opcion en la plataforma
            opcionesAdicionalesPlataforma = docVehiculo.get("opcionesAdicionalesPlataforma", [])
            if not(opcionesAdicionalesPlataforma == None):
              if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                resultadoData.append(filaResultado)
        else:
            #consulta normal si no se recibe el parametro numeroOpcionHabilitadaPlataforma
            resultadoData.append(filaResultado)

    return {
        "success" : True,
        "data"    : resultadoData
    }
            
    
def wsReporteGraficoVehiculoEstadisticaPorFecha( peticion ):

    resultadoData = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio     = data["fechaInicio"]
    fechaFin        = data["fechaFin"]
    idVehiculo      = data["idVehiculo"]
    tipoEstadistica = data["tipoEstadistica"]
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }


    docVehiculo = db[idVehiculo]


    fechaIteracion = dateutil.parser.parse(fechaInicio)
    fechaFin       = data["fechaFin"][:10]
    while fechaIteracion.isoformat()[:10] <= fechaFin:
        filaResultado = {}    
        fecha = fechaIteracion.isoformat()[:10]

        valor = 0
        
        if tipoEstadistica == "kilometrosRecorridos":        
            valor = calcularKilometrosRecorridos(
                db,
                idVehiculo,
                fecha,            
                fecha
            )
        elif tipoEstadistica == "velocidadPromedio":
            valor = calcularVelocidadPromedio(
                db,
                idVehiculo,
                fecha,
                fecha
            )
        elif tipoEstadistica == "excesosVelocidad":
            valor = calcularExcesosVelocidad(
                db,
                idVehiculo,
                fecha,
                fecha
            )
        elif tipoEstadistica == "duracionExcesosVelocidad":
            valor = calcularDuracionExcesosVelocidad(
                db,
                idVehiculo,
                fecha,
                fecha
            )
        elif tipoEstadistica == "velocidadMaxima":
            valor = calcularVelocidadMaxima(
                db,
                idVehiculo,
                fecha,
                fecha
            )
        elif tipoEstadistica == "totalParadas":
            valor = calcularTotalParadas(
                db,
                idVehiculo,
                fecha,
                fecha
            )
        elif tipoEstadistica == "R0-15":
            valor = calcularParadasRangos(
                db,
                ["R0-15"],
                idVehiculo,
                fecha,
                fecha        
            )[0]["valorRango"]
        elif tipoEstadistica == "R15-30":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fecha,
                fecha        
            )[0]["valorRango"]
        elif tipoEstadistica == "R30-60":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fecha,
                fecha        
            )[0]["valorRango"]
        elif tipoEstadistica == "R60-120":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fecha,
                fecha        
            )[0]["valorRango"]
        elif tipoEstadistica == "R120":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fecha,
                fecha        
            )[0]["valorRango"]
        elif tipoEstadistica == "R0-60":
            valor = calcularParadasRangos(
                db,
                [tipoEstadistica],
                idVehiculo,
                fecha,
                fecha        
            )[0]["valorRango"]
        elif tipoEstadistica == "tiempoEncedido":
            valor = calcularTiempoEncendido(
                db,
                idVehiculo,
                fecha,
                fecha            
            )
        elif tipoEstadistica == "numeroPanicos":
            valor = calcularNumeroPanicos(
                db,
                idVehiculo,
                fecha,
                fecha            
            )

        elif tipoEstadistica == "desconexionesBateria":
            desconexionesBateria = calcularDesconexionesBateria(
                db,
                idVehiculo,
                fecha,
                fecha            
            )
        elif tipoEstadistica == "consumoGalCombustible":        
            valor = calcularKilometrosRecorridos(
                db,
                idVehiculo,
                fecha,            
                fecha
            ) * docVehiculo.get("consumoGalKm",0)
            valor = "{0:.2f}".format(valor)

        
        resultadoData.append({
            "idVehiculo" : idVehiculo,
            "fecha"      : fecha,
            "valor"      : valor
        })

        fechaIteracion = fechaIteracion + datetime.timedelta(days=1)
        
        
    return {
        "success" : True,
        "data" : resultadoData
    }

def wsReporteParadasVehiculosEnZonas(peticion):
    resultadoData = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"]
    fechaFin    = data["fechaFin"]
    vehiculos   = data.get("vehiculos", [])
    tipoZonas   = data.get("tipoZonas", [])
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    filas = db.view(
        '_design/estadisticas/_view/paradasVehiculosPorFecha',
        include_docs  = True ,        
        startkey     = [fechaInicio[:10]],
        endkey       = [fechaFin[:10]+"Z"]
    )

    listadoZonas      = cargarZonas(db)
    listadoTiposZonas = cargarTiposZonas(db)
    listadoVehiculos  = cargarVehiculos(db)
    
    
    for fila in filas:
        key   = fila.key
        value = fila.value
        docParada   = fila.doc

        idVehiculo = docParada.get("idVehiculo")
        tipoZonasPertenece, zonasPertenece = calcularPertenenciaZonas(docParada, listadoTiposZonas, listadoZonas )
        
        debeAgregarAlListado = True
        if len(vehiculos) > 0:
            if not idVehiculo in vehiculos:
                debeAgregarAlListado = False

        if debeAgregarAlListado:
            if len(tipoZonas)>0:
                for idTipoZona in tipoZonas:
                    if not estaTipoZonaEnTiposZonas(idTipoZona, tipoZonasPertenece):
                    #if not idTipoZona in tipoZonasPertenece:
                        debeAgregarAlListado = False
                        break
        if debeAgregarAlListado:
            docVehiculoParada = listadoVehiculos.get(
                docParada.get("idVehiculo", ""),
                {"placa": ""})
            vehiculoParada = {
                "placa" : docVehiculoParada.get("placa","")
            }

            zonasParada = []
            for zonaPertenece in zonasPertenece:
                zonasParada.append({
                    "id" : zonaPertenece.get("_id",""),
                    "nombre" : zonaPertenece.get("nombre", "")
                })

            tipoZonasParada = []
            for tipoZonaPertenece in tipoZonasPertenece:
                tipoZonasParada.append({
                    "id"          : tipoZonaPertenece.get("_id", ""),
		    "nombre"      : tipoZonaPertenece.get("nombre", ""),
		    "descripcion" : tipoZonaPertenece.get("descripcion", ""),
                })

            dateFechaInicio = dateutil.parser.parse(docParada.get("fechahoraInicio", "")[:19])

             
            dateFechaFin    = dateutil.parser.parse(docParada.get("fechahoraFin", docParada.get("fechahoraInicio", ""))[:19])

            print dateFechaInicio
            print dateFechaFin
            
            duracionParadaSegundos = (dateFechaFin-dateFechaInicio).total_seconds()
            
            if len(tipoZonasParada) >0:
                resultadoData.append({
                    "latitud"                : docParada.get("latitud", ""),
		    "longitud"               : docParada.get("longitud", ""),
		    "fechahoraInicio"        : docParada.get("fechahoraInicio", ""),
		    "fechahoraFin"           : docParada.get("fechahoraFin", ""),
		    "idVehiculo"             : docParada.get("idVehiculo", ""),
		    #"duracionParadaSegundos" : docParada.get("duracionParadaSegundos", ""),
                    "duracionParadaSegundos" : duracionParadaSegundos,
		    "vehiculo"  : vehiculoParada,
                    "zonas"     : zonasParada,
                    "tipoZonas" : tipoZonasParada 
                })
            
    return {
        "success" : True,
        "data" : resultadoData
    }



def wsReporteMapaCalorActividadVehiculo(peticion):

    
    maximoValor   = 0
    rangoInicio   = ""
    rangoFin      = ""
    puntosDeCalor = []

    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"][:10]
    fechaFin    = data["fechaFin"][:10]
    idVehiculo  = data["idVehiculo"]
    
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    fechaActual = fechaInicio


    formatoHoras = [
        "12:00am",
        "01:00am",
        "02:00am",
        "03:00am",
        "04:00am",
        "05:00am",
        "06:00am",
        "07:00am",
        "08:00am",
        "09:00am",
        "10:00am",
        "11:00am",
        "12:00pm",
        "01:00pm",
        "02:00pm",
        "03:00pm",
        "04:00pm",
        "05:00pm",
        "06:00pm",
        "07:00pm",
        "08:00pm",
        "09:00pm",
        "10:00pm",
        "11:00pm"        
    ]
    
    while fechaActual <= fechaFin:

        print fechaActual

        horas = []
        for x in range(0,24):
            horas.append({
                "hora"       : x,
                "horaFormato": formatoHoras[x],
                "kms"        : 0,
                "color"      : "#FFFFFF",
                "intensidad" : 0.0
            })
        
        
        
        #---------------------------------------------------            
        filas = db.view(
            '_design/estadisticas/_view/kilometrosRecorridosPorVehiculoPorFechaHora',
            include_docs = False,            
            reduce       = False,
            startkey     = [idVehiculo, fechaActual],
            endkey       = [idVehiculo, fechaActual+"Z"]                        
        )

        
        for fila in filas:
            distanciaMetros  = fila.value
            key              = fila.key
            horaRegistrada   = key[1]
                
            hora               = int( horaRegistrada[11:13])
            horas[hora]["kms"] = (horas[hora]["kms"] + distanciaMetros/1000.0)
            
            
        #-----------------------------------------------------

        for horita in horas:                        
            if horita["kms"] > maximoValor:
                maximoValor = horita["kms"]
                

        puntosDeCalor.append({
            "dia"   : fechaActual,
            "horas" : horas
        })
                
        #Cambio de delta.
        dateFechaActual = dateutil.parser.parse(fechaActual) + timedelta(days=1)        
        fechaActual     = dateFechaActual.isoformat()[:10]

    for puntoDeCalor in puntosDeCalor:
        for hora in puntoDeCalor.get("horas", []):

            intensidad = 0

            if maximoValor > 0:
                intensidad = hora["kms"] / maximoValor
            
            colorInt   = int( (1.0-intensidad) * 255)
            colorCode  = "%0.2X" % colorInt
            hora["intensidad"] = intensidad
            hora["color"]      = u"#FF{}{}".format(colorCode,colorCode)
            print hora

    return {
        "success" : True,
        "data"    : {
            "maximoValor"   : maximoValor,
	    "rangoInicio"   : fechaInicio,
	    "rangoFin"      : fechaFin,
	    "puntosDeCalor" : puntosDeCalor
        }
    }


def wsReporteMapaCalorActividadVehiculoGOODOLD(peticion):
    
    maximoValor   = 0
    rangoInicio   = ""
    rangoFin      = ""
    puntosDeCalor = []

    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"][:10]
    fechaFin    = data["fechaFin"][:10]
    idVehiculo  = data["idVehiculo"]
    
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    fechaActual = fechaInicio


    formatoHoras = [
        "12:00am",
        "01:00am",
        "02:00am",
        "03:00am",
        "04:00am",
        "05:00am",
        "06:00am",
        "07:00am",
        "08:00am",
        "09:00am",
        "10:00am",
        "11:00am",
        "12:00pm",
        "01:00pm",
        "02:00pm",
        "03:00pm",
        "04:00pm",
        "05:00pm",
        "06:00pm",
        "07:00pm",
        "08:00pm",
        "09:00pm",
        "10:00pm",
        "11:00pm"        
    ]
    
    while fechaActual <= fechaFin:

        print fechaActual

        horas = []
        for x in range(0,24):
            horas.append({
                "hora"       : x,
                "horaFormato": formatoHoras[x],
                "kms"        : 0,
                "color"      : "#FFFFFF",
                "intensidad" : 0.0
            })
        
        
        #busco el ultimo punto que usaré como referencia
        docUltimoPunto = {}
        
        filas = db.view(
            '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
            include_docs = True ,
            startkey     = [idVehiculo, fechaActual],
            limit        = 1,
            descending   = True
        )

        for fila in filas:
            docUltimoPunto = fila.doc

        #---------------------------------------------------            
        filas = db.view(
            '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
            include_docs = True ,
            startkey     = [idVehiculo, fechaActual],
            endkey       = [idVehiculo, fechaActual+"Z"]                        
        )

        
        for fila in filas:
            docPuntoActual = fila.doc

            puntoInicial    = (
                float(docUltimoPunto.get("latitud","0")),
                float(docUltimoPunto.get("longitud","0"))
            )

            puntoFinal      = (
                float(docPuntoActual.get("latitud","0")),
                float(docPuntoActual.get("longitud","0"))
            )

            if docUltimoPunto.get("latitud","0") == "0":
                puntoInicial = puntoFinal
                
            distanciaMetros = vincenty(puntoInicial, puntoFinal).meters

            datetimeInicio  = dateutil.parser.parse(docUltimoPunto.get("horaRegistrada", ""))
            datetimeFin     = dateutil.parser.parse(docPuntoActual.get("horaRegistrada", ""))
            distanciaTiempo = (datetimeFin - datetimeInicio).total_seconds()

            velocidadAprox  = 0
            
            if distanciaTiempo > 0 :
                velocidadAprox = (distanciaMetros/1000.0) / ( distanciaTiempo/(60.0*60.0) )

            if velocidadAprox < 300: #Menor a 300
                
                hora = int( docPuntoActual.get("horaRegistrada","")[11:13])
                horas[hora]["kms"] = (horas[hora]["kms"] + distanciaMetros/1000.0)

                docUltimoPunto = docPuntoActual
        #-----------------------------------------------------

        for horita in horas:                        
            if horita["kms"] > maximoValor:
                maximoValor = horita["kms"]
                

        puntosDeCalor.append({
            "dia"   : fechaActual,
            "horas" : horas
        })
                
        #Cambio de delta.
        dateFechaActual = dateutil.parser.parse(fechaActual) + timedelta(days=1)        
        fechaActual     = dateFechaActual.isoformat()[:10]

    for puntoDeCalor in puntosDeCalor:
        for hora in puntoDeCalor.get("horas", []):

            intensidad = 0

            if maximoValor > 0:
                intensidad = hora["kms"] / maximoValor
            
            colorInt   = int( (1.0-intensidad) * 255)
            colorCode  = "%0.2X" % colorInt
            hora["intensidad"] = intensidad
            hora["color"]      = u"#FF{}{}".format(colorCode,colorCode)
            print hora

    return {
        "success" : True,
        "data"    : {
            "maximoValor"   : maximoValor,
	    "rangoInicio"   : fechaInicio,
	    "rangoFin"      : fechaFin,
	    "puntosDeCalor" : puntosDeCalor
        }
    }


def wsReporteCalificacionConductores(peticion):
    
    dataResultado = []
    
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio = data["fechaInicio"][:10]
    fechaFin    = data["fechaFin"][:10]
    conductores = data.get("conductores", [])

    if fechaInicio > fechaFin:
        fechaInicio = fechaFin
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    configuraciones = configuracion.getTodaConfiguracion(db)

    pesosInfracciones = {
        "aceleracion"       : configuraciones.get("PENALIZACIONACELERACIONES",1),
        "frenadas"          : configuraciones.get("PENALIZACIONFRENADAS",1),
        "movimientoAbrupto" : configuraciones.get("PENALIZACIONMOVIMIENTOSABRUPTOS",1),
        "excesosVelocidad"  : configuraciones.get("PENALIZACIONEXCESOSVELOCIDAD",1)
    }

    filasConductores = db.view(
        '_design/conductores/_view/listarConductores',
            include_docs = True 
        )

        
    for filaConductor in filasConductores:
        docConductor       = filaConductor.doc
        idConductor        = docConductor["_id"]
        if len(conductores)>0:
            if not idConductor in conductores:
                continue
        conductor          = {
            "nombres"   : docConductor.get("nombres",   ""),
	    "apellidos" : docConductor.get("apellidos", ""),
	    "celular"   : docConductor.get("celular",   ""),
	    "cedula"    : docConductor.get("cedula",    "")
        }
        calificacionesDict = {}

        #Inicializo las calificaciones:-------------------------
        fechaActual = fechaInicio

        while fechaActual <= fechaFin:

            #print fechaActual
            calificacionesDict[fechaActual] = {
                "dia"          : fechaActual,
                "calificacion" : 100
            }
            
            #Cambio de delta.
            dateFechaActual = dateutil.parser.parse(fechaActual) + timedelta(days=1)        
            fechaActual     = dateFechaActual.isoformat()[:10]
        #--------------------------------------------------------

        #Buscar aceleraciones -----------------------------------
        filasAceleraciones = db.view(
            '_design/seguridadVial/_view/listarAceleracionPorConductor',
            include_docs = False,
            startkey     = [idConductor, fechaInicio],
            endkey       = [idConductor, fechaFin+"Z"]
            
        )

        
        for filaAceleracion in filasAceleraciones:
            keyVehiculo = filaAceleracion.key
            fecha       = keyVehiculo[1][:10]
            calificacionesDict[fecha]["calificacion"] -= pesosInfracciones["aceleracion"]
            if calificacionesDict[fecha]["calificacion"] < 0:
                calificacionesDict[fecha]["calificacion"] = 0
                
        #--------------------------------------------------------

        #Buscar frenadas-----------------------------------------
        filasFrenadas = db.view(
            '_design/seguridadVial/_view/listarFrenadasPorConductor',
            include_docs = False,
            startkey     = [idConductor, fechaInicio],
            endkey       = [idConductor, fechaFin+"Z"]
            
        )
        
        for filaFrenada in filasFrenadas:
            keyFrenada  = filaFrenada.key
            fecha       = keyFrenada[1][:10]
            calificacionesDict[fecha]["calificacion"] -= pesosInfracciones["frenadas"]
            if calificacionesDict[fecha]["calificacion"] < 0:
                calificacionesDict[fecha]["calificacion"] = 0
        #--------------------------------------------------------

        #Buscar abrupto-----------------------------------------
        filasMovimientoAbrupto = db.view(
            '_design/seguridadVial/_view/listarMovimientoAbruptoConductor',
            include_docs = False,
            startkey     = [idConductor, fechaInicio],
            endkey       = [idConductor, fechaFin+"Z"]
            
        )
        
        for filaMovimientoAbrupto in filasMovimientoAbrupto:
            keyAbrupto  = filaMovimientoAbrupto.key
            fecha       = keyAbrupto[1][:10]
            calificacionesDict[fecha]["calificacion"] -= pesosInfracciones["movimientoAbrupto"]
            if calificacionesDict[fecha]["calificacion"] < 0:
                calificacionesDict[fecha]["calificacion"] = 0
        #--------------------------------------------------------

        #Buscar exceso velocidad---------------------------------
        filasExcesosVelocidad = db.view(
            '_design/seguridadVial/_view/listarExcesoVelocidadPorConductor',
            include_docs = False,
            startkey     = [idConductor, fechaInicio],
            endkey       = [idConductor, fechaFin+"Z"]
            
        )
        
        for filaExcesoVelocidad in filasExcesosVelocidad:
            keyVelocidad  = filaExcesoVelocidad.key
            fecha         = keyVelocidad[1][:10]
            calificacionesDict[fecha]["calificacion"] -= pesosInfracciones["excesosVelocidad"]
            if calificacionesDict[fecha]["calificacion"] < 0:
                calificacionesDict[fecha]["calificacion"] = 0
        #--------------------------------------------------------

        calificaciones = []
        for key in sorted(calificacionesDict.keys()):
            calificaciones.append(calificacionesDict[key])
            
        dataResultado.append({
            "idConductor"    : idConductor,
            "conductor"      : conductor,
            "calificaciones" : calificaciones
        })
            

    return {
        "success" : True,
        "data"    : dataResultado
    }



def wsReporteConduccionPorFueraDeHorario(peticion):
        
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio         = data["fechaInicio"][:10]
    fechaFin            = data["fechaFin"][:10]
    horaInicioOperacion = data["horaInicioOperacion"]
    horaFinOperacion    = data["horaFinOperacion"]
    numeroOpcionHabilitadaPlataforma = data.get("numeroOpcionHabilitadaPlataforma",None)

    horarioFuera        = [] #Resultado va acá
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    
    filasVehiculos = db.view(
        '_design/vehiculos/_view/vehiculos',
        include_docs = True 
    )

        
    for filaVehiculo in filasVehiculos:
        docVehiculo = filaVehiculo.doc
        idVehiculo  = docVehiculo["_id"]        
        fechaActual = fechaInicio
        
        while fechaActual <= fechaFin:

            kmsAntes    = 0
            kmsDespues  = 0
            
            # Horas antes---------------------------------------------------------------
            filas = db.view(
                '_design/estadisticas/_view/kilometrosRecorridosPorVehiculoPorFechaHora',
                include_docs = False ,
                startkey     = [idVehiculo, fechaActual+"T00:00:00"],
                endkey       = [idVehiculo, fechaActual+"T"+horaInicioOperacion],
                reduce       = True,
                group_level  = 0                        
            )

            for fila in filas:
                kmsAntes = fila.value / 1000.0

            # Horas Despues---------------------------------------------------------------
            filas = db.view(
                '_design/estadisticas/_view/kilometrosRecorridosPorVehiculoPorFechaHora',
                include_docs = False ,
                startkey     = [idVehiculo, fechaActual+"T"+horaFinOperacion],
                endkey       = [idVehiculo, fechaActual+"T24:00:00"],
                reduce       = True,
                group_level  = 0                        
            )

            for fila in filas:
                kmsDespues = fila.value / 1000.0
        
                        
            if kmsAntes > 1 or kmsDespues > 1:
                if not(numeroOpcionHabilitadaPlataforma == None):
                    # Consulta realizada para validar si un vehiculo tiene configurada la opcion en la plataforma
                    opcionesAdicionalesPlataforma = docVehiculo.get("opcionesAdicionalesPlataforma", [])
                    if not(opcionesAdicionalesPlataforma == None):
                        if numeroOpcionHabilitadaPlataforma in opcionesAdicionalesPlataforma:
                            horarioFuera.append({
                                "idVehiculo" : idVehiculo,
                                "placa"      : docVehiculo.get("placa"),
                                "fecha"      : fechaActual,
                                "kmsAntes"   : kmsAntes,
                                "kmsDespues" : kmsDespues
                            })
                else:
                    horarioFuera.append({
                        "idVehiculo" : idVehiculo,
                        "placa"      : docVehiculo.get("placa"),
                        "fecha"      : fechaActual,
                        "kmsAntes"   : kmsAntes,
                        "kmsDespues" : kmsDespues
                    })

            #Cambio de delta.
            dateFechaActual = dateutil.parser.parse(fechaActual) + timedelta(days=1)        
            fechaActual     = dateFechaActual.isoformat()[:10]


    return {
        "success" : True,
        "data"    : horarioFuera
    }

def wsReporteConduccionPorFueraDeHorarioOLDGOOD(peticion):
        
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']

    fechaInicio         = data["fechaInicio"][:10]
    fechaFin            = data["fechaFin"][:10]
    horaInicioOperacion = data["horaInicioOperacion"]
    horaFinOperacion    = data["horaFinOperacion"]

    horarioFuera        = [] #Resultado va acá
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    
    filasVehiculos = db.view(
        '_design/vehiculos/_view/vehiculos',
        include_docs = True 
    )

        
    for filaVehiculo in filasVehiculos:
        docVehiculo = filaVehiculo.doc
        idVehiculo  = docVehiculo["_id"]        
        fechaActual = fechaInicio
        
        while fechaActual <= fechaFin:
            #busco el ultimo punto que usaré como referencia
            docUltimoPunto = {}
            
            filas = db.view(
                '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
                include_docs = True ,
                startkey     = [idVehiculo, fechaActual],
                limit        = 1,
                descending   = True
            )

            for fila in filas:
                docUltimoPunto = fila.doc

            #---------------------------------------------------            

            filas = db.view(
                '_design/posicionVehiculoRangoFecha/_view/posicionVehiculoRangoFecha',
                include_docs = True ,
                startkey     = [idVehiculo, fechaActual],
                endkey       = [idVehiculo, fechaActual+"Z"]                        
            )
        
            kmsAntes    = 0
            kmsDespues  = 0
            kmsTotales  = 0
            
            for fila in filas:
                docPuntoActual = fila.doc                
                horaActual     = docPuntoActual.get("horaRegistrada")[11:19]
                puntoInicial    = (
                    float(docUltimoPunto.get("latitud","0")),
                    float(docUltimoPunto.get("longitud","0"))
                )

                puntoFinal      = (
                    float(docPuntoActual.get("latitud","0")),
                    float(docPuntoActual.get("longitud","0"))
                )

                if docUltimoPunto.get("latitud","0") == "0":
                    puntoInicial = puntoFinal

                distanciaMetros = vincenty(puntoInicial, puntoFinal).meters

                datetimeInicio  = dateutil.parser.parse(docUltimoPunto.get("horaRegistrada", ""))
                datetimeFin     = dateutil.parser.parse(docPuntoActual.get("horaRegistrada", ""))
                distanciaTiempo = (datetimeFin - datetimeInicio).total_seconds()

                velocidadAprox  = 0

                if distanciaTiempo > 0 :
                    velocidadAprox = (distanciaMetros/1000.0) / ( distanciaTiempo/(60.0*60.0) )

                #Verificar datos-----------------------------------------------------------
                if velocidadAprox < 300: 
                    if horaActual < horaInicioOperacion:
                        kmsAntes += (distanciaMetros/1000.0)
                    if horaActual > horaFinOperacion:
                        kmsDespues += (distanciaMetros/1000.0)
                    docUltimoPunto = docPuntoActual
                    
                #--------------------------------------------------------------------------

            if kmsAntes > 1 or kmsDespues > 1:
                horarioFuera.append({
                    "idVehiculo" : idVehiculo,
                    "placa"      : docVehiculo.get("placa"),
                    "fecha"      : fechaActual,
                    "kmsAntes"   : kmsAntes,
                    "kmsDespues" : kmsDespues
                })
            #Cambio de delta.
            dateFechaActual = dateutil.parser.parse(fechaActual) + timedelta(days=1)        
            fechaActual     = dateFechaActual.isoformat()[:10]


    return {
        "success" : True,
        "data"    : horarioFuera
    }


######################################################
# Funciones auxiliares
######################################################

#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularKilometrosRecorridos(db, idVehiculo, fechaInicio, fechaFin):
    kilometrosRecorridos = 0

    
    
    filasKilometros = db.view(
        '_design/estadisticas/_view/kilometrosRecorridosPorVehiculoPorFecha',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]+"Z"],
        reduce       = True,
        group_level  = 0
    )

    for filaKilometros in filasKilometros:
        kilometrosRecorridos = filaKilometros.value / 1000.0

    return kilometrosRecorridos


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularVelocidadPromedio(db, idVehiculo, fechaInicio, fechaFin):
    velocidadPromedio = 0
    
    filasVelocidadPromedio = db.view(
        '_design/estadisticas/_view/velocidadPorVehiculoPorFecha',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]+"Z"],
        reduce       = True,
        group_level  = 0
    )

    for filaVelocidadPromedio in filasVelocidadPromedio:
        value = filaVelocidadPromedio.value
        print "calculando por velocidad promedio"
        print value
        velocidadPromedio = value["sum"] / value["count"]
        
    return velocidadPromedio


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularExcesosVelocidad(db, idVehiculo, fechaInicio, fechaFin):
    excesosVelocidad = 0
    
    filasExcesosVelocidad = db.view(
        '_design/estadisticas/_view/excesosVelocidaPorVehiculoPorFecha',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]+"Z"],
        reduce       = True,
        group_level  = 0
    )

    for filaExcesoVelocidad in filasExcesosVelocidad:
        
        excesosVelocidad = filaExcesoVelocidad.value
        
    return excesosVelocidad


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularDuracionExcesosVelocidad(db, idVehiculo, fechaInicio, fechaFin):
    tiempoExcesoVelocidad = 0
    
    filasExcesosVelocidad = db.view(
        '_design/estadisticas/_view/tiempoExcesoVelocidaPorVehiculoPorFecha',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]],
        reduce       = True,
        group_level  = 0
    )

    for filaExcesoVelocidad in filasExcesosVelocidad:
        
        tiempoExcesoVelocidad = filaExcesoVelocidad.value
        
    return tiempoExcesoVelocidad


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularVelocidadMaxima(db, idVehiculo, fechaInicio, fechaFin):
    velocidadMaxima = 0
    
    filasVelocidadMaxima = db.view(
        '_design/estadisticas/_view/velocidadPorVehiculoPorFecha',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]],
        reduce       = True,
        group_level  = 0
    )

    for filaVelocidadMaxima in filasVelocidadMaxima:

        value = filaVelocidadMaxima.value

        velocidadMaxima = value["max"]
        
    return velocidadMaxima


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularTotalParadas(db, idVehiculo, fechaInicio, fechaFin):

    totalParadas = 0
    
    filasTotalParadas = db.view(
        '_design/estadisticas/_view/cantidadParadasVehiculos',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]+"Z"],
        reduce       = True,
        group_level  = 0
    )

    for filaTotalParada in filasTotalParadas:
        totalParadas = filaTotalParada.value
        
    return totalParadas


#db          : enlace a la base de datos.
#rangos      : ["R0-60", "R60-120"]
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularParadasRangos(db, rangos, idVehiculo, fechaInicio, fechaFin):

    listado = []

    for rango in rangos:
        filasTotalParadas = db.view(
            '_design/estadisticas/_view/rangosParadasVehiculos',
            include_docs = False,
            startkey     = [idVehiculo, rango,  fechaInicio[:10]],
            endkey       = [idVehiculo, rango,  fechaFin[:10]+"Z"],
            reduce       = True,
            group_level  = 0
        )

        valorRango = 0
        for filaTotalParada in filasTotalParadas:
            valorRango = filaTotalParada.value
            
        listado.append({
            "codigoRango" : rango,
            "valorRango"  : valorRango
        })
    
    return listado


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularTiempoEncendido(db, idVehiculo, fechaInicio, fechaFin):
    
    totalTiempoEncendido = 0
    
    filasEncendido = db.view(
        '_design/estadisticas/_view/tiempoMotorEncendidoPorVehiculoPorFecha',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]+"Z"],
        reduce       = True,
        group_level  = 0
    )

    for filaEncendido in filasEncendido:
        totalTiempoEncendido = int( filaEncendido.value / 60 )
        
    return totalTiempoEncendido


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularNumeroPanicos(db, idVehiculo, fechaInicio, fechaFin):
    totalPanicos = 0
    
    filasPanicos = db.view(
        '_design/estadisticas/_view/cantidadBotonesPanico',
        include_docs = False,
        startkey     = [idVehiculo, fechaInicio[:10]],
        endkey       = [idVehiculo, fechaFin[:10]+"Z"],
        reduce       = True,
        group_level  = 0
    )

    for filaPanico in filasPanicos:
        totalPanicos = filaPanico.value
        
    return totalPanicos


#db          : enlace a la base de datos.
#idVehiculo  : id del vehículo a buscar (string)
#fechaInicio : fecha en string formato iso8660
#fechaFin    : fecha en string formato iso8660
def calcularDesconexionesBateria(db, idVehiculo, fechaInicio, fechaFin):
    return 0

def cargarZonas(db):
    resultado = {}

    filas = db.view('_design/vigilancias/_view/monitoreoZonas',
                    include_docs  = True)

    for fila in filas:
        doc = fila.doc
        resultado[doc["_id"]] = doc
    
    
    return resultado

def cargarTiposZonas(db):
    resultado = {}

    filas = db.view(
        '_design/tipoZona/_view/listarTipoZona',
        include_docs  = True
    )

    for fila in filas:
        doc = fila.doc
        resultado[doc["_id"]] = doc
    
    
    return resultado

def cargarVehiculos(db):
    resultado = {}

    filas = db.view(
        '_design/vehiculos/_view/vehiculos',
        include_docs  = True
    )
    
    for fila in filas:
        doc = fila.doc
        resultado[doc["_id"]] = doc
    
    
    return resultado

#Retorna dos valores, tipoZonasPertenece, zonasPertenece, son los list
#de documentos que entran en las zonas.
def calcularPertenenciaZonas(docParada, listadoTiposZonas, listadoZonas ):

    tipoZonasPertenece = []
    zonasPertenece     = []

    puntoInicial    = (
        float(docParada.get("latitud","0")),
        float(docParada.get("longitud","0"))
    )
    
    for idZona, docZona in listadoZonas.iteritems() :
        
        latitudMZona  = docZona.get("latitud","0")
        longitudMZona = docZona.get("longitud","0")               
        radioMZona    = docZona.get("radio","0")               
        
        puntoFinal      = (float(latitudMZona), float(longitudMZona)) 
        distanciaMetros = vincenty(puntoInicial, puntoFinal).meters

        if distanciaMetros <= float(radioMZona): #esta en zona
            zonasPertenece.append(docZona)
            tipoZonasPertenece.append(
                listadoTiposZonas.get( docZona.get("tipoZona",""), {} )
            )

    return (tipoZonasPertenece, zonasPertenece)    


def estaTipoZonaEnTiposZonas(idTipoZona, tipoZonasPertenece):
    resultado = False
    for tipoZona in tipoZonasPertenece:
        if idTipoZona == tipoZona.get("_id", ""):
            resultado = True
            break
    return resultado


def wsReportesCadenaFrio(peticion):
    resultadoData = []
    autenticacion = peticion["autenticacion"]
    data          = peticion["data"]
    usuario     = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    fechaInicio = data["fechaInicio"]
    fechaFin    = data["fechaFin"]
    vehiculos   = data.get("vehiculos", [])
    datosVehiculos = []
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }
    
    if len(vehiculos) == 0:
        filasVehiculos = db.view(
            '_design/vehiculos/_view/vehiculos',
            include_docs = True
        )
        for filaVehiculo in filasVehiculos:
            key                             = filaVehiculo.key
            idVehiculo                      = key[0]    
            docVehiculo                     = filaVehiculo.doc
            estaAlarmaCadenaFrioActivada    = docVehiculo.get("estaAlarmaCadenaFrioActivada", False)
            placa    = docVehiculo.get("placa", "")
            if estaAlarmaCadenaFrioActivada:
                datosVehiculos.append({
                    "idVehiculo" : idVehiculo,
                    "placa"      : placa
                    })
    else:
        #busco las placas de los vehiculos seleccionados del picker
        for idVehiculo in vehiculos:
            #busco la placa del vehiculo
            placa = buscarPlacaVehiculo(db, idVehiculo)
            datosVehiculos.append({
                "idVehiculo" : idVehiculo,
                "placa"      : placa
                })

    for vehiculo in datosVehiculos:
        temperaturaMaxima   = 0
        temperaturaMinima   = 0
        temperaturaPromedio = 0
        filas = db.view('_design/cadenaFrio/_view/puntoCadenaFrio',      
            startkey     = [vehiculo["idVehiculo"], fechaInicio[:10]],
            endkey       = [vehiculo["idVehiculo"], fechaFin[:10]+"Z"]
        )
        for fila in filas:
            key   = fila.key
            value = fila.value
            temperaturaMinima   = value["min"]
            temperaturaMaxima   = value["max"]
            temperaturaPromedio = value["sum"] / value["count"]
        resultadoData.append({
                    "idVehiculo"            : vehiculo["idVehiculo"],
                    "placa"                 : vehiculo["placa"],
                    "temperaturaMinima"     : temperaturaMinima,
                    "temperaturaMaxima"     : temperaturaMaxima,
                    "temperaturaPromedio"   : temperaturaPromedio
                })
    return {
        "success" : True,
        "data" : resultadoData
    }


def buscarPlacaVehiculo(db, idVehiculo):
    docVehiculo = db[idVehiculo]
    return docVehiculo.get("placa", "")