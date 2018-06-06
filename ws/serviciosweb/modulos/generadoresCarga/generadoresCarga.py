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
import random
from ws.serviciosweb.modulos.conexion      import conexion
import smtplib

#-------------------------------------------------------------
def listarCodigosGenerados(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    fechaInicio  = datos['fechaInicio']
    fechaFin     = datos['fechaFin']
    
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/generadoresDeCarga/_view/listarCodigosGenerados',
                    startkey      = [fechaInicio],
                    endkey        = [fechaFin],
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          cantidadVehiculos = doc['vehiculos']
          fechaCaducidad    = doc['fechaCaducidad']
          if doc['anulado']:
            estado = "Anulado"
          else:
            fecha1      = parser.parse(fechaCaducidad)
            fechaActual = str(datetime.now(settings.EST).isoformat())
            fecha2  = parser.parse(fechaActual)
            diferencia  = fecha1 - fecha2
            segundosDiferencias = diferencia.total_seconds()
            if segundosDiferencias < 0 :
                estado = "Vencido"
            else:
                estado = "Disponible"
          dataRaw.append({
	      	'id' 				: doc['_id'],
	      	'codigo'      		: doc['codigo'],
	      	'fechaGeneracion'   : doc['fechaGeneracion'],
	      	'fechaCaducidad'    : fechaCaducidad,
	      	'descripcion'	    : doc['descripcion'],
	      	'vehiculos'			: len(cantidadVehiculos),
	      	'estado'			: estado
	      	})            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------
def consultarDetalleVehiculosCodigoGenerado(peticion):
    autenticacion           = peticion['autenticacion']
    datos                   = peticion['data']
    usuario                 = autenticacion['usuario']
    tenant                  = autenticacion['tenant']
    doc_idCodigosGenerados  = datos['id']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []
        placa               = ""
        nombresConductor    = ""
        apellidosConductor  = ""
        docCodigosGenerados = db[doc_idCodigosGenerados]
        #obtiene la lista de los vehiculos
        vehiculos           = docCodigosGenerados["vehiculos"]
        for idDocVehiculo in vehiculos:
            #consulta la placa del vehiculo
            docVehiculos    = db[idDocVehiculo]
            placa           = docVehiculos["placa"] #se envia al html
            idDocConductor  = docVehiculos["conductor"]
            #consulta el nombre del conductor asignado
            if idDocConductor !="":
                docConductor        = db[idDocConductor]
                nombresConductor    = docConductor["nombres"]
                apellidosConductor  = docConductor["apellidos"]
            else:
                nombresConductor    = ""
                apellidosConductor  = ""
            dataRaw.append({
                'placa'     : placa,
                'nombres'   : nombresConductor,
                'apellidos' : apellidosConductor
                })            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------
def anularCodigoGenerado(peticion):
    autenticacion           = peticion['autenticacion']
    datos                   = peticion['data']
    usuario                 = autenticacion['usuario']
    tenant                  = autenticacion['tenant']
    doc_idCodigosGenerados  = datos['id']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        docCodigosGenerados             = db[doc_idCodigosGenerados]
        docCodigosGenerados["anulado"]  = True
        db.save(docCodigosGenerados)         
        return {
            'success' : True
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#-------------------------------------------------------------
def consultarTenants():
    #funcion que busca los tenants en la bd fleetbi
    dbFleet = conexion.getConexionFleet()
    listaTenants = []
    if dbFleet == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        dataRaw = {}
        filas = dbFleet.view(
            '_design/tenant/_view/visualizarTenants',
            include_docs  = True
        )
        
        for fila in filas:
            #key                     = fila.key
            #value                   = fila.value
            doc                     = fila.doc
            #urlTenant               = doc.get('urlTenant')      
            listaTenants.append(doc)
        
    except ValueError:
        pass

    return listaTenants

def verificarCodigoAccesoGenerado(codigoAcceso):
    codigoAccesoBD      = ""
    existeCodigoAcceso  = False
    docsTenants = consultarTenants()
    for docTenant in docsTenants:
        print "==================================="
        tenant = docTenant.get("urlTenant","")
        print tenant
        if tenant == "":
            continue
        db = conexion.getConexionTenant(tenant)
        if db == None:
            continue
        try:
            filas = db.view('_design/generadoresDeCarga/_view/listarCodigoGeneradoPorCodigoAcceso',
                        key      = [codigoAcceso])
            for fila in filas:
              key = fila.key
              value = fila.value
              doc = fila.doc
              existeCodigoAcceso = True
        except ValueError:
            return False
    return existeCodigoAcceso


def construirCodigoAcceso(cantidadCaracteres):
    eligeNumeros = False
    codigoAcceso    = ""
    numeros = "0123456789"
    letras  = "QWERTYUIOPASDFGHJKLZXCVBNM"
    longitudCodigoAcceso = len(codigoAcceso)
    existeCodigoAcceso = False
    if longitudCodigoAcceso == None:
        #la cadena no tiene carateres entonces es igual a cero
        longitudCodigoAcceso = 0
    while(longitudCodigoAcceso < cantidadCaracteres):
        randonEleccion = random.randrange(2)
        #posicionElegir = 5
        if randonEleccion == 0:
            #elige caracter de la listaNumeros
            caracter = random.choice(numeros)
        else:
            #elige caracteres de listaLetras
            caracter = random.choice(letras)
        codigoAcceso += caracter
        longitudCodigoAcceso += 1
        if longitudCodigoAcceso == cantidadCaracteres:
            print codigoAcceso
            existeCodigoAcceso = verificarCodigoAccesoGenerado(codigoAcceso)
            if existeCodigoAcceso:
                codigoAcceso = ""
                longitudCodigoAcceso = 0
    return codigoAcceso

def generarCodigoAcceso(peticion):
    autenticacion           = peticion['autenticacion']
    datos                   = peticion['data']
    usuario                 = autenticacion['usuario']
    tenant                  = autenticacion['tenant']
    #cantidadCaracteres      = int(datos['cantidadCaracteres'])
    cantidadCaracteres      = settings.CANTIDAD_CARACTERES_CODIGO_ACCESO
    codigoAccesoGenerado    = construirCodigoAcceso(cantidadCaracteres)

    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        return {
            'success' : True,
            "codigoAccesoGenerado": codigoAccesoGenerado
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }



def crearCodigoAcceso(peticion):
    autenticacion           = peticion['autenticacion']
    datos                   = peticion['data']
    usuario                 = autenticacion['usuario']
    tenant                  = autenticacion['tenant']
    codigoAcceso            = datos['codigoAcceso']
    fechaGeneracion         = datos['fechaGeneracion']
    descripcion             = datos['descripcion']
    vehiculos               = datos['vehiculos']
    fechaCaducidad          = datos['fechaCaducidad']
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        doc_id, doc_rev = db.save({
            "tipoDato"          : "codigosGenerados",
            "creadoEn"          : datetime.now().isoformat(),
            "modificadoEn"      : datetime.now().isoformat(),
            "modificadoPor"     : usuario,
            "codigo"            : codigoAcceso,
            "fechaGeneracion"   : fechaGeneracion,
            "fechaCaducidad"    : fechaCaducidad,
            "descripcion"       : descripcion,
            "vehiculos"         : vehiculos,
            "anulado"           : False,
            "tenant"            : tenant,
            "activo"            : True
        })
        return { 'success' : True }
    except ValueError:
        return { 'success' : False, 'mensaje':"error desconocido" }


def guardarGeneradorCarga(nombreGenerador, email, contrasena, tenant):
    #guarda los datos del generador de carga en el tenant generadorescarga
    docGenerador = {}
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return False
    try:
        doc_id, doc_rev = db.save({
            "tipoDato"          : "generadoresDeCarga",
            "creadoEn"          : datetime.now().isoformat(),
            "modificadoEn"      : datetime.now().isoformat(),
            "nombreGenerador"    : nombreGenerador,
            "email"             : email,
            "contrasena"        : contrasena,
            "activo"            : True
        })
        docGenerador["docId"]       = doc_id
        docGenerador["guardoDoc"]   = True
    except ValueError:
        docGenerador["docId"]       = None
        docGenerador["guardoDoc"]   = False
    return docGenerador


def verificarVencimientoCodAcceso(fechaCaducidad):
    fecha1      = parser.parse(fechaCaducidad)
    fechaActual = str(datetime.now(settings.EST).isoformat())
    fecha2  = parser.parse(fechaActual)
    diferencia  = fecha1 - fecha2
    segundosDiferencias = diferencia.total_seconds()
    if segundosDiferencias < 0 :
        #Esta vencido
        return True
    else:
        #No esta vencido
        return False


def verificarCodigoAccesoGeneradorCarga(codigoAcceso):
    #verifica los codigos de acceso en todos los tenants
    infoCodAcceso = {}
    infoCodAcceso["existeCodigoAcceso"] = False
    codigoAccesoBD      = ""
    existeCodigoAcceso  = False
    docsTenants = consultarTenants()
    for docTenant in docsTenants:
        print "==================================="
        tenant = docTenant.get("urlTenant","")
        print tenant
        if tenant == "":
            continue
        db = conexion.getConexionTenant(tenant)
        if db == None:
            continue
        try:
            filas = db.view('_design/generadoresDeCarga/_view/listarCodigoGeneradoPorCodigoAcceso',
                        key      = [codigoAcceso],
                        include_docs  = True)
            for fila in filas:
              key = fila.key
              value = fila.value
              doc = fila.doc
              codAcceso         = doc.get('anulado', False)
              fechaCaducidad    = doc.get('fechaCaducidad')
              estaVencido       = verificarVencimientoCodAcceso(fechaCaducidad)
              if not(codAcceso) and not(estaVencido):
                #existeCodigoAcceso = True
                infoCodAcceso["existeCodigoAcceso"] = True
                infoCodAcceso["idDoc"]              = doc.get('_id')
                infoCodAcceso["codigo"]             = doc.get('codigo')
                infoCodAcceso["fechaGeneracion"]    = doc.get('fechaGeneracion')
                infoCodAcceso["fechaCaducidad"]     = doc.get('fechaCaducidad')
                infoCodAcceso["tenant"]             = doc.get('tenant')
                infoCodAcceso["vehiculos"]          = doc.get('vehiculos')  
        except ValueError:
            return False
    #return existeCodigoAcceso
    return infoCodAcceso


def validarEmail(email, tenant):
    existemail = False 
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return False
    try:
        filas = db.view('_design/generadoresDeCarga/_view/listarGeneradoresCarga',
            key      = [email])
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            existemail = True
        return existemail
    except ValueError:
        return False


def guardarAutenticacion(token, email, tenant):
    #guarda la autenticacion en el tenant 'generadorescarga' 
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return False
    try:
        doc_id, doc_rev = db.save({
            "tipoDato"          : "autenticacion",
            "creadoEn"          : datetime.now().isoformat(),
            "loginUsuario"      : email,
            "token"             : token,
            "activo"            : True
        })
        return True
    except ValueError:
        return False 


def guardarCodigoDelGenerador(infoCodAcceso, idDocGenerador):
    tenantGeneradorCarga = settings.TENANT_GENERADOR_CARGA 
    db = conexion.getConexionTenant(tenantGeneradorCarga)
    if db == None:
        return False
    try:
        doc_id, doc_rev = db.save({
            "tipoDato"                  : "codigosAcceso",
            "creadoEn"                  : datetime.now().isoformat(),
            "idDocCodAcceso"            : infoCodAcceso["idDoc"],
            "tenantDelCodGenerado"      : infoCodAcceso["tenant"],
            "idGeneradorCarga"          : idDocGenerador,
            "codigo"                    : infoCodAcceso["codigo"],
            "activo"                    : True
        })
        return True
    except ValueError:
        return False 



def autenticarGeneradorCarga(peticion):
    datos               = peticion['data']
    nombreGenerador     = datos['nombreGenerador']
    codigoAcceso        = datos['codigoAcceso']
    email               = datos['email']
    contrasena          = datos['contrasena']
    infoCodAcceso       = {}
    docGenerador        = {}
    #existeCodigoAcceso  = verificarCodigoAccesoGeneradorCarga(codigoAcceso)
    infoCodAcceso       = verificarCodigoAccesoGeneradorCarga(codigoAcceso)
    #tenant = "generadorescarga"
    tenant = settings.TENANT_GENERADOR_CARGA
    #valida que le email no este registrado
    existemail = validarEmail(email, tenant)
    if infoCodAcceso["existeCodigoAcceso"] and not(existemail):
        # si un cliente ha creado el código de acceso se permitira ingresar al sistema
        md5Contrasena = salarConMd5(contrasena)
        token = uuid.uuid4().hex
        docGenerador = guardarGeneradorCarga(nombreGenerador, email, md5Contrasena, tenant)
        guardarAutenticacion(token, email, tenant)
        if docGenerador["guardoDoc"]:
            #guarda el cod del generador en el tenant fleetbigeneradorCarga
            guardarCodigoDelGenerador(infoCodAcceso, docGenerador["docId"])
            db = conexion.getConexionTenant(tenant)
            if db == None:
                return {
                    'success' : False,
                    "mensaje" : "No existe el tenant"
                }
            doc_id, doc_rev = db.save({
                "tipoDato"      : "autenticacion",
                "activo"        : True,
                "creadoEn"      : datetime.now().isoformat(),
                "loginUsuario"  : docGenerador["docId"],
                "token"         : token
            })
            return {
                'success'           : True,
                'token'             : token,                 
                'login'             : email,
                'nombreUsuario'     : email,
                'idUsuario'         : docGenerador["docId"],
                'tenant'            : tenant,
                'nombreGenerador'   : nombreGenerador,
                'perfil'            : "generadorCarga",
                'mensaje'           : "Bienvenido a FleetBi"  

            }
        else:
            return {    'success' : False,
                        'mensaje':"Error desconocido"}
    else:
        return {    'success' : False,
                    'mensaje':"El código de acceso o el email no es válido"}


def autenticarGeneradorCargaLogin(peticion):
    usuario     = peticion['usuario']
    accion      = peticion['accion']
    #tenant = "generadorescarga"
    tenant = settings.TENANT_GENERADOR_CARGA
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return {
            'success' : False,
            "mensaje" : "No existe el tenant"
        }

    if accion == 'ingresar':
        contrasena  = salarConMd5(peticion['contrasena'])
        logging.warning(contrasena)
        idUsuario = buscarIdGeneradorCarga(usuario)
        filas = db.view('_design/generadoresDeCarga/_view/generadoresCargaPorContrasena',
                    include_docs  = True,
                    startkey      = [usuario,contrasena],
                    endkey        = [usuario,contrasena],
                    limit         = 1)        
        for fila in filas:
            doc             = fila.doc
            llave           = fila.key
            token           = uuid.uuid4().hex
            idUsuario       = doc.get("_id")
            nombreGenerador = doc.get("nombreGenerador")
            doc_id, doc_rev = db.save({
                "tipoDato"      : "autenticacion",
                "activo"        : True,
                "creadoEn"      : datetime.now().isoformat(),
                "loginUsuario"  : idUsuario,
                "token"         : token
            })
            return {
                'success'           : True,
                'token'             : token,                 
                'login'             : usuario,
                'nombreUsuario'     : usuario,
                'idUsuario'         : idUsuario,
                'tenant'            : tenant,
                'nombreGenerador'   : nombreGenerador,
                'perfil'            : "generadorCarga",
                'mensaje'           : "Bienvenido a FleetBi"  

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
 

def buscarCorreoGeneradorBD(db, usuarioCorreo):
    doc = None
    correo = None
    try:
        filas = db.view('_design/generadoresDeCarga/_view/listarGeneradoresCarga',
                    include_docs  = True,
                    key      = [usuarioCorreo])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          correo = doc.get('email')
        return correo       
    except ValueError:
        pass    


def salarConMd5(texto):
    texto = texto+"cualquiercosa"
    m = hashlib.md5()
    m.update(texto.encode('utf8'))
    return m.hexdigest()


def buscarExistenciaTokenGenerador(db, token):
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


def guardarDocRecuperarContrasena(db, token, correo):
    try:    
        doc_id, doc_rev = db.save({
            "tipoDato"      : "recuperacionContrasena",
            "token"         : token,
            "estaUsado"     : False,
            "usuario"       : correo,
            "creadoEn"      : datetime.now().isoformat(),
            "activo"        : True
        })
        return doc_id
    except ValueError:
        pass


def recuperarContrasena( peticion ):
    #recordar crear vistas en la base de datos modelo y fleetbi y exxonmobil usuariosporcontrasena y recuperacionContrasena
    try:
        correoInput = peticion['correo']
        tenant      = settings.TENANT_GENERADOR_CARGA
        db          = conexion.getConexionTenant(tenant)
        correo      = buscarCorreoGeneradorBD(db, correoInput)
        if not correo == None:
            intento = 1
            tiempo  = time.time()
            token   = salarConMd5( '{}{}{}'.format( correo, 
                                                             str(tiempo), 
                                                           str(intento) ) )
            existeToken = False
            #verificar si alguna vez se ha registrado el token
            existeToken = buscarExistenciaTokenGenerador(db, token)
            while existeToken:
                intento += 1
                token   = salarConMd5( '{}{}{}'.format(correo, str(tiempo), str(intento)))
                existeToken = buscarExistenciaTokenGenerador(db, token)
                #se guarda en bd del tenant
            guardarDocRecuperarContrasena(db, token, correo)
            url    = "{}{}".format(
                settings.BASE_URL_RECUPERARCONTRASENA,
                reverse('recuperarContrasena', args=[tenant,token])
            )
            #url = "http://52.55.0.240/webfleetbigui/generadorescarga/login"
            asunto = u"Recuperación de contraseña"
            html = u"""
                <h2>Se ha solicitado una recuperación de contraseña</h2>
                </br>
                Puede cambiar su contraseña en el siguiente enlace 
                <a href="{}">cambiar contrasena</a>
                """.format(url) 
            envioGodaddy(correo, html, asunto, settings.CORREO_USUARIO)
        else:
            return {'success' : False}
                
    except ValueError as e:
        pass
    return { 'success' : True }


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


def obtenerDatosCodAcceso(idDocCodAcceso, tenantDelCodGenerado):
    #funcion que consulta los datos del cod generado segun el cliente    
    db = conexion.getConexionTenant(tenantDelCodGenerado)
    docCodigoAcceso         = db[idDocCodAcceso]
    idDoc                   = docCodigoAcceso["_id"]
    codigo                  = docCodigoAcceso["codigo"]
    fechaGeneracion         = docCodigoAcceso["fechaGeneracion"]
    fechaCaducidad          = docCodigoAcceso["fechaCaducidad"]
    vehiculos               = docCodigoAcceso["vehiculos"]
    anulado                 = docCodigoAcceso["anulado"]
    return {
            'id'                : idDoc,
            'codigo'            : codigo,
            'fechaGeneracion'   : fechaGeneracion,
            'fechaCaducidad'    : fechaCaducidad,
            'transportador'     : tenantDelCodGenerado,
            'vehiculos'         : len(vehiculos),
            'anulado'           : anulado   }


def buscarInfoCodAccesoClientes(datosCodigoAccesoGenerador, fechaInicio, fechaFin):
    #editando
    dataRaw = []
    for codAccesoGenerador in datosCodigoAccesoGenerador:
        idDocCodAcceso          =  codAccesoGenerador.get("idDocCodAcceso", None)
        tenantDelCodGenerado    =  codAccesoGenerador.get("tenantDelCodGenerado", None)
        #llama a la funcion que consulta los datos del cod generado segun el cliente
        if not(idDocCodAcceso == None):
            datosLlave  =  obtenerDatosCodAcceso(idDocCodAcceso, tenantDelCodGenerado)
            estaVencido       = verificarVencimientoCodAcceso(datosLlave.get('fechaCaducidad'))
            if not(datosLlave.get('anulado', True)) and not(estaVencido):
                if (fechaInicio <= datosLlave.get('fechaGeneracion') <= fechaFin):
                    dataRaw.append(datosLlave)
    return dataRaw


def listarCodigosAgregados(peticion):
    autenticacion       = peticion['autenticacion']
    datos               = peticion['data']
    usuario             = autenticacion['usuario']
    #tenant              = autenticacion['tenant']
    fechaInicio         = datos['fechaInicio']
    fechaFin            = datos['fechaFin']
    tenant              = settings.TENANT_GENERADOR_CARGA
    dbGenerador         = conexion.getConexionTenant(tenant)
    #primero consulto los codigos del usuario
    #docIdGeneradorCarga             = buscarIdGeneradorCarga(usuario)
    docIdGeneradorCarga             = usuario
    datosCodigoAccesoGenerador      = []
    if dbGenerador == None:
        return False
    try:
        filas = dbGenerador.view('_design/codigosAcceso/_view/listarCodigosAcceso',
            key      = [docIdGeneradorCarga],          
            include_docs  = True)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            codigoAcceso            = doc.get('codigo', None)
            tenantDelCodGenerado    = doc.get('tenantDelCodGenerado', None)
            idDocCodAcceso          = doc.get('idDocCodAcceso', None)
            datosCodigoAccesoGenerador.append({
                'codigoAcceso'          : codigoAcceso,
                'tenantDelCodGenerado'  : tenantDelCodGenerado,
                'idDocCodAcceso'        : idDocCodAcceso
            })   
        #funcion que consulta la informacion de los cod acceso de los clientes
        infoCodAccesoClientes       = buscarInfoCodAccesoClientes(datosCodigoAccesoGenerador, fechaInicio, fechaFin)
        #cod accesos del generador que se envian a la plantilla web
        return {
            'success' : True,
            'data'    : infoCodAccesoClientes
        }
    except ValueError:
        return False




def buscarIdGeneradorCarga(usuario):
    tenant  = settings.TENANT_GENERADOR_CARGA
    docId   = None
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return False
    try:
        filas = db.view('_design/generadoresDeCarga/_view/listarGeneradoresCarga',
            key      = [usuario],
            include_docs  = True)
        for fila in filas:
            key = fila.key
            value = fila.value
            doc = fila.doc
            docId = doc.get('_id', None) 
        return docId
    except ValueError:
        return False


def existeCodigoDelGenerador(codigoAcceso, idGeneradorCarga):
    tenant  = settings.TENANT_GENERADOR_CARGA
    existeCodigo   = False
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return False
    try:
        filas = db.view('_design/codigosAcceso/_view/listarCodigosAccesoPorCodigo',
            key      = [codigoAcceso, idGeneradorCarga])
        for fila in filas:
            key = fila.key
            value = fila.value
            existeCodigo = True  
        return existeCodigo
    except ValueError:
        pass


def agregarCodigoAcceso(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    #tenant        = autenticacion['tenant']
    codigoAcceso  = datos['codigoAcceso']
    infoCodAcceso       = {}
    infoCodAcceso = verificarCodigoAccesoGeneradorCarga(codigoAcceso)
    if infoCodAcceso["existeCodigoAcceso"]:
        #docIdGeneradorCarga = buscarIdGeneradorCarga(usuario)
        docIdGeneradorCarga = usuario
        #verifica si el codigo existe en la bd
        existeCodGenerado = existeCodigoDelGenerador(infoCodAcceso["codigo"], docIdGeneradorCarga)
        #guarda el cod del generador en el tenant fleetbigeneradorCarga
        if not(existeCodGenerado):
            guardoCodigo = guardarCodigoDelGenerador(infoCodAcceso, docIdGeneradorCarga)
            if guardoCodigo:
                return {'success' : True,
                        'mensaje': "Código agregado" }
            else:
                return {'success' : False,
                        'mensaje': "El código no fue agregado" }
        else:
            return {'success' : False,
                        'mensaje': "El codigo ya está registrado" }
    else:
        return {'success' : False,
                        'mensaje': "Código de acceso no valido" }


def actualizarDocGeneradorCarga(db, usuario, datos):
    resultado = False
    if db == None:
        return { 'success' : False }
    try:
        md5Salada = ""
        m = hashlib.md5()
        # idDoc                   = buscarIdGeneradorCarga(usuario)
        idDoc                   = usuario 
        doc = db[idDoc]
        doc["modificadoEn"]     = datetime.now().isoformat()
        doc["modificadoPor"]    = usuario
        doc["nombreGenerador"]  = datos["nombreGenerador"]
        doc["email"]            = datos["correo"]
        if datos["contrasena"] != "":
            md5Salada = salarConMd5(datos["contrasena"])
            doc["contrasena"] =  md5Salada  
        db.save(doc)
        resultado = True
        return resultado
    except ValueError:
        return resultado


def verificarExisteEmail(correo, idUsuario):
    tenant      = settings.TENANT_GENERADOR_CARGA
    db          = conexion.getConexionTenant(tenant)
    existeEmail = False
    if db == None:
        return False
    try:
        filas = db.view('_design/generadoresDeCarga/_view/listarGeneradoresCarga',
            key      = [correo],
            include_docs  = True)
        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            docId   = doc.get('_id',None)
            email   = doc.get('email', None)
            if email == correo and docId != idUsuario:
                existeEmail = True
        return existeEmail 
    except ValueError:
        pass


def actualizarDatosCuentaGeneradorCarga(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    #tenant          = autenticacion['tenant']
    tenantGeneradorCarga = settings.TENANT_GENERADOR_CARGA 
    dbTenant        = conexion.getConexionTenant(tenantGeneradorCarga)
    resultado       = False
    #funcion para actualizar los datos del generador de carga
    nombreGenerador =  datos["nombreGenerador"]
    correo          =  datos["correo"]
    existeEmail     = verificarExisteEmail(correo, usuario)
    #si no existe email se puede actualizar los datos
    if not(existeEmail):
        resultado       = actualizarDocGeneradorCarga(dbTenant, usuario, datos)
    if resultado:
        return { 'success' : True }
    else:
        return { 'success' : False,
                 'mensaje':"El email ya se está registrado"}


def clientesCodGenerados(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    #idGeneradorCarga = buscarIdGeneradorCarga(usuario)
    idGeneradorCarga  = usuario
    try:
        dataRaw = []

        filas = db.view('_design/codigosAcceso/_view/listarCodigosAcceso',
            key      = [idGeneradorCarga],
            include_docs  = True
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          codigoAcceso = doc.get('codigo', '')
          infoCodAcceso = verificarCodigoAccesoGeneradorCarga(codigoAcceso)
          if infoCodAcceso["existeCodigoAcceso"]: 
              dataRaw.append(
                  {
                  'tenant'          : infoCodAcceso["tenant"],
                  'nombre'          : u"{} - {} ".format(infoCodAcceso["codigo"], infoCodAcceso["tenant"]),
                  'codigoAcceso'    : infoCodAcceso["codigo"],
                  'fechaGeneracion' : infoCodAcceso["fechaGeneracion"],
                  'fechaCaducidad'  : infoCodAcceso["fechaCaducidad"]
                  }
              )          
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }




def buscarVehiculosActivados(peticion):
    autenticacion   = peticion['autenticacion']
    datos           = peticion['data']
    usuario         = autenticacion['usuario']
    tenant          = autenticacion['tenant']
    codigoAcceso    = autenticacion['codigoAcceso']
    db = conexion.getConexionTenant(tenant)
    vehiculos       = []
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []

        filas = db.view('_design/generadoresDeCarga/_view/listarCodigoGeneradoPorCodigoAcceso',
            key      = [codigoAcceso],
            include_docs  = True
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          vehiculos = doc.get('vehiculos', '')         
        return vehiculos
    except ValueError:
        pass


def buscarConductorDelVehiculo(peticion, idVehiculo):
    autenticacion   = peticion['autenticacion']
    tenant          = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    conductor       = ""
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []

        filas = db.view('_design/generadoresDeCarga/_view/listarVehiculosPorId',
            key      = [idVehiculo],
            include_docs  = True,
            limit = 1
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          conductor = doc.get('conductor', '')         
        return conductor
    except ValueError:
        pass


def buscarCofiguracionGenerador(peticion):
    autenticacion   = peticion['autenticacion']
    tenant          = autenticacion['tenant']
    db          = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False, 'mensaje': "existe el bd" }
    try:
        filas = db.view('_design/configuracion/_view/configuraciones',
            key             = ["CONFIGURACIONGENERADORCARGA"],
            limit           = 1,
            include_docs    = False)
        for fila in filas:
            key                             = fila.key
            value                           = fila.value   
        return value
    except ValueError:
        pass

def buscarUsuarioRegistroTenant(peticion, usuarioRegistro):
    autenticacion   = peticion['autenticacion']
    tenant          = autenticacion['tenant']
    db              = conexion.getConexionTenant(tenant)
    respuesta       = False
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []

        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
            key      = [usuarioRegistro],
            include_docs  = False,
            limit = 1
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          #doc = fila.doc
          respuesta = True        
        return respuesta
    except ValueError:
        return False



def procesarPermisoDatosGeneradorCarga(peticion, respuestaRaw, idUsuarioPeticion):
    dataRaw = []
    i       = 0
    #consulta la configuracion del generador en el sistema si es todaInformacion, soloGenerador, generadorMiInformacion
    configuracionGenerador  = buscarCofiguracionGenerador(peticion)
    for i in range(0, len(respuestaRaw["data"])):
        usuarioRegistro     = respuestaRaw["data"][i]["creadoPor"]
        if configuracionGenerador == "soloGenerador":
            #compara de que el registro fue realizado por el generador de carga
            if idUsuarioPeticion == usuarioRegistro:
                dataRaw.append(respuestaRaw["data"][i])
        elif configuracionGenerador == "generadorMiInformacion":
                esUsuarioTenant = buscarUsuarioRegistroTenant(peticion, usuarioRegistro)#pendiente
                if idUsuarioPeticion == usuarioRegistro or esUsuarioTenant:
                    #agrega los registros del generador y del tenant
                    dataRaw.append(respuestaRaw["data"][i])
        else:
            #la configuracion es de todaInformacion por lo que se agrega todos los registros
            dataRaw.append(respuestaRaw["data"][i])
    return dataRaw



# def agregarListaRespuestaVehiculos(listaVehiculosBD, listaRespuestaVehiculos):
#     #funcion que agrega un vehiculo a la lista y verifica si no esta repetido
#     banderaEstaVehiculo = False
#     for vehiculoBD in listaVehiculosBD:
#         for vehiculoListaRespuesta in listaRespuestaVehiculos:
#             if vehiculoBD == vehiculoListaRespuesta:
#                 banderaEstaVehiculo = True
#                 continue
#         if not(banderaEstaVehiculo):
#             #si no esta en la lista respuesta se agrega el vehiculo
#             listaRespuestaVehiculos.append(vehiculoBD)
#             banderaEstaVehiculo = False
#     return listaRespuestaVehiculos


# def buscarTodosVehiculosActivados(peticion):
#     #temporal
#     #Busca todos los vehiculos activados del generador de carga logueado
#     autenticacion           = peticion['autenticacion']
#     tenant                  = autenticacion['tenant']
#     usuario                 = autenticacion['usuario']
#     tenantGeneradorCarga    = settings.TENANT_GENERADOR_CARGA 
#     dbTenantGenerador       = conexion.getConexionTenant(tenantGeneradorCarga)
#     listaVehiculosRespuesta = []
#     if dbTenantGenerador == None:
#         return { 'success' : False, 'mensaje': "existe el tenant" }
#     try:
#         dataRaw = []

#         filas = dbTenantGenerador.view('_design/codigosAcceso/_view/listarCodigosAcceso',
#             key      = [usuario],
#             include_docs  = True
#         )
#         for fila in filas:
#           key = fila.key
#           value = fila.value
#           doc = fila.doc
#           idDocCodAcceso        = doc.get('idDocCodAcceso','')
#           tenantDelCodGenerado  = doc.get('tenantDelCodGenerado', '')
#           dbTenant = conexion.getConexionTenant(tenantDelCodGenerado)
#           docCodAccesoTenant    = dbTenant[idDocCodAcceso]
#           fechaCaducidad        = docCodAccesoTenant["fechaCaducidad"]
#           estaVencido           = verificarVencimientoCodAcceso(fechaCaducidad)
#           if not(estaVencido):
#             #agregarListaRespuestaVehiculos(docCodAccesoTenant["vehiculos"] , listaVehiculosRespuesta)
#             # List merge without dupe
#             dataRaw.extend([element for element in docCodAccesoTenant["vehiculos"] if element not in dataRaw])
#         return dataRaw
#     except ValueError:
#         return False


def buscarTodosVehiculosActivadosTenant(peticion):
    #Busca todos los vehiculos activados del generador de carga logueado
    autenticacion           = peticion['autenticacion']
    tenant                  = autenticacion['tenant']
    usuario                 = autenticacion['usuario']
    tenant                  = autenticacion['tenant']
    codigoAcceso            = autenticacion['codigoAcceso']
    db                      = conexion.getConexionTenant(tenant)
    listaVehiculosRespuesta = []
    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try:
        dataRaw = []

        filas = db.view('_design/generadoresDeCarga/_view/listarCodigoGeneradoPorCodigoAcceso',
            key           = [codigoAcceso],
            include_docs  = True,
            limit         = 1
        )
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          vehiculos             =  doc.get('vehiculos','')
        return vehiculos
    except ValueError:
        return False


def buscarTipoZonasRegistro(tiposZonasGenerador, tiposZonasConsulta):
    #funcion que construye una nueva lista de tipos zonas segun 
    #los tipos zonas que estan habilitadas por el codigo de acceso 
    nuevaListaTipoZonas = []
    for tipoZonaGenerador in tiposZonasGenerador:
        for tiposZonaConsulta in tiposZonasConsulta:
            if tipoZonaGenerador["id"] == tiposZonaConsulta["id"]:
                nuevaListaTipoZonas.append({'descripcion': tiposZonaConsulta["descripcion"], 
                    'nombre': tiposZonaConsulta["nombre"], 'id': tiposZonaConsulta["id"]})
    return nuevaListaTipoZonas