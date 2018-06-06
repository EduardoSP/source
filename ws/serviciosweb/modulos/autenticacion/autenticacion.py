# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion              import conexion
from datetime                 import datetime
import smtplib
import couchdb
from  ws.serviciosweb.modulos.notificaciones.notificaciones import notificarTenant, notificarAlertaSeguridad
from  ws.serviciosweb.modulos.geocoderFleet.geocoderFleet   import getLatLngDireccionIp
from geopy.distance import vincenty

def autenticar( peticion ):
    usuario     = peticion['usuario']
    accion      = peticion['accion']
    tenant      = peticion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return {
            'success' : False,
            "mensaje" : "No existe el tenant"
        }

    if accion == 'ingresar':
        contrasena  = salarConMd5(peticion['contrasena'])
        logging.warning(contrasena)
        filas = db.view('_design/usuarios/_view/usuariosPorContrasena',
                    include_docs  = True,
                    startkey      = [usuario,contrasena,0],
                    endkey        = [usuario,contrasena,{}],
                    limit         = 1)        
        for fila in filas:
            doc   = fila.doc
            llave = fila.key
            token = uuid.uuid4().hex
                        
            doc_id, doc_rev = db.save({
                "tipoDato"		: "autenticacion",
                "activo"		: True,
                "creadoEn"		: datetime.now().isoformat(),
                "loginUsuario" 	: usuario,
                "token"         : token
            })
            return {
                'success' : True,
                'token'   : token,                 
                'usuario' : usuario,
                'perfil'  : llave[2],
                'tenant' : tenant
            }
        return { 'success' : False, "mensaje" : "Usuario o contraseña incorrecta"  }
    elif accion == 'cerrar' :
        token = peticion['token']
        filas = db.view('_design/autenticaciones/_view/autenticacion',
                    include_docs  = True,
                    key      = [usuario,token],
                    limit         = 1)
        
        for fila in filas:
            doc   = fila.doc
            db.delete(doc)
            return { 'success' : True }
    
        
    return { 'success' : False, "mensaje" : "Error desconocido login"  }
 
#---------------------------------------------------------------

#Autenicar unificado solo aplica par ingreso
def autenticarUnificado( peticion ):
    usuario = peticion['usuario']
    accion  = peticion['accion']
    dbFleet = conexion.getConexionFleet()
    tipoSesion = ""
    tipoIngreso = peticion.get("tipoIngreso", "None")
    direccionIp = peticion.get("direccionIp", "")
    #direccionIp = "190.242.75.28" #bogota
    dispositivo = peticion.get("dispositivo", "")
    if accion == 'ingresar':
        #El login es por plataforma web
        if not(tipoIngreso == "None"):
            tipoSesion = tipoIngreso
            
            filasTenants = dbFleet.view(
                '_design/tenantPorTenant/_view/tenantPorTenant',
                include_docs  = False
            )

            listadoTenants = []
            
            for filaTenant in filasTenants:
                llave = filaTenant.key
                listadoTenants.append(llave[0])

            # listadoTenants = ["exxonmobil"]

            for tenant in listadoTenants:
                
                db = conexion.getConexionTenant(tenant)
                if db == None:
                    continue
                
                contrasena  = salarConMd5(peticion['contrasena'])            

                filas = db.view(
                    '_design/usuarios/_view/usuariosPorContrasena',
                    include_docs  = True,
                    startkey      = [usuario,contrasena, 0],
                    endkey        = [usuario,contrasena,{}],
                    limit         = 1 )
                
                for fila in filas:
                    doc   = fila.doc
                    llave = fila.key
                    #encontro el usuario entonces verifica si tiene la sesion activa segun el tipoIngreso
                    idUsuario       =   doc.get("_id", "")
                    sesion      = {}
                    datosVisita = {}
                    #verifica si una sesion esta activa
                    #sesion                  = verificarEstadoSesionUsuario(db, usuario, idUsuario, tipoSesion)
                    sesion                  = obtenerUltimaSesionUsuario(db, idUsuario, tipoSesion)
                    fechaHoraActualSesion   = datetime.now().isoformat()
                    #obtiene la latitud y longitud a partir de una direccion ip geocoderFleet
                    datosDireccion          = getLatLngDireccionIp(direccionIp, tipoSesion)
                    #Datos de la sesion anterior
                    datosSesionAnterior = {
                        "identificadorAnteriorSesion"   : sesion["identificadorSesion"],
                        "dispositivoAnteriorSesion"     : sesion["dispositivo"],
                        "fechaHoraAnteriorSesion"       : sesion["creadoEn"],
                        "direccionAnteriorSesion"       : sesion["direccionCompleta"],
                        "ciudadAnteriorSesion"          : sesion["ciudad"],
                        "latitudAnteriorSesion"         : sesion["latitud"],
                        "longitudAnteriorSesion"        : sesion["longitud"]
                    }                 
                    #Datos sesion actual
                    if direccionIp == "":
                         #peticion IOS y android 
                        identificadorActualSesion = peticion.get("idTelefono", "")
                    else:
                        #peticion navegador web
                        identificadorActualSesion = direccionIp

                    datosSesionActual ={
                        "identificadorActualSesion" : identificadorActualSesion,
                        "dispositivoActualSesion"   : dispositivo,
                        "fechaHoraActualSesion"     : fechaHoraActualSesion,
                        "direccionActualSesion"     : datosDireccion["direccionCompleta"],
                        "ciudadActualSesion"        : datosDireccion["ciudad"],
                        "latitudActualSesion"       : datosDireccion["latitud"],
                        "longitudActualSesion"      : datosDireccion["longitud"]
                    }
                    #Funcion que Verifica la sesion de multiples ciudades
                    multipleCiudad = verificarSesionMultiplesCiudades(db, tipoSesion, datosSesionAnterior, datosSesionActual)
                    if multipleCiudad and not sesion["validadoMultipleCiudad"] and tipoSesion == "fleetBiWeb":
                        #registra bd multiple ciudad con la plataforma web
                        guardarEnviarAlertaSesionBaseDatos(db, tenant, usuario, idUsuario, "Cliente", "fleetBiWeb", 
                                                            datosSesionAnterior, datosSesionActual, u"Multiple ciudad")
                        #actualizo a true que ha sido validada la multiple ciudad
                        actualizarEstadoMultipleCiudad(db, sesion["idSesion"])
                        #Notificar por corrreo
                    else:
                        #Ya registro la multiple ciudad con la sesion anterior
                        multipleCiudad = False
                    if not(sesion["sesionActiva"]) and not(multipleCiudad):
                        #No existe una sesion activa

                        #actualizo la ultima sesion activa
                        docAutenticacion                    = db[sesion["idSesion"]]
                        docAutenticacion['ultimaSesion']    = False
                        db.save(docAutenticacion)

                        token = uuid.uuid4().hex
                        docAutenticacion = {
                            "tipoDato"		        : "autenticacion",
                            "activo"		        : True,
                            "creadoEn"		        : fechaHoraActualSesion,
                            "loginUsuario" 	        : usuario,
                            "token"                 : token,
                            "tipoSesion"            : tipoSesion,
                            "idUsuario"             : idUsuario,
                            "identificadorSesion"   : identificadorActualSesion,
                            "dispositivo"           : dispositivo,
                            "latitud"               : datosDireccion["latitud"],
                            "longitud"              : datosDireccion["longitud"],
                            "direccionCompleta"     : datosDireccion["direccionCompleta"],
                            "ciudad"                : datosDireccion["ciudad"],
                            "ultimaSesion"          : True,
                            "validadoMultipleCiudad": False   
                        }

                        origen = peticion.get("origen", None)
                        idPush = peticion.get("idPush", None)
                        
                        if not origen == None and not idPush == None:
                            eliminarPush( db, idPush )
                            docAutenticacion["origen"] = origen
                            docAutenticacion["idPush"] = idPush
                            
                        doc_id, doc_rev = db.save( docAutenticacion )
                        return {
                            'success'   : True,
                            'token'     : token,                 
                            'usuario'   : usuario,
                            'perfil'    : llave[2],
                            'tenant'    : tenant,
                            'idUsuario' : idUsuario,
                            'idSesion'  : doc_id
                        }
                    else:
                        #existe una sesion activa entonces notifica, registra el evento en el sistema, cierra la sesion activa notificando el suceso, y redirige al login principal
                        #se actualiza el campo activo como False
                        if tipoSesion == "fleetBiWeb" and sesion["sesionActiva"]:
                            #si la solicitud es desde fleetBiWeb y la sesion esta activa
                            #envia alerta notier
                            notificarAlertaSeguridad(tenant, "seguridadAutenticacion", dispositivo, datetime.now().isoformat())
                            #actualizar el estado a false de la sesion actual para que se pueda realizar el nuevo ingreso
                            #luego de ser notificado al usuario
                            actualizarEstadoSesionActual(db, sesion["idSesion"])
                            guardarEnviarAlertaSesionBaseDatos(db, tenant, usuario, idUsuario, "Cliente", "fleetBiWeb", 
                                                            datosSesionAnterior, datosSesionActual, u"Sesión simultanea")
                            mensaje = "Ya existe una sesión activa se notificará en el sistema"
                            #notificar por correo
                        if tipoSesion == "fleetBiWeb" and multipleCiudad:
                            mensaje = "Sesión multiple ciudad se notificará al sistema"
                        if tipoSesion == "fleetBiWeb" and sesion["sesionActiva"] and multipleCiudad:
                            mensaje = "Ya existe una sesión activa y registra una multiple ciudad se notificará en el sistema"                    
                        return { 'success' : False, 
                                'mensaje' : mensaje,
                                'sesionActiva': True  }               
            #Si llego hasta acá, no existe el usuario
            return { 'success' : False, "mensaje" : "Usuario o contraseña incorrecta"  }
            
        return { 'success' : False, "mensaje" : "Error desconocido login"  }


def verificarSesionMultiplesCiudades(db, tipoSesion, datosSesionAnterior, datosSesionActual):
    multipleCiudad      = False
    if tipoSesion == "fleetBiWeb":
        puntoInicial        = (float(datosSesionAnterior["latitudAnteriorSesion"]), float(datosSesionAnterior["longitudAnteriorSesion"]))
        puntoFinal          = (float(datosSesionActual["latitudActualSesion"]), float(datosSesionActual["longitudActualSesion"]))
        distanciaMetros     =  vincenty(puntoInicial, puntoFinal).meters
        distanciaKilometros =  distanciaMetros/1000
        fechaHoraAnteriorSesion = datosSesionAnterior["fechaHoraAnteriorSesion"][:16]+"Z"
        fechaHoraActualSesion 	= datosSesionActual["fechaHoraActualSesion"][:16]+"Z"
        fechaHoraAnteriorSesion = datetime.strptime(fechaHoraAnteriorSesion, '%Y-%m-%dT%H:%MZ')
        fechaHoraActualSesion 	= datetime.strptime(fechaHoraActualSesion, '%Y-%m-%dT%H:%MZ')
        diferenciaHoras 		= fechaHoraActualSesion - fechaHoraAnteriorSesion
        minutos = diferenciaHoras.total_seconds() / 60
        cantidadHoras = float(minutos)/60
        velocidad = 0
        if not cantidadHoras == 0:
            velocidad = float(distanciaKilometros) / cantidadHoras
        if distanciaKilometros < 100:
            if (velocidad == 0 and not(distanciaKilometros == 0)) or velocidad > settings.VELOCIDAD_KM_H_AUTOMOVIL:
                multipleCiudad = True
        else:
            if (velocidad == 0 and not(distanciaKilometros == 0)) or velocidad > settings.VELOCIDAD_KM_H_AVION:
                multipleCiudad = True
    return multipleCiudad


def guardarEnviarAlertaSesionBaseDatos(db, tenant, usuario, idUsuario, tipoUsuario, tipoSesion, datosSesionAnterior, datosSesionActual, concepto):
    observaciones = ""
    mismaIp       = False
    if datosSesionAnterior["identificadorAnteriorSesion"] == datosSesionActual["identificadorActualSesion"]:
        observaciones = u"Sesiones con el mismo identificador"
        mismaIp = True
    if db == None:
        return {'success': False, 'mensaje': "No exixte el tenant"}
    try:
        doc_id, doc_rev = db.save({
            "tipoDato"                      : "alertasSesion",
            "creadoEn"                      : datetime.now().isoformat(),
            "usuario"                       : usuario,
            "idUsuario"                     : idUsuario,
            "tipoUsuario"                   : tipoUsuario,
            "tipoSesion"                    : tipoSesion,
            "identificadorAnteriorSesion"   : datosSesionAnterior["identificadorAnteriorSesion"],
            "dispositivoAnteriorSesion"     : datosSesionAnterior["dispositivoAnteriorSesion"],
            "fechaHoraAnteriorSesion"       : datosSesionAnterior["fechaHoraAnteriorSesion"],
            "direccionAnteriorSesion"       : datosSesionAnterior["direccionAnteriorSesion"],
            "ciudadAnteriorSesion"          : datosSesionAnterior["ciudadAnteriorSesion"],
            "latitudAnteriorSesion"         : datosSesionAnterior["latitudAnteriorSesion"],
            "longitudAnteriorSesion"        : datosSesionAnterior["longitudAnteriorSesion"],
            "identificadorActualSesion"     : datosSesionActual["identificadorActualSesion"],
            "dispositivoActualSesion"       : datosSesionActual["dispositivoActualSesion"],
            "fechaHoraActualSesion"         : datosSesionActual["fechaHoraActualSesion"],
            "direccionActualSesion"         : datosSesionActual["direccionActualSesion"],
            "ciudadActualSesion"            : datosSesionActual["ciudadActualSesion"],
            "latitudActualSesion"           : datosSesionActual["latitudActualSesion"],
            "longitudActualSesion"          : datosSesionActual["longitudActualSesion"],
            "concepto"                      : concepto,
            "observaciones"                 : observaciones,
            "activo"            : True
        })
        #envia un correo de alerta de seguridad al usuario
        if not(mismaIp):
            #si no es la misma ip con la sesion anterior y la actual envia correo electronico
            #enviarCorreoAlertaSeguridad(tenant, usuario, correo, dispositivo)
            pass
    except ValueError as error:
        return {'success': False}

def obtenerUltimaSesionUsuario(db, idUsuario, tipoSesion):
    sesion = {
        'sesionActiva'          : False,
        'idSesion'              : "",
        'dispositivo'           : "",
        'creadoEn'              : "",
        'direccionCompleta'     : "",
        'ciudad'                : "",
        'latitud'               : "" ,
        'longitud'              : "",
        'identificadorSesion'   : ""
    }   
    try:
        filas = db.view('_design/autenticaciones/_view/autenticacionesUltimaSesion',
                    include_docs  = True, 
                    key      = [idUsuario, tipoSesion])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            activo  = doc.get('activo', False) 
            if activo:
                sesion["sesionActiva"]  = True
            else:
                sesion["sesionActiva"]  = False
            sesion["idSesion"]      = doc.get('_id', None)
            sesion["dispositivo"]   = doc.get('dispositivo', '')
            sesion["creadoEn"]      = doc.get('creadoEn', '')
            sesion["direccionCompleta"]     = doc.get('direccionCompleta' ,'')
            sesion["ciudad"]        = doc.get('ciudad', '')
            sesion["latitud"]       = doc.get('latitud', 0)
            sesion["longitud"]      = doc.get('longitud', 0)
            sesion["identificadorSesion"]   = doc.get('identificadorSesion', "")
            sesion["validadoMultipleCiudad"]    = doc.get('validadoMultipleCiudad', False)
        return sesion           
    except ValueError as e:
        return False

def verificarEstadoSesionUsuario(db, usuario, idUsuario, tipoSesion):
    sesion = {}
    sesion["sesionActiva"]  = False
    sesion["idSesion"]      = ""    
    try:
        filas = db.view('_design/autenticaciones/_view/autenticacionesTipoSesionActivos',
                    include_docs  = True, 
                    key      = [idUsuario, tipoSesion])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            sesion["sesionActiva"]  = True
            sesion["idSesion"]      = doc.get('_id', None)
            sesion["dispositivo"]   = doc.get('dispositivo', '')
            sesion["creadoEn"]      = doc.get('creadoEn', '')
            sesion["direccionCompleta"]     = doc.get('direccionCompleta' ,'')
            sesion["ciudad"]        = doc.get('ciudad', '')
            sesion["latitud"]       = doc.get('latitud', 0)
            sesion["longitud"]      = doc.get('longitud', 0)
            sesion["identificadorSesion"]   = doc.get('identificadorSesion', "")
        return sesion           
    except ValueError as e:
        return False
 

def actualizarEstadoSesionActual(db, idSesion):
    docAutenticacion            = db[idSesion]
    docAutenticacion['activo']  = False
    db.save(docAutenticacion)


def actualizarEstadoMultipleCiudad(db, idSesion):
    docAutenticacion            = db[idSesion]
    docAutenticacion['validadoMultipleCiudad']  = True
    db.save(docAutenticacion)

# def actualizarCerrarSesion(peticion):
#     autenticacion = peticion['autenticacion']
#     usuario       = autenticacion['usuario']
#     tenant        = autenticacion['tenant']
#     idUsuario     = autenticacion['idUsuario']
#     idSesion      = autenticacion['idSesion']
#     print "******************************************"
#     print idSesion
#     tipoIngreso   = autenticacion.get("tipoIngreso", "None")       
#     db                      = conexion.getConexionTenant(tenant)
#     actualizoAutenticacion  = False
#     if db == None:
#         return { 'success' : False, 'mensaje': "existe el tenant" }

#     try:
#         dataRaw = []
#         filas = db.view('_design/autenticaciones/_view/autenticacionesTipoSesionActivos',
#                     include_docs  = True,
#                     key      = [idUsuario, tipoIngreso],
#                     limit = 1)
#         for fila in filas:
#             key                 = fila.key
#             value               = fila.value
#             doc                 = fila.doc
#             idDocAutenticacion  = doc.get('_id',"")
#             docAutenticacion            = db[idDocAutenticacion]
#             docAutenticacion['activo']  = False
#             db.save(docAutenticacion)
#             actualizoAutenticacion  = True
#         if actualizoAutenticacion:          
#             return { 'success' : True }
#         else:
#             return {'success'  : False, 'mensaje' : 'Error al cerrar sesión'}
#     except ValueError:
#         return {'success'  : False, 'mensaje' : 'Error al cerrar sesión'}

def actualizarCerrarSesion(peticion):
    autenticacion = peticion['autenticacion']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    idSesion      = autenticacion['idSesion']     
    db            = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        docAutenticacion            = db[idSesion]
        docAutenticacion['activo']  = False
        db.save(docAutenticacion)     
        return { 'success' : True }
    except couchdb.http.ResourceNotFound:
        return {'success'  : True, 'mensaje' : 'Error al cerrar sesión'}
#---------------------------------------------------------------

def buscarUsuarioBD(db, usuarioInput):
    doc = None
    usuario = {}
    usuario["loginUsuario"] = None
    usuario["correo"]       = None
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    key      = [usuarioInput])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          usuario["loginUsuario"]   = doc.get('loginUsuario')
          usuario["correo"]         = doc.get('correo')
        return usuario       
    except ValueError:
        pass

def buscarCorreoBD(db, usuarioInput):
    doc = None
    correo = {}
    correo["loginUsuario"] = None
    correo["correo"]       = None
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorCorreo',
                    include_docs  = True,
                    key      = [usuarioInput])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          correo["loginUsuario"]   = doc.get('loginUsuario')
          correo["correo"]         = doc.get('correo')
        return correo       
    except ValueError:
        pass    

def guardarDocRecuperarContrasena(db, token, loginUsuario):
    try:    
        doc_id, doc_rev = db.save({
            "tipoDato"      : "recuperacionContrasena",
            "token"         : token,
            "estaUsado"     : False,
            "usuario"       : loginUsuario,
            "creadoEn"      : datetime.now().isoformat(),
            "activo"        : True
        })
        return doc_id
    except ValueError:
        pass

def buscarExistenciaToken(db, token):
    existeToken = False
    try:
        filas = db.view('_design/recuperacionContrasena/_view/recuperacionPorToken',
                    include_docs  = True,
                    key      = [token])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          existeToken = True
        return existeToken       
    except ValueError:
        pass        

def envioGodaddy(correo, mensaje, asunto, remitente):
    print "envie correo"
    correoRemitente = remitente

    fromaddr = correoRemitente
    toaddrs  = correo
    message  = u"""From: <%s>                                                                                                                              
To: <%s>                                                                                                                                                   
MIME-Version: 1.0                                                                                                                                          
Content-type: text/html; charset=UTF-8                                                                                                                     
Subject: %s                                                                                                                                                
%s                                                                                                                                                         
""" % (fromaddr, toaddrs, asunto, mensaje)
    username = settings.CORREO_USUARIO
    password = settings.CORREO_CONTRASENA
    #server = smtplib.SMTP('smtp.gmail.com:587')                                                                                                           
    #server = servers.get(username)
    
    #    print "repitiendo3"
    server = smtplib.SMTP_SSL(settings.CORREO_SMTP, settings.CORREO_PUERTO)
    server.login(username,password)
    #servers[username] = server
    #server.sendmail(fromaddr, toaddrs, msg)                                                                                                               
    server.sendmail(fromaddr, toaddrs, message.encode('utf8'))
    #server.quit()                                                                                                                                         


def recuperarContrasena( peticion ):
    #recordar crear vistas en la base de datos modelo y fleetbi y exxonmobil usuariosporcontrasena y recuperacionContrasena
    try:

        tenant          = peticion['tenant']
        usuarioInput    = peticion['usuario']
        dbFleetbi       = None 
        dbTenant        = None
        usuario         = {}
        usuario["loginUsuario"] = None
        usuario["correo"]       = None
        correo          = {}
        correo["loginUsuario"]  = None
        correo["correo"]        = None

        if tenant == settings.TENANT_ADMINISTRACION:
            dbFleetbi = conexion.getConexionFleet()
            #busco primero por nombre de usuario
            usuario   = buscarUsuarioBD(dbFleetbi, usuarioInput)
            if usuario["loginUsuario"] == None:
                #si no encontre por nombre de usuario busco por correo
                correo = buscarCorreoBD(dbFleetbi, usuarioInput) 
        else:
            #busco primero por nombre de usuario
            dbTenant = conexion.getConexionTenant(tenant)
            usuario  = buscarUsuarioBD(dbTenant, usuarioInput)
            if usuario["loginUsuario"] == None:
                #si no encontre por nombre de usuario busco por correo
                correo = buscarCorreoBD(dbTenant, usuarioInput)            
        
        if dbFleetbi == None and dbTenant == None:
            return {
            'success' : False,
            "mensaje" : "No existe el tenant"}
      
        if not usuario["loginUsuario"] == None or not correo["loginUsuario"] == None:

            if not usuario["loginUsuario"] == None:
                #el usuario ingreso el nombre de usuario
                loginUsuario    = usuario["loginUsuario"]
                correoUsuario   = usuario["correo"]
            else:
                # el usuaro ingreso el correo
                loginUsuario    = correo["loginUsuario"]
                correoUsuario   = correo["correo"]    
            intento = 1
            tiempo  = time.time()
            token   = salarConMd5( '{}{}{}'.format( loginUsuario, 
                                                         str(tiempo), 
                                                       str(intento) ) )
            if not tenant == settings.TENANT_ADMINISTRACION:
                #verificar si alguna vez se ha registrado el token
                existeToken = False
                existeToken = buscarExistenciaToken(dbTenant, token)
                while existeToken:
                    intento += 1
                    token   = salarConMd5( '{}{}{}'.format( loginUsuario, 
                                                                 str(tiempo), 
                                                               str(intento) ) )                    
                    existeToken = buscarExistenciaToken(dbTenant, token)                   
                # se guarda en bd del tenant
                guardarDocRecuperarContrasena(dbTenant, token, loginUsuario)
            else:
                #verificar si alguna vez se ha registrado el token
                existeToken = False
                existeToken = buscarExistenciaToken(dbFleetbi, token)
                while existeToken:
                    intento += 1
                    token   = salarConMd5( '{}{}{}'.format( loginUsuario, 
                                                                 str(tiempo), 
                                                               str(intento) ) )                    
                    existeToken = buscarExistenciaToken(dbFleetbi, token)                
                # se guarda bd administracion
                guardarDocRecuperarContrasena(dbFleetbi, token, loginUsuario)

            url    = "{}{}".format(
                settings.BASE_URL_RECUPERARCONTRASENA,
                reverse('recuperarContrasena', args=[tenant,token])
            )

            #url = "http://52.55.0.240/webfleetbigui/exxonmobil/login"
            correo = correoUsuario
            asunto = u"Recuperación de contraseña"
            html = u"""
                <h2>Se ha solicitado una recuperación de contraseña</h2>
                </br>
                Puede cambiar su contraseña en el siguiente enlace 
                <a href="{}">cambiar contrasena</a>
                """.format(url) 
            envioGodaddy(correo, html, asunto, settings.CORREO_USUARIO)
                       
                
        else:
            return { 'success' : False }          

    except ValueError as e:
        pass
    return { 'success' : True }


#Pendiente
def recuperarContrasenaUnificado( peticion ):
    #recordar crear vistas en la base de datos modelo y fleetbi y exxonmobil usuariosporcontrasena y recuperacionContrasena
    try:

        usuarioInput    = peticion['usuario']
        dbFleet = conexion.getConexionFleet()

        filasTenants = dbFleet.view(
            '_design/tenantPorTenant/_view/tenantPorTenant',
            include_docs  = False
        )

        listadoTenants = []
        
        for filaTenant in filasTenants:
            llave = filaTenant.key
            listadoTenants.append(llave[0])

        # listadoTenants = ["exxonmobil"]

        for tenant in listadoTenants:            
            db = conexion.getConexionTenant(tenant)
            #tenant          = peticion['tenant']
            dbTenant                = None
            usuario                 = {}
            usuario["loginUsuario"] = None
            usuario["correo"]       = None
            correo                  = {}
            correo["loginUsuario"]  = None
            correo["correo"]        = None
            
            dbTenant = conexion.getConexionTenant(tenant)

            if dbTenant == None:
                continue
            
            usuario  = buscarUsuarioBD(dbTenant, usuarioInput)

            
            
            if usuario["loginUsuario"] == None:
                #si no encontre por nombre de usuario busco por correo
                correo = buscarCorreoBD(dbTenant, usuarioInput)


            if not usuario["loginUsuario"] == None or not correo["loginUsuario"] == None:

                if not usuario["loginUsuario"] == None:
                    #el usuario ingreso el nombre de usuario
                    loginUsuario    = usuario["loginUsuario"]
                    correoUsuario   = usuario["correo"]
                else:
                    # el usuaro ingreso el correo
                    loginUsuario    = correo["loginUsuario"]
                    correoUsuario   = correo["correo"]

                intento = 1
                tiempo  = time.time()
                token   = salarConMd5( '{}{}{}'.format( loginUsuario, 
                                                             str(tiempo), 
                                                           str(intento) ) )
                if not tenant == settings.TENANT_ADMINISTRACION:
                    #verificar si alguna vez se ha registrado el token
                    existeToken = False
                    existeToken = buscarExistenciaToken(dbTenant, token)
                    while existeToken:
                        intento += 1
                        token   = salarConMd5( '{}{}{}'.format( loginUsuario, 
                                                                     str(tiempo), 
                                                                   str(intento) ) )                    
                        existeToken = buscarExistenciaToken(dbTenant, token)                   
                    # se guarda en bd del tenant
                    guardarDocRecuperarContrasena(dbTenant, token, loginUsuario)
                else:
                    #verificar si alguna vez se ha registrado el token
                    existeToken = False
                    existeToken = buscarExistenciaToken(dbFleetbi, token)
                    while existeToken:
                        intento += 1
                        token   = salarConMd5( '{}{}{}'.format( loginUsuario, 
                                                                     str(tiempo), 
                                                                   str(intento) ) )                    
                        existeToken = buscarExistenciaToken(dbFleetbi, token)                
                    # se guarda bd administracion
                    guardarDocRecuperarContrasena(dbFleetbi, token, loginUsuario)

                url    = "{}{}".format(
                    settings.BASE_URL_RECUPERARCONTRASENA,
                    reverse('recuperarContrasena', args=[tenant,token])
                )

                #url = "http://52.55.0.240/webfleetbigui/exxonmobil/login"
                correo = correoUsuario
                asunto = u"Recuperación de contraseña"
                html = u"""
                    <h2>Se ha solicitado una recuperación de contraseña</h2>
                    </br>
                    Puede cambiar su contraseña en el siguiente enlace 
                    <a href="{}">cambiar contrasena</a>
                    """.format(url) 
                envioGodaddy(correo, html, asunto, settings.CORREO_USUARIO)
                return { 'success' : True }

            
        return { 'success' : False }
                
        # Maginot -------------------------------------------------
        
        
      
                  

    except ValueError as e:
        pass
    return { 'success' : True }


def buscarRecuperacionContrasena(db, token):
    recuperacionContrasena = {}
    recuperacionContrasena["usuario"]       = None
    recuperacionContrasena["estaUsado"]     = False
    try:
        filas = db.view('_design/recuperacionContrasena/_view/recuperacionPorToken',
                    include_docs  = True,
                    key      = [token])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          recuperacionContrasena["usuario"]     = doc.get('usuario')
          recuperacionContrasena["estaUsado"]   = doc.get('estaUsado')
        return recuperacionContrasena       
    except ValueError:
        pass 

def getEstadoToken(tenant, token):
    resultado = {
        'esValido' : False,
        'usuario'  : ''        
    }
    recuperacionContrasena = {}
    recuperacionContrasena["usuario"]       = None
    recuperacionContrasena["estaUsado"]     = None    
    try:
        if tenant == settings.TENANT_ADMINISTRACION:
            dbFleetbi   = conexion.getConexionFleet()
            recuperacionContrasena = buscarRecuperacionContrasena(dbFleetbi, token) 
        else:
            dbTenant    = conexion.getConexionTenant(tenant) 
            recuperacionContrasena = buscarRecuperacionContrasena(dbTenant, token)    

        if recuperacionContrasena["estaUsado"]:
            resultado['esValido'] = False
        else:
            resultado['esValido'] = True
            resultado['usuario']  = recuperacionContrasena["usuario"]  
    except:
        pass
    
    return resultado

#------------------------------------------------------------------
def buscarTokenUsado(db, token, estaUsado):
    resultadoTokenUsado = {
        'idDoc' : None,
        'usuario'  : None       
    }
    try:
        filas = db.view('_design/recuperacionContrasena/_view/recuperacionPorTokenYuso',
                    include_docs  = True,
                    key      = [token, estaUsado])

        for fila in filas:
          key       = fila.key
          value     = fila.value
          doc       = fila.doc
          resultadoTokenUsado['idDoc']    = doc.get('_id')
          resultadoTokenUsado['usuario']  = doc.get('usuario')
        return resultadoTokenUsado      
    except ValueError:
        pass    

def buscarUsuario(db, usuario):
    idDoc = None
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    key      = [usuario])

        for fila in filas:
          key       = fila.key
          value     = fila.value
          doc       = fila.doc
          idDoc     = doc.get('_id')
        return idDoc      
    except ValueError:
        pass    


def actualizarContrasena(db, usuario, contrasena):
    idDoc = None
    idDoc = buscarUsuario(db, usuario)
    if not idDoc == None:
        docUsuario = db[idDoc]
        docUsuario["contrasena"] = salarConMd5(contrasena)
        db.save(docUsuario)        

def autenticarUsuario(db, usuario):
    token = uuid.uuid4().hex
                
    doc_id, doc_rev = db.save({
        "tipoDato"      : "autenticacion",
        "activo"        : True,
        "creadoEn"      : datetime.now().isoformat(),
        "loginUsuario"  : usuario,
        "token"         : token,
    })    
    return token


def buscarUsuarioGeneradorCarga(db, usuario):
    idDoc = None
    try:    
        filas = db.view('_design/generadoresDeCarga/_view/listarGeneradoresCarga',
                    include_docs  = True,
                    key      = [usuario])

        for fila in filas:
          key       = fila.key
          value     = fila.value
          doc       = fila.doc
          idDoc     = doc.get('_id')
        return idDoc      
    except ValueError:
        pass    


def actualizarContrasenaGeneragorCarga(db, usuario, contrasena):
    idDoc = None
    idDoc = buscarUsuarioGeneradorCarga(db, usuario)
    if not idDoc == None:
        docUsuario = db[idDoc]
        docUsuario["contrasena"] = salarConMd5(contrasena)
        db.save(docUsuario) 

def cambiarContrasena( peticion ):
    token           = peticion['token']
    contrasena      = peticion['contrasena']
    tenant          = peticion['tenant']
    usuario         = None
    resultadoTokenUsado = {
        'idDoc' : None,
        'usuario'  : None       
    }
    resultado  = {'success' : False}

    try:
        if tenant == settings.TENANT_ADMINISTRACION:
            dbFleetbi   = conexion.getConexionFleet()
            resultadoTokenUsado     = buscarTokenUsado(dbFleetbi, token, False)
            actualizarContrasena(dbFleetbi, resultadoTokenUsado['usuario'], contrasena) 
            docRecuperacionContrasena = dbFleetbi[resultadoTokenUsado['idDoc']]
            docRecuperacionContrasena["estaUsado"] = True
            dbFleetbi.save(docRecuperacionContrasena)
            token   = autenticarUsuario(dbFleetbi, resultadoTokenUsado['usuario'])
            perfil  = "superAdministrador"
        elif tenant == settings.TENANT_GENERADOR_CARGA:
            #autentica a los generadores de carga
            dbGeneradorCarga    = conexion.getConexionTenant(tenant)
            resultadoTokenUsado = buscarTokenUsado(dbGeneradorCarga, token, False)
            actualizarContrasenaGeneragorCarga(dbGeneradorCarga, resultadoTokenUsado['usuario'], contrasena)
            docRecuperacionContrasena = dbGeneradorCarga[resultadoTokenUsado['idDoc']]
            docRecuperacionContrasena["estaUsado"] = True
            dbGeneradorCarga.save(docRecuperacionContrasena)
            perfil = "generadorCarga"
        else:
            #por aqui va pasar la prueba
            dbTenant    = conexion.getConexionTenant(tenant)  
            resultadoTokenUsado     = buscarTokenUsado(dbTenant, token, False) 
            actualizarContrasena(dbTenant, resultadoTokenUsado['usuario'], contrasena)
            docRecuperacionContrasena = dbTenant[resultadoTokenUsado['idDoc']]
            docRecuperacionContrasena["estaUsado"] = True
            dbTenant.save(docRecuperacionContrasena)
            token   = autenticarUsuario(dbTenant, resultadoTokenUsado['usuario']) 
            perfil  = "adminTenant"
          
        return { 
            'success' : True,
            'token'   : token,
            'perfil'  : perfil,
            'usuario' : resultadoTokenUsado['usuario'],
            'tenant' : tenant
        }

    except ValueError as e:
        pass
    # except:
    #     pass
    
    return resultado



#-------------------------------------------------------------
def verificarCredenciales( peticion ):
    usuario     = peticion['usuario']
    token       = peticion['token']
    tenant      = peticion['tenant']

    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, "mensaje" : "No existe el tenant" }

    filas = db.view('_design/autenticaciones/_view/autenticacion',
                    include_docs  = True,
                    key           = [usuario,token],                    
                    limit         = 1)        
    for fila in filas:        
        return {'success' : True }
    
    return { 'success' : False, "mensaje" : "No existen credenciales"  }
    
# === Auxiliares ===============================================================
def getUsuario (usuario, token):
    docAutenticacion = None
    docUsuario       = None
    perfil           = None

    db = conexion.getConexionTenant(usuario[:3])
    logging.warning("F1")
    if db == None:
        logging.warning("E1")
        return None
    
    # Parametrización de valores y validación inicial
    filas = db.view('_design/autenticaciones/_view/autenticacion',
                    include_docs  = True,
                    startkey      = [usuario,token],
                    limit         = 1)    
    
    for fila in filas:
        docAutenticacion   = fila.doc

    logging.warning("F2")
    if docAutenticacion == None:
        logging.warning("E2")
        return None

    filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True,
                    startkey      = [usuario],
                    limit         = 1)    
    
    for fila in filas:
        docUsuario   = fila.doc
        value        = fila.value
        perfil       = value.get('perfil')

    logging.warning("F3")
    if docUsuario == None or perfil == None:
        logging.warning("E3")
        return None

    #-----------------------------------------------------        
    return {
        'usuario' : usuario,
        'perfil'  : perfil
    }

def eliminarPush(db,idPush):
        
    filas = db.view('_design/autenticaciones/_view/autenticacionesIdPush',
                    include_docs  = True,
                    key      = [idPush]
                    )
    
    for fila in filas:
        doc   = fila.doc
        llave = fila.key
        
        doc["idPush"]   = ""
        doc["activo"]   = False
        db.save(doc)

            

def salarConMd5(texto):
    texto = texto+"cualquiercosa"
    m = hashlib.md5()
    m.update(texto.encode('utf8'))
    return m.hexdigest()
