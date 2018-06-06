# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from jsonschema               import validate, ValidationError
from django.core.urlresolvers import reverse
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
from ..autenticacion          import autenticacion as moduloAutenticacion
#-------------------------------------------------------------
def consultarCantidadVehiculos(tenant):
    cantVehiculos = 0
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return 0
    try:
        filas = db.view(
            '_design/detalleVehiculo/_view/detalleVehiculo',
            include_docs = True
        )
        for fila in filas:
            doc = fila.doc 
            cantVehiculos += 1               
        return cantVehiculos    
    except:
        return 0


def listarTenants( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
      
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:

        filas = db.view(
            '_design/tenant/_view/visualizarTenants',
            include_docs = True
        )

        dataRaw = []
        for fila in filas:
            doc             = fila.doc
            cantVehiculos   = consultarCantidadVehiculos(doc.get("urlTenant",""))           
            dataRaw.append(
                {
                "id"                   : doc['_id'],
                    "activo"           : doc.get("activo",""),
                    "nombreGeneral"    : doc.get("nombreGeneral",""),
                    "nit"              : doc.get("nit",""),
                    "urlTenant"        : doc.get("urlTenant",""),
                    "urlLogo"          : doc.get("urlLogo",""),
                    "telefono"         : doc.get("telefono",""),
                    "direccion"        : doc.get("direccion",""),
                    "celularEmergencia": doc.get("celularEmergencia",""),
                    "numeroVehiculos"  : str(cantVehiculos)
               
            }
            )        
            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    
    except:
        pass

    return { 'success' : False }

def crearTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db    = conexion.getConexionTenant(tenant)
    couch = conexion.getCouch()
    
    if db == None:
        return { 'success' : False, 'mensaje': "no existe el tenant" }

    try:

        nuevaBaseDatos = u'{}{}'.format(
            settings.BASEDB, datos.get("urlTenant",""))
        
        if existeDB( nuevaBaseDatos, couch ):
            return { 'success' : False, 'mensaje': "El tenant ya existe" }


        doc = {
            "tipoDato"              : "tenant",
            "activo"                : True,
            "nit"                   : datos.get("nit",""),
    	    "urlTenant"             : datos.get("urlTenant",""),
    	    "nombreGeneral"         : datos.get("nombreGeneral",""),
    	    "idImagenLogo"          : datos.get("idImagenLogo",""),
    	    "telefono"              : datos.get("telefono",""),
    	    "direccion"             : datos.get("direccion",""),
            "celularEmergencia"     : datos.get("celularEmergencia",""),
            "correo"                : datos.get("correo",""),
        }

        db.save(doc)
        crearNuevaBaseDatos(nuevaBaseDatos, couch)
        
        return {
            'success' : True,
            'data'    : {}
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


#Recibe el nombre completo de la base de datso con todo y fleetbi
def crearNuevaBaseDatos(nuevaBase,couch):
    modeloBase = u'{}{}'.format(settings.BASEDB, settings.TENANT_MODELO)
    #nuevaBase  = u'{}{}'.format(settings.BASEDB, codigobase)        

    modeloBase = "fleetbieduardo2exxonmobil"
    print u"creando {}".format(modeloBase)
    
    dbModelo = couch[modeloBase]
    
    if not existeDB(nuevaBase, couch):
        couch.create(nuevaBase)
        
    dbDestino = couch[nuevaBase]
            

    filas = dbModelo.view(
        '_all_docs',
        include_docs  = True,
        startkey = '_design/',
        endkey   = '_design0'
    )
    
    for fila in filas:
        doc = fila.doc
        print doc
        del doc['_rev']
        dbDestino.save(doc)
            

def existeDB(nombreBase, couch):
    resultado = True
        
    try:
        db = couch[nombreBase]
    except:
        resultado = False
        
    return resultado


#---- 8< ----------------- 8< -----------------------
def crearTenantOLD( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tennant       = usuario[:3]
    
    db = conexion.getConexionTenant(usuario[:3])

    if db == None:
        return { 'success' : False }


    existeDb = conexion.existeDb(datos.get("codigo"))

    if existeDb:
        return {
            'success' : False,
            'mensaje'   : u"El código {} ya existe."
        }

    conexion.crearDb(datos.get("codigo"))

    
    try: 
        doc_id, doc_rev = db.save({
            "estado"		: "activo",
            "tipoDato"		: "tenant",
            "creadoEn"		: datetime.now().isoformat(),
            "modificadoEn"	: datetime.now().isoformat(),
            "modificadoPor"	: usuario,
            "nombre"            : datos.get("nombre"),
            "codigo"            : datos.get("codigo"),
            "limiteUsuarios"    : datos.get("limiteUsuarios"),
            "identificacion"    : datos.get("identificacion"),
            "telefono"          : datos.get("telefono"),
            "direccion"         : datos.get("direccion"),
            
        })
        return {
            'success' : True,
            'data'    : {
                'id' : doc_id
            }            
        }
    except:
        pass

    return { 'success' : False }

# #-------------------------------------------------------------

def editarTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)
    print "despues de conectar tenant"+datos['id']

    if db == None:
        print "no encuentro db"
        return { 'success' : False }

    try:
        
        doc = db[datos['id']]
        print "traje  documento:"
        
        #doc['modificadoPor']  = usuario
        #doc['modificadoEn']   = datetime.now().isoformat()

        doc['activo']                = datos.get('activo',   doc['activo'])
        doc['nombreGeneral']         = datos.get('nombreGeneral',    doc['nombreGeneral'])
        #doc['codigo']         = datos.get('codigo',         doc['codigo'])
        doc['urlTenant']             = datos.get('urlTenant', doc['urlTenant'])
        doc['nit']                   = datos.get('nit', doc['nit'])
        doc['idImagenLogo']          = datos.get('idImagenLogo', doc['idImagenLogo'])
        doc['celularEmergencia']     = datos.get('celularEmergencia', doc['celularEmergencia'])
        doc['telefono']              = datos.get('telefono',       doc['telefono'])
        doc['direccion']             = datos.get('direccion',      doc['direccion'])
        doc['correo']                = datos.get('correo',      doc['correo']) 
        print "antes de guardar"
   
        db.save(doc)
        print "despues de guardar"
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except ValidationError as e:
        respuesta['mensaje'] = e.message
        print "error del try "+e

    return { 'success' : False }

# #-------------------------------------------------------------

def eliminarTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    
    db = conexion.getConexionTenant(usuario[:3])

    if db == None:
        return { 'success' : False }

    try:
        idEquipo    = datos['id']
        doc = db[datos['id']]
        doc['modificadoPor'] = usuario
        doc['modificadoEn']  = datetime.now().isoformat()

        doc['estado']        = "inactivo"
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }

# #-------------------------------------------------------------

def detalleTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]

        #Me busco los usuarios y vehiculos de ese tenant
        usuarios = []       
        vehiculos = []   
         
        urlTenant          = doc.get('urlTenant', '')
        
        if not urlTenant == "":
            
             dbTenant = conexion.getConexionTenant(urlTenant)
             
             filas = dbTenant.view(
                 '_design/usuarios/_view/usuariosPorLoginUsuario',
                 include_docs = True
             )
             for fila in filas:
                 docAdministrador = fila.doc
                 #if docAdministrador.get("activo", False): 
                 usuarios.append(
                     {
                         "id"            : docAdministrador.get("_id"),
                         "nombres"       : docAdministrador.get("nombres"),
                         "correo"        : docAdministrador.get("correo"),
                         "loginUsuario"  : docAdministrador.get("loginUsuario"),
                         "activo"        : docAdministrador.get("activo"),
                         "identificacion": docAdministrador.get("identificacion"),          
                         "telefono"      : docAdministrador.get("telefono"),
                         "idTenant"      : doc.get("_id"),
                     }
  
                 )
                     
             filasVehiculos = dbTenant.view(
                 '_design/vehiculos/_view/vehiculosTodos',
                 include_docs = True
             )
                          
             for filaVehiculo in filasVehiculos:
                 docVehiculo    = filaVehiculo.doc
                 idVehiculo     = docVehiculo.get("_id")
                 filasGps       = db.view(
                                     '_design/GPS/_view/gpsPorVehiculo',
                                     include_docs = True,
                                     startkey = [idVehiculo,0],
                                     endkey = [idVehiculo,{}]
                                 )
                 
                 
                 imeiGps            = ""
                 numSimCard         = ""
                 identificadorGps   = ""
                 tipoGps            = ""
                 if not len(filasGps) == 0:
                     for filaGps in filasGps:
                         docGps             = filaGps.doc
                         idVehiculo         = docVehiculo.get("_id") 
                         imeiGps            = docGps.get("imei",'') 
                         numSimCard         = docGps.get("numSimCard",'') 
                         identificadorGps   = docGps.get("identificadorGPS",'') 
                         tipoGps            = docGps.get("tipo",'') 
                        
                 
                 #if docVehiculo.get("activo", False): 
                 vehiculos.append(
                     {
                         "id"               : docVehiculo.get("_id", ""),
                         "placa"            : docVehiculo.get("placa", ""),
                         "marca"            : docVehiculo.get("marca", ""),
                         "modelo"           : docVehiculo.get("modelo", ""),
                         "imeiGps"          : imeiGps,
                         "numSimCard"       : numSimCard,          
                         "tipoGps"          : tipoGps,
                         "identificadorGps" : identificadorGps,
                         "activo"           : docVehiculo.get("activo"),
                         "opcionesAdicionalesPlataforma" : docVehiculo.get("opcionesAdicionalesPlataforma", None)
                     }
  
                 )
               

        dataResponse = {
            'id'                   : doc['_id'],
            'activo'               : doc.get('activo', ''),
            'nombreGeneral'        : doc.get('nombreGeneral', ''),
            'nit'                  : doc.get('nit', ''),
            'urlTenant'            : doc.get('urlTenant', ''),
            'idImagenLogo'         : doc.get('idImagenLogo', ''),
            'urlImagen'            : settings.NISABU_IMAGE_URL+doc['idImagenLogo'],
            'telefono'             : doc.get('telefono', ''),
            'direccion'            : doc.get('direccion', ''),
            'celularEmergencia'    : doc.get('celularEmergencia', ''),
            'correo'               : doc.get('correo', ''),
            'usuarios'             : usuarios,            
            'vehiculos'            : vehiculos,  
           
        }
        return {
            'success' : True,
            'data'    : dataResponse 
        }    
    except ValidationError as e:
        print "error del try "+e.message
        pass

    return { 'success' : False }

#TODO

def verificarUsuario(db, usuario):
    existeUsuario = False    
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True, 
                    key      = [usuario])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            existeUsuario = True     
        return existeUsuario
    except :
        return existeUsuario


def verificarCorreo(db, correo):
    existeCorreo = False    
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorCorreo',
                    include_docs  = True, 
                    key      = [correo])
        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            existeCorreo = True     
        return existeCorreo
    except:
        return existeCorreo



def crearAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    tennant   = docTenant.get("urlTenant")
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    usuario = datos["loginUsuario"]
    correo  = datos["correo"]
    existeUsuario   =   verificarUsuario(db, usuario)
    existeCorreo    =   verificarCorreo(db, correo)
    if existeUsuario or existeCorreo:
        return { 'success' : False, 
                 'data'    : {
                    'existeUsuario' : existeUsuario,
                    'existeCorreo'  : existeCorreo
                 }
        }
    else:       
        try: 
            doc_id, doc_rev = db.save({
                "activo"		: True,
                "tipoDato"		: "adminTenant",
                "creadoEn"		: datetime.now().isoformat(),
                "modificadoEn"	: datetime.now().isoformat(),
                "modificadoPor"	: usuario,
                "nombres"		: datos["nombres"],
                "identificacion": datos["identificacion"],
                
                "correo"        : datos["correo"],
                "telefono"      : datos["telefono"],
                "loginUsuario"  : datos["loginUsuario"],
                "contrasena"    : moduloAutenticacion.salarConMd5(datos["contrasena"])

            })
            
            return {
                'success' : True,
                'data'    : {
                    'id' : doc_id
                }            
            }
        
        except:
            pass

        return { 'success' : False }

#-------------------------------------------------------------

def compararUsuarios(db, usuario, idDocUsuario):
    docsUsuarios = db[idDocUsuario]
    if docsUsuarios["loginUsuario"] == usuario:
        return True
    else:
        return False    

def buscarUsuarioRepetido(db, usuario, idUsuario):
    existeUsuario = False
    docsUsuarios = []    
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorLoginUsuario',
                    include_docs  = True, 
                    key      = [usuario])

        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            idDoc   = doc.get('_id')
            if idDoc != idUsuario:
                docsUsuarios.append(idDoc) 
        for idDocUsuario in docsUsuarios:
            usuariosIguales =   compararUsuarios(db, usuario, idDocUsuario)
            if usuariosIguales:
                return True
        return False           
    except :
        return existeUsuario

def compararCorreos(db, correo, idDocUsuario):
    docsUsuarios = db[idDocUsuario]
    if docsUsuarios["correo"] == correo:
        return True
    else:
        return False    

def buscarCorreoRepetido(db, correo, idUsuario):
    docsUsuarios = [] 
    existeCorreo = False    
    try:
        filas = db.view('_design/usuarios/_view/usuariosPorCorreo',
                    include_docs  = True, 
                    key      = [correo])
        for fila in filas:
            key     = fila.key
            value   = fila.value
            doc     = fila.doc
            idDoc   = doc.get('_id')
            if idDoc != idUsuario:
                docsUsuarios.append(idDoc) 
        for idDocUsuario in docsUsuarios:
            correosIguales =   compararCorreos(db, correo, idDocUsuario)
            if correosIguales:
                return True
        return False           
    except ValueError:
        return existeCorreo

def editarAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return {
            'success' : False,
            "mensaje" : "NO se encuentra la base de datos"
        }

    docTenant = dbAdmin[datos["idTenant"]]
    Tennant   = docTenant.get("urlTenant")
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    usuario     = datos["loginUsuario"]
    correo      = datos["correo"]
    idUsuario   = datos["id"]
    existeUsuario   =   buscarUsuarioRepetido(db, usuario, idUsuario)
    existeCorreo    =   buscarCorreoRepetido(db, correo, idUsuario)
    if existeUsuario or existeCorreo:
        return { 'success' : False, 
                 'data'    : {
                    'existeUsuario' : existeUsuario,
                    'existeCorreo'  : existeCorreo
                 }
        }
    else:        
        try:
            doc = db[datos['id']]
            doc['modificadoPor'] = usuario
            doc['modificadoEn']  = datetime.now().isoformat()

            doc['nombres']          = datos['nombres']
            doc['identificacion']   = datos['identificacion']
            doc['activo']           = datos['activo']
            doc['correo']           = datos['correo']
            doc['telefono']         = datos['telefono']
            doc['loginUsuario']     = datos['loginUsuario']
            doc['contrasena']       = moduloAutenticacion.salarConMd5( datos['contrasena'] ) if not datos.get('contrasena',"").strip() == ""  else doc['contrasena'] 
            
            db.save(doc)
            
            return {
                'success' : True,
                'data'    : {
                }            
            }
        except ValueError:
            pass

        return {
            'success' : False,
            "mensaje" : "Error desconocido"
        }

#-------------------------------------------------------------

def eliminarAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    
    try:
        idEquipo    = datos['id']
        doc = db[datos['id']]
        doc['modificadoPor'] = usuario
        doc['modificadoEn']  = datetime.now().isoformat()

        doc['activo']        = False
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }

#-------------------------------------------------------------

def detalleAdminTenant( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']

    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))
    
            
    try:
        doc = db[datos['id']]
        dataResponse = {
            'id'                    : doc['_id'],
            'activo'                : doc['activo'],
            'nombres'               : doc.get('nombres', ''),
            'identificacion'        : doc.get('identificacion', ''),
            'correo'                : doc.get('correo', ''),
            'telefono'              : doc.get('telefono', ''),
            'loginUsuario'          : doc.get('loginUsuario', ''),
            'codigoTenant'          : doc.get('urlTenant', ''),
            
        }
        return {
            'success' : True,
            'data'    : dataResponse 
        }    
    except:
        pass

    return { 'success' : False }

#-------------------------------------------------------------

def activarPermisosPlataforma( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))     
    try:
        idPermiso           = datos.get("idPermiso", None)
        listaIdVehiculos    = datos.get("listaIdVehiculos", [])
        for idVehiculo in listaIdVehiculos:
            permisos = []
            docVehiculo = db[idVehiculo]
            #print docVehiculo.get('placa', None)
            permisos = docVehiculo.get('opcionesAdicionalesPlataforma', [])
            #print idPermiso
            if not(permisos == None):
                if not(idPermiso in permisos):
                    permisos.append(u''+str(idPermiso))
                    permisos.sort()
            else:
                permisos = [u''+str(idPermiso)]        
            #print permisos
            docVehiculo['opcionesAdicionalesPlataforma'] = permisos
            db.save(docVehiculo)
        return {
            'success' : True 
        }    
    except ValueError as e:
        print e
    return { 'success' : False }

#-------------------------------------------------------------

def desactivarPermisosPlataforma( peticion ):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    dbAdmin = conexion.getConexionTenant(tenant)

    if dbAdmin == None:
        return { 'success' : False }

    docTenant = dbAdmin[datos["idTenant"]]
    db = conexion.getConexionTenant(docTenant.get("urlTenant"))     
    try:
        idPermiso           = datos.get("idPermiso", None)
        listaIdVehiculos    = datos.get("listaIdVehiculos", [])
        for idVehiculo in listaIdVehiculos:
            permisos = []
            docVehiculo = db[idVehiculo]
            #print docVehiculo.get('placa', None)
            permisos = docVehiculo.get('opcionesAdicionalesPlataforma', [])
            #print idPermiso
            if not(permisos == None):
                if idPermiso in permisos:
                    permisos.remove(u''+str(idPermiso))
            print "---------------------------------------------"   
            print permisos
            docVehiculo['opcionesAdicionalesPlataforma'] = permisos
            db.save(docVehiculo)
        return {
            'success' : True 
        }    
    except ValueError as e:
        print e
    return { 'success' : False }

#-------------------------------------------------------------


# === Auxiliares ===============================================================


