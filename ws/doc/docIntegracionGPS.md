#Fleetbi Integración GPS

# Se crea base de datos FleetBi para guardar el documento de los GPS

#Webservice NUevo!!!!

#Registrar Posiciones del GPS

*Nombre:* wsregistrarPosicionesGPS 

*URL:* `http://54.243.219.114:56899/ws/botonPanicoGPS`

*Descripción:* ws que registra un botón de pánico, latitud y longitud
puede ser "0", igual se recibe y se usa el punto mas reciente que
existe en fleet.

```
//Peticiónn
{
    "autenticacion" : {
        "usuario" : "admin",
	"token" : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant" : "exxonmobil"
    },
    "data" : {
        "posiciones"            : [
            {
		"latitud"        : "3.4206",
		"longitud"       : "-76.5222",
		"velocidad"      : "30.35 km/h",
		"horaRegistrada" : 	"2016-08-19T08:07:19Z"	
            }
        ],
        "identificadorGPS"  : "20140803"
    }
}

//Respuesta
{
  "success" : true
}
```

#==============================================================================
#A partir de esta linea se van a definir los documentos del sistema Fleetbiweb

### GPS:

*Documentos:*
```
{
    "tipoDato"      	: "GPS",
    "creadoEn"      	: "2016-03-12T08:07:19Z",
    "modificadoEn"  	: "2016-03-13T05:07:19Z",
    "modificadoPor" 	: "Pablo Solarte",
    "marca"				: "KEnWorth",
    "modelo"			: "2014",
    "identificadorGPS" 	: "20160302",
    "imei"    			: "sajljallk22112",
    "numSimCard"		: "+5752255000",
    "tipo"				: "I857422451",
    "tenant"			: "Exxonmobil",
    "idVehiculo"    	: "95ea81741bbfba959550827b15003985",
    "activo"        	: true
}
```

{
    "tipoDato"        : "GPS",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "marca"       : "KEnWorth",
    "modelo"      : "2014",
    "identificadorGPS"  : "20160303",
    "imei"          : "sajljallk22112",
    "numSimCard"    : "+5752255000",
    "tipo"        : "I857422451",
    "tenant"      : "Exxonmobil",
    "idVehiculo"      : "ed41642e1f5c98f28f039448c5068edf",
    "activo"          : true
}

### inspeccionImagen:

*Documentos:*
```
{
    "tipoDato"      		  : "inspeccionImagen",
    "fechaHoraSolicitud"	: "2016-03-12T08:07:19Z",
    "estado"				      : "pendiente","entregado"
    "identificadorGPS"		: "sajljallk22112",
    "idVehiculo"    		  : "95ea81741bbfba959550827b15003985",
    ##esDirecta true cuando se presiona directamente desde el boton
    ##false cuando es registrado de una zona o una vigilancia
    "esDirecta"           : true, false
    "esPanico"           : true, false      
    "idZona"              :[],
    "idVigilancia"        :[],
    "activo"        		  : true
}
```

{
   "tipoDato": "inspeccionImagen",
   "fechaHoraSolicitud": "2016-09-01T08:11:00Z",
   "estado": "pendiente",
   "identificadorGPS": "sajljallk22112",
   "idVehiculo": "95ea81741bbfba959550827b15003985",
   "esDirecta": true,
   "idZona": [
   ],
   "idVigilancia": [
   ],
   "activo": true
}


##vistas

### vista GPS
```
{
   "_id": "_design/GPS",
   "views": {
       "GPS": {
           "map": "function(doc){if(doc.tipoDato == \"GPS\" && doc.activo){ emit([doc.idVehiculo, doc.tenant], null );}}"
       },
       "idVehiculoGPS": {
           "map": "function(doc){if(doc.tipoDato == \"GPS\" && doc.activo){ emit([doc.identificadorGPS, doc.tenant], null );}}"
       },
       "gpsPorIdVehiculo": {
           "map": "function(doc){\n\tif(doc.tipoDato == \"GPS\" && doc.activo){ \n\t\temit([doc.idVehiculo], null );\n\t}\n}"
       },
       "gpsPorNumSimCard": {
           "map": "function(doc){\n\tif(doc.tipoDato == \"GPS\" && doc.activo){ \n\t\temit([doc.numSimCard], null );\n\t}\n}"
       },
       "gpsPorImei": {
           "map": "function(doc){\n\tif(doc.tipoDato == \"GPS\" && doc.activo){ \n\t\temit([doc.imei], null );\n\t}\n}"
       }        
   }
}
```

### vista Inspección GPS
```
{
   "_id": "_design/inspeccionGPS",
   "views": {
       "inspeccionImagen": {
           "map": "function(doc){if(doc.tipoDato == \"inspeccionImagen\" && doc.activo && doc.estado == \"pendiente\"){ emit([doc.identificadorGPS, doc.fechaHoraSolicitud], null );}}"
       },
       "verRegistrosInspeccionImagen":{
          "map": "function(doc){if(doc.tipoDato == \"inspeccionImagen\" && doc.activo){ emit([doc.identificadorGPS, doc.fechaHoraSolicitud], null );}}"
     },
       "imagenesNoDirectasPendientesVehiculo":{
          "map": "function(doc){if(doc.tipoDato == \"inspeccionImagen\" && doc.activo && doc.estado == \"pendiente\" && !doc.esDirecta){ emit([doc.idVehiculo], null );}}"
     }
   }
}
```

### vista Posicion Vehiculos punto anterior
#esta vista es para aclarar lo que se utilizo para traer la ultima posición para integrar la información con el GPS. La vista definida en posicion veh��culos en doc.md

```
{
   "_id": "_design/posicionVehiculos",
   "views": {
       "anteriorPosicionVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){ emit([doc.idVehiculo, doc.horaRegistrada ], null );}}"
       }
   }
}
```
### vista obtener idZonaMonitoreada
#obtiene el identificador de la zona monitoreada en el documentos zona alramas. La vista definida en la bd FleetTenant

```
{
   "_id": "_design/idZonaMonitoreada",
   "views": {
       "idZonaMonitoreada": {
           "map": "function(doc){if(doc.tipoDato == \"zonaAlarma\" && doc.activo){ emit([doc._id, doc.idZona ], null );}}"
       }
   }
}
```


## web services


### Listado de GPS

*Nombre:* wslistadoGPS
*URL:* `http://localhost/ws/listadoGPS`
*Descripción:* trae el listado de los GPS esta será una función auxiliar de SolicitarCapturaImagen, fines de prueba se estableció esta petición
```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc"
  },

  "data" : {
  "idVehiculo" : "95ea81741bbfba959550827b15003985"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "identificadorGPS" : "sajljallk22112"
    }
  ]
}



### SolicitarCapturaImagen
q
*Nombre:* wssolicitarCapturaImagen
*URL:* `http://localhost/ws/solicitarCapturaImagen`
*Descripción:*  solicita al GPS la captura de una imagen enviando la posición donde se va a guardar la respuesta, el identificadorGPS y un identificadorSolicitud(_id). Se hace en otro webService(la respuesta esperada es la creación de la foto en esa posición.Además la latitud, longitud, el identificadorGPS la fecha de creación (creadoEn) que se guardara en un archivo jsonData 95ea81741bbfba959550827b15003985.txt)
//peticion

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  	"idVehiculo"	: "95ea81741bbfba959550827b15005700"
  }
}

//Respuesta
{
    "success" : true
}
```
#=====================================================================================


### examinarImagenesPendientes

*Nombre:* wsexaminarImagenesPendientes
*URL:* `http://localhost/ws/examinarImagenesPendientes`
*Descripción:* Consulta las solicitudes pendientes y verifica si encuentra la carpeta creada. Si la encuentra cambia el estado del pendiente en el documento inspeccionImagen y se extrae la información del archivo JsonData y obtiene la imagen
Este archivo se encontrara en management/commands/examinarImagenesPendientes


#Registrar Posiciones del GPS

*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`
*Descripción:* ws que registra el listado de posiciones que envía el GPS para ser guardados en la base de datos 
//peticion

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.4206", "longitud": "-76.5222","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "6.2359", "longitud": "-75.5751","velocidad": "30.35 km/h", "horaRegistrada": "2016-08-19T08:07:19Z"},
  			{"latitud": "10,4137", "longitud": "-75,5336", "velocidad": "30.35 km/h", "horaRegistrada": "2016-08-19T08:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

```
# A partir de esta linea comienzan las pruebas para las posiciones de los GPS para saber si pertenecen a una zonaAlarma
##documento de pruebas

```
{
    "tipoDato"      : "posicionVehiculos",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "horaRegistrada": "2016-08-25T08:07:19Z",
    "horaRecibida"  : "2016-08-25T08:07:19Z",
    "latitud"       : "3.502652",
    "longitud"      : "-76.536543",
    "velocidad"     : "30.35 km/h",
    "idVehiculo"    : "95ea81741bbfba959550827b15003985",
    "estado"        : "activo",
    "activo"        : true,
    "ultimaPosicion": true,
    "zonaAlarmas" : ["992604b50a790a6831b1380908001c30","992604b50a790a6831b13809080039ed"],
    "programacionVigilancia" : []

}
```
doc id = 992604b50a790a6831b13809080042c4

###===================================================
### zona Alarma
{
    "tipoDato"      : "zonaAlarma",
    "fecha" : "2016-03-12",
    "horaInicio"  : "07:19",
    "horaFin"  : "07:19",
    "estado": "Finalizado",
    "idVehiculo": "95ea81741bbfba959550827b15003985",
    "idZona" : "3e8f127632561e88b4acd1d8f000626a",
    "activo" : true
}

{
    "tipoDato"      : "zonaAlarma",
    "fecha" : "2016-03-12",
    "horaInicio"  : "11:19",
    "horaFin"  : "12:19",
    "estado": "Finalizado",
    "idVehiculo": "95ea81741bbfba959550827b15003985",
    "idZona" : "992604b50a790a6831b13809080039ed",
    "activo" : true
}

###===================================================



#Registrar Posiciones del GPS PUEBAS---------------

*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`
*Descripción:* ws que registra el listado de posiciones que envía el GPS para ser guardados en la base de datos 
//peticion

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.502652", "longitud": "-76.536543","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "3.529589", "longitud": "-76.336639","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "4.783922", "longitud": "-75.595620","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

```
#Registrar Posiciones del GPS PUEBAS 2---------------

*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`
*Descripción:* ws que registra el listado de posiciones que envía el GPS para ser guardados en la base de datos 
//peticion

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.502652", "longitud": "-76.536543","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

```

#Registrar Posiciones del GPS PUEBAS 3 zonas compartidas---------------

*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`
*Descripción:* ws que registra el listado de posiciones que envía el GPS para ser guardados en la base de datos 
//peticion

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "4.049706", "longitud": "-76.201538","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
   			{"latitud": "3.366509", "longitud": "-76.540243","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

```

#prueba 4

//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.502652", "longitud": "-76.536543","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "3.529589", "longitud": "-76.336639","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "4.783922", "longitud": "-75.595620","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "3.502652", "longitud": "-76.536543","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

```



//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.364298", "longitud": "-76.539258","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"},
  			{"latitud": "3.413908", "longitud": "-74.654558","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-19T08:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

```

esta en la zona 1 "latitud": "3.443949", "longitud": "-76.531007"

esta en la zona 1 y la zona 2 3.364298, -76.539258


no esta en la zona "latitud": "3.413908", "longitud": "-74.654558"


//================================================================================
registrarPosiProgramacionVigilancia es un punto que tiene la programacion vigilancia
#la vista consultarRangoFechasAlarmas se encuentra en el archivo doc.md
#prueba programacion vigilancia
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`

//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.364298", "longitud": "-76.539258","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-08-30T10:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//Respuesta
{
  "success" : true
}

//=================================================================================

# segundo punto de prueba para saber si esta cerca del anterios
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`

//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.364300", "longitud": "-76.539300","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:20Z"}
      ],
    "identificadorGPS"  : "sajljallk22112"  
  }
}

//Respuesta
{
  "success" : true
}


//=================================================================================

# tercer punto de prueba para saber si esta cerca del anterios
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost/ws/registrarPosicionesGPS`

//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.364400", "longitud": "-76.539400","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:20Z"}
      ],
    "identificadorGPS"  : "sajljallk22112"  
  }
}

//Respuesta
{
  "success" : true
}

//==========================================================================
#Se ha isntalado la siguiente libreria en python
#pip install requests 
# ws que permite solicitar al gps la toma de una foto
//Petición
# Solicitar toma de foto
*Nombre:* wssolicitarTomarFoto
*URL:* `http://localhost:8080/ws/solicitarTomarFoto`

//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc"
  },

  "data" : {
      "idFoto"   : "1212ui12i1u21i2",
      "rutaFoto" : "/tmp/fotos/",
      "idGps"    : "20160101"
  }    
}

//Respuesta
{
  "success" : true
}


# prueba captura imagen plataforma con permisos
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://localhost:8080/ws/registrarPosicionesGPS`

//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": 6.2527, "longitud": -75.5859,"velocidad": 30, "horaRegistrada":   "2017-12-11T10:15:20Z", "dataTraccar": {}, "estaMotorEncendido" : false}
      ],
    "identificadorGPS"  : "11235556"  
  }
}