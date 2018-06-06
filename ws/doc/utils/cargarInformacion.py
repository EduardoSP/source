#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import couchdb

couch  = couchdb.Server(url='http://localhost:5984')
db     = couch["geocoder"]

archivoMunicipios = "municipios.csv"
archivoPeajes     = "peajes.csv"
archivoPostes     = "postes.csv"
archivoVias       = "vias.csv"

def cargarMunicipios():
    with open(archivoMunicipios) as csvfile:
        reader = csv.DictReader(csvfile)
        documentosMuicipios = []
        for row in reader:
            try:
                #print row
                print row['municipio'], row['departamento']
                latitud      = float(row['latitud'])
                longitud     = float(row['longitud'])            
                municipio    = u"{}".format(row['municipio'].decode('utf8'))
                departamento = u"{}".format(row['departamento'].decode('utf8'))

                print(u"{} {} {} {}".format(latitud,longitud,municipio, departamento))
                doc = {
                    "tipoDato"      : "puntoreferencia",
                    "creadoEn"      : "2016-03-12T08:07:19Z",
                    "activo"        : True,

                    "latitud"        : latitud,
                    "longitud"       : longitud,
                    "tipoReferencia" : "municipio",
                    "nombre"         : municipio,
                    "departamento"   : departamento	            
                }
                documentosMuicipios.append(doc)
            except:
                pass
            
        print len(documentosMuicipios)              
        db.update(documentosMuicipios)

def cargarPeajes():
    with open(archivoPeajes) as csvfile:
        reader = csv.DictReader(csvfile)
        documentosPeajes = []
        for row in reader:
            try:
                latitud      = float(row['latsig'])
                longitud     = float(row['longsig'])
                nombre       = row['nombre'].decode('utf8')
                departamento = row['territoria'].decode('utf8')
                sector       = row['sector'].decode('utf8')

                doc = {
                    "tipoDato"      : "puntoreferencia",
                    "creadoEn"      : "2016-03-12T08:07:19Z",
                    "activo"        : True,

                    "latitud"        : latitud,
                    "longitud"       : longitud,
                    "tipoReferencia" : "peaje", 
	            "nombre"         : nombre,
	            "departamento"   : departamento,
	            "sector"         : sector         
                }
                print doc
                documentosPeajes.append(doc)
            except:
                print row
                print "ERROR"
                
            
        print len(documentosPeajes)              
        db.update(documentosPeajes)


def cargarPostes():
    vias = leerVias()    
    
    with open(archivoPostes) as csvfile:
        reader = csv.DictReader(csvfile)
        documentosPostes = []
        for row in reader:
            #print "SEPARADOR---------------------"
            #print row
            try:
                latitud      = float(row['lat'])
                longitud     = float(row['lon'])
                nombre       = row['cod_pr'].decode('utf8')                
                cod_via      = row['cod_via']

                tramo        = ""
                sector       = ""

                if cod_via in vias:
                    tramosVias = vias[cod_via]
                    for tramoVia in tramosVias:
                        pr_inicial = tramoVia['pr_inicial']
                        pr_finl    = tramoVia['pr_finl']
                        pr_code    = int(nombre)
                        if pr_code >= pr_inicial and pr_code <= pr_finl:
                            tramo        = tramoVia['tramo']
                            sector       = tramoVia['sector']

                if tramo == "" and sector == "":
                    continue
                doc = {
                    "tipoDato"      : "puntoreferencia",
                    "creadoEn"      : "2016-03-12T08:07:19Z",
                    "activo"        : True,

                    "latitud"        : latitud,
                    "longitud"       : longitud,
                    "tipoReferencia" : "poste", 
                    "nombre"         : nombre,
                    "tramo"          : tramo,
                    "sector"         : sector         
                }
                #print doc
                documentosPostes.append(doc)
            except:
                #print row
                print "ERROR"
                #return
                
            
        print len(documentosPostes)
        #print documentosPostes
        db.update(documentosPostes)

def leerVias():
    vias = {}
    with open(archivoVias) as csvfile:
        reader = csv.DictReader(csvfile)        
        for row in reader:
            try:
                codigo_via   = row['codigo_via']
                pr_inicial   = int(row['pr_inicial'])
                pr_finl      = int(row['pr_finl'])
                tramo        = row['tramo'].decode('utf8')
                sector       = row['sector'].decode('utf8')
                
                if not codigo_via in vias:
                    vias[codigo_via] = []

                docVia = {
                    'codigo_via' : codigo_via,
                    'pr_inicial' : pr_inicial,
                    'pr_finl'    : pr_finl,
                    'tramo'      : tramo,
                    'sector'     : sector                    
                }
                
                vias[codigo_via].append(docVia)                    
            
                
            except:
                print row
                print "ERROR"
    
    return vias
        
def borrarPuntosReferencia():
    filas = db.view(
        '_design/geocoder/_view/puntosreferencialongitud',
        include_docs = True
    )
    
    
    for fila in filas:
        doc = fila.doc
        print doc["_id"]
        db.delete(doc)
#------------------------------------
#cargarMunicipios()
#cargarPostes()
#cargarPeajes()
#borrarPuntosReferencia()
