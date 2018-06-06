# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime, timedelta
from ..autenticacion          import autenticacion as moduloAutenticacion
from geopy.distance import vincenty
from paradas                        import evaluarParadas, actualizarPosicionVehiculoParadas
from audiosZonaAlarma               import ejecutarAudioZonaAlarma, verificarLlamadaEnCursoZA, terminarLlamadaSaleZonaAlarma, verificarLlamadaZAEjecutada
from programacionVigilanciaAudio    import ejecutarAudioProgramacionVigilancia, verificarLlamadaPVEjecutada, verificarLlamadaEnCursoPV
from verificarSolicitaTomarFoto     import solicitaTomarFotoZonaAlarma, solicitaTomarFotoProgramacionVigilancia
from llamadasSimultaneas            import verificarLlamadaProgramacionVigilancia, guardarLlamadaSimultaneaZA, verificarDoccapturaAudioZonaAlarmaCreada, verificarLlamadaZonaAlarma, verificarDocaudioProgramacionVigilancia, guardarLlamadaSimultaneaPV, obtenerLimiteMayorZonaAlarmas, obtenerLimiteMayorProgramacion, actualizarDocLLamadasRazonLimite
from verificarActivarProgramacionVigilancia import puedoUsarPV, guardarProgramacionVigilanciaComoEjecutada
import requests
import json
from dateutil import parser
import pytz
from  ws.serviciosweb.modulos.notificaciones.notificaciones import notificarTenant
import random
#----------------------------------------------------------------------------------------
def solicitarTomarFoto(idFoto, rutaFoto, idGps):
    # se solicita la toma de la captura al GPS
    try:
        peticion = {
            "autenticacion" : {  
                "usuario" : "gps",     "token"   : "123456"  
            }, 
            "data" : {  
                "idFoto"   : idFoto,       
                "rutaFoto" : rutaFoto,       
                "idGps"    : idGps   
            } 

        } 

        datos ={"request": json.dumps(peticion) }

        cabeceras = {
           "Content-Type" : "application/x-www-form-urlencoded"
            }
        url = settings.URL_SOLICITAR_FOTO
        response = requests.post(url, data=datos, headers=cabeceras)
        print response.text
    except requests.exceptions.RequestException as e:
        print e


def wslistadoGPS(idVehiculo):
    datosGPS = ["",""]
    dbFleet = conexion.getConexionFleet()
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view('_design/GPS/_view/GPS',
                    include_docs  = True, 
                    startkey = [idVehiculo, 0],
                    endkey = [idVehiculo, {}])

        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            identificadorGPS = doc.get('identificadorGPS') 
            datosGPS[0] = doc.get('identificadorGPS') 
            datosGPS[1] = doc.get('tenant')      
        return datosGPS

    except :
        pass

    return { 'success' : False}


def ejecutarSolicitudCapturaImagen(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    dbFleet = conexion.getConexionFleet()

    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:     
        idVehiculo          =   datos['idVehiculo']
        #consulta vista para extraer el identificador del GPS
        datosGPS    =   wslistadoGPS(idVehiculo)
        if datosGPS[0] != "" and datosGPS[1] != "":     
            doc_id, doc_rev = dbFleet.save({
                "tipoDato"              :   "inspeccionImagen",
                "fechaHoraSolicitud"    :   datetime.now().isoformat(),  
                "estado"                :   "pendiente",
                "identificadorGPS"      :   datosGPS[0],
                "idVehiculo"            :   idVehiculo,
                "esDirecta"             :   True,
                "esPanico"              :   False,
                "idZona"                :   [],
                "idVigilancia"          :   [],
                #"idPanico"             :   idPanico,
                "idPanico"              :   "",
                "tenant"                :   datosGPS[1],
                "activo"                :   True
            })

            #crear el documento inspeccionImagen
            #Se llama a la funcion de node para que me genere la imagen el GPS
            idFoto = doc_id
            #Llamar a ws para que el GPS tome la foto
            rutaCreacion = settings.GPS_RUTA_FOTO
            solicitarTomarFoto(idFoto, rutaCreacion, datosGPS[0]) 
        else:
            doc_id = "El vehiculo no tiene un GPS asociado"           
        return {
            'success' : True, 
            'data'    : {
                'id' : doc_id
            }              
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------

#----------------------------------------------------------------------------
#Inicio funciones auxiliares para registrar los puntos del GPS 

def guardarDocumentoPosicionVehiculos(peticion,latitud,longitud,horaRegistrada,estado,idVehiculo,ultimaPosicion, zonaAlarmas, programacionVigilancia):
    #funcion que guarda el documento en la bd
    autenticacion = peticion['autenticacion']
    dataJson      = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:        
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        logging.warning("GOOD!!")

        posiciones = dataJson.get("posiciones",[])
        estaMotorEncendido = True
        for posicion in posiciones:
            estaMotorEncendido = posicion.get("estaMotorEncendido",True) 
        
        doc_id, doc_rev = db.save({
            "tipoDato"                  : "posicionVehiculos",
            "creadoEn"                  : datetime.now().isoformat(), 
            "modificadoEn"              : datetime.now().isoformat(), 
            "modificadoPor"             : usuario,
            "horaRegistrada"            : horaRegistrada,
            "horaRecibida"              : datetime.now().isoformat(),
            "latitud"                   : latitud,
            "longitud"                  : longitud,
            "idVehiculo"                : idVehiculo,
            "estado"                    : estado,
            "activo"                    : True,
            "ultimaPosicion"            : ultimaPosicion,
            "zonaAlarmas"               : zonaAlarmas,
            "programacionVigilancia"    : programacionVigilancia,
            "idParada"                  : "",
            "idFragmento"               : "",
            "estaEncendidoMotor"        : estaMotorEncendido,
        })
        return doc_id
    except ValueError:
        logging.warning("GOOD!")
        pass

def obteneridVehiculo(identificadorGPS):
    #obtiene el id de vehiculo segun el numero del identificador del GPS
    idVehiculo = ""
    dbFleet = conexion.getConexionFleet()
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view('_design/GPS/_view/idVehiculoGPS',
                    include_docs  = True, 
                    startkey = [identificadorGPS, 0],
                    endkey = [identificadorGPS, {}])

        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            idVehiculo = doc.get('idVehiculo')   
        return idVehiculo
    except :
        pass

def obtenerTenantVehiculo(identificadorGPS):
    #obtiene el tenant de vehiculo segun el numero del identificador del GPS
    tenantVehiculo = ""
    dbFleet = conexion.getConexionFleet()
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view(
            '_design/GPS/_view/idVehiculoGPS',
            include_docs  = True, 
            startkey      = [identificadorGPS, 0],
            endkey        = [identificadorGPS, {}]
        )

        for fila in filas:
            key        = fila.key
            value      = fila.value
            doc        = fila.doc
            tenantVehiculo = doc.get('tenant')   
        return tenantVehiculo
    except :
        pass

#Fin funciones auxiliares para registrar los puntos del GPS
#----------------------------------------------------------------------------------
def crearZonaAlarma(peticion, horaInicioZonaAlarma, horaFinZonaAlarma, estado, idMZona, idVehiculo):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    try: 

        doc_id, doc_rev = db.save({
            "tipoDato"      : "zonaAlarma",
            "fecha"         : datetime.now().isoformat(),  
            "horaInicio"    : horaInicioZonaAlarma,
            "horaFin"       : horaFinZonaAlarma,
            "estado"        : estado,
            "idVehiculo"    : idVehiculo,
            "idZona"        : idMZona,
            "activo"        : True,
            "timeStamp"     : time.time() 
        })
        docVehiculo = db[idVehiculo]
        placa       = docVehiculo["placa"]         
        notificarTenant(tenant, "alarma", u"El vehículo {} ingresó a una zona Alarma".format(placa))
          
    except ValueError:
        pass
    return doc_id


def buscarPuntoAnterior(peticion, idVehiculo):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    doc = None
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/posicionVehiculos/_view/ultimaPosicionGuardada',
                    include_docs  = True,
                    key      = [True, idVehiculo])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
        return doc
    except ValueError:
        pass


def obteneridZonaMonitoreada(peticion, idZonaAlarmaAnterior):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    idZonaMonitoreadaAnterior = None
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []
        filas = db.view('_design/idZonaMonitoreada/_view/idZonaMonitoreada',
                    include_docs  = True,
                    startkey = [idZonaAlarmaAnterior,0],
                    endkey = [idZonaAlarmaAnterior,{}],
                    limit = 1)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          idZonaMonitoreadaAnterior = doc.get('idZona')         
    except ValueError:
        pass
    return idZonaMonitoreadaAnterior


def evaluarZonaMonitoreadaExistente(peticion, idZonaAlarmaAnterior, idMZona):
    #idMZona es el identificador de la zona monitoreada
    #busco el identificador de la zona monitoreada
    idZonaMonitoreadaAnterior = obteneridZonaMonitoreada(peticion, idZonaAlarmaAnterior)  
    #print idZonaMonitoreadaAnterior
    #print idMZona
    if idZonaMonitoreadaAnterior == idMZona:
        return True
    else:
        return False


def zonaDetectadaExiste(peticion, idMZona, docPuntoAnterior):
    respuesta = None
    for idZonaAlarmaAnterior in docPuntoAnterior.get('zonaAlarmas'):
        if evaluarZonaMonitoreadaExistente(peticion, idZonaAlarmaAnterior, idMZona):
            respuesta = idZonaAlarmaAnterior
    return respuesta

def modificarDocumentoZonaAlarma(peticion, idZonaAlarmaAnterior, horaFin):
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    docZonaAlarma = db[idZonaAlarmaAnterior]
    docZonaAlarma["estado"] = "Finalizado"
    docZonaAlarma["horaFin"]= horaFin
    db.save(docZonaAlarma) 


def verificarPuntosContinuaZonaAlarma(peticion, docPuntoAnterior, puntoZonaAlarmaActual):
    #Nota Falta acomodar bien el formato de la hora fin
    estaZonaAlarma  = False
    for i in range(len(docPuntoAnterior.get('zonaAlarmas'))):
        idZonaAlarmaAnterior = docPuntoAnterior.get('zonaAlarmas')[i]
        for k in range(len(puntoZonaAlarmaActual)):
            idZonaAlarmaActual   = puntoZonaAlarmaActual[k]
            if idZonaAlarmaAnterior == idZonaAlarmaActual:
                estaZonaAlarma  = True
        if not(estaZonaAlarma):
            modificarDocumentoZonaAlarma(peticion, idZonaAlarmaAnterior, docPuntoAnterior.get('horaRegistrada'))
        estaZonaAlarma  = False



def puntosEstaEnZona(peticion, idVehiculo, latitudVehiculo, longitudVehiculo, horaRegistrada, zonasMonitoreadas):
    puntoZonaAlarma         = [] # p["za"]
    estado                  = "En curso"
    horaFinZonaAlarma       = ""
    docPuntoAnterior = buscarPuntoAnterior(peticion, idVehiculo) #buscarPAnterior del vehiculo registrado en la bd
    for i in range(len(zonasMonitoreadas)):
        Zona            = zonasMonitoreadas[i]
        idMZona         = Zona[0]
        latitudMZona    = Zona[1]
        longitudMZona   = Zona[2]
        radioMZona      = Zona[3]
        puntoInicial    =   (float(latitudVehiculo), float(longitudVehiculo))
        puntoFinal      =   (float(latitudMZona), float(longitudMZona)) 
        distanciaMetros = vincenty(puntoInicial, puntoFinal).meters
        if distanciaMetros <= float(radioMZona): #esta en zona
            if docPuntoAnterior != None: #si existe anterior
                #la zona detectada existe?
                docIdZonaDetectada =   zonaDetectadaExiste(peticion, idMZona, docPuntoAnterior)
                if docIdZonaDetectada != None: # si existe la zona detectada
                    puntoZonaAlarma.append(docIdZonaDetectada)
                else: #si no existe la zona detectada
                    #crear za
                    horaInicioZonaAlarma    = horaRegistrada
                    doc_idZonaAlarma = crearZonaAlarma(peticion, horaInicioZonaAlarma, horaFinZonaAlarma, estado, idMZona, idVehiculo)
                    puntoZonaAlarma.append(doc_idZonaAlarma)
            else: # si no existe anterior
                #Crear zona
                horaInicioZonaAlarma    = horaRegistrada
                doc_idZonaAlarma =crearZonaAlarma(peticion, horaInicioZonaAlarma, horaFinZonaAlarma, estado, idMZona, idVehiculo)
                puntoZonaAlarma.append(doc_idZonaAlarma)
    if docPuntoAnterior != None:
        verificarPuntosContinuaZonaAlarma(peticion, docPuntoAnterior, puntoZonaAlarma)           
    return puntoZonaAlarma

#-----------------------------------------------------------------------------------------
#busca las zonas monitoreadas en la base de datos

def buscarMonitoreoZonas(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    zonasMonitoreadas = []

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/vigilancias/_view/monitoreoZonas',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          idMZona       =   doc.get('_id')
          latitudMZona  =   doc.get('latitud')
          longitudMZona =   doc.get('longitud')
          radioMZona    =   doc.get('radio') 
          zonasMonitoreadas.append([idMZona, latitudMZona, longitudMZona, radioMZona])        
        return zonasMonitoreadas
    except ValueError:
        pass
    return { 'success' : False}

#=====================================================================================
def evaluarHora(horaInicio, horaFin, hora):
    numHoraInicio       = int(horaInicio[:2])
    numMinInicio        = int(horaInicio[3:5])
    numHoraFin          = int(horaFin[:2])
    numMinFin           = int(horaFin[3:5])
    numhoraRegistrada   = int(hora[:2])
    numMinRegistrada    = int(hora[3:5])
    horaEncontrada      = False
    conteoHora          = numHoraInicio
    conteoMinuto        = numHoraFin
    continuarevaluacion = True
    while continuarevaluacion:
        if conteoMinuto == 60:
            conteoMinuto = 0
            conteoHora   +=1         
        if conteoHora == numhoraRegistrada and conteoMinuto == numMinRegistrada:
            horaEncontrada      = True
            continuarevaluacion = False
        if conteoHora == numHoraFin and conteoMinuto == numMinFin:
            horaEncontrada      = False
            continuarevaluacion = False
        conteoMinuto     += 1
    return horaEncontrada

#Inicio  busqueda posiciones de la programacion vigilancia
def puntosEstaEnProgramacionVigilancia(peticion, idVehiculo, horaRegistrada):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    hora            = horaRegistrada[11:16] #solo la hora de hora registrada
    programacionVigilancias = []
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        filas = db.view('_design/consultarRangoFechasAlarmas/_view/consultarRangoFechasAlarmas',
                    include_docs  = True,
                    key=[horaRegistrada[:10],idVehiculo])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          idDocProgramacionVigilancia   =   doc.get('_id')
          horaInicio                    =   doc.get('horaInicio')
          horaFin                       =   doc.get('horaFin')
          horaEncontrada                =   evaluarHora(horaInicio, horaFin, hora)
          if horaEncontrada:
            programacionVigilancias.append(idDocProgramacionVigilancia)
        return programacionVigilancias
    except ValueError:
        pass
    return { 'success' : False}


#////Fin busqueda busqueda de la programacion vigilancia
#=====================================================================================

#===================================================================================
#=============== Inicio para guardar inspeccionImagen ===========================
def guardarDocInspeccionImagen(peticion, idVehiculo, zonaAlarmas, programacionVigilancia, identificadorGPS):
    #funcion que guarda el documento en la bd
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionFleet()
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:    
        doc_id, doc_rev = db.save({
            "tipoDato"                  :   "inspeccionImagen",
            "fechaHoraSolicitud"        :   datetime.now().isoformat(), 
            "estado"                    :   "pendiente",
            "identificadorGPS"          :   identificadorGPS,
            "idVehiculo"                :   idVehiculo,
            "esDirecta"                 :   False,
            "esPanico"                  :   False, 
            "idZona"                    :   zonaAlarmas,
            "idVigilancia"              :   programacionVigilancia,
            "idPanico"                  :   "",
            "activo"                    :   True,
            "tenant"                    :   tenant
        })
        return doc_id
        #Llamar Ws que ssolicitara al GPS la captura de la imagen
    except ValueError:
        pass
#==============  Fin para guardar inspeccionImagen ===============================
#-------------------------Inicio para evaluar zona alarmas--------------------
def buscarZonaAlarma(peticion, idZonaAlarma):
    autenticacion       = peticion['autenticacion']
    usuario             = autenticacion['usuario']
    tenant              = autenticacion['tenant']
    db                  = conexion.getConexionTenant(tenant)
    docZonaAlarma       = db[idZonaAlarma]
    idZona              = docZonaAlarma["idZona"] 
    docMonitoreoZona    = db[idZona]
    return docMonitoreoZona 


def obtenerTipoCapturaZona(docMonitoreoZona):
    registrarImagen     = docMonitoreoZona["registrarImagen"]
    registrarAudio      = docMonitoreoZona["registrarAudio"]
    if registrarImagen == True and registrarAudio == False:
        return "registrarImagen"
    if registrarImagen == False and registrarAudio == True:
        return "registrarAudio"
    if registrarImagen == True and registrarAudio == True:
        return "ambasCapturas"

def verificarTomarFotoZonaAlarma(docMonitoreoZonas):
    tomaFoto = False
    print "-------------------------------------------------------------------"
    print docMonitoreoZonas
    numeroCapturasMax = docMonitoreoZonas.get('numeroCapturasMax')
    if numeroCapturasMax == "":
        numeroCapturasMax = settings.CANT_FOTOS_A_TOMAR
    contadorFotosTomadas = docMonitoreoZonas.get('contadorFotosTomadas')
    if contadorFotosTomadas <=  int(numeroCapturasMax):
        tomaFoto = True
    else:
        tomaFoto = False
    return tomaFoto


def evaluarTipoCapturaZonaAlarmas(peticion, idVehiculo, zonaAlarmas, identificadorGPS):
    #sirven para identificar que tipo de recurso se va a guardar "imagenes, audios o ambas"
    fotosZonaAlarma     = []
    audiosZonaAlarma    = []
    resultados          = ["",[],""]
    if zonaAlarmas != None:
        for i in range(len(zonaAlarmas)):
            idZonaAlarma = zonaAlarmas[i]
            docMonitoreoZonas = buscarZonaAlarma(peticion, idZonaAlarma)
            tipoCaptura = obtenerTipoCapturaZona(docMonitoreoZonas)
            if tipoCaptura == "registrarImagen":
                tomaFoto = verificarTomarFotoZonaAlarma(docMonitoreoZonas)
                if tomaFoto:
                    fotosZonaAlarma.append(idZonaAlarma)
            if tipoCaptura == "registrarAudio":
                # para guardar la captura de audio
                audiosZonaAlarma.append(idZonaAlarma)
            if tipoCaptura == "ambasCapturas":
                #Nota: falta----
                tomaFoto = verificarTomarFotoZonaAlarma(docMonitoreoZonas)
                if tomaFoto:
                    fotosZonaAlarma.append(idZonaAlarma)
                audiosZonaAlarma.append(idZonaAlarma)
    if fotosZonaAlarma != [] and audiosZonaAlarma != []:
        #para guardar en documento Audio para alarma e inspeccionImagen
        resultados[0] = "guardarImagenAudio"
        resultados[1] = fotosZonaAlarma 
        resultados[2] = audiosZonaAlarma
        return resultados
    else:
        if fotosZonaAlarma != []:
            #sirve para identificar que se guardara en el doc inspeccion imagen
            resultados[0] = "guardarImagen"
            resultados[1] = fotosZonaAlarma 
            resultados[2] = []
            return resultados
        else:  
            if audiosZonaAlarma != []:
                #para registrar en el documento guardarDocInspeccionAudio
                resultados[0] = "guardarAudio"
                resultados[1] = [] 
                resultados[2] = audiosZonaAlarma
                return resultados
            else:
                return resultados
#-------------------------Fin para evaluar zona alarmas--------------------

#-------------------------Inicio para evaluar programacion vigilancia--------------------
def buscarProgramacionVig(peticion, idProgramacionVigilancia):
    autenticacion               = peticion['autenticacion']
    usuario                     = autenticacion['usuario']
    tenant                      = autenticacion['tenant']
    db                          = conexion.getConexionTenant(tenant)
    docProgramacionVigilancia   = db[idProgramacionVigilancia]
    return docProgramacionVigilancia


def obtenerTipoCapturaProgramacionVig(docProgramacionVigilancia):
    registrarImagen     = docProgramacionVigilancia["registrarImagen"]
    registrarAudio      = docProgramacionVigilancia["registrarAudio"]
    if registrarImagen == True and registrarAudio == False:
        return "registrarImagen"
    if registrarImagen == False and registrarAudio == True:
        return "registrarAudio"
    if registrarImagen == True and registrarAudio == True:
        return "ambasCapturas"

def verificarTomarFotoProgramacionVig(docProgramacionVigilancia):
    tomaFoto = False
    numeroCapturasMax = docProgramacionVigilancia.get('capturasMax')
    contadorFotosTomadas = docProgramacionVigilancia.get('contadorFotosTomadas')
    if contadorFotosTomadas <=  int(numeroCapturasMax):
        tomaFoto = True
    else:
        tomaFoto = False
    return tomaFoto


def evaluarTipoCapturaProgramacionVigilancia(peticion, idVehiculo, programacionVigilancia, identificadorGPS):
    #sirven para identificar que tipo de recurso se va a guardar "imagenes, audios o ambas"
    fotosProgramacionVigilancia     = []
    audiosProgramacionVigilancia    = []
    resultados          = ["",[],""]
    if programacionVigilancia != None:
        for i in range(len(programacionVigilancia)):
            idProgramacionVigilancia   = programacionVigilancia[i]
            docProgramacionVigilancia = buscarProgramacionVig(peticion, idProgramacionVigilancia)
            tipoCaptura = obtenerTipoCapturaProgramacionVig(docProgramacionVigilancia)            
            if tipoCaptura == "registrarImagen":
                tomaFoto = verificarTomarFotoProgramacionVig(docProgramacionVigilancia)
                if tomaFoto:
                    fotosProgramacionVigilancia.append(idProgramacionVigilancia)
            if tipoCaptura == "registrarAudio":
                # a partir de aqui es para guardar en el el audio----
                audiosProgramacionVigilancia.append(idProgramacionVigilancia)
            if tipoCaptura == "ambasCapturas":
                #Nota: falta----
                tomaFoto = verificarTomarFotoProgramacionVig(docProgramacionVigilancia)
                if tomaFoto:
                    fotosProgramacionVigilancia.append(idProgramacionVigilancia)
                audiosProgramacionVigilancia.append(idProgramacionVigilancia)
    if fotosProgramacionVigilancia != [] and audiosProgramacionVigilancia != []:
        #para guardar en documento InspeccionAudio e inspeccionImagen
        resultados[0] = "guardarImagenAudio"
        resultados[1] = fotosProgramacionVigilancia 
        resultados[2] = audiosProgramacionVigilancia
        return resultados
    else:
        if fotosProgramacionVigilancia != []:
            #sirve para identificar que se guardara en el doc inspeccion imagen
            resultados[0] = "guardarImagen"
            resultados[1] = fotosProgramacionVigilancia 
            resultados[2] = []
            return resultados  
        else:
            if audiosProgramacionVigilancia != []:
                #para registrar en el documento guardarDocInspeccionAudio
                resultados[0] = "guardarAudio"
                resultados[1] = [] 
                resultados[2] = audiosProgramacionVigilancia
                return resultados
            else:
                return resultados


#-------------------------Fin para evaluar programacion vigilancia-----------------------
#===================================================================================
def crearPosicionVehiculo(peticion,horaRegistrada, latitud, longitud, velocidad, idVehiculo, estado, ultimaPosicion, zonaAlarmas, programacionVigilancia, estaEncendidoMotor, dataTraccar):
    autenticacion = peticion['autenticacion']
    dataJson      = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    #print horaRegistrada
    fechaParse = parser.parse(horaRegistrada).astimezone(settings.EST).isoformat()[0:19]
    #print fechaParse
    if db == None:
        return { 'success' : False }
    try: 

        # posiciones = dataJson.get("posiciones",[])
        # estaMotorEncendido = True
        # for posicion in posiciones:
        #     estaMotorEncendido = posicion.get("estaMotorEncendido",True)
            
        doc_id, doc_rev = db.save({
            "tipoDato"      : "posicionVehiculos",
            "creadoEn"      : datetime.now().isoformat(),  
            "modificadoEn"  : datetime.now().isoformat(),
            "modificadoPor" : "GPS",
            "horaRegistrada": fechaParse,
            #"horaRegistrada": "2016-10-13T17:19",
            "horaRecibida"  : datetime.now().isoformat(),
            "latitud"       : latitud,
            "longitud"      : longitud,
            "velocidad"     : velocidad,
            "idVehiculo"    : idVehiculo,
            "estado"        : estado,
            "ultimaPosicion": ultimaPosicion,
            "zonaAlarmas"   : zonaAlarmas,
            "programacionVigilancia" : programacionVigilancia,
            "activo"        : True,
            "idParada"      :   "",
            "idFragmentoParada"   :   "",
            "estaEncendidoMotor"  : estaEncendidoMotor,
            "dataTraccar"         : dataTraccar    
        })
        return doc_id
    except ValueError:
        print "error"


def modificarEstadoUltimaPosicion(peticion, idVehiculo):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        filas = db.view('_design/posicionVehiculos/_view/ultimaPosicionGuardada',
                    include_docs  = True,
                    key      = [True, idVehiculo])
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          doc["ultimaPosicion"] = False
          #logging.warning(fila)
          db.save(doc)
    except ValueError:
        print "Error modificarEstadoUltimaPosicion"



#Inicio ws principal
def registrarPosicionesGPS(peticion):
    logging.warning("Regstrar posiciones gps")
    datos = peticion['data']
    idBdCreadosPosicionVehiculos=[]
    zonaAlarmas = None
    programacionVigilancia = None
    try:   
        posiciones          = datos["posiciones"]
        identificadorGPS    = datos["identificadorGPS"] 
        #se consulta el id del vehiculo
        idVehiculo          = obteneridVehiculo(identificadorGPS)
        tenantVehiculo      = obtenerTenantVehiculo(identificadorGPS)
        peticion["autenticacion"]["tenant"] = tenantVehiculo
        if idVehiculo != "":
            cantPosiciones      = len(posiciones)
            ultimaPosicion      = False
            estado              = "inactivo"
            i = 0
            cantPosiciones      = len(posiciones)
            ultimaPosicion      = False
            estado              = "inactivo"
            zonasMonitoreadas = buscarMonitoreoZonas(peticion)
            for posicion in posiciones:
                latitud             = posicion["latitud"]
                longitud            = posicion["longitud"]
                horaRegistrada      = posicion["horaRegistrada"]
                horaRegistrada      = parser.parse(horaRegistrada).astimezone(settings.EST).isoformat()
                velocidad           = posicion["velocidad"]
                dataTraccar         = posicion["dataTraccar"]
                estaEncendidoMotor  = posicion["estaMotorEncendido"]
                #estaEncendidoMotor  = False #variable para saber si el motor esta encendido(True) o apagado(False)
                i +=1
                if i == cantPosiciones:
                    estado = "activo"
                    ultimaPosicion = True
                zonaAlarmas = puntosEstaEnZona(peticion, idVehiculo, latitud, longitud, horaRegistrada, zonasMonitoreadas)
                #print "puntos zonas a guardar --"
                #print zonaAlarmas
                programacionVigilancia = puntosEstaEnProgramacionVigilancia(peticion, idVehiculo, horaRegistrada)
                # si hay una programacion vigilacia o una zonaAlarma
                if zonaAlarmas != None or programacionVigilancia != None:
                    #resEvalCapturaZonaAlarma[0] # en esta posicion guarda el concepto a guardar, 
                    #ya sea guardarImagen, guardarAudio guardarImagenAudio
                    #resEvalCapturaZonaAlarma[1] # identificadores de la zona alarma donde se registraran las fotos 
                    #resEvalCapturaZonaAlarma[2] = ## identificadores de la zona alarma donde se registraran las fotos
                    # De la misma forma se tratara a resEvalCapturaProgramacion como resEvalCapturaZonaAlarma
                    resEvalCapturaZonaAlarma = evaluarTipoCapturaZonaAlarmas(peticion, idVehiculo, zonaAlarmas, identificadorGPS)
                    resEvalCapturaProgramacion = evaluarTipoCapturaProgramacionVigilancia(peticion, idVehiculo, programacionVigilancia, identificadorGPS)

                    if resEvalCapturaZonaAlarma[0] == "guardarImagen" or resEvalCapturaProgramacion[0] == "guardarImagen":
                        # solicitaTomarFotoZonaAlarma() if true solicitarTomarFoto else no
                        solicitaTomarFotoZA = solicitaTomarFotoZonaAlarma(peticion, idVehiculo, identificadorGPS, zonaAlarmas)
                        #verifica si se puede tomar fotos segun la programacion vigilancia
                        solicitaTomarFotoPV = solicitaTomarFotoProgramacionVigilancia(peticion, idVehiculo, identificadorGPS, programacionVigilancia)    
                        #================================================================================================================
                        #if solicitaTomarFotoZA and not(solicitaTomarFotoPV):
                            #TomarFoto ZA
                        #    idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, resEvalCapturaZonaAlarma[1], [], identificadorGPS)
                        #    rutaCreacion = settings.GPS_RUTA_FOTO
                        #    solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)

                        if solicitaTomarFotoZA and resEvalCapturaProgramacion[0] != "guardarImagen":
                            #TomarFoto ZA
                            idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, resEvalCapturaZonaAlarma[1], [], identificadorGPS)
                            rutaCreacion = settings.GPS_RUTA_FOTO
                            solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)
                        
                        #if solicitaTomarFotoPV and not(solicitaTomarFotoZA):
                            #Tomar foto PV
                        #    idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, [], resEvalCapturaProgramacion[1], identificadorGPS)
                        #    rutaCreacion = settings.GPS_RUTA_FOTO
                        #    solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)

                        if resEvalCapturaProgramacion[0] == "guardarImagen":
                            #Tomar foto PV
                            for i in range(settings.TOMAR_N_FOTOS_PV):
                                idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, [], resEvalCapturaProgramacion[1], identificadorGPS)
                                rutaCreacion = settings.GPS_RUTA_FOTO
                                solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)

                        #if solicitaTomarFotoZA and solicitaTomarFotoPV:
                            #permite tomar la foto porque el numero max de la zona es menor a las tomadas
                        #    idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, resEvalCapturaZonaAlarma[1], resEvalCapturaProgramacion[1], identificadorGPS)
                        #    rutaCreacion = settings.GPS_RUTA_FOTO
                        #    solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)
                        #================================================================================================================
                    #--- Inicio condiciones para guardar el audio de las llamadas para la zona alarma y para la programacion vigilancia---
                    if resEvalCapturaZonaAlarma[0] == "guardarAudio":
                        #-------------------------------------------------------------
                        #Inicio Guardar Audio ZA
                        #Si existe una llamada en curso de la programacion vigilancia 
                        #entonces se guarda el id de la llamada de la PV como una llamada
                        #de ZA y se actualiza el limite
                        #--FALTA : SABER SI UNA LLAMADA DEL BOTON DE PANICO ESTA EN CURSO----
                        llamadaPV = verificarLlamadaProgramacionVigilancia(peticion, idVehiculo)      
                        #if not(llamadaPV['EnCurso'] or llamadaBotonPanico)
                        if not(llamadaPV['EnCurso']): #Si no hay llamada PV en curso
                            #---------------------------------------------------------------
                            #Funcion para verificar si solicita llamar o no en la zona Alarma debido 
                            #a que ya a llamado y cumplio el limite
                            #resEvalCapturaZonaAlarma[2]= Identificadores de la Zona Alarma
                            #verificar en el doc capturaAudioZonaAlarma si el estado esta estado="Finalizado"
                            # Si esta finalizado no volver a llamar crear una vista que consulte con el campo ZonaAlarma
                            llamadaZonaAlarmaEjecutada = verificarLlamadaZAEjecutada(peticion, idVehiculo, zonaAlarmas) 
                            if not(llamadaZonaAlarmaEjecutada):
                                #----------------------------------------------------------------
                                #llamada actual de la zona alarma
                                llamadaEnCurso = verificarLlamadaEnCursoZA(peticion, idVehiculo)
                                # Si no hay llamada actual zona alarma y reingreso a la zona entonces llamar
                                if not(llamadaEnCurso["estado"]):
                                    # se hara llamada y se guardara en el documento capturaAudioZonaAlarma
                                    try:
                                        ejecutarAudioZonaAlarma(peticion, latitud, longitud, horaRegistrada, idVehiculo, zonaAlarmas)# llama a la funcion ejecutarAudioZonaAlarma de audios.py
                                    except:
                                        print "Saldo insuficiente para hacer la llamada zona alarma"
                                #else:
                                    #verifica el limite de la llamada y actualiza con el mayor y le enviamos llamadaEncurso
                                #    print "Se debe verificar el limite de la llamada y actualizarlo con el mayor y le enviamos llamadaEncurso"
                                #    print llamadaEnCurso
                                    #pendiente:Por el momento parece que funciona bien
                                    #actualizarLimiteLlamadaZAEnCurso(peticion, idVehiculo, llamadaEnCurso, resEvalCapturaZonaAlarma[2])
                        else:
                            #Actualizo el limite mayor de la llamada con el identificador de la llamada de la PV
                            # o de las zonas alarmas y creo una capturaAudioZonaAlarma con los datos de la PV
                            #Antes de crear el doc ZA verificar si existe una capturaAudioZonaAlarma creada
                            existeDoccapturaAudioZonaAlarmaCreada = verificarDoccapturaAudioZonaAlarmaCreada(peticion, idVehiculo, llamadaPV["idLlamada"])
                            if not(existeDoccapturaAudioZonaAlarmaCreada):
                                limiteMayor = obtenerLimiteMayorZonaAlarmas(peticion,zonaAlarmas, llamadaPV["limite"])
                                #guarda en el doc capturaAudioZonaAlarma
                                guardarLlamadaSimultaneaZA(peticion,llamadaPV, idVehiculo, latitud, longitud, zonaAlarmas, limiteMayor)
                                #actualiza la razon de la llamada a zonaAlarmaProgramacionVigilancia y el limite de la llamada
                                # al doc llamadas
                                actualizarDocLLamadasRazonLimite(peticion, llamadaPV, limiteMayor)
                        #Fin Guardar Audio ZA
                        #---------------------------------------------------------------------
                    if resEvalCapturaProgramacion[0] == "guardarAudio": #programacion vigilancia
                    #---Inicio llamadas PV    
                        # se hara llamada y se guardara en el documento audioProgramacionVigilancia
                        #----------------------------------------
                        #NOTA: Incorporar.Si existe una llamada en curso de la Zona alarma 
                        #entonces se guarda el id de la llamada de la ZA como una llamada
                        #de PV y se actualiza el limite si es mayor antes de que se haga la llamada
                        #----------------------------------------
                        #FALTA: VERIFICAR SI HAY UNA LLAMADA BOTON DE PANICO
                        #if not(llamadaZA['EnCurso'] or llamadaBotonPanico) 
                        #editando pendiente
                        activoProgramacionVigilancia = puedoUsarPV(peticion, idVehiculo, horaRegistrada, programacionVigilancia)
                        if not(activoProgramacionVigilancia):
                            llamadaZA = verificarLlamadaZonaAlarma(peticion, idVehiculo)
                            if not(llamadaZA['EnCurso']): #Si no hay llamada ZA en curso
                                #llamadaProgramacionVigilanciaEjecutada = verificarLlamadaPVEjecutada(peticion, idVehiculo, resEvalCapturaProgramacion[2]) 
                                #print "##############"
                                #print llamadaProgramacionVigilanciaEjecutada
                                #print "##############"
                                #if not(llamadaProgramacionVigilanciaEjecutada):
                                #----------------------------------------------------------------
                                #llamada actual de la programacion vigilancia
                                llamadaEnCursoPV = verificarLlamadaEnCursoPV(peticion, idVehiculo)
                                # Si no hay llamada actual programacion vigilancia
                                if not(llamadaEnCursoPV["estado"]):
                                    try:
                                        ejecutarAudioProgramacionVigilancia(peticion, latitud, longitud, horaRegistrada, idVehiculo, programacionVigilancia)
                                    except:
                                        print "Saldo insuficiente para hacer la llamada programacion vigilancia"           
                            else:
                                existeDocaudioProgramacionVigilancia = verificarDocaudioProgramacionVigilancia(peticion, idVehiculo, llamadaZA["idLlamada"])
                                if not(existeDocaudioProgramacionVigilancia):
                                    #VERIFICA EL LIMITE DE LA LLAMADA MAXIMA PV#
                                    limiteMayor = obtenerLimiteMayorProgramacion(peticion,programacionVigilancia, idVehiculo, llamadaZA["limite"])
                                    #guarda en el doc capturaAudioZonaAlarma
                                    guardarLlamadaSimultaneaPV(peticion,llamadaZA, idVehiculo, latitud, longitud, programacionVigilancia, limiteMayor)
                                    actualizarDocLLamadasRazonLimite(peticion, llamadaZA, limiteMayor)
                            #funcion que guarda la programacion vigilancia como ejecutada
                            guardarProgramacionVigilanciaComoEjecutada(peticion,horaRegistrada, programacionVigilancia, idVehiculo)
                    #---Fin llamadas PV
                    # Si el vehiculo sale de las zonas alarmas terminar llamada
                    #si el nuevo punto no esta en ninguna zona alarma terminar la que se esta ejecutando
                    if resEvalCapturaZonaAlarma[0] != "guardarAudio" and resEvalCapturaZonaAlarma[0] != "guardarImagenAudio": #zona alarmas
                        #sale de la zona alarma
                        llamadaEnCursoZA = verificarLlamadaEnCursoZA(peticion, idVehiculo)
                        #print "LA LLAMADA ESTA EN CURSO"
                        #print llamadaEnCurso
                        #Terminar llamada si tiene una en curso
                        #pasar el id del vehiculo y verificar si esta en curso alguna llamada
                        if llamadaEnCursoZA["estado"]:
                            #OJO FALTA GUARDAR LA URL AUDIO
                            print "-------------------------------"
                            print llamadaEnCursoZA
                            terminarLlamadaSaleZonaAlarma(peticion, idVehiculo, llamadaEnCursoZA) # llama a la funcion terminarLlamadaSaleZonaAlarma de audios.py
                        #--- Fin condiciones para guardar el audio de las llamadas para la zona alarma y para la programacion vigilancia---
                        #--- Inicio condiciones para guardar imagen y audio de la zona alarma y de la programacion vigilancia---
                    if resEvalCapturaZonaAlarma[0] == "guardarImagenAudio": #zona alarmas
                        # solicitaTomarFotoZonaAlarma() if true solicitarTomarFoto else no
                        solicitaTomarFotoZA = solicitaTomarFotoZonaAlarma(peticion, idVehiculo, identificadorGPS, zonaAlarmas)
                        #================================================================================================================
                        if solicitaTomarFotoZA:
                            #TomarFoto ZA
                            idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, resEvalCapturaZonaAlarma[1], [], identificadorGPS)
                            rutaCreacion = settings.GPS_RUTA_FOTO
                            
                            solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)                  
                        #-------------------------------------------------------------
                        #Inicio Guardar Audio ZA
                        #Si existe una llamada en curso de la programacion vigilancia 
                        #entonces se guarda el id de la llamada de la PV como una llamada
                        #de ZA y se actualiza el limite
                        #--FALTA : SABER SI UNA LLAMADA DEL BOTON DE PANICO ESTA EN CURSO----
                        llamadaPV = verificarLlamadaProgramacionVigilancia(peticion, idVehiculo)      
                        #if not(llamadaPV['EnCurso'] or llamadaBotonPanico)
                        if not(llamadaPV['EnCurso']): #Si no hay llamada PV en curso
                            #---------------------------------------------------------------
                            #Funcion para verificar si solicita llamar o no en la zona Alarma debido 
                            #a que ya a llamado y cumplio el limite
                            #resEvalCapturaZonaAlarma[2]= Identificadores de la Zona Alarma
                            #verificar en el doc capturaAudioZonaAlarma si el estado esta estado="Finalizado"
                            # Si esta finalizado no volver a llamar crear una vista que consulte con el campo ZonaAlarma
                            llamadaZonaAlarmaEjecutada = verificarLlamadaZAEjecutada(peticion, idVehiculo, zonaAlarmas) 
                            if not(llamadaZonaAlarmaEjecutada):
                                #----------------------------------------------------------------
                                #llamada actual de la zona alarma
                                llamadaEnCurso = verificarLlamadaEnCursoZA(peticion, idVehiculo)
                                # Si no hay llamada actual zona alarma y reingreso a la zona entonces llamar
                                if not(llamadaEnCurso["estado"]):
                                    # se hara llamada y se guardara en el documento capturaAudioZonaAlarma
                                    try:
                                        ejecutarAudioZonaAlarma(peticion, latitud, longitud, horaRegistrada, idVehiculo, zonaAlarmas)# llama a la funcion ejecutarAudioZonaAlarma de audios.py
                                    except:
                                        print "Saldo insuficiente para hacer la llamada zona alarma"
                                #else:
                                    #verifica el limite de la llamada y actualiza con el mayor y le enviamos llamadaEncurso
                                #    print "Se debe verificar el limite de la llamada y actualizarlo con el mayor y le enviamos llamadaEncurso"
                                #    print llamadaEnCurso
                                    #pendiente:Por el momento parece que funciona bien
                                    #actualizarLimiteLlamadaZAEnCurso(peticion, idVehiculo, llamadaEnCurso, resEvalCapturaZonaAlarma[2])
                        else:
                            #Actualizo el limite mayor de la llamada con el identificador de la llamada de la PV
                            # o de las zonas alarmas y creo una capturaAudioZonaAlarma con los datos de la PV
                            #Antes de crear el doc ZA verificar si existe una capturaAudioZonaAlarma creada
                            existeDoccapturaAudioZonaAlarmaCreada = verificarDoccapturaAudioZonaAlarmaCreada(peticion, idVehiculo, llamadaPV["idLlamada"])
                            if not(existeDoccapturaAudioZonaAlarmaCreada):
                                limiteMayor = obtenerLimiteMayorZonaAlarmas(peticion,zonaAlarmas, llamadaPV["limite"])
                                #guarda en el doc capturaAudioZonaAlarma
                                guardarLlamadaSimultaneaZA(peticion,llamadaPV, idVehiculo, latitud, longitud, zonaAlarmas, limiteMayor)
                                #actualiza la razon de la llamada a zonaAlarmaProgramacionVigilancia y el limite de la llamada
                                # al doc llamadas
                                actualizarDocLLamadasRazonLimite(peticion, llamadaPV, limiteMayor)
                        #Fin Guardar Audio ZA
                        #---------------------------------------------------------------------
                    if resEvalCapturaProgramacion[0] == "guardarImagenAudio": # Programacion vigilancia
                        #verifica si se puede tomar fotos segun la programacion vigilancia
                        #solicitaTomarFotoPV = solicitaTomarFotoProgramacionVigilancia(peticion, idVehiculo, identificadorGPS, programacionVigilancia)      
                        #if solicitaTomarFotoPV:
                            #Tomar foto PV
                        #    idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, [], resEvalCapturaProgramacion[1], identificadorGPS)
                        #    rutaCreacion = settings.GPS_RUTA_FOTO
                        #    solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)

                        for i in range(settings.TOMAR_N_FOTOS_PV):
                            #Tomar foto PV
                            idFoto = guardarDocInspeccionImagen(peticion, idVehiculo, [], resEvalCapturaProgramacion[1], identificadorGPS)
                            rutaCreacion = settings.GPS_RUTA_FOTO
                            #DESCOMENTAR
                            solicitarTomarFoto(idFoto, rutaCreacion, identificadorGPS)
                            
                        activoProgramacionVigilancia = puedoUsarPV(peticion, idVehiculo, horaRegistrada, programacionVigilancia)
                        if not(activoProgramacionVigilancia):
                            llamadaZA = verificarLlamadaZonaAlarma(peticion, idVehiculo)
                            if not(llamadaZA['EnCurso']): #Si no hay llamada ZA en curso
                                #llamadaProgramacionVigilanciaEjecutada = verificarLlamadaPVEjecutada(peticion, idVehiculo, resEvalCapturaProgramacion[2]) 
                                #print "##############"
                                #print llamadaProgramacionVigilanciaEjecutada
                                #print "##############"
                                #if not(llamadaProgramacionVigilanciaEjecutada):
                                #----------------------------------------------------------------
                                #llamada actual de la programacion vigilancia
                                llamadaEnCursoPV = verificarLlamadaEnCursoPV(peticion, idVehiculo)
                                # Si no hay llamada actual programacion vigilancia
                                if not(llamadaEnCursoPV["estado"]):
                                    try:
                                        ejecutarAudioProgramacionVigilancia(peticion, latitud, longitud, horaRegistrada, idVehiculo, programacionVigilancia)
                                    except:
                                        print "Saldo insuficiente para hacer la llamada programacion vigilancia"           
                            else:
                                existeDocaudioProgramacionVigilancia = verificarDocaudioProgramacionVigilancia(peticion, idVehiculo, llamadaZA["idLlamada"])
                                if not(existeDocaudioProgramacionVigilancia):
                                    #VERIFICA EL LIMITE DE LA LLAMADA MAXIMA PV#
                                    limiteMayor = obtenerLimiteMayorProgramacion(peticion,programacionVigilancia, idVehiculo, llamadaZA["limite"])
                                    #guarda en el doc capturaAudioZonaAlarma
                                    guardarLlamadaSimultaneaPV(peticion,llamadaZA, idVehiculo, latitud, longitud, programacionVigilancia, limiteMayor)
                                    actualizarDocLLamadasRazonLimite(peticion, llamadaZA, limiteMayor)
                            #funcion que guarda la programacion vigilancia como ejecutada
                            guardarProgramacionVigilanciaComoEjecutada(peticion,horaRegistrada, programacionVigilancia, idVehiculo)
                    #---Fin llamadas PV


                    #--- Fin condiciones para guardar imagen y audio de la zona alarma y de la programacion vigilancia---
                # A partir de esta linea se evaluan las paradas  de un vehiculo
                #Inicio evaluar paradas de un vehiculo
                #La funcion evaluarParadas se encuentra en el archivo paradas.py
                datos = evaluarParadas(peticion, latitud, longitud, idVehiculo, horaRegistrada)
                #Fin evaluar paradas de un vehiculo
                #ojo Debo modificar el campo del vehiculo ultimaPosicion a false segun la fechaCreacion
                modificarEstadoUltimaPosicion(peticion, idVehiculo)# ojo verificar
                doc_idPosicionVehiculo = crearPosicionVehiculo(peticion,horaRegistrada, latitud, longitud, velocidad, idVehiculo, estado, ultimaPosicion, zonaAlarmas, programacionVigilancia, estaEncendidoMotor, dataTraccar)
                #Funcion para actualizar la parada y el fragmento parada del punto. esta en el archivo paradas.py
                actualizarPosicionVehiculoParadas(peticion, doc_idPosicionVehiculo, datos[0], datos[1])
                idBdCreadosPosicionVehiculos.append(doc_idPosicionVehiculo)
            return {
                'success' : True, 
                'data'    : {
                    'id' : idBdCreadosPosicionVehiculos
                }              
            }
            
    except BufferError:
        logging.warning("Registrar posiciones gps VELUES ERROR")
        pass



    #----------------------------------------------------------------------

       
        
        
