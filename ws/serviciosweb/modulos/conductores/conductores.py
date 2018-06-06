# -*- coding: utf-8 -*-
import hashlib
import uuid
import logging
import time
from django.core.urlresolvers import reverse
from django.http                import HttpResponse
from jsonschema               import validate, ValidationError
from django.conf              import settings
from ..conexion               import conexion
from datetime                 import datetime
from ..autenticacion          import autenticacion as moduloAutenticacion
from django.db              import IntegrityError, transaction
import time
import csv

def listarConductores(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/conductores/_view/listarConductores',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          if not(doc['eliminado']):
		      dataRaw.append({
		      	'id' 				: doc['_id'],
		      	'cedula'      		: doc['cedula'],
		      	'nombres'    		: doc['nombres'],
		      	'apellidos'   		: doc['apellidos'],
		      	'fechaNacimiento'	: doc['fechaNacimiento'],
		      	'celular'			: doc['celular'],
		      	'activo'			: doc['activo'],
		      	'eliminado'			: doc['eliminado']
		      	})            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


def crearConductor(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }
    try: 
        cedula  =   datos["cedula"]
        if existeConductor(db,cedula) == None:
            doc_id, doc_rev = db.save({
                "tipoDato"        	: "conductores",
                "creadoEn"        	: datetime.now().isoformat(),
                "modificadoEn"    	: datetime.now().isoformat(),
                "modificadoPor"   	: usuario,
                "cedula"			: cedula,
                "nombres"			: datos["nombres"],
                "apellidos"			: datos["apellidos"],
                "fechaNacimiento"	: datos["fechaNacimiento"],
                "celular"			: datos["celular"],
                "activo"          	: True,
                "eliminado"         : False
            })
            return { 'success' : True }
        else:
            return { 
                'success' : False,
                'error' : "La cédula se encuentra registrada" 
                }

    except ValueError:
        return { 'success' : False }


def eliminarConductor(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]
        doc['modificadoPor'] = usuario
        doc['modificadoEn']  = datetime.now().isoformat()
        doc['eliminado']     = True
        db.save(doc)
        
        return {
            'success' : True,
            'data'    : {
            }            
        }
    except:
        pass

    return { 'success' : False }


def detalleConductor(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant      = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        doc = db[datos['id']]
        data= {
        	"cedula"			: doc["cedula"],
            "nombres"			: doc["nombres"],
            "apellidos"			: doc["apellidos"],
            "fechaNacimiento"	: doc["fechaNacimiento"],
            "celular"			: doc["celular"],
            "activo"          	: doc["activo"],           
        }          
        return {
            'success' : True,
            'data'    : data         
        }
    except:
        pass
    return { 'success' : False }


def editarConductor(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        bandera         = True
        docConductor    = None
        idDocConductor  = datos['id']
        cedula          = datos.get('cedula', '')
        docConductor    = existeConductor(db, cedula)
        if not(docConductor == None) and not(docConductor['_id'] == idDocConductor):
            bandera = False    

        if bandera:    
            doc = db[datos['id']]
            doc['modificadoPor']         = usuario
            doc['modificadoEn']          = datetime.now().isoformat()
            doc['activo']                = datos.get('activo',   doc['activo'])
            doc['cedula']         		 = datos.get('cedula',    doc['cedula'])
            doc['nombres']               = datos.get('nombres',    doc['nombres'])
            doc['apellidos']      		 = datos.get('apellidos', doc['apellidos'])
            doc['fechaNacimiento']       = datos.get('fechaNacimiento', doc['fechaNacimiento'])
            doc['celular']               = datos.get('celular',       doc['celular'])
            db.save(doc)
            #si activo es falso busca si tiene vehiculo asignado y le quita la asignacion al vehiculo
            if not(doc['activo']):
                #obtengo el vehiculo del conductor
                filas = db.view('_design/conductores/_view/listarVehiculosPorConductor',
                            include_docs  = True,
                            key      = [datos['id']])

                for fila in filas:
                  key = fila.key
                  value = fila.value
                  docVehiculo = fila.doc
                  docVehiculo['conductor'] = "" 
                  db.save(docVehiculo) 
           
            return {
                'success' : True,
                'data'    : {
                }            
            }
        else:
            return { 
                'success' : False,
                'error' : "La cédula se encuentra registrada a otro conductor" 
                }
            
    except ValidationError as e:
        print "error del try "+e

    return { 'success' : False }



def descargarArchivoCsvConductores(usuario, tenant):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_{}.csv"'.format('DocumentosConductores', datetime.now().isoformat().split('.')[0])
    
    titulosCeldas = [ 
        'cedula', 
        'nombres', 
        'apellidos', 
        'fechaNacimiento', 
        'celular',
        'activo']
    
    descripcionCeldas = [
        u'C.C. Conductor'.encode('latin1'),
        u'Nombres'.encode('latin1'),
        u'Apellidos'.encode('latin1'),
        u'Fecha de nacimiento'.encode('latin1'),
        u'Celular'.encode('latin1'),
        u'Estado'.encode('latin1')
        ]
    writer = csv.writer(response)
    #writer.writerow(titulosCeldas)
    writer.writerow(descripcionCeldas)
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view('_design/conductores/_view/listarConductores',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          if not(doc['eliminado']):
            datoConductor = []
            for titulo in titulosCeldas:
                dato = doc.get(titulo, '')
                if dato == None:
                    dato = ''
                if titulo == 'activo':
                    if dato:
                        dato = 'Activo'
                    else:
                        dato = 'Inactivo'   
                datoConductor.append(dato.encode('latin1'))
            writer.writerow(datoConductor)                  
        return response        
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }                    
    

def cargarArchivoCsvConductores(peticion, request):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    
    db = conexion.getConexionTenant(tenant)
    if db == None:
        return { 'success' : False }
    
    try:
        
        reader = None
        
        if 'archivo' in  request.FILES:
            archivo     = request.FILES['archivo']
            reader      = csv.reader(archivo,delimiter = ',')#Delimitador es una coma
           
        else:
            raise ValueError(u'No se envió archivo')

        cabeceras       = []
        indexCsv        = 0
        doc             = None
        docConductores  = None
        for row in reader:
            conductores = {}                    
            if indexCsv >= 1:      
                for i in range(0, len(row)):
                    celda   = row[i]
                    celda   = celda.decode('iso-8859-1').encode('utf8')
                    #logging.warning("Fila: {} - {}".format(i,celda))
                    if i == 0:
                        doc     = existeConductor(db,celda)
                        cedula = celda
                    if not(doc == None):
                        #existe cedula entonces se actualizan los datos
                        idDocConductores    = doc.get('_id')
                        docConductores      = db[idDocConductores]
                        print "pase porr aqui--------------"
                        if i == 1:
                            docConductores["nombres"] = celda
                            db.save(docConductores)
                        if i == 2:
                            docConductores["apellidos"] = celda
                            db.save(docConductores)
                            print "celda apellidos {} ".format(celda)
                        if i == 3:
                            docConductores["fechaNacimiento"] = celda
                            db.save(docConductores)
                        if i == 4:
                            docConductores["celular"] = celda
                            db.save(docConductores)
                        if i == 5:
                            if celda == "Activo":
                                docConductores["activo"] = True
                                db.save(docConductores)
                            else:
                                docConductores["activo"] = False
                                db.save(docConductores)

                                
                    else:
                        #No existe la cedula, entonces se guardan los datos
                        if i == 1:
                            nombres = celda;
                        if i == 2:
                            apellidos = celda
                        if i == 3:
                            fechaNacimiento = celda
                        if i == 4:
                            celular = celda
                if doc == None:
                    #Crea conductores
                    doc_id, doc_rev = db.save({
                        "tipoDato"          : "conductores",
                        "creadoEn"          : datetime.now().isoformat(),
                        "modificadoEn"      : datetime.now().isoformat(),
                        "modificadoPor"     : usuario,
                        "cedula"            : cedula,
                        "nombres"           : nombres,
                        "apellidos"         : apellidos,
                        "fechaNacimiento"   : fechaNacimiento,
                        "celular"           : celular,
                        "activo"            : True,
                        "eliminado"         : False
                    })
                else:
                    #Actualizo informacion"
                    doc = None     

            indexCsv += 1    

        return {
            'success' : True
        }                     

    except KeyError as e:
        return {
            'success' : False,
            'error' : "KeyError:" + e.message
        }


#=============================================================================

def existeConductor(db,cedula):
    doc = None
    try:
        dataRaw = []
        filas = db.view('_design/conductores/_view/listarConductores',
                    include_docs  = True,
                    key      = [cedula])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
        return doc
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }

#=============================================================================


def pickerConductores(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    numeroOpcionHabilitadaPlataforma = datos.get("numeroOpcionHabilitadaPlataforma",None)
    
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False, 'mensaje': "existe el tenant" }

    try:
        dataRaw = []
        filas = db.view(
                        '_design/conductores/_view/listarConductores',
                        include_docs  = True
                        )
        
        for fila in filas:
          key               = fila.key
          value             = fila.value
          doc               = fila.doc
          eliminado         = doc.get('eliminado','')
          activo         = doc.get('activo','')
          if not(eliminado) and activo:
              if not(numeroOpcionHabilitadaPlataforma == None):
                  idConductor   = doc.get('_id','')
                  estaConductor = validarConductorPermisoHabilitado(db, idConductor, numeroOpcionHabilitadaPlataforma)
                  if estaConductor:
                    # valida el permiso de la plataforma segun el numeroOpcionHabilitadaPlataforma
                      dataRaw.append(
                          {
                            'id'                : doc.get('_id',''),
                            'cedula'            : doc.get('cedula', ''),
                            'nombres'           : doc.get('nombres', ''),
                            'apellidos'         : doc.get('apellidos', ''),
                            'fechaNacimiento'   : doc.get('fechaNacimiento',''),
                            'celular'           : doc.get('celular','')
                          }
                    )  
              else: 
                 # sigue el paso normal si no se envia numeroOpcionHabilitadaPlataforma
                  dataRaw.append(
                      {
                        'id'                : doc.get('_id',''),
                        'cedula'            : doc.get('cedula', ''),
                        'nombres'           : doc.get('nombres', ''),
                        'apellidos'         : doc.get('apellidos', ''),
                        'fechaNacimiento'   : doc.get('fechaNacimiento',''),
                        'celular'           : doc.get('celular','')
                      }
                    )            
        return {
            'success' : True,
            'data'    : dataRaw
        }
    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


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



def asignarConductor(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:

        doc = db[datos['idVehiculo']]
        doc['modificadoPor']         = usuario
        doc['modificadoEn']          = datetime.now().isoformat()
        doc['conductor']             = datos.get('idConductor', '')
        db.save(doc)
        return {
            'success' : True,
            'data'    : {
            }            
        }
            
    except ValidationError as e:
        print "error del try "+e

    return { 'success' : False }


def verificarConductorAsignado(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)
    doc = None
    try:
        idConductor = datos['idConductor']
        filas = db.view('_design/conductores/_view/listarVehiculosPorConductor',
                    include_docs  = True,
                    key      = [idConductor])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
        if not(doc == None):
            return {
                'success' : True,
                'existe'  : True            
            }
        else:
            return {
                'success' : True,
                'existe'  : False            
            }

    except ValueError:
        pass

    return { 'success' : False, 'mensaje':"error desconocido" }


def reAsignarConductor(peticion):
    autenticacion = peticion['autenticacion']
    datos         = peticion['data']
    usuario       = autenticacion['usuario']
    tenant        = autenticacion['tenant']
    db = conexion.getConexionTenant(tenant)

    if db == None:
        return { 'success' : False }

    try:
        docVehiculoDatos    = db[datos['idVehiculo']]

        idConductorDatos    = datos['idConductor']
        #obtengo el vehiculo del conductor
        filas = db.view('_design/conductores/_view/listarVehiculosPorConductor',
                    include_docs  = True,
                    key      = [idConductorDatos])

        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc

        if not(docVehiculoDatos['conductor'] == idConductorDatos): 
            doc['conductor'] = "" 
            db.save(doc) 
            docVehiculoDatos['conductor'] = idConductorDatos
            db.save(docVehiculoDatos)
        return {
            'success' : True,
            'data'    : {
            }            
        }
            
    except ValidationError as e:
        print "error del try "+e

    return { 'success' : False }

