
#Fleetbi

#=======================================================================================
Desde aqui se va a definir las partes nuevas de  fleet

## Base de datos modelo

Para crear las base de datos de modelo se tiene una base dedatos base,
'fleetbimodelo' esta tendrá todos los design cprrespondientes sin
ningun dato, cuando se cree una nueva base de datos se hará una copia
de estos diseños que se encuentren en esta base de datos.

## Usuarios
```
{
   "_id": "3f84d2f0510aea66ac92c2b42d004505",
   "_rev": "1-d8259e38e3d95500df64c5610c282d08",
   "modificadoPor": "huvadmin451236",
   "tipoDato": "superAdministrador",
   "nombres": "admin",
   "correo": "administrador@gmail.com",
   "loginUsuario": "admin",
   "activo": true,
   "creadoEn": "2016-10-18T12:06:17.789000",
   "identificacion": "542355",
   "contrasena": "396d6174f78903caed6218a115202a72",
   "telefono": "3799764",
   "modificadoEn": "2016-10-18T12:13:44.592000",
   "ultimoIngresoAlarmas": 1482355653.846376
}

{
   "_id": "_design/usuarios",
   "views": {
       "usuariosPorContrasena": {
           "map": "function(doc){if(doc.tipoDato == \"superAdministrador\"){ emit([doc.loginUsuario, doc.contrasena, \"superAdministrador\"], null );}}"
       },
       "usuariosPorLoginUsuario": {
           "map": "function(doc){if(doc.tipoDato == \"superAdministrador\" && doc.activo){ emit([doc.loginUsuario], {perfil:\"superAdministrador\"} );}}"
       },
       "usuariosPorCorreo": {
           "map": "function(doc){if(doc.tipoDato == \"superAdministrador\" && doc.activo){ emit([doc.correo], {perfil:\"superAdministrador\"} );}}"
       }       
   }
}
```

## Autenticacioes

```
{
   "_id": "_design/autenticaciones",
   "views": {
       "autenticacion": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\"){ emit([doc.loginUsuario, doc.token], null );}}"
       }
   }
}
```

# Webservices Design

## Picker Tenants
*Nombre:* wsPickerTenants
*URL:* `http://localhost/ws/pickerTenants`
*Descripción:* Trae un listado e tenants para pintar en un picker

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
    "idVehiculo"  : "95ea81741bbfba959550827b15005700"
  }
}

//Respuesta
{
    "success" : true,
    "data"    : [{
			"id"     : "exxonmobil",
			"nombre" : "Exxon mobil de colombia"
	}]
}

```


## Listar Tenants
*Nombre:* wslistarTenants
*URL:* `http://localhost/ws/listadoTenants`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : [
	{
            "id"               : "8912121298129",
            "activo"           : true,
            "nombreGeneral"    : "Exxon mobil de colombia",
           
            "nit"              : "8218912",
            "urlTenant"        : "http://fleetbi/exxonmobil/login",
            "idImagenLogo"          : "http://fleetbi/exxonmobil/login",
            "telefono"         : "271827812",
            "direccion"        : "cra 152 1288121892",
            "celularEmergencia"        : "3105642147",
	}
    ]
}
```

## Crear Tenant 
*Nombre:* wsCrearTenant
*URL:* `http://localhost/ws/crearTenant`
*Descripción:* El idImagenLogo es el id de nisabu, el cliente es el urlTenant, que es lo que se usa en la url.

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
	"nit"           : "56468789355",
	"urlTenant"     : "ecopetrol",
	"nombreGeneral" : "Exopetrol SA",
	"idImagenLogo"  : "1911e9b72f67bf6ac72b6ace06002cef",
	"telefono"      : "831928192891",
	"direccion"     : "cra 172 nu j21212",
	"celularEmergencia"        : "3105642147",
	"correo"		: "fleetbi@gmail.com"	
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {}
}
```

## Detalle Tenant 
*Nombre:* wsDetalleTenant
*URL:* `http://localhost/ws/detalleTenant`
*Descripción:* El idImagenLogo es el id de nisabu, el cliente es el urlTenant, que es lo que se usa en la url. Administradores es el arreglo que devuelve los usuarios administradores de un cliente Tenant

```
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "administracion" 
		},

    "data" : {	
		"id"           : "56468789355",
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
	    			'id'                   : "6552625565655554sf4f559",
		            'activo'               : true,
		            'nombreGeneral'        : "Exxon Mobil de Colombia",
		            'nit'                  : "555458545644"
		            'urlTenant'            : "fleetbiexxonmobil",
		            'idImagenLogo'         : "1911e9b72f67bf6ac72b6ace06002cef",
		            'telefono'             : "831928192891",
					"direccion"     		: "cra 172 nu j21212",
		            'urlImagen'              : "http://localhost/nisabu/image/1911e9b72f67bf6ac72b6ace06002cef",
		            "celularEmergencia"        : "3105642147",	  
		            'usuarios'      	   : usuarios,  
		            'correo'			   : "fleetbi@gmail.com"       
    			}
}
```

## Editar Tenant 
*Nombre:* wsEditarTenant
*URL:* `http://localhost/ws/editarTenant`
*Descripción:* El idImagenLogo es el id de nisabu, el cliente es el urlTenant, que es lo que se usa en la url.

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
    		"id"			:"d5569893cs656565",
    		"activo"           : true,
			"nit"           : "56468789355",
			"urlTenant"     : "ecopetrol", #en la interfaz este dato no se modifica
			"nombreGeneral" : "Exopetrol SA",
			"idImagenLogo"  : "1911e9b72f67bf6ac72b6ace06002cef",
			"telefono"      : "831928192891",
			"direccion"     : "cra 172 nu j21212",
			"celularEmergencia"        : "3105642147",
			"correo"		: "fleetbi@gmail.com"	
    } 
  
}

//Respuesta
{
    "success" : true,
    "data"    : {}
}
```

## Crear Usuario Admin tenant 
*Nombre:* wsCrearAdminTenant
*URL:* `http://localhost/ws/crearAdminTenant`
*Descripción:* El idImagenLogo es el id de nisabu, el cliente es el urlTenant, que es lo que se usa en la url.

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
							
				"idTenant"           : "545454545fsf415s4dfxc",	
	            "nombres"		: "Carlos arturo Serrano",
	            "identificacion": "256822444",
	            "correo"        : "carlosarturo@gmail.com",
	            "telefono"      : datos["telefono"],
	            "loginUsuario"  : "admin",
	            "contrasena"    : "123455"	
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
    			'id' : "545445656cvxzz454545s"
    			}
}
```

## Detalle usuario Admin Tenant 
*Nombre:* wsDetalleTenant
*URL:* `http://localhost/ws/detalleTenant`
*Descripción:* El idImagenLogo es el id de nisabu, el cliente es el urlTenant, que es lo que se usa en la url. Administradores es el arreglo que devuelve los usuarios administradores de un cliente Tenant

```
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "administracion" 
    },

    "data" : {	
		"id"           : "56468789355",
	
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
	    			'id'                   : "6552625565655554sf4f559",
		            'nombres'        	   : "Carlos",
		            'identificacion'       : "11435628956"
		            'correo'               : "carlos@gmail.com",
		            'activo'			   : true, 
		            'telefono'             : "831928192891",
					"loginUsuario"     		: "carlos",
					'codigoTenant'          :  "terpel",
    			}
}
```

## Editar usuario Admin Tenant 
*Nombre:* wsEditarTenant
*URL:* `http://localhost/ws/editarTenant`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
	    		"activo" : true,
				"nombres" : "Fabio soto",
				"identificacion"  : "11425623214",
				"correo"		: "fabio@gmail.com"	
				"telefono"      : "3105235689",
				"loginUsuario"     : "fabioAdmin",
				"contrasena"        : "123456",
				
    } 
  
}

//Respuesta
{
    "success" : true,

    "data"    : {}
}
```

## Eliminar usuario Admin Tenant 
*Nombre:* wsEditarTenant
*URL:* `http://localhost/ws/editarTenant`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
	    		"activo" : true,
				"nombres" : "Fabio soto",
				"identificacion"  : "11425623214",
				"correo"		: "fabio@gmail.com"	
				"telefono"      : "3105235689",
				"loginUsuario"     : "fabioAdmin",
				"contrasena"        : "123456",
				
    } 
  
}

//Respuesta
{
    "success" : true,
    "data"    : {}
}
```

## Listar Gps
*Nombre:* wslistarGps
*URL:* `http://localhost/ws/listadoGps`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : [
					{
			            "id"                : "8912121298129",
			            "activo"            : true,
			            "observaciones"     : "Se desconecto por motivos de fallas frecuentes",
			            "identificadorGPS"  : "892223252",
			            "numSimCard"        : "http://fleetbi/exxonmobil/login",
			            "tipoGps"          	: "http://fleetbi/exxonmobil/login",
			            "tenant"         	: "271827812",
			            "imei"         		: "271827812",
			            "idVehiculo"        : "cra 152 1288121892",
			            "placaVehiculo"        : "FGB456"
			          
			}
    ]
}
```

## Crear Gps tenant 
*Nombre:* wsCrearGps
*URL:* `http://localhost/ws/crearGps`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
							
				"identificadorGps"      : "545454545fsf415s4dfxc",	
	            "numeroSimCard"			: "898222366",
	            "tipo"					: "256822444",
	            "imei"        			: "889321259",
	            "observaciones" 		: "Este gps esta funcionando perfectamente"
    		 }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
    			
    			}
}
```

## Detalle gps
*Nombre:* wsDetalleGps
*URL:* `http://localhost/ws/detalleGps`
*Descripción:* 

```
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "administracion" 
    },

    "data" : {	
		"id"           : "56468789355",
	
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
	    			'id'                   : "6552625565655554sf4f559",
		            'observaciones'        : "Esta en perfectas condiciones",
		            'identificadorGPS'     : "11435628956"
		            'imei'                 : "8512154546",
		            'activo'			   : true, 
		            'numSimCard'           : "3105332412",
					"tipoGps"     		   : "VT1000",
					'tenant'          	   :  "terpel",
					'idVehiculo'           : "6552625565655554sf4f559",
					"placaVehiculo"        : "FGB456"
    			}
}
```

## Editar gps
*Nombre:* wsEditarGps
*URL:* `http://localhost/ws/editarGps`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
    			'id'			: "5776d71ff8f8442ca8326d04987a9bdc",
	    		"activo" 		: true,
				"identificadorGPS" 		: "4212121345847878",
				"numSimCard"  	: "3124568256",
				"tipo"			: "VT1000"	
				"imei"      	: "84512315465454",
				"observaciones"     : "esta en un estado elegante "
			
				
    } 
  
}

//Respuesta
{
    "success" : true,
    "data"    : {}
}
```


## Picker Tenants
*Nombre:* wsPickerGps
*URL:* `http://localhost/ws/pickerGps`
*Descripción:* Trae un listado de gps para pintar en un picker

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  
  }
}

//Respuesta
{
    "success" : true,
    "data"    : [
	{
	    "id"     : "98988565454",
	    "nombre" : "20160215"
	}
    ]
}

```


## Crear Vehiculo Admin tenant 
*Nombre:* wsCrearVehiculoAdminTenant
*URL:* `http://localhost/ws/crearVehiculoAdminTenant`
*Descripción:* 

```
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "administracion" 
    },

    "data" : {	
							
				"idTenant"      : "545454545fsf415s4dfxc",	
	            "placa"			: "FGB235",
	            "marca"			: "kenwoth",
	            "modelo"        : "2015",
	            "idGps"      	: "54874512321",
                'referencia'      : 'SPARK',
	            'marcaMotor'      : 'cummins',
	            'referenciaMotor' : 'IPS400',
	            'consumoGalKm'    : 40.15
	
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
    			'id' : "545445656cvxzz454545s"
    			}
}
```

## Detalle vehiculo Admin Tenant 
*Nombre:* wsDetalleVehiculoAdminTenant
*URL:* `http://localhost/ws/detalleVehiculoAdminTenant`
*Descripción:*

- estaAlarmaCadenaFrioActivada: indica si la alarma de cadena de frio está activada.

- tempLimSuperior: límite superior de temperatura
- tempLimInferior: límite inferior de temperatura

```
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "administracion" 
    },

    "data" : {	
		"id"           : "56468789355",
	
    }   
}

//Respuesta
{
    "success" : true,
    "data"    : {
	    			'id'                : "6552625565655554sf4f559",
		            'placa'        	   	: "FGB568",
		            'marca'       		: "Kenworth"
		            'modelo'            : "2015",
		            'activo'			: true, 
		            'idGps'             : "831928192891",
					
	                'referencia'      : 'SPARK',
	                'marcaMotor'      : 'cummins',
	                'referenciaMotor' : 'IPS400',
	                'consumoGalKm'    : 40.15,

                    'estaAlarmaCadenaFrioActivada' : true,
                    "tempLimSuperior" : 30,
                    "tempLimInferior" : 20,
				
    			}
}
```
=======
##Nota:
#Por favor ejecutar en cron los archivos
#-examinarImagenesPendientes.py
#-verificarEstadoVehiculo.py
#-colgarLlamada.py


#========================================================================================
#Para terminar las llamadas  segun un tiempo establecido se estara ejecutando un archivo 
# para verificar las llamadas en curso y que se ha superado el tiempo

#A partir de esta linea se van a definir los documentos del sistema Fleetbiweb

### tenant:
*Documentos:*
```
{
    "tipoDato"      : "tenant",
    "nombreGeneral" : "Exxon Mobil de Colombia",
    "urlTenant"     : "fleetbiexxonmobil",
    "idImagenLogo"  : "http://localhost/nisabu/image/1911e9b72f67bf6ac72b6ace06002cef",
    "activo"        : true
    "nit"        	: "555458545644"
	"telefono"      : "831928192891",
	"direccion"     : "cra 172 nu j21212",
	"celularEmergencia"        : "3105642147",	
}
```

### recuperacionContrasena:
*Documentos:*
```
{
    "tipoDato"      : "recuperacionContrasena",
    "token" 		: "",
    "estaUsado"		: true,
    "usuario"		: "admin",
    "creadoEn"		: "2016-03-12T08:07:19Z",
    "activo"        : true
}
```

*Documentos:*	
```
{
    "tipoDato"      : "vehiculos",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "placa"         : "TVH123",
    "marca"         : "KEnworth",
    "modelo"        : "2014",
    "activo"        : true,    
	"referencia"    : "SPARK",
	"marcaMotor"      : "cummins",
	"referenciaMotor" : "IPS400",
	"consumoGalKm"    : 40.15,
    "conductor"       : "98986565465",
    "cargado"         : true,
    "debeExportarPegaso" : true,
    'estaAlarmaCadenaFrioActivada' : true,
                    "tempLimSuperior" : 30,
                    "tempLimInferior" : 20,
 

}
```

*marca:* marca del vehiculo

*referencia:* referencia del vehiculo

*marcaMotor:* marca del motor

*referenciaMotor:* Referencia del motor

*consumoGalKm* : número float que indica cuantos galones consume por kilometro recorrido.

*debeExportarPegaso:* Indica si los datos de geoposiciones deben enviarse a pegaso.

*Documentos:*
```
{
    "tipoDato"      : "vehiculos",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "placa"         : "KIQ095",
    "marca"         : "Chevrolet",
    "modelo"        : "2011",
    "activo"        : true,
	"referencia"    : "SPARK",
	"marcaMotor"      : "cummins",
	"referenciaMotor" : "IPS400",
	"consumoGalKm"    : 40.15,
  "conductor"       : "98986565465" ,
  "cargado"         : true

}
```



### posicionVehiculos:

- *estaEncendidoMotor:* indica si el motor estaba encendido en ese punto

- *idPosicionVehiculoInicialEncendidoMotor:* indica cual es el punto
  inicial de encendido del motor o de apagado según el orden, bajo
  este número se agrupan.

- *complementosEstadisticas:* son los datos que se calculan
  posteriormente para hacer el tramite de las estádisticas.
  
- *metrosRecorridos:* número de metros recorridos entre el punto
  actual y el anterior.
  
- *idPrimerPuntoExcesoVelociad:* indica el primer punto en que ocurrió
  un exceso de velocidad.

- *segundosAlPuntoAnterior:* número de segundos que han transcurrido
  entre este punto y el punto anterior.

- *idPrimerPuntoCambioEncendido:*el id de la posición en que ocurrió
  un cambio en el estado de encendido del vehículo,



*Documentos:*
```
{
    "tipoDato"      : "posicionVehiculos",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "horaRegistrada": "2016-03-12T08:07:19Z",
    "horaRecibida"  : "2016-03-12T08:07:19Z",
    "latitud"       : "-30.37812817283",
    "longitud"      : "70.6271265342323",
    "velocidad"     : "30.35 km/h",
    "idVehiculo"    : "95ea81741bbfba959550827b15003985",
    "estado"        : "activo","inactivo"
    "activo"        : true,
    "ultimaPosicion": true,
    "zonaAlarmas" : ["95ea81741bbfba959550827b150045d0","95ea81741bbfba959550827b1500aefa"],
    "programacionVigilancia" : ["64dab9c38af9d45fc669c7456d004bf1","ea9581e8514614132fa9797f9800042f"],
    "idParada"          : "",
    "idFragmentoParada" : ""
	"estaEncendidoMotor" : true,
	"idPosicionVehiculoInicialEncendidoMotor" : "1821928192",
	"nombreGeoposicion"                       : "Av 6, Cali, Valle del Cauca, Colombia",
	"complementosEstadisticas" : {
		"metrosRecorridos" : 10,
		"idPrimerPuntoExcesoVelocidad" : "12981928192",        
		"segundosAlPuntoAnterior" : 130,
		"idPrimerPuntoCambioEncendido" : "2819281928"		
	}

}
```
###===================================================
### fragmentoParada
{
    "tipoDato"          : "fragmentoParada",
    "latitud"           : "-30.37812817283",
    "longitud"          : "70.6271265342323",
    "fechaHoraRegistro" : "2016-03-12T08:07:19Z",
    "idVehiculo"        : "3e8f127632561e88b4acd1d8f000626a",
    "idParada"          : "95ea81741bbfba959550827b15003985",
    "activo" : true
}
###===================================================

###===================================================
### paradaVehiculo
{
    "tipoDato"          : "paradaVehiculo",
    "latitud"           : "-30.37812817283",
    "longitud"          : "70.6271265342323",
    "fechahoraInicio"   : "2016-03-12T08:07:19Z",
    "fechahoraFin"      : "2016-03-12T08:07:19Z",
    "idVehiculo"        : "3e8f127632561e88b4acd1d8f000626a",
	"duracionParadaSegundos" : 2123,
    "activo"            : true,
	"nombreGeoposicion" : "Av 6, Cali, Valle del Cauca, Colombia",
	
}
###===================================================



###===================================================
### zona Alarma
{
    "tipoDato"   : "zonaAlarma",
    "fecha"      : "2016-03-12",
    "horaInicio" : "07:19",
    "horaFin"    : "07:19",
    "estado"     : "En curso",
    "idVehiculo" : "3e8f127632561e88b4acd1d8f000626a",
    "idZona"     : "95ea81741bbfba959550827b15003985",
    "activo"     : true,
    "timeStamp"  : 1482355653.846376,
	"idTipoZona" : "12389cf82919889a819289b898192a89"
}
###===================================================

### capturaImagenes:

*Documentos:*
```
{
    "tipoDato"      : "capturaImagenes",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "-30.37812817283",
    "longitud"        : "70.6271265342323",
    "idVehiculo"      : "ca759f5632ec30e319570ba94b000743",
    "idImagen"        : "1911e9b72f67bf6ac72b6ace06002cef",
    "urlImagen"       : "http://localhost/nisabu/image/1911e9b72f67bf6ac72b6ace06002cef",
    "activo"          : true

}
```
### capturaAudio:

*Documentos:*
```
{
    "tipoDato"        : "capturaAudio",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "-30.37812817283",
    "longitud"        : "70.6271265342323",
    "duracion"        : "6000",
    "idLlamada"       : "131239183719271382", #id Doc llamadas
    "idVehiculo"      : "ca759f5632ec30e319570ba94b000743",
    "estado"          : "En curso", "Finalizado"
    "urlAudio"        : "",
    "activo"          : true

}
```

#-------------------------------------------------------------------
##Documentos para las alarmas boton de panico en docBotonPanico.md

#-------------------------------------------------------------------

### Monitoreo de zonas:

*Documentos:*
```
{
    "tipoDato"            : "monitoreoZonas",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "nombre"              : "Zona de descargue",
    "descripcion"         : "nota del proceso",
    "registrarAudio"      : true,
    "registrarImagen"     : false,
    "tiempoMaxGrabAudio"  : "30",
    "numeroCapturasMax"   : "30",
    "contadorFotosTomadas"   : "0",
    "latitud" : "3.41306",
    "longitud": "-76.3511",
    "radio" : "500",
    "activo"              : true
}
```

### programacion

*Documentos:*
```
{
    "tipoDato"    : "programacionVigilancia",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "idVehiculo"  : "95ea81741bbfba959550827b15003985",
    "registrarAudio"      : true,
    "registrarImagen"     : false,
    "tiempoMaxGrabAudio"  : "30",
    "capturasMax" : "20",
    "contadorFotosTomadas"   : "0",
    "fechaInicio" : "2016-03-12",
    "fechaFin"    : "2016-03-20",
    "horaInicio"  : "07:19",
    "horaFin"     : "07:59",
    "estadoProgramacion" : "Iniciado", "En curso", "finalizado", "Sin iniciar"
    "activo"        : true  
}
```

###usuario

*Documentos:*
```
{
   "modificadoPor": "huvadmin451236",
   "tipoDato": "adminTenant",
   "nombres": "pepito",
   "correo": "fjhk@gm.vo",
   "loginUsuario": "admin",
   "activo": true,
   "creadoEn": "2016-03-31T12:06:17.789000",
   "identificacion": "365248",
   "contrasena": "e363ee6d530010515d4dc56bd41f6a7a",
   "telefono": "45632",
   "modificadoEn": "2016-03-31T12:13:44.592000"
}
```

### capturaImagenesZonaAlarma:

y*Documentos:*
```
{
    "tipoDato"      : "capturaImagenesZonaAlarma",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "3.41306",
    "longitud"        : "-76.3511",
    "idVehiculo"      : "ca759f5632ec30e319570ba94b000743",
    "idImagen"        : "1911e9b72f67bf6ac72b6ace06002cef",
    "urlImagen"       : "http://localhost/nisabu/image/1911e9b72f67bf6ac72b6ace06002cef",
    "activo"          : true,
    "zonaAlarmas" : ["026b8e0d73b1739a3871cda683004e7e","95ea81741bbfba959550827b1500aefa"]
}
```

### capturaAudioZonaAlarma:

*Documentos:*
```
{
    "tipoDato"      : "capturaAudioZonaAlarma",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "3.41306",
    "longitud"        : "-76.3511",
    "duracion"        : "6000",
    "idLlamada"       : "131239183719271382", #id Doc llamadas
    "idVehiculo"      : "95ea81741bbfba959550827b15005700",
    "estado"          : "En curso", "Finalizado"
    "urlAudio"        : "",
    "activo"          : true,
    "zonaAlarmas" : ["026b8e0d73b1739a3871cda683004e7e","95ea81741bbfba959550827b1500aefa"]
}
```


### imagenesProgramacionVigilancia:

*Documentos:*
```
{
    "tipoDato"      : "imagenesProgramacionVigilancia",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "3.41306",
    "longitud"        : "-76.3511",
    "idVehiculo"      : "95ea81741bbfba959550827b15005700",
    "idImagen"        : "1911e9b72f67bf6ac72b6ace06002cef",
    "urlImagen"       : "http://localhost/nisabu/image/1911e9b72f67bf6ac72b6ace06002cef",
    "activo"          : true,
    "idProgramacion" : ["cfbf997830cd3734846b60c2cf0906bd"]
}
```

### audioProgramacionVigilancia:

*Documentos:*
```
{
    "tipoDato"      : "audioProgramacionVigilancia",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "3.41306",
    "longitud"        : "-76.3511",
    "duracion"        : "6000",
    "idLlamada"       : "131239183719271382", #id Doc llamadas
    "idVehiculo"      : "ca759f5632ec30e319570ba94b000743",
    "estado"          : "En curso", "Finalizado"
    "urlAudio"        : "",
    "activo"          : true,
    "idProgramacion" : ["6f82b5881412978eed2265b9a90008c4"]
}
```

### parada: Documento que guarda el promedio de paradas

*Documentos:*
```
{
    "tipoDato"      : "parada",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "5.0671",
    "longitud"        : "-75.5183",
    "activo"          : true
}
```

### llamadas: Documento que guarda las llamadas a Twilio registradas por usuario, botón de pánico, zona Alarma 
## El limite debe estar guardado en minutos
*Documentos:*
```
{
    "tipoDato"      : "llamadas",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "idVehiculo"    : "46545665456645645" ,
    "sidLlamada"    : "ABOO4545454545450",
    "estado"        : "En curso", "Finalizado", "Sin iniciar"
    "razonLLamada"  : "usuario", "botonPanico", "zonaAlarma","programacionVigilancia", "zonaAlarmaProgramacionVigilancia"
    "idRemitente"   :"54546554654", #id de usuario si es de un GPS idGps quien hace la llamada
    "limite"        : "57", # para saber si entra a otra zona alarma y me actualiza el limite
    "activoPanico"  : True,#campo para saber si en algun momento activo el boton de panico
    "activo"        : true
}
```


### programacionVigilanciaEjecutadas: Documento que guarda todas las programacion vigilancias ejecutadas
# con su fechaInicio, fechaFin, HoraInicio y HoraFin         
*Documentos:*
```
{
    "tipoDato"      : "programacionVigilanciaEjecutadas",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "idVehiculo"    : "95ea81741bbfba959550827b15005700" ,
    "fechaInicio" : "2016-11-02",
    "fechaFin"    : "2016-11-07",
    "horaInicio"  : "01:19",
    "horaFin"     : "07:59",
    "idProgramacion" : ["44e08c4872d5f4a4e14fd9e12d01ea82"],
    "activo"        : true
}
```





# WebServices Asignacion ruta

## Listar asignaciones ruta

*Nombre:* listarAsignacionesRutas

*URL:* http://localhost/ws/listarAsignacionesRutas

*Descripción:* Trae un listado de todas als asignaciones de rutas
desde el limite inferior de días.

- estado : `programada` todavía no se inicia, `iniciada` se encuentra
  en curso, `finalizada` se ejecutó completamente. `abortada` si se
  inicio pero el usuario indicó que la cancela (útil para iniciar otra
  ruta a mitad de ejecución de otra). `noejecutada` cuando no se
  inicia y ya se pasaron las fechas, `sinfinalizar` la ruta inició
  pero se deterctó que nunca la finalizará porque iniciio una nueva
  ruta.

- fechaHoraCruce : momento en que atrevezó el punto de control
  virtual.

- minutosTolerancia: número de minutos de tolerancia de cruce por
  punto de control

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
	}
}

//Respuesta
{
    "success" : true,
    "data"    : [
		{
			"id"              : "1920120129012901",
			"idRuta"          : "44444654454555412",
			"idVehiculo"      : "18291829192812892",
			"idConductor"     : "18291820ihaj81298",
			"fechaInicioProgramada" : "2016-03-12T08:07:19Z",
			"fechaFinProgramada"    : "2016-03-12T08:07:19Z",
			"fechaInicioReal"       : "2016-03-12T08:07:19Z",
			"fechaFinReal"          : "2016-03-12T08:07:19Z",
			"estado"                 : "programada",
			"puntosDeControlVirtual" : [
				{
					"latitud"                  : "16.909009090",
					"longitud"                 : "-70.12819281",
					"direccion"                : "Av 123 # 678",
					"fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
					"fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z",
					"minutosTolerancia"        : 30
				}		 
			],
			"ruta" : {
				"nombreRuta" : "ruta cavasa",
				"origen": {
					"latitud"   : 3.5266987,
					"longitud"  : -76.32760560000003,
					"direccion" : "Cra 123 # 23-45"
				},
				"destino": {
					"latitud"   : 3.5266987,
					"longitud"  : -76.32760560000003,
					"direccion" : "Cra 123 # 23-45"
				}
			},
			"vehiculo" : {
				"placa" : "18218291"				
			},
			"conductor" : {
				"nombres"   : "Hector",
				"apellidos" : "Machuca",
				"celular"   : "5555",
				"cedula"    : "12345"
			}
			
		}
    ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Crear asignación de ruta

*Nombre:* CrearAsignacionRuta

*URL:* http://localhost/ws/crearAsignacionRuta

*Descripción:* Crea una asignacion de ruta

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
		"idRuta"                 : "a1981929128qwqwqw",
		"idVehiculo"             : "18291829192812892",
		"idConductor"            : "18291820ihaj81298",
		"fechaInicioProgramada"  : "2016-03-12T08:07:19Z",
		"fechaFinProgramada"     : "2016-03-12T08:07:19Z",
		"puntosDeControlVirtual" : [
			{
				"latitud"   : "16.909009090",
				"longitud"  : "-70.12819281",
				"direccion" : "Av 123 # 678",
				"fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
				"fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z",
				"minutosTolerancia"        : 30
			}		
		],
		
	}
}

//Respuesta
{
    "success" : true,
    "data"    : {
		"id" : "1291821928"
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Detalle asignación ruta

*Nombre:* wsDetalleAsignacionRuta

*URL:* http://localhost/ws/detalleAsignacionRuta

*Descripción:* Detalle de una asignación ruta.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
		"idAsignacionRuta" : "18291829189182"
	}
}

//Respuesta
{
    "success" : true,
    "data"    :  {
		"id"                     : "1920120129012901",
		"idRuta"                 : "44444654454555412",
		"idVehiculo"             : "18291829192812892",
		"idConductor"            : "18291820ihaj81298",
		"fechaInicioProgramada"  : "2016-03-12T08:07:19Z",
		"fechaFinProgramada"     : "2016-03-12T08:07:19Z",
		"fechaInicioReal"        : "2016-03-12T08:07:19Z",
		"fechaFinReal"           : "2016-03-12T08:07:19Z",
		"estado"                 : "programada",
		"puntosDeControlVirtual" : [
			{
				"latitud"                  : "16.909009090",
				"longitud"                 : "-70.12819281",
				"direccion"                : "Av 123 # 678",
				"fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
				"fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z",
				"minutosTolerancia"        : 30
			}		
		],
		"ruta" : {
			"nombreRuta" : "ruta cavasa"
		},
		"vehiculo" : {
			"placa" : "18218291"				
		},
		"conductor" : {
			"nombres"   : "Hector",
			"apellidos" : "Machuca",
				"celular"   : "5555",
			"cedula"    : "12345"
		}		
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Editar Asignación Ruta

*URL:* http://localhost/ws/editarAsignacionRuta

*Descripción:* Edita una asignación ruta.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
		"idAsignacionRuta" : "18291829189182",
		//"idRuta"                 : "44444654454555412",
		//"idVehiculo"             : "18291829192812892",
		"idConductor"            : "18291820ihaj81298",
		"fechaInicioProgramada"  : "2016-03-12T08:07:19Z",
		"fechaFinProgramada"     : "2016-03-12T08:07:19Z",
		//"fechaInicioReal"        : "2016-03-12T08:07:19Z",
		//"fechaFinReal"           : "2016-03-12T08:07:19Z",
		//"estado"                 : "programada",
		"puntosDeControlVirtual" : [
			{				
				"direccion"                : "Av 123 # 678",				
				"fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z"
				"minutosTolerancia"        : 30
			}		
		],
	}
}

//Respuesta
{
    "success" : true,
    "data"    :  {
		"id"                     : "1920120129012901",
		"idRuta"                 : "44444654454555412",
		"idVehiculo"             : "18291829192812892",
		"idConductor"            : "18291820ihaj81298",
		"fechaInicioProgramada"  : "2016-03-12T08:07:19Z",
		"fechaFinProgramada"     : "2016-03-12T08:07:19Z",
		"fechaInicioReal"        : "2016-03-12T08:07:19Z",
		"fechaFinReal"           : "2016-03-12T08:07:19Z",
		"estado"                 : "programada",
		"puntosDeControlVirtual" : [
			{
				"latitud"                  : "16.909009090",
				"longitud"                 : "-70.12819281",
				"direccion"                : "Av 123 # 678",
				"fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
				"fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z"
			}		
		],
		"ruta" : {
			"nombreRuta" : "ruta cavasa"
		},
		"vehiculo" : {
			"placa" : "18218291"				
		},
		"conductor" : {
			"nombres"   : "Hector",
			"apellidos" : "Machuca",
				"celular"   : "5555",
			"cedula"    : "12345"
		}		
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## eliminar Asignación Ruta

*URL:* http://localhost/ws/eliminarAsignacionRuta

*Descripción:* Elimina.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
		"idAsignacionRuta" : "18291829189182"
	}
}

//Respuesta
{
    "success" : true,
    "data"    :  {
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## abortar Asignación Ruta

*URL:* http://localhost/ws/abortarAsignacionRuta

*Descripción:* aborta.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
		"idAsignacionRuta" : "18291829189182"
	}
}

//Respuesta
{
    "success" : true,
    "data"    :  {
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Detalle Seguimiento Ruta

*URL:* http://localhost/ws/detalleSeguimientoAsignacionRuta

*Descripción:* Trae el detalle del seguimiento de una ruta.


- *seguimientoAsignacionRuta*: Lleva registro del avance dle seguimiento de la ruta, ver el documento `seguimientoAsignacionRuta`

- *direccion:* Irá casi siempre vacio, pero si va "" toca buscarlo por interfaz gráfica.

- *paradas.tipo:* `Carga` o `Descarga`

- *limitesDeVelocidad.estado:* `ok` sin infracciones, `vigilando` vigila el curso, todavía no la ha transitado totalmente, `excedido` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
	},
	
	"data" : {
		"idAsignacionRuta" : "18291829189182"
	}
}

//Respuesta
{
    "success" : true,
    "data"    :  {

		"ruta" : {
			"fechaInicioProgramada" : "2017-08-16T07:50:00-05:00",
			"fechaInicioReal"       : "2017-08-16T08:00:44",
			"fechaFinProgramada"    : "2017-08-17T11:00:00-05:00",
			"fechaFinReal"          : "2017-08-16T08:09:38",
			"origen": {
				"latitud"   : 3.5266987,
				"longitud"  : -76.32760560000003,
				"direccion" : "Cra 123 # 23-45",
				"velocidad" : 34.1212331212
			},
			"destino": {
				"latitud"   : 3.5266987,
				"longitud"  : -76.32760560000003,
				"direccion" : "Cra 123 # 23-45",
				"velocidad" : 34.1212331212
			}
		},
		
		"seguimientoAsignacionRuta" : {
			"fechaHoraInicioSeguimiento" : "2017-08-11T05:07:19",
			"fechaHoraFinSeguimiento"    : "2017-08-13T05:07:19",
			"fechaHoraUltimaRevision"    : "2017-08-13T05:07:19",
			"estado"                     : "enruta"
		},	
		"puntosDeControl" :{
			"latitud"   : "16.909009090", 
			"longitud"  : "-76.53887",
			"direccion" : "Av 123 # 678", 
			"fechaHoraCruceReal"       : "2016-07-08T08:07:19Z",
			"fechaHoraCruceProgramada" : "2016-07-08T08:07:19Z",
			"minutosTolerancia"        : 30,
			"velocidadDeCruce"         : 79.88
		},
		"paradas" : [{
			"latitud"  : 12.12012,
			"longitud" : -77.219201,
			"tipo"     : "Carga",
			"direccion" : "Cra 1212, cali colombia",
			"fechaHoraInicioParada" : "2016-03-12T08:07:19Z",
			"fechaHoraFinParada" : "2016-03-12T08:07:Web"
		}],
		"limitesDeVelocidad":[
			{
				"latitud"          : 12.12012,
				"longitud"         : -77.219201,
				"direccion"        : "Cra 123 # 456 Cali",
				"limiteCargado"    : 60,
				"limiteDescargado" : 80,
				"estado"           : "ok",
				"velocidadMaximaRegistrada" : "",
				"infracciones"     : [{
					"latitud"          : 12.12012,
					"longitud"         : -77.219201,
					"direccion"        : "Cra 123 # 456 Cali",
					"tipo"             : "Carga",
					"velocidad"        : 65
					"fechaHoraInfraccion" : "2016-03-12T08:07:Web"
				}]
			}
		]
		
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# 19Z Services Rutas

## Picker Rutas
*Nombre:* wsPickerRutas
*URL:* `http://localhost/ws/pickerRutas`
*Descripción:* Trae un listado de rutas para pintar en un picker

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil" 
  },
  "data" : { }
}

//Respuesta
{
    "success" : true,
    "data"    : [
		{
			"id"     : "81201291212891082",
			"nombre" : Ruta prueba 1"
		}
    ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#fin Editado Documentos Fleetbiweb
#========================================================================================


##vistas

##Vista Tenant: Se encuentra en la base de datos fleetbi
```
{
   "_id": "_design/tenant",
   "views": {
       "visualizarTenants": {
           "map": "function(doc){if(doc.tipoDato == \"tenant\" && doc.activo){ emit([doc._id, doc.urlTenant ], null );}}"
       }
   }
}
```





### vista usuarios
```
{
   "_id": "_design/usuarios",
   "views": {
       "usuariosPorContrasena": {
           "map": "function(doc){if(doc.tipoDato == \"adminTenant\"){ emit([doc.loginUsuario, doc.contrasena, \"adminTenant\"], null );}}"
       },
       "usuariosPorLoginUsuario": {
           "map": "function(doc){if(doc.tipoDato == \"adminTenant\" && doc.activo){ emit([doc.loginUsuario], {perfil:\"adminTenant\"} );}}"
       },
       "usuariosPorCorreo": {
           "map": "function(doc){if(doc.tipoDato == \"adminTenant\" && doc.activo){ emit([doc.correo], {perfil:\"adminTenant\"} );}}"
       }     
   }
}
```

### vista recuperacionContrasena  en adminTenant y superAdministrador falta agregar en couch pruebas y usuariosPorCorreo en la vista usuarios
```
{
   "_id": "_design/recuperacionContrasena",
   "views": {
       "recuperacionPorLoginUsuario": {
           "map": "function(doc){if(doc.tipoDato == \"recuperacionContrasena\" && doc.activo){ emit([doc.usuario], null );}}"
       },
       "recuperacionPorToken": {
           "map": "function(doc){if(doc.tipoDato == \"recuperacionContrasena\" && doc.activo){ emit([doc.token], null );}}"
       },
        "recuperacionPorTokenYuso": {
           "map": "function(doc){if(doc.tipoDato == \"recuperacionContrasena\" && doc.activo){ emit([doc.token, doc.estaUsado], null );}}"
       }       
   
   }
}
```


### vista autenticaciones
```
{
   "_id": "_design/autenticaciones",
   "views": {
       "autenticacion": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\"){ emit([doc.loginUsuario, doc.token], null );}}"
       },
       "autenticacionesPush": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\" && doc.origen && doc.idPush){ emit([doc.loginUsuario, doc.origen, doc.idPush], null );}}"
       },
       "autenticacionesIdPush": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\" && doc.origen && doc.idPush && doc.activo){ emit([doc.idPush], null );}}"
       },
       "autenticacionesTipoSesion": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\"){ emit([doc.idUsuario, doc.tipoSesion], null );}}"
       },
       "autenticacionesTipoSesionActivos": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\" && doc.activo){ emit([doc.idUsuario, doc.tipoSesion], null );}}"
       },
       "autenticacionesUltimaSesion": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\" && doc.ultimaSesion){ emit([doc.idUsuario, doc.tipoSesion], null );}}"
       },
       "alertasSesion": {
           "map": "function(doc){if(doc.tipoDato == \"alertasSesion\" && doc.activo){ emit([doc.fechaHoraActualSesion, doc.concepto], null );}}"
       }
   }
}

```

### vista posicionVehiculos 
```
{
   "_id": "_design/posicionVehiculos",
    "views": {
       "posicionVehiculos": {
           "map": "function(doc){if(doc.tipoDato == \"posicionVehiculos\") { emit([doc._id], null );} }"
       },
       "posicionVehiculosUltimaPosicion" : {
          "map" : "function(doc){  if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){    emit([doc.ultimaPosicion, doc.idVehiculo],     {       \"_id\": doc.idVehiculo,       \"latitud\" : doc.latitud,      \"longitud\" : doc.longitud,      \"velocidad\" : doc.velocidad,      \"horaRecibida\" : doc.horaRecibida,      \"horaRegistrada\" : doc.horaRegistrada, \"estado\" : doc.estado    } );  }}"
       },
      "poscionVehiculoPorZonaAlarma" : {
       "map" : "function(doc){  if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){    for(var i = 0 ; i < doc.zonaAlarmas.length ; i++){      var idZonaAlarma = doc.zonaAlarmas[i];      emit([idZonaAlarma, doc.horaRegistrada],null);      }      }}"

      },
       "anteriorPosicionVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){ emit([doc.idVehiculo, doc.horaRegistrada ], null );}}"
       },
       "paradaVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"paradaVehiculo\" && doc.activo){ emit([doc.idVehiculo, doc.fechahoraInicio ], null );}}"
       },
       "ultimaPosicionGuardada":{
          "map": "function(doc){if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){ emit([doc.ultimaPosicion, doc.idVehiculo ], null );}}"
       },
       "posicionFechaCreacion":{
          "map": "function(doc){if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){ emit([ doc.idVehiculo, doc.horaRegistrada ], null );}}"   
       }
   }
}

//posicionVehiculosUltimaPosicion
function(doc){
  if(doc.tipoDato == "posicionVehiculos" && doc.activo){
    emit([doc.ultimaPosicion, doc.idVehiculo], 
    { 
      "_id": doc.idVehiculo, 
      "latitud" : doc.latitud,
      "longitud" : doc.longitud,
      "velocidad" : doc.velocidad,
      "horaRecibida" : doc.horaRecibida,
      "horaRegistrada" : doc.horaRegistrada
    } );
  }
}


poscionVehiculoPorZonaAlarma
function(doc){
  if(doc.tipoDato == "posicionVehiculos" && doc.activo){
    for(var i = 0 ; i < doc.zonaAlarmas.length ; i++){
      var idZonaAlarma = doc.zonaAlarmas[i];

      emit([idZonaAlarma, horaRegistrada],null);  
    }
    
  }
}
```

### vehiculos 

```
{
   "_id": "_design/vehiculos",
   "views": {
       "vehiculos": {
           "map": "function(doc){ if(doc.tipoDato == \"vehiculos\" && doc.activo){ emit( [doc._id, doc.placa] , null); } }"
       }
   }
}
```


### detalleVehiculo 

```
{
   "_id": "_design/detalleVehiculo",
   "views": {
       "detalleVehiculo": {
           "map": "function(doc){ if(doc.tipoDato == \"vehiculos\" && doc.activo){ emit( [doc._id, doc.placa] , null); } }"
       },
       "buscarPlacaVehiculo": {
           "map": "function(doc){ if(doc.tipoDato == \"vehiculos\" && doc.activo){ emit( [doc.placa] , null); } }"
       }       
   }
}
```

### detalleZona 

```
{
   "_id": "_design/detalleZona",
   "views": {
       "detalleZona": {
           "map": "function(doc){ if(doc.tipoDato == \"monitoreoZonas\" && doc.activo){ emit( [doc._id, doc.nombre] , null); } }"
       }
   }
}
```


### posicionVehiculoRangoFecha 

```
{
   "_id": "_design/posicionVehiculoRangoFecha",
   "views": {
       "posicionVehiculoRangoFecha": {
           "map": "function(doc){ if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){ emit( [doc.idVehiculo, doc.horaRegistrada ] , null); } }"
       },
       "capturaImagenes": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaImagenes\" && doc.activo){ emit( [doc.idVehiculo, doc.horaRegistrada ] , null); } }"
       },
       "capturaAudio": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudio\" && doc.activo){ emit( [doc.idVehiculo, doc.horaRegistrada] , null); } }"
       },
       "capturaAlarmas": {
           "map": "function(doc){ if(doc.tipoDato == \"alarmas\" && doc.activo){ emit( [doc.idVehiculo, doc.horaRegistrada] , null); } }"
       }
   }
}
```


### vigilancias 

```
{
   "_id": "_design/vigilancias",
   "views": {
       "monitoreoZonas": {
           "map": "function(doc){ if(doc.tipoDato == \"monitoreoZonas\" && doc.activo){ emit( [doc._id, doc.nombres] , null); } }"
       },
       "programacionVigilancia": {
           "map": "function(doc){ if(doc.tipoDato == \"programacionVigilancia\"){ emit( [doc._id, doc.idVehiculo] , null); } }"
       },
       "zonaAlarma": {
           "map": "function(doc){ if(doc.tipoDato == \"zonaAlarma\" && doc.activo){ emit( [doc.idZona, doc._id] , null); } }"
       },
       "capturaImagenesZonaAlarma": {
           "map": "function(doc){  if(doc.tipoDato == \"capturaImagenesZonaAlarma\" && doc.activo){    for(var i = 0 ; i < doc.zonaAlarmas.length ; i++){      var idZonaAlarma = doc.zonaAlarmas[i];      emit([idZonaAlarma, doc.horaRegistrada],null);      }      }}"
       },
       "capturaAudioZonaAlarma": {
           "map": "function(doc){  if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo){    for(var i = 0 ; i < doc.zonaAlarmas.length ; i++){      var idZonaAlarma = doc.zonaAlarmas[i];      emit([idZonaAlarma, doc.horaRegistrada],null);      }      }}"
       },
       "vehiculosPosicion": {
           "map": "function(doc){  if(doc.tipoDato == \"posicionVehiculos\" && doc.activo){    for(var i = 0 ; i < doc.programacionVigilancia.length ; i++){      var idProgramacion = doc.programacionVigilancia[i];      emit([idProgramacion, doc.horaRegistrada],null);      }      }}"
       }
       "imagenesProgramacionVigilancia": {
           "map": "function(doc){ if(doc.tipoDato == \"imagenesProgramacionVigilancia\" && doc.activo){ emit( [doc.idProgramacion, doc.horaRegistrada ] , null); } }"
       },
       "audioProgramacionVigilancia": {
           "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo){ emit( [doc.idProgramacion, doc.horaRegistrada ] , null); } }"
       },
       "fragmentoParada": {
           "map": "function(doc){ if(doc.tipoDato == \"fragmentoParada\" && doc.activo){ emit( [doc._id, doc.fechaHoraRegistro ] , null); } }"
       },
       "listadoAudiosProgramacionVigilancia":{
          "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo){             for(var i=0; i< doc.idProgramacion.length; i++){              emit( [doc.idProgramacion[i], doc.horaRegistrada ] , null);              } } }
"
        },

       "imagenesZonaAlarmaPorVehiculo": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaImagenesZonaAlarma\" && doc.activo){ emit( [doc.idVehiculo] , null); } }"
       },
       "imagenesProgramacionVigilanciaPorVehiculo": {
           "map": "function(doc){ if(doc.tipoDato == \"imagenesProgramacionVigilancia\" && doc.activo){ emit( [doc.idVehiculo] , null); } }"
       },
         "listarImagenesProgramacionVigilancia": {
           "map": "function(doc){ if(doc.tipoDato == \"imagenesProgramacionVigilancia\" && doc.activo){ for(var i = 0 ; i < doc.idProgramacion.length ; i++){   var dato = doc.idProgramacion[i];   emit( [dato, doc.horaRegistrada ] , null);  } } }"
       }

   }
}


{
   "_id": "_design/consultarRangoFechasAlarmas",
   "language": "javascript",
   "views": {
       "consultarRangoFechasAlarmas": {
           "map": "function(doc) {\nif(doc.tipoDato == \"programacionVigilancia\" && doc.activo){\n\tvar fechaInicio = doc.fechaInicio;\n\tvar fechaFin = doc.fechaFin;\n\tvar resFechaInicio = fechaInicio.split(\"-\");\n\tvar resFechaFin    = fechaFin.split(\"-\");\n\tvar diaInicio = parseFloat(resFechaInicio[2]);\n\tvar diaFin = parseFloat(resFechaFin[2]);\n\tvar mesInicio = parseFloat(resFechaInicio[1]);\n\tvar mesFin = parseFloat(resFechaFin[1]);\n\tvar anioInicio = parseFloat(resFechaInicio[0]);\n\tvar anioFin = parseFloat(resFechaFin[0]);\n\tvar conteoDia = parseFloat(diaInicio);\n\tvar conteoMes = parseFloat(mesInicio);\n\tvar conteoAnio = parseFloat(anioInicio);\n\tvar continuaGenerarFechas = true;\n        emit(fechaInicio,fechaFin)\n\tif(anioInicio <= anioFin){\n\t\twhile(continuaGenerarFechas){\n\t\t\t\n                        \n                        if(conteoDia == 32){\n\t\t\t\tconteoDia = 0;\n\t\t\t\tconteoMes +=1;\n\t\t\t}\n                         \n                        \n\t\t\tif(conteoMes == 13 && conteoDia == 0){\n\t\t\t\tconteoDia = 1\n\t\t\t\tconteoMes = 1\n\t\t\t\tconteoAnio +=1\n\t\t\t}\n                        \n                         \n\t\t\tif(conteoDia == diaFin && conteoMes == mesFin && conteoAnio == anioFin){\n\t\t\t\tcontinuaGenerarFechas = false;\n\t\t\t}\n                       \n\t\t\temit([conteoDia , conteoMes , conteoAnio],doc._id)\n\n\t\t\tconteoDia += 1;\n\n\n\t\t}\n\t}\n        \n}\n\n}\n"
       }
   }
}

consultarRangoFechasAlarmas
function(doc) {
if(doc.tipoDato == "programacionVigilancia" && doc.activo){
  var fechaInicio = doc.fechaInicio;
  var fechaFin = doc.fechaFin;
  var resFechaInicio = fechaInicio.split("-");
  var resFechaFin    = fechaFin.split("-");
  var diaInicio = parseFloat(resFechaInicio[2]);
  var diaFin = parseFloat(resFechaFin[2]);
  var mesInicio = parseFloat(resFechaInicio[1]);
  var mesFin = parseFloat(resFechaFin[1]);
  var anioInicio = parseFloat(resFechaInicio[0]);
  var anioFin = parseFloat(resFechaFin[0]);
  var conteoDia = parseFloat(diaInicio);
  var conteoMes = parseFloat(mesInicio);
  var conteoAnio = parseFloat(anioInicio);
  var continuaGenerarFechas = true;
  var sMes = "";
  var sDia = "";  
  if(anioInicio <= anioFin){
    while(continuaGenerarFechas){
      
                        
                        if(conteoDia == 32){
        conteoDia = 0;
        conteoMes +=1;
      }
                         
                        
      if(conteoMes == 13 && conteoDia == 0){
        conteoDia = 1
        conteoMes = 1
        conteoAnio +=1
      }
                        
                         
      if(conteoDia == diaFin && conteoMes == mesFin && conteoAnio == anioFin){
        continuaGenerarFechas = false;
      }
      if(conteoMes <10){
  sMes = "0"+conteoMes;
  
      }else{
  sMes = conteoMes; 
  }
      if(conteoDia < 10 ){
       sDia = "0"+conteoDia;
  }else{
  sDia = conteoDia;
  }
               
      emit([conteoAnio+"-"+sMes+"-"+sDia, doc.idVehiculo])

      conteoDia += 1;


    }
  }
        
}

}



{
   "_id": "_design/consultarRangoProgramacionVigilanciaEjecutadas",
   "language": "javascript",
   "views": {
       "consultarRangoProgramacionVigilanciaEjecutadas": {
           "map": "function(doc) {\nif(doc.tipoDato == \"programacionVigilanciaEjecutadas\" && doc.activo){\n\tvar fechaInicio = doc.fechaInicio;\n\tvar fechaFin = doc.fechaFin;\n\tvar resFechaInicio = fechaInicio.split(\"-\");\n\tvar resFechaFin    = fechaFin.split(\"-\");\n\tvar diaInicio = parseFloat(resFechaInicio[2]);\n\tvar diaFin = parseFloat(resFechaFin[2]);\n\tvar mesInicio = parseFloat(resFechaInicio[1]);\n\tvar mesFin = parseFloat(resFechaFin[1]);\n\tvar anioInicio = parseFloat(resFechaInicio[0]);\n\tvar anioFin = parseFloat(resFechaFin[0]);\n\tvar conteoDia = parseFloat(diaInicio);\n\tvar conteoMes = parseFloat(mesInicio);\n\tvar conteoAnio = parseFloat(anioInicio);\n\tvar continuaGenerarFechas = true;\n        emit(fechaInicio,fechaFin)\n\tif(anioInicio <= anioFin){\n\t\twhile(continuaGenerarFechas){\n\t\t\t\n                        \n                        if(conteoDia == 32){\n\t\t\t\tconteoDia = 0;\n\t\t\t\tconteoMes +=1;\n\t\t\t}\n                         \n                        \n\t\t\tif(conteoMes == 13 && conteoDia == 0){\n\t\t\t\tconteoDia = 1\n\t\t\t\tconteoMes = 1\n\t\t\t\tconteoAnio +=1\n\t\t\t}\n                        \n                         \n\t\t\tif(conteoDia == diaFin && conteoMes == mesFin && conteoAnio == anioFin){\n\t\t\t\tcontinuaGenerarFechas = false;\n\t\t\t}\n                       \n\t\t\temit([conteoDia , conteoMes , conteoAnio],doc.idVehiculo, doc.idProgramacion)\n\n\t\t\tconteoDia += 1;\n\n\n\t\t}\n\t}\n        \n}\n\n}\n"
       }
   }
}
```

### llamadas 

```
{
   "_id": "_design/llamadas",
   "views": {
       "llamadas": {
           "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo){ emit( [ doc.sidLlamada] , null); } }"
       },
       "audiosLlamadas": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudio\" && doc.activo){ emit( [ doc.idLlamada] , null); } }"
       },
       "estadoLlamadas":{
          "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo){ emit( [ doc.idVehiculo, doc.estado] , null); } }"
      },
      "zonaAlarmasEnCurso":{
        "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.estado] , null); } }"
      },
      "llamadacapturaAudioZA":{
        "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo){ emit( [ doc.idLlamada, doc.estado] , null); } }"
      },
       "llamadasEnCurso":{
          "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo){ emit( [doc.estado] , null); } }"
      },
      "programacionVigilanciaEnCurso":{
        "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.estado] , null); } }"
      },
      "llamadacapturaAudioPV":{
        "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo){ emit( [ doc.idLlamada, doc.estado] , null); } }"
      },
      "llamadasRealizadasZA":{
        "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo && doc.estado == \"Finalizado\"){ emit( [ doc.idVehiculo, doc.zonaAlarmas] , null); } }"
      },
      "llamadasZAVehiculoLlamada":{
        "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.idLlamada] , null); } }"
      },
      "llamadasPVVehiculoLlamada":{
        "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.idLlamada] , null); } }"
      },
      "llamadasRealizadasPV":{
        "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo && doc.estado == \"Finalizado\"){ emit( [ doc.idVehiculo, doc.idProgramacion] , null); } }"
      },
      "llamadacapturaBotonPanico":{
        "map": "function(doc){ if(doc.tipoDato == \"capturaAudioBotonPanico\" && doc.activo){ emit( [ doc.idLlamada, doc.estado] , null); } }"
      },
      "llamadaEnCursoVehiculo":{
        "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo] , null); } }"
      },
      "buscarLlamadaConSID":{
        "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.sidLlamada] , null); } }"
      }      

   }
}
```

#diseno copia de llamadas es el que se enecuentra en couch dejo anterior por si se presenta #una falla

```
{
   "_id": "_design/llamadas",
   "_rev": "26-8e152920de2b6002e20908e246688414",
   "views": {
       "llamadas": {
           "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo){ emit( [doc.sidLlamada] , null); } }"
       },
       "audiosLlamadas": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudio\" && doc.activo){ emit( [ doc.idLlamada] , null); } }"
       },
       "estadoLlamadas": {
           "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo){ emit( [ doc.idVehiculo, doc.estado] , null); } }"
       },
       "zonaAlarmasEnCurso": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.estado] , null); } }"
       },
       "llamadacapturaAudioZA": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo){ emit( [ doc.idLlamada, doc.estado] , null); } }"
       },
       "llamadasEnCurso": {
           "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo){ emit( [doc.estado] , null); } }"
       },
       "programacionVigilanciaEnCurso": {
           "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.estado] , null); } }"
       },
       "llamadacapturaAudioPV": {
           "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo){ emit( [ doc.idLlamada, doc.estado] , null); } }"
       },
       "llamadasRealizadasZA": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo && doc.estado == \"Finalizado\"){ emit( [ doc.idVehiculo, doc.zonaAlarmas] , null); } }"
       },
       "llamadasZAVehiculoLlamada": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudioZonaAlarma\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.idLlamada] , null); } }"
       },
       "llamadasPVVehiculoLlamada": {
           "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo, doc.idLlamada] , null); } }"
       },
       "llamadasRealizadasPV": {
           "map": "function(doc){ if(doc.tipoDato == \"audioProgramacionVigilancia\" && doc.activo && doc.estado == \"Finalizado\"){ emit( [ doc.idVehiculo, doc.idProgramacion] , null); } }"
       },
       "llamadacapturaBotonPanico": {
           "map": "function(doc){ if(doc.tipoDato == \"capturaAudioBotonPanico\" && doc.activo){ emit( [ doc.idLlamada, doc.estado] , null); } }"
       },
       "llamadaEnCursoVehiculo": {
           "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.idVehiculo] , null); } }"
       },
       "buscarLlamadaConSID": {
           "map": "function(doc){ if(doc.tipoDato == \"llamadas\" && doc.activo && doc.estado == \"En curso\"){ emit( [ doc.sidLlamada] , null); } }"
       }
   }
}

```

### Alarmas

*Diseño:* `_design/alarmas`

~~~~~~~~~~~~~~~~~~~~~~~~~~~{javascript}
//alarmasRangoFecha
function(doc){
    if( doc.tipoDato == "zonaAlarma" && doc.activo ){
   	emit([doc.horaInicio, doc.tipoDato],null);	
    }else if(doc.tipoDato == "alarmasBotonPanico" && doc.activo){
	emit([doc.horaRegistrada, doc.tipoDato],null);
    }

}  

//alarmasTimestamp
function(doc){
    if( doc.tipoDato == "zonaAlarma" && doc.activo ){
    emit([doc.timeStamp, doc.tipoDato],null);  
    }else if(doc.tipoDato == "alarmasBotonPanico" && doc.activo){
  emit([doc.timeStamp, doc.tipoDato],null);
    }

}  

 "capturaImagenesAlarmaPanico": {
  "map": "function(doc){ if(doc.tipoDato == \"capturaImagenesBotonPanico\" && doc.activo){ emit( [doc.idAlarmaBotonPanico, doc.horaRegistrada ] , null); } }" 
   } 

 "capturaAudioAlarmaPanico": {
  "map": "function(doc){ if(doc.tipoDato == \"capturaAudioBotonPanico\" && doc.activo){ emit( [doc.idAlarmaBotonPanico, doc.horaRegistrada ] , null); } }" 
   }    

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


//alarmasRangoFechaPorVehiculo
~~~~~~~~~~~~~~~~~~~~~~~~~~~{javascript}
function(doc){
    if( doc.tipoDato == "zonaAlarma" && doc.activo ){
    emit([doc.idVehiculo, doc.horaInicio],null);  
    }else if(doc.tipoDato == "alarmasBotonPanico" && doc.activo){
  emit([doc.idVehiculo, doc.horaRegistrada],null);
    }

}  

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Design Estadisticas.

Rangos de paradas:

- R0-15

- R15-30

- R30-60

- R60-120

- R120

- R0-60

R0-15 = entre 0 y 15 minutos ; R120 = 120 minutos o mas

*Diseño:* `_design/estadisticas`

#### Pendientes Por Renderizar Estadisticas

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/pendientesPorRenderizarEstadisticas` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && doc.activo){
		if( ! ("complementosEstadisticas" in doc )){
			emit([doc.horaRegistrada, doc._id], null);
		}
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Kilometros recorridos por vehiculo por fecha.

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/kilometrosRecorridosPorVehiculoPorFecha` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && ("complementosEstadisticas" in doc) &&  doc.activo){
		
		emit([doc.idVehiculo, doc.horaRegistrada.substring(0,10)], doc.complementosEstadisticas.metrosRecorridos);
		
	}
}
//Reduce: _sum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Kilometros recorridos por vehiculo por fecha hora. 

Listas las posiciones que tienen registrada la fechaHora

*View:* `_design/estadisticas/view/kilometrosRecorridosPorVehiculoPorFechaHora` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && ("complementosEstadisticas" in doc) &&  doc.activo){
		
		emit([doc.idVehiculo, doc.horaRegistrada], doc.complementosEstadisticas.metrosRecorridos);
		
	}
}
//Reduce: _sum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



### Velocidad por vehiculo por fecha.

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/velocidadPorVehiculoPorFecha` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && ("complementosEstadisticas" in doc) &&  doc.activo){
		
		emit([doc.idVehiculo, doc.horaRegistrada.substring(0,10)], doc.complementosEstadisticas.velocidad);
		
	}
}
//Reduce: _stats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Tiempo Exceso de Velocidad por vehiculo por fecha.

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/tiempoExcesoVelocidaPorVehiculoPorFecha` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && ("complementosEstadisticas" in doc) &&  doc.activo){

		if(doc.complementosEstadisticas.idPrimerPuntoExcesoVelocidad != ""){
			emit([doc.idVehiculo, doc.horaRegistrada.substring(0,10)], doc.complementosEstadisticas.segundosAlPuntoAnterior);
		}
		
	}
}
//Reduce: _sum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


### CAntidad Excesos de Velocidad por vehiculo por fecha.

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/excesosVelocidaPorVehiculoPorFecha` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && ("complementosEstadisticas" in doc) &&  doc.activo){
		if(doc.complementosEstadisticas.idPrimerPuntoExcesoVelocidad != ""){
		    if (doc.complementosEstadisticas.idPrimerPuntoExcesoVelocidad == doc._id){
				emit([doc.idVehiculo, doc.horaRegistrada.substring(0,10)], null);
		    }			
		}		
	}
}
//Reduce: _count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Rangos paradas vehiculos

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/rangosParadasVehiculos` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc) {
    if (doc.tipoDato == "paradaVehiculo" && ("duracionParadaSegundos" in doc) && doc.activo) {
		
		var segundos = doc.duracionParadaSegundos;
		
		if( segundos >= 0 && segundos < 900 ){
			emit([doc.idVehiculo, "R0-15",   doc.fechahoraInicio.substring(0,10)], null);
		} else if( segundos >= 900 && segundos < 1800 ){
			emit([doc.idVehiculo, "R15-30",  doc.fechahoraInicio.substring(0,10)], null);
		} else if( segundos >= 1800 && segundos < 3600 ){
			emit([doc.idVehiculo, "R30-60",  doc.fechahoraInicio.substring(0,10)], null);
		} else if( segundos >= 3600 && segundos < 7200 ){
			emit([doc.idVehiculo, "R60-120", doc.fechahoraInicio.substring(0,10)], null);
		} else if( segundos >= 7200) {
			emit([doc.idVehiculo, "R120",    doc.fechahoraInicio.substring(0,10)], null);
		}

		if( segundos >= 0 && segundos < 3600 ){
			emit([doc.idVehiculo, "R0-60",   doc.fechahoraInicio.substring(0,10)], null);
		}
    }
}
//Reduce: _count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



### Tiempo Motor encendido por vehiculo por fecha.

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/tiempoMotorEncendidoPorVehiculoPorFecha` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if(doc.tipoDato == "posicionVehiculos" && ("complementosEstadisticas" in doc) && ('estaEncendidoMotor' in doc) &&  doc.activo){

		
		if(doc.estaEncendidoMotor){
			emit([doc.idVehiculo, doc.horaRegistrada.substring(0,10)], doc.complementosEstadisticas.segundosAlPuntoAnterior);
		}
		
	}
}
//Reduce: _sum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Cantidad de paradas de vehiculos

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/cantidadParadasVehiculos` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc) {
    if (doc.tipoDato == "paradaVehiculo" && doc.activo) {
        emit([doc.idVehiculo, doc.fechahoraInicio], null);
    }
}
//Reduce: _count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


### Cantidad de botones de pánico

Lista todas las posicionVehiculos que aun no tienen calculada la
información.

*View:* `_design/estadisticas/view/cantidadBotonesPanico` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc) {
	if(doc.tipoDato == "alarmasBotonPanico" && doc.activo){
		emit([doc.idVehiculo, doc.horaRegistrada.substring(0,10)],null);
    }    

}
//Reduce: _count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Paradas Vehiculos por Fecha

Muestra todas las paradas de los vehículos por fecha.

*View:* `_design/estadisticas/view/paradasVehiculosPorFecha` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc) {
	if(doc.tipoDato == "paradaVehiculo" && doc.activo){
		emit([doc.fechahoraInicio.substring(0,10)],null);
    }

}
//Reduce: NONE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



### Design GeoPosiciones.

*Diseño:* `_design/geoposiciones`

#### Geoposiciones Precalculadas

Lista todas las geoposiciones pasadas que ya se han calculado, esto
para ahorrar datos.

*View:* `_design/geoposiciones/view/geoposicionesPrecalculadas` 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if( (doc.tipoDato == "posicionVehiculos" || doc.tipoDato == "paradaVehiculo") && doc.nombreGeoposicion != ""  && doc.activo){
		
		emit([doc.latitud, doc.longitud], doc.nombreGeoposicion);
		
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Geoposiciones Pendientes

Lista todas las paradas que tiene pendientes el cálculo del nombre de la geoposición,

*View:* `_design/geoposiciones/view/geoposicionesPendientes`

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
function(doc){
	if( (doc.tipoDato == "posicionVehiculos" || doc.tipoDato == "paradaVehiculo") && ( !('nombreGeoposicion' in doc) || doc.nombreGeoposicion == ""  )  && doc.activo){
		
		emit([doc.tipoDato], null);
		
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



## web services

### autenticacion

*Nombre:* wsautenticar
*URL:* `http://localhost/ws/autenticar`
*Descripción:*

```
//Petición
{
  "accion" : "ingresar",
  "usuario" : "admin",
  "contrasena" : "123456",
  "tenant" : "exxonmobil"
}

//Respuesta
{
  "success" : true,
  "token" : "asdfasdfasdfasdf",
  "usuario" : "admin",
  "perfil" : "adminTenant",
  "tenant" : "exxonmobil"
}

```

### verificarCredenciales

*Nombre:* wsVerificarCredenciales
*URL:* `http://localhost/ws/verificarCredenciales`
*Descripción:* Verifica que el token del usuario sea válido.

```
//Petición
{
  "usuario" : "admin",
  "token"   : "asdkjj23sndm123j123asd",
  "tenant"  : "exxonmobil"
}

//Respuesta
{
  "success" : true
}

```


### Listado mapa vehículos

*Nombre:* wslistadoMapaVehiculos
*URL:* `http://localhost/ws/listadoMapaVehiculos`
*Descripción:* trae el listado de vehiculos para ser pintados en google maps

- estado : "activo" cuando envió señal en las ultimas horas, "inactivo" cuando no.
- velocidad: última velocidad registrada del vehículo
- opcionesAdicionalesPlataforma: ?????
- cadenaFrio: Datos de frio
- temperatura: en grados centigrados
- estadoTemperatura: "ok", "porencima", "pordebajo"

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {}
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa"      : "TVH123",
      "latitud"    : "75.3232323",
      "longitud"   : "-10.3232323",
      "estado"     : "activo",      
      "movimiento" : false
      "opcionesAdicionalesPlataforma" : null
      "velocidad"  : 0,
      "cadenaFrio" : {
          "temperatura" : 30,
          "estadoTemperatura" : "ok"
      }
    }
  ]
}

```

### Listado de vehículos

*Nombre:* wslistarVehiculos
*URL:* `http://localhost/ws/listadoVehiculos`
*Descripción:* trae el listado de vehiculos, velocidad en kilometros por hora

- *incluirDireccion:* por defecto true, si es true retorna la direcciones de geocoderFleet

//peticion

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
        "incluirDireccion" : true,
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa" : "TVH123",
      "marca" : "KEnworth",
      "modelo": "2014",
      "imeiGps"       : "l857482904667632",
      "numSimCard"    : "3147896544",
      "tipoGps"       : "VT1000",
      "ultimaPosicion" : {
          "latitud"        : -77.281298192,
          "longitud"       : 60.28128,
          "horaRecibida"   : "2016-03-12T08:07:19Z",
          "horaRegistrada" : "2016-03-12T08:07:19Z",
          "velocidad"      : 79.0212,
      },
      "direccion"  : "Cra 123 # 34-34"
    }
  ]
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Listado de paradaVehiculo

*Nombre:* wslistarParadaVehiculo
*URL:* `http://localhost/ws/listadoParadaVehiculo`
*Descripción:* trae el listado de la parada vehiculo 
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
  "fechaInicio" : "2014-01-12T08:07:19",
  "fechaFin"    : "2017-03-12T08:07:20",
  "id"          : "95ea81741bbfba959550827b15005700"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {

    "latitud"           : "-30.37812817283",
    "longitud"          : "70.6271265342323",
    "fechahoraInicio"   : "2016-03-12T08:07:19Z",
    "fechahoraFin"      : "2016-03-12T08:07:19Z",
    "idVehiculo"        : "3e8f127632561e88b4acd1d8f000626a"
    }

  ]
}

```



### Listado detalle de vehículos

*Nombre:* wslistadoDetalleVehiculo
*URL:* `http://localhost/ws/listadoDetalleVehiculo`
*Descripción:* trae el listado del vehiculo por placa 
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
  "id" : "95ea81741bbfba959550827b15003985"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa" : "TVH123",
      "marca" : "KEnworth",
      "modelo": "2014",
      "imeiGps"       : "l857482904667632",
      "numSimCard"    : "3147896544",
      "tipoGps"       : "VT1000"
    }
  ]
}

```


## Picker Vehiculos
*Nombre:* wsPickerVehiculos
*URL:* `http://localhost/ws/pickerVehiculos`
*Descripción:* Trae un listado de vehículos para pintar en un picker

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil" 
  },
  "data" : { }
}

//Respuesta
{
    "success" : true,
    "data"    : [
		{
			"id"     : "81201291212891082",
			"nombre" : "TTY789 - Raul Gutierrez",
			"conductor" : {
				"nombres"   : "Raul",
				"apellidos" : "Gutierrez",
				"cedula"    : "1288192"
			},
			"vehiculo" : {
				"placa" : "TTY789"
			}
		}
    ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


### Listado posicion vehiculo por rango fecha 

*Nombre:* wsPosicionVehiculoRangoFecha
*URL:* `http://localhost/ws/posicionVehiculoRangoFecha`
*Descripción:* trae el listado de las posiciones del vehiculo por fechas 

- intercalarDatos: booleano (opcional), si true, no trae todos los datos en el
  rango sino que trae máximo los especificados en el campo
  numeroDatosIntercalados
  
- numeroDatosIntercalados: entero (opcional), define cuantos datos de deben intercalar.

- velocidad: en kilometros por hora

~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
	"autenticacion" : {
		"usuario" : "admin",
		"token" : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant" : "exxonmobil" 
	},

	"data" : {
		"fechaInicio"             : "2016-01-12T08:07:19",
		"fechaFin"                : "2016-03-12T08:07:20",
		"idVehiculo"              : "4212212132321132",
		"intercalarDatos"         : true,
		"numeroDatosIntercalados" : 1000
	}
}

//Respuesta
{
	"success" : true,
	"data" : [
      {
		  
		  "idVehiculo" : "812736127qhdtastdah",
		  "horaRegistrada": "2016-03-12T08:07:19Z",
		  "horaRecibida"  : "2016-03-12T08:07:19Z",
		  "latitud"       : "-30.37812817283",
		  "longitud"      : "70.6271265342323",
		  "velocidad"     : 30.75
      }		
  ]
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~


### Listado ultima posicion por identificador 

*Nombre:* wsultimaPosicionVehiculo
*URL:* `http://localhost/ws/ultimaPosicionVehiculo`
*Descripción:* trae el la ultima posicion del vehículo 
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
  "id" : "95ea81741bbfba959550827b15003985"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {

    "idVehiculo" : "812736127qhdtastdah",
    "horaRegistrada": "2016-03-12T08:07:19Z",
    "horaRecibida"  : "2016-03-12T08:07:19Z",
    "latitud"       : "-30.37812817283",
    "longitud"      : "70.6271265342323",
    "ultimaPosicion"     : true 
    }

  ]
}

```


### Listado posicion vehiculo por rango fecha por imagenes

*Nombre:* wsVehiculoRangoFechaCapturaImagen
*URL:* `http://localhost/ws/vehiculoRangoFechaCapturaImagen`
*Descripción:* trae el listado de las posiciones del vehiculo  con imagenes por fechas
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
  "fechaInicio": "2015-01-12T08:07:19",
  "fechaFin": "2016-03-12T08:07:20"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {

    "idVehiculo" : "812736127qhdtastdah",
    "horaRegistrada": "2016-03-12T08:07:19Z",
    "latitud"       : "-30.37812817283",
    "longitud"      : "70.6271265342323",
    "idAudio"        : "131239183719271382",
    "urlAudio"       : "http://localhost/nisabu/audio/723498213471293487"
    }

  ]
}

```


### Listado posicion vehiculo por rango fecha por audio

*Nombre:* wsvehiculoRangoFechaCapturaAudio
*URL:* `http://localhost/ws/vehiculoRangoFechaCapturaAudio`
*Descripción:* trae el listado de las posiciones del vehiculo  con Audio por fechas
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
  "fechaInicio": "2015-01-12T08:07:19",
  "fechaFin": "2016-03-12T08:07:20"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {

    "idVehiculo" : "812736127qhdtastdah",
    "horaRegistrada": "2016-03-12T08:07:19Z",
    "latitud"       : "-30.37812817283",
    "longitud"      : "70.6271265342323",
    "idAudio"        : "131239183719271382",
    "urlAudio"       : "http://localhost/nisabu/audio/723498213471293487"

    }

  ]
}

```

### Listado posicion vehiculo por rango fecha alarma

*Nombre:* wsvehiculoRangoFechaAlarma
*URL:* `http://localhost/ws/vehiculoRangoFechaAlarma`
*Descripción:* trae el listado de las posiciones del vehiculo según el filtro de alarmas
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
  "fechaInicio": "2015-01-12T08:07:19",
  "fechaFin": "2016-03-12T08:07:20"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {

    "idVehiculo" : "812736127qhdtastdah",
    "horaRegistrada": "2016-03-12T08:07:19Z",
    "descripcion" : "ingreso a zona restringida",
    "idCaptura"        : "131239183719271382",
    "urlCaptura"       : "http://localhost/nisabu/audio/723498213471293487"
    "tipoCaptura" : "audio", "imagen"
    }

  ]
}

```    


### Listado de zonas monitoreadas
*Nombre:* wsmonitoreoZonas
*URL:* `http://localhost/ws/monitoreoZonas`
*Descripción:* trae la información de las zonas monitoreadas
//peticion

```


//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {}
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
    "nombre"      : "Zona de descargue",
    "latitud"         : "-30.378128,70.66216",
    "longitud" : "-25.4555",
    "radio" : "500m",
    "tipoVigilancia": "solo audio"
    }

  ]
}

```    


### Listado de vigilancias
*Nombre:* wslistarVigilancias
*URL:* `http://localhost/ws/listarVigilancias`
*Descripción:* trae la información de las vigilancias de un vehiculo
//peticion

```


//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {}
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
    "idVehiculo"  : "378482378423498",
    "fechaInicio" : "2016-03-12",
    "fechaFin"    : "2016-03-12",
    "horaInicio"  : "07:19",
    "horaFin"     : "07:59",
    "registrarAudio"  : true,
    "registrarImagen" : false,
    }

  ]
}


  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

<!-- ========================================================= -->
# Módulo

### Crear monitoreoZonas

*Nombre:* wscrearZonas
*Descripción:* ---
*url:* `http://localhost/ws/crearZonas`
```js
{

  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },


  "data" : {
    "nombre"    : "Zona de descargue 2",
    "descripcion" : "nota del proceso 2",
    "registrarAudio" : true,
    "registrarImagen" : false,
    "tiempoMaxGrabAudio": "70.2121212",
    "numeroCapturasMax" : "30",
    "latitud"             : "4.5981",
    "longitud"            : "-74.0758",
    "radio"               : "300"

    }
}

//http://localhost/ws/crearzonas
{
    "success" : true
}
```


<!-- ------------------------------------------------------------ -->

### Eliminar  monitoreoZonas


*Nombre:* wseliminarMonitoreoZonas
*Descripción:* ---
*url:* `http://localhost/ws/eliminarZonas`
```js
{
 
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

    "data" : {
  "id"        : "3e8f127632561e88b4acd1d8f0005d24"
    }
}


{
    "success" : true
}
```

<!-- ------------------------------------------------------------ -->




<!-- ========================================================= -->
# Módulo

### Crear programacion

*Nombre:* wscrearProgramacion
*Descripción:* Guarda una programacion
*url:* `http://localhost/ws/crearProgramacion`
```js
{

  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },


  "data" : {
    "idVehiculo"  : "378482378423498",
    "registrarAudio"      : true,
    "registrarImagen"     : false,
    "fechaInicio" : "2016-03-12",
    "fechaFin"    : "2016-03-12",
    "horaInicio"  : "07:19",
    "horaFin"     : "07:59"

    }
}

//http://localhost/ws/crearProgramacion
{
    "success" : true
}
```

### Listado de programacion vigilancia

*Nombre:* wslistarProgramacionVigilancia
*URL:* `http://localhost/ws/listadoProgramacionVigilancia`
*Descripción:* trae el listado de la programacion vigilanca 
//peticion

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {}
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa" : "TVH123",
      "registrarAudio"      : true,
      "registrarImagen"     : false,
      "fechaInicio" : "2016-03-12",
      "fechaFin"    : "2016-03-12",
      "horaInicio"  : "07:19",
      "horaFin"     : "07:59"

    }
  ]
}

```
<!-- ------------------------------------------------------------ -->

### Eliminar  programacionVigilancia


*Nombre:* wseliminarprogramacionVigilancia
*Descripción:* ---
*url:* `http://localhost/ws/eliminarProgramacionVigilancia`
```js
{
 
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

    "data" : {
  "id"        : "9c5fb7617f6ffe09f7907348c30022ab"
    }
}

//http://localhost/ws/editarrol
{
    "success" : true
}
```

###----------------pendiente
### Listado de zona Alarma
*Nombre:* wszonaAlarma
*URL:* `http://localhost/ws/zonaAlarmas`
*Descripción:* trae la información de las zonas zonas de las alarmas
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
  "id"        : "3e8f127632561e88b4acd1d8f000626a"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
    "idVehiculo"      : "ca759f5632ec30e319570ba94b000743",
    "placa" :"TYV334"
    }

  ]
}

```  



### Listado detalle de zonas

*Nombre:* wslistarDetalleZona
*URL:* `http://localhost/ws/listadoDetalleZona`
*Descripción:* trae el listado de zonas
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
  "id" : "3e8f127632561e88b4acd1d8f000626a"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
    "nombre"    : "Zona de descargue 2",
    "descripcion" : "nota del proceso 2",
    "registrarAudio" : true,
    "registrarImagen" : false,
    "tiempoMaxGrabAudio": "70.2121212",
    "numeroCapturasMax" : "30",
    "latitud"             : "4.5981",
    "longitud"            : "-74.0758",
    "radio"               : "300"

    }
  ]
}

```



### Listado de la zona alarma

*Nombre:* wslistarDetalleZonaAlarma
*URL:* `http://localhost/ws/listadoDetalleZonaAlarma`
*Descripción:* trae el listado de zona alarma
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
  "id" : "3e8f127632561e88b4acd1d8f000626a"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
   "fecha": "2016-03-12",
   "horaInicio": "07:19",
   "horaFin": "07:19",
   "estado": "En curso",
   "idVehiculo": "3e8f127632561e88b4acd1d8f000626a",
   "idZona": "95ea81741bbfba959550827b15003985"
    }
  ]
}

```


### Listado detalle vehiculo de la zona Alrma

*Nombre:* wslistadoDetalleVehiculo
*URL:* `http://localhost/ws/listadoDetalleVehiculoZonaAlarma`
*Descripción:* trae el listado del detalle del vehículo de la zona alarma 
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
  "id" : "026b8e0d73b1739a3871cda683004e7e"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa" : "TVH123",
      "marca" : "KEnworth",
      "modelo": "2014",
      "imeiGps"       : "l857482904667632",
      "numSimCard"    : "3147896544",
      "tipoGps"       : "VT1000"
    }
  ]
}

```


### Listado detalle posicion vehículo por zona Alarma

*Nombre:* wslistarPosicionZonaAlarma
*URL:* `http://localhost/ws/listadoPosicionZonaAlarma`
*Descripción:* trae el listado del detalle del vehículo de la zona alarma 
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
  "id" : "026b8e0d73b1739a3871cda683004e7e"
  }
}


//Respuesta
{
  "success" : true,
  "data" : [
    {
      "horaRegistrada" : "2016-03-12T08:07:19Z",
      "horaRecibida" : "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220",
      "velocidad"       : "30.35 km/h"
    }
  ]
}

```

###===================================================


### Listado detalle de las imagenes por zona Alarma

*Nombre:* wslistarCapturaImagenesZonaAlarma
*URL:* `http://localhost/ws/listadoCapturaImagenesZonaAlarma`
*Descripción:* trae el listado de las capturas de imagenes de la zona alarma 
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
  "id" : "026b8e0d73b1739a3871cda683004e7e"
  }
}


//Respuesta
{
  "success" : true,
  "data" : [
    {
      "horaRegistrada" : "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220"
    }
  ]
}

```

###===================================================



### Listado detalle de las audios por zona Alarma

*Nombre:* wslistarCapturaAudiosZonaAlarma
*URL:* `http://localhost/ws/listadoCapturaAudiosZonaAlarma`
*Descripción:* trae el listado de las capturas de audios de la zona alarma 
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
  "id" : "026b8e0d73b1739a3871cda683004e7e"
  }
}


//Respuesta
{
  "success" : true,
  "data" : [
    {
      "horaRegistrada" : "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220",
      "Duracion" :"grabando..."
    }
  ]
}

```

###===================================================


### Listado de vehículos

*Nombre:* wslistVehiculos
*URL:* `http://localhost/ws/listVehiculos`
*Descripción:* trae el listado de vehiculos para ser pintados en datapicker
```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {}
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa" : "TVH123",
    }
  ]
}

```
<!-- ========================================================= -->
# Módulo

### Crear programacionVigilancia

*Nombre:* wscrearProgramacionVigilancia
*Descripción:* ---
*url:* `http://localhost/ws/crearProgramacionVigilancia`
```js
{

  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },


  "data" : {
    "idVehiculo"  : "95ea81741bbfba959550827b15003985",
    "registrarAudio"      : true,
    "registrarImagen"     : false,
    "capturasMax"         : "20",
    "fechaInicio" : "2016-03-12",
    "fechaFin"    : "2016-03-12",
    "horaInicio"  : "07:19",
    "horaFin"     : "07:59",
    "estadoProgramacion" : "finalizado"

    }
}

//http://localhost/ws/programacionVigilancia
{
    "success" : true
}
```

### Listado campos vehículo por programacion vigilancia

*Nombre:* wslistarDetalleVehiculoProgramacionVigilancia
*URL:* `http://localhost/ws/listadoDetalleVehiculoProgramacionVigilancia`
*Descripción:* trae el listado de vehiculos 
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
  "id" : "64dab9c38af9d45fc669c7456d004bf1"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      "idVehiculo" : "812736127qhdtastdah",
      "placa" : "TVH123",
      "marca" : "KEnworth",
      "modelo": "2014",
      "imeiGps"       : "l857482904667632",
      "numSimCard"    : "3147896544",
      "tipoGps"       : "VT1000"
    }
  ]
}

```



### Listado detalle posicion vehículo vigilancia

*Nombre:* wslistarPosicionesVehiculoVigilancia
*URL:* `http://localhost/ws/listadoPosicionesVehiculoVigilancia`
*Descripción:* trae el listado de las posiciones de un vehiculo en particular 
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
  "id" : "64dab9c38af9d45fc669c7456d004bf1"
  }
}


//Respuesta
{
  "success" : true,
  "data" : [
    {
      "horaRegistrada" : "2016-03-12T08:07:19Z",
      "horaRecibida" : "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220",
      "velocidad"       : "30.35 km/h"
    }
  ]
}

```

###===================================================



###===================================================


### Listado detalle de las imagenes por programacion vigilancia

*Nombre:* wslistarImagenesProgramacionVigilancia
*URL:* `http://localhost/ws/listadoImagenesProgramacionVigilancia`
*Descripción:* trae el listado de las capturas de imagenes de la programacion vigilancia
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
  "id" : "64dab9c38af9d45fc669c7456d004bf1"
  }
}


//Respuesta
{
  "success" : true,
  "data" : [
    {
      "horaRegistrada" : "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220"
    }
  ]
}

```

###===================================================



### Listado detalle de las audios por programacion vigilancia

*Nombre:* wslistarAudiosProgramacionVigilancia
*URL:* `http://localhost/ws/listadoAudiosProgramacionVigilancia`
*Descripción:* trae el listado de las capturas de audios de la programacion vigilancia
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
  "id" : "6f82b5881412978eed2265b9a90008c4"
  }
}


//Respuesta
{
  "success" : true,
  "data" : [
    {
      "horaRegistrada" : "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220",
      "Duracion" :"grabando..."
    }
  ]
}

```

###===================================================


### Listado de paradas por rango fecha

*Nombre:* wsparadaPorRangoFecha
*URL:* `http://localhost/ws/listadoParadaPorRangoFecha`
*Descripción:* trae el listado del promedio de paradas
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
  "fechaInicio": "2014-01-12T08:07:19",
  "fechaFin": "2017-10-12T08:07:20"
  }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {

    "horaRegistrada": "2016-03-12T08:07:19Z",
      "latitud" : "10,9642",
      "longitud": "-5,5220"
    }

  ]
}

``` 



{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "fechaInicio": "2020-01-12T08:07:19",
  "fechaFin": "2020-10-12T08:07:20"
  }
}


//===================================================================

### SolicitarCapturaAudio

*Nombre:* wssolicitarCapturaAudio
*URL:* `http://localhost/ws/solicitarCapturaAudio`
*Descripción:*  solicita a twilio la llamada a un dispositivo para que guarde la grabacion
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
    "idVehiculo"  : "95ea81741bbfba959550827b15005700"
  }
}

//Respuesta
{
    "success" : true
}
```
//==========================================================================
#verificar estado de llamada

*Nombre:* wsverificarEstadoLlamada
*URL:* `http://localhost/ws/verificarEstadoLlamada`
*Descripción:* Verifica el estado de la llamada para pintar un botón a stop  
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
    "idVehiculo"  : "95ea81741bbfba959550827b15005700"
  }
}

//Respuesta
{
    "success" : true
}
```

### Listado de alarmas

*Nombre:* wslistarAlarmas 

*URL:* `http://localhost/ws/listadoAlarmas`

*Descripción:* actualmente hay dos tipos de alarmas `zonaAlarma` y
`alarmasBotonPanico`, idDocumento corresponde al id documento según
corresponda el tipoAlarma.

~~~~~~~~~~~~~~~~~~~~~~~~~~{javascript}
//Petición
{
    "autenticacion" : {
	"usuario" : "admin",
	"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
	"tenant"  : "exxonmobil" 
    },
    
    "data" : {
	"fechaInicio" : "2014-01-12T08:07:19",
	"fechaFin"    : "2017-03-12T08:07:20"
    }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
	"tipoAlarma"    : "zonaAlarma"
	"id"            : "813y12ui312g312h3j12g"
	"horaRegistrada": "2014-10-25T21:35Z",		
	"idVehiculo"    : "811923912312903821",
	"placa"         : "TVH123",
	"latitud"       : "75.2121212",
	"logitud"       : "-14.281291",	
    }
  ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


### Listado detalleAlarmaPanico

*Nombre:* wslistarDetalleAlarmaPanico 

*URL:* `http://localhost:8080/ws/listadoDetalleAlarmaPanico`

*Descripción:* actualmente hay dos tipos de alarmas `zonaAlarma` y
`alarmasBotonPanico`, idDocumento corresponde al id documento según
corresponda el tipoAlarma.

~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
  "usuario" : "admin",
  "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
  "tenant"  : "exxonmobil" 
    },
    
    "data" : {
      "id" :  "5ff7fb03366934d344ed968c90001659" 
    }
}

//Respuesta
{
  "success" : true,
  "data" : [
    {
      'placa' : "abc456",
      'marca' : "chevrolet,
      'modelo' : "2014",                
      'imeiGps' : "457879435132,
      'numSimCard' : "351651101",
      'tipoGps' : "docVehiculo.get("tipoGps", "")",
      'latitud' : "-3.2511",
      'longitud': "5235646512"
    }
  ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### traer buscarLlamadaActivaDirecta

*Nombre:* wsbuscarLlamadaActivaDirecta 

*URL:* `http://localhost:8080/ws/buscarLlamadaActivaDirecta`

*Descripción:* actualmente hay dos tipos de alarmas `zonaAlarma` y
`alarmasBotonPanico`, idDocumento corresponde al id documento según
corresponda el tipoAlarma.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
  "usuario" : "admin",
  "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
  "tenant"  : "exxonmobil" 
    },
    
    "DATA" : {
      "IDVEHICULO" :  "95EA81741BBFBA959550827B15005700" 
    }
}

//RESPUESTA
{
  "SUCCESS" : TRUE,
  "DATA" : [
    {
      'PLACA' : "ABC456",
      'MARCA' : "CHEVROLET,
      'MODELO' : "2014",                
      'IMEIGPS' : "457879435132,
      'NUMSIMCARD' : "351651101",
      'TIPOGPS' : "DOCVEHICULO.GET("TIPOGPS", "")",
      'LATITUD' : "-3.2511",
      'LONGITUD': "5235646512"
    }
  ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Crear Tipo Zona
*Nombre:* wsCrearTipoZona
*URL:* `http://localhost/ws/crearTipoZona`
*Descripción:* crear un tipo zona.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
    },
    
    "data" : {
      "nombre" : "Parqueadero",
	  "descripcion" : "Sitios de parqueo"
    }
}

//RESPUESTA
{
	"success" : true,
	"data"    : {}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Detalle Tipo Zona
*Nombre:* wsDetalleTipoZona
*URL:* `http://localhost/ws/detalleTipoZona`
*Descripción:* Detalle un tipo zona.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
    },
    
    "data" : {
		"idTipoZona" : "1289129c8912819s981928s903",		
    }
}

//RESPUESTA
{
	"success" : true,
	"data"    : {
		"id"     : "1289129c8912819s981928s903",
		"nombre" : "parqueadero",
	    "descripcion" : "Sitios de parqueo",
		"activo" : true		
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Editar Tipo Zona
*Nombre:* wsEditarTipoZona
*URL:* `http://localhost/ws/EditarTipoZona`
*Descripción:* edita un tipo zona

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
    },
    
    "data" : {
		"id"         : "1289129c8912819s981928s903",		
		"nombre"     : "parqueadero",
	    "descripcion" : "Sitios de parqueo",
		"activo"     : true,
    }
}

//RESPUESTA
{
	"success" : true,
	"data"    : { }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Listar Tipo Zona
*Nombre:* wsListarTiposZonaz
*URL:* `http://localhost/ws/listarTiposZonas`
*Descripción:* listar un tipo zona.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
    },
    
    "data" : [{
		"id"         : "1289129c8912819s981928s903",		
		"nombre"     : "parqueadero",		
	    "descripcion" : "Sitios de parqueo",
		"activo"     : true,
		"eliminado"  : false
    }]
}

//RESPUESTA
{
	"success" : true,
	"data"    : { }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Eliminar Tipo Zona
*Nombre:* wsEliminarTipoZona
*URL:* `http://localhost/ws/EliminarTipoZona`
*Descripción:* edita un tipo zona

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
		"usuario" : "admin",
		"token"   : "5776d71ff8f8442ca8326d04987a9bdc",
		"tenant"  : "exxonmobil" 
    },
    
    "data" : {
		"id"         : "1289129c8912819s981928s903"
    }
}

//RESPUESTA
{
	"success" : true,
	"data"    : { }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulo Reportes

## Reporte estádisticas por vehículos

*Nombre:* wsReporteEstadisticasVehiculos
*URL:* `http://localhost:8080/ws/reporteEstadisticasVehiculos`
*Descripción:* Trae el listado de completo de campos correspondiente a los reportesm, trae todos los campos.


- *vehiculos:* Esta campo si está vació o no viene se asume que son todos los vehiculos.
- *kilometrosRecorridos:* Número en kilometros
- *velocidadPromedio:*  en km/h
- *Duración excesos de velocidad* : en segundos
- *TiempoEncendido:* en segundo, tiempo total de encendido del motor.
- *NumeroPanicos:* Número de panicos
- *consumoGalCombustible:* Cantidad de  galones consumidos según los kilometros recorridos.

~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
	  "fechaInicio" : "2014-01-12T08:07:19",
	  "fechaFin"    : "2017-03-12T08:07:20",
	  "vehiculos"   : [
		  "9114de62e4a98b11669dd37ff5a40c71",
		  "95ea81741bbfba959550827b15005700"
	  ]
	  
  }
}

//respuesta:

{
  "success" : true,
  "data" : [
    {
		"idVehiculo"    : "18291829",
		"placaVehiculo" : "tku123",
		"kilometrosRecorridos"     : 88.5,
		"velocidadPromedio"        : 99.77
		"excesosVelocidad"         : 33,
		"duracionExcesosVelocidad" : 38912,
		"velocidadMaxima"          : 120.77,
		"totalParadas"             : 6,
		"paradasRangos"            : [
			{
				"codigoRango" : "R001",
				"nombreRango" : "Menor <1hora",
				"valorRango"  : "500"
			},
			{
				"codigoRango" : "R002",				
				"valorRango"  : "500"
			}
		],
		"tiempoEncedido" : 389912,
		"numeroPanicos"  : 21,
		"desconexionesBateria" : 12,
		"consumoGalCombustible" : 271827182
    }

  ]
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Reporte Estadísticas de vehículo por día

*Nombre:* wsReporteEstadisticasVehiculoPorDia
*URL:* `http://localhost:8080/ws/reporteEstadisticasVehiculoPorDia`
*Descripción:* Trae el listado de completo de campos correspondiente a los reportesm, trae todos los campos.


- *vehiculos:* Esta campo si está vació o no viene se asume que son todos los vehiculos.
- *kilometrosRecorridos:* Número en kilometros
- *velocidadPromedio:*  en km/h
- *Duración excesos de velocidad* : en segundos
- *TiempoEncendido:* en segundo, tiempo total de encendido del motor.
- *NumeroPanicos:* Número de panicos
- *consumoGalCombustible:* Cantidad de  galones consumidos según los kilometros recorridos.


~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
	  "fechaInicio" : "2017-02-20T08:07:19",
	  "fechaFin"    : "2017-02-24T08:07:20",
	  "idVehiculo"  : "9114de62e4a98b11669dd37ff5a40c71"
	  
  }
}

//respuesta:

{
	"success" : true,
	"data" : [
		{
			"fecha"         : "2014-01-12",
			"idVehiculo"    : "18291829",
			"placaVehiculo" : "tku123",
			"kilometrosRecorridos"     : 88.5,
			"velocidadPromedio"        : 99.77
			"excesosVelocidad"         : 33,
			"duracionExcesosVelocidad" : 38912,
			"velocidadMaxima"          : 120.77,
			"totalParadas"             : 6,
			"paradasRangos"            : [
				{
					"codigoRango" : "R0-60",
					"valorRango"  : "500"
				},
				{
					"codigoRango" : "R60-120"
					"valorRango"  : "500"
				}
			],
			"tiempoEncedido" : 389912,
			"numeroPanicos"  : 21,
			"desconexionesBateria" : 12,			
			"consumoGalCombustible" : 271827182
		}

	]
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Reporte Paradas de vehículo

*Nombre:* wsReporteParadasVehiculo
*URL:* `http://localhost:8080/ws/reporteParadasVehiculo`
*Descripción:* Trae el listado de las paradas de los vehículos.

- *Vehiculos:* Si vehiculos  esta vacio o se envía signnifca que son todos los vehiculos.
- *NombreGeoPosición:* Dirección en texto de la posición. Geolocalización reverse.

- *duracionInicioMinutos:* Filtrar los valores anteriores a este. mandar en 0 para no aplicar
- *duracionFinMinutos:* filtrar los valores posteriores a este, mandar en 0 pra no aplicar
~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
	  "fechaInicio" : "2017-02-20T08:07:19",
	  "fechaFin"    : "2017-02-24T08:07:19",
	  "duracionInicioMinutos" : 0,
	  "duracionFinMinutos" : 15,
	  "vehiculos"   : [
		  "9114de62e4a98b11669dd37ff5a40c71"
	  ]	  
  }
}

//respuesta:

{
  "success" : true,
  "data" : [
    {
		"idVehiculo"    : "18291829",
		"placaVehiculo" : "tku123",
		"latitud"           : "-30.37812817283",
		"longitud"          : "70.6271265342323",
		"fechahoraInicio"   : "2016-03-12T08:07:19Z",
		"fechahoraFin"      : "2016-03-12T08:07:19Z",
		"idVehiculo"        : "3e8f127632561e88b4acd1d8f000626a"
		"nombreGeoposicion" : "Av 123 Cali colombia",
		"duracionMinutos"   : "1"
    }

  ]
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Reporte Gráfico Vehículos por Estadistica

*Nombre:* wsReporteGraficoVehiculosPorEstadistica
*URL:* `http://localhost:8080/ws/reporteGraficoVehiculosPorEstadistica`
*Descripción:* Se muestra un grafico vehiculo por estadística.

Los campos 

- `kilometrosRecorridos`

- `velocidadPromedio`

- `excesosVelocidad`

- `duracionExcesosVelocidad` 

- `velocidadMaxima` 

- `totalParadas` 

- `paradaR001` : es parada y el nombre del codigo de la parada.

- `tiempoEncedido` en minutos

- `numeroPanicos`

- `desconexionesBateria`

- `consumoGalCombustible`



~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
	  "fechaInicio"  : "2017-02-20T08:07:19",
	  "fechaFin"     : "2017-02-24T08:07:19",
	  "vehiculos"    : ["9114de62e4a98b11669dd37ff5a40c71"],
	  "tipoEstadistica" : "totalParadas"
  }
}

//respuesta:

{
  "success" : true,
  "data" : {
	  "valores":[
		  {
		      "idVehiculo"    : "121212",
			  "placaVehiculo" : "TYU123" 
			  "valor"         : 77		
			  
		  },
		  {
			  "idVehiculo"    : "121212",
			  "placaVehiculo" : "TYU123" 
			  "valor"         : 77		
			  
		  }
	  ]
  }
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reporte Gráfico Vehículo Estadistica por fecha

*Nombre:* wsReporteGraficoVehiculoEstadisticaPorFecha
*URL:* `http://localhost:8080/ws/reporteGraficoVehiculoEstadisticaPorFecha`
*Descripción:* Se muestra un grafico vehiculo por estadística.


Valores tipo vehículo

- `kilometrosRecorridos`

- `velocidadPromedio`

- `excesosVelocidad`

- `duracionExcesosVelocidad` 

- `velocidadMaxima` 

- `totalParadas` 

- `paradaR001` : es parada y el nombre del codigo de la parada.

- `tiempoEncedido`

- `numeroPanicos`

- `desconexionesBateria`

- `consumoGalCombustible`


~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
	  "fechaInicio"  : "2017-02-20T08:07:19",
	  "fechaFin"     : "2017-02-24T08:07:19",
	  "idVehiculo"   : "9114de62e4a98b11669dd37ff5a40c71",
	  "tipoEstadistica" : "totalParadas"
  }
}

//respuesta:

{
  "success" : true,
  "data" : [
      {
		  "idVehiculo"    : "128129182",
		  "fecha" : "2014-12-24",
		  "valor"         : 77		
		  
      },
	  {
		  "idVehiculo"    : "128129182",
		  "fecha"         : "2014-12-25",
		  "valor"         : 89		
		  
	  }
	  

  ]
}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Reporte paradas vehículos en zonas

*Nombre:* wsReporteParadasVehiculosEnZonas
*URL:* `http://localhost:8080/ws/reporteParadasVehiculos`
*Descripción:* Se muestra un listado de paradas de vehículos según el tipo de zonas en que haya entrado.

Campos:

*vehiculos:* listado de vehiculos de filtro del reporte, se puede omitir o mandar solo [] si se quieren todos.

*tipoZonas:* listado de tipoZonas de filtro del reporte, se puede omitir o mandar solo []


~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil"
  },

  "data" : {
	  "fechaInicio"  : "2017-02-20T08:07:19",
	  "fechaFin"     : "2017-02-24T08:07:19",
	  "vehiculos"    : [ "af1820ab21ce", "af1820ab21ce"],
	  "tipoZonas"    : [ "af1820ab21ce", "18291281928a"]
  }
}

//respuesta:

{
  "success" : true,
  "data" : [
	  {
		  "latitud"           : "-30.37812817283",
		  "longitud"          : "70.6271265342323",
		  "fechahoraInicio"   : "2016-03-12T08:07:19Z",
		  "fechahoraFin"      : "2016-03-12T08:07:19Z",
		  "idVehiculo"        : "3e8f127632561e88b4acd1d8f000626a",
		  "duracionParadaSegundos" : 2123,
		  "vehiculo" : {
			  "placa" : "TVH123"
		  },
		  "zonas" : [{
			  "id"                  : "192019212121910",
			  "nombre"              : "Zona de descargue"
		  }],
		  "tipoZonas" : [{
			  "id"          : "1298102912h1i2h121",
			  "nombre"      : "Parqueadero",
			  "descripcion" : "Sitio de parqueo de vehiculos",
		  }]
		  
	  }
  ]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reporte mapa de calor de actividad por vehículo

*Nombre:* wsReporteMapaCalorActividadPorVehiculo
*URL:* `http://localhost:8080/ws/reporteMapaCalorActividadVehiculo`
*Descripción:* Se retorna los datos para generar el mapa de calor por vehículo según los kilometros recorridos.

*maximoValor:* valor máximo encontrado en el rango

*puntosDeCalor:* array dia a dia con cada uno de los puntos.

*dia:* fecha del día

*horas:* listado de horas de ese día

*hora:* hora del día, rango de 0 a 23

*kms:* kilometros recorridos

*color:* Valor en hexadecimal tipo html-css.

*intensidad:* valor entre 0.0 y 1.0 

~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil"
  },

  "data" : {
	  "fechaInicio"  : "2017-08-01",
	  "fechaFin"     : "2017-08-08",
	  "idVehiculo"   : "1829182192"
  }
}

//respuesta:

{
  "success" : true,
  "data" :  {
	"maximoValor"   : 200.0,
	"rangoInicio"   : "2014-08-01",
	"rangoFin"      : "2014-08-15",
	"puntosDeCalor" : [
		{
			"dia"   : "2014-08-01",
			"horas" : [
				{
					"hora"       : 0,
					"horaFormato": "12:00am",
					"kms"        : 100.0,
					"color"      : "#FF00FF",
					"intensidad" : 1.0
				},{
					"hora"       : 1,
					"horaFormato": "01:00am",
					"kms"        : 100.00,
					"color"      : "#FF00FF",
					"intensidad" : 0.5
				}				
			] 
		}
		
	]
	
  }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reporte Calificación de Conductores

*Nombre:* wsReporteCalificacionConductores
*URL:* `http://localhost:8080/ws/reporteCalificacionConductores`
*Descripción:* Trae las calificaciones día por día de los conductores en este rango de fechas.

*conductores:* lista de conductores para filtrar el resultado, mandar [] o no mandar llave para todos.
*calificacion:* valor entre 0 y 100
~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil"
  },

  "data" : {
	  "fechaInicio"  : "2017-08-01",
	  "fechaFin"     : "2017-08-08",
	  "conductores"  : ["1298128192018291", "19820918201821829"]
  }
}

//respuesta:

{
  "success" : true,
  "data" :  [
	  {
		  "idConductor"     : "128091820918209128",
		  "conductor" : {
			  "nombres"   : "Hector",
			  "apellidos" : "Machuca",
			  "celular"   : "5555",
			  "cedula"    : "12345"
		  },
		  "calificaciones" :  [
			  {
				  "dia" : "2015-16-08",
				  "calificacion" : "100"
			  }
		  ]		  
		  
	  }
  ]
	
	
  
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reporte Conducción por fuera de horario

*Nombre:* wsReporteConduccionPorFueraDeHorario
*URL:* `http://localhost:8080/ws/reporteConduccionPorFueraDeHorario`
*Descripción:* Trae las conducciones por fuera los de horarios indicados

~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil"
  },

  "data" : {
	  "fechaInicio"         : "2017-08-01",
	  "fechaFin"            : "2017-08-08",
	  "horaInicioOperacion" : "06:00:00",
	  "horaFinOperacion"    : "20:00:00"
  }
}

//respuesta:

{
  "success" : true,
  "data" :  [
	  {
		  "idVehiculo"     : "128091820918209128",
		  "placa"          : "ABC123",
		  "fecha"          : "2017-09-30",
		  "kmsAntes"       : 89,
		  "kmsDespues"     : 13		  
	  }
  ]
	
	
  
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



##===================Inicio Mejoras Ecopetrol========================================
# Creado en 11 de mayo del 2017

*Documentos:*
```
//Conductores
{
    "tipoDato"        : "conductores",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "cedula"          : "2221001",
    "nombres"         : "Luisa",
    "apellidos"       : "Paz Romero",
    "fechaNacimiento" : "1991-03-12",
    "celular"         : "56622144444",
    "activo"          : true,
    "eliminado"       : false
}

//tipoZona indica los tipos de zona que puede ser una zona alarma
{
    "tipoDato"        : "tipoZona",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "nombre"          : "Parqueadero",
	"descripcion"     : "Sitio de parqueo de vehiculos",
    "activo"          : true,
    "eliminado"       : false
}

```
#=====================================================================================================
#Documentos para rutas
```
{
    "tipoDato"        : "puntosRutaDefinida",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "puntosRuta"      : [[latitud, longitud], [latitud, longitud] ,[latitud, longitud]],
    "activo"          : true,
    "eliminado"       : false
}
```

```
{
    "tipoDato"        : "rutas",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "nombreRuta"      : "Ruta cavasa",
    "origen"          : [latitud, longitud],
    "destino"         : [latitud, longitud],
    "direccionOrigen" : "Via Guachene, Puerto Tejada, Caloto, Cauca, Colombia",
    "direccionDestino": "Via Guachene, Puerto Tejada, Caloto, Cauca, Colombia",
    "idPuntosRutaDefinida"  : "665656544adkmjadjjkad0", #se referencia al documento puntosRutaDefinida
    "puntosParadas"   : [[latitud, longitud, "Carga"], [latitud, longitud, "Descarga"] ,[latitud, longitud, "Carga"]],
    "activo"          : true,
    "eliminado"       : false
}
```


```
{
    "tipoDato"        : "puntosControl",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "idRuta"          : "444446544545554",
    "idPuntosRuta"    : "idisidfsioi8778787878",
    "puntosControl"   : [[latitud, longitud, direccion]],  
    "activo"          : true,
    "eliminado"       : false
}
```

```
{
    "tipoDato"        : "puntosVelocidad",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "idRuta"          : "444446544545554",
    "idPuntosRuta"    : "idisidfsioi8778787878",
    "puntosVelocidad"   : [[latitud, longitud, direccion]],  
    "activo"          : true,
    "eliminado"       : false
}
```
```
{
    "tipoDato"        : "puntosInteres",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "idRuta"          : "444446544545554",
    "idPuntosRuta"    : "idisidfsioi8778787878",
    "puntosInteres"   : [[latitud, longitud, direccion]],  
    "activo"          : true,
    "eliminado"       : false
}
```

## Asignación de rutas:

Puntos de control virtual es una copia en el mismo momento en que
ocurre, se ignoran los cambios en las rutas pero se mostrará en la
interfaz que existen fechas.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
{
    "tipoDato"        : "asignacionRuta",
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
	"activo"          : true,
    "eliminado"       : false,

	"estado"          : "programada",
    "idRuta"          : "44444654454555412",
    "idVehiculo"      : "18291829192812892",
	"idConductor"     : "18291820ihaj81298",
	"fechaInicioReal" : "2016-03-12T08:07:19Z",
	"fechaFinReal"    : "2016-03-12T08:07:19Z",
	"fechaInicioProgramada"  : "2016-03-12T08:07:19Z",
	"fechaFinProgramada"     : "2016-03-12T08:07:19Z",
	
	"ruta" : {
		"origen": {
			"latitud"   : 3.5266987,
			"longitud"  : -76.32760560000003,
			"direccion" : "Cra 123 # 23-45",
			"velocidad" : 34.1212331212
		},
		"destino": {
			"latitud"   : 3.5266987,
			"longitud"  : -76.32760560000003,
			"direccion" : "Cra 123 # 23-45",
			"velocidad" : 34.1212331212
		}
	},
	
	"puntosDeControlVirtual" : [
		{
			"latitud"   : "16.909009090",
			"longitud"  : "-70.12819281",
			"direccion" : "Av 123 # 678", 
			"fechaHoraCruceReal"       : "2016-03-12T08:07:19Z",
			"fechaHoraCruceProgramada" : "2016-03-12T08:07:19Z"
		}		
	],
	"puntosParadas": [
		{
			"latitud"   : "16.909009090",
			"longitud"  : "-70.12819281",
			"direccion" : "Av 123 # 678",
			"tipo"      : "Carga",
			"fechaHoraInicioParada" : "2016-03-12T08:07:19Z",
			"fechaHoraFinParada"    : "2016-03-12T08:07:Web"
			
		}
	],
	"limitesDeVelocidad":[
		{
			"latitud"          : 12.12012,
			"longitud"         : -77.219201,
			"direccion"        : "Cra 123 # 456 Cali",
			"limiteCargado"    : 60,
			"limiteDescargado" : 80,
			"velocidadMaximaRegistrada" : 69.28172,
			"estado"           : "ok",
			"infracciones"     : [{
				"latitud"          : 12.12012,
				"longitud"         : -77.219201,
				"direccion"        : "Cra 123 # 456 Cali",
				"tipo"             : "Carga",
				"velocidad"        : 65
			}]
		}
	]
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#=====================================================================================================

#documento para guardar el nombre de las geoposiciones
```
{
    "tipoDato"          : "posicionesGeocoder",
    "latitud"           : "3.2037033333333333",
    "longitud"          : "-76.42142",
    "nombreGeoposicion" : "Via Guachene, Puerto Tejada, Caloto, Cauca, Colombia",
    "activo"            : true

}
```

#Al documento vehiculos se le agrego el campo conductor: "conductor"  : "98986565465"

#Al documento vehiculos se le agrego el campo booleano cargado: "cargado"  : true 

#Al documento zonaAlarma se le agrego el campo foráneo: "idTipoZona"  : "12389cf82919889a819289b898192a89" 



### vista conductores
```
{
   "_id": "_design/conductores",
   "views": {
       "listarConductores": {
           "map": "function(doc){if(doc.tipoDato == \"conductores\"){ emit([doc.cedula], null );}}"
       },
       "listarVehiculosPorConductor": {
           "map": "function(doc){if(doc.tipoDato == \"vehiculos\"){ emit([doc.conductor], null );}}"
       }
   }
}
```

### Vista tipozona

~~~~~~~~~~~~~~~~~~{.javascript}

{
   "_id": "_design/tiposZonas",
   "_rev": "1-0ce4c4f1cb729f34d452b4cfaae5f232",
   "language": "javascript",
   "views": {
       "listarTiposZonas": {
           "map": "function(doc){\n\tif( doc.tipoDato == \"tipoZona\" && !doc.eliminado){\n\t\temit( [doc.nombre],null); \n\t}\n}"
       }
   }
}


//listarTiposZonas
function(doc){
	if( doc.tipoDato == "tipoZona" && !doc.eliminado){
		emit( [doc.nombre],null); 
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### vista rutas
```
{
   "_id": "_design/rutas",
   "views": {
       "listarRutas": {
           "map": "function(doc){if(doc.tipoDato == \"rutas\" && doc.activo){ emit([doc._id], null );}}"
       }
   }
}

## La vista geopoiciones calculadas se actualizo de la siguiente forma: 

function(doc){
  if( (doc.tipoDato == "posicionVehiculos" || doc.tipoDato == "paradaVehiculo" || doc.tipoDato == "posicionesGeocoder") && ( ('nombreGeoposicion' in doc) && doc.nombreGeoposicion != "" ) && doc.activo){
    var lat1 = doc.latitud.split(".")[0];
    var lat2 = doc.latitud.split(".")[1];
    var lng1 = doc.longitud.split(".")[0];
    var lng2 = doc.longitud.split(".")[1];
    emit([lat1+"."+lat2.substring(0,4), lng1+"."+lng2.substring(0,4) ], doc.nombreGeoposicion);
    
  }
}

## Vista para asignaciones Rutas

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//_design/asignacionRuta/_view/asignacionRuta
function(doc){
	if(doc.tipoDato == "asignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.fechaInicio, doc._id],null);
	}
}
//_design/asignacionRuta/_view/asignacionPorEstadoVehiculoFechaInicio
function(doc){
	if(doc.tipoDato == "asignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.estado, doc.idVehiculo, doc.fechaInicioProgramada],null);
	}
}

//_design/asignacionRuta/_view/asignacionPorEstadoVehiculoFechaFin
function(doc){
	if(doc.tipoDato == "asignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.estado, doc.idVehiculo, doc.fechaFinProgramada],null);
	}
}


//_design/asignacionRuta/_view/asignacionPorEstadoFechaInicio
function(doc){
	if(doc.tipoDato == "asignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.estado, doc.fechaInicioProgramada],null);
	}
}

//_design/asignacionRuta/_view/asignacionPorEstadoFechaFin
function(doc){
	if(doc.tipoDato == "asignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.estado, doc.fechaFinProgramada],null);
	}
}


//
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


##===================Fin Mejoras Ecopetrol===========================================


##Inicio de sección de pedido -------------------------------------------------------


# Seguimientos

## Documentos

### seguimiento Asignacion de ruta

Define los seguimientos de rutas que se han definido.

- *idAsignacionRuta:* ruta a la cual está asignada.

- *fechaHoraInicioSeguimiento:* inicio del seguimiento de la ruta.

- *fechaHoraFinSeguimiento:* fin de qfinalizado el seguimiento

- *fechaHoraUltimaRevision:* ultima fecha del listado de puntos que se
  analizó para el seguimiento, la idea es que desde este punto a la
  fecha actual se relice el análisis

- *estado:* si está en ruta o no, `enruta` siguen bien la ruta,
  `noiniciada` la ruta debió empezar pero no ha iniciado,
  `fueraderuta` no está siguiendo la ruta (pero ya la empezó en algún
  momento) `finalizadaCompleta` la ruta finalizó correctamente, `finalizadaIncompleto`


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
{
    "tipoDato"        : "seguimientoAsignacionRuta",
	
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "activo"          : true,
    "eliminado"       : false,
	
	"idAsignacionRuta"           : "182018291820192",
	"fechaHoraInicioSeguimiento" : "2016-03-13T05:07:19Z",
	"fechaHoraFinSeguimiento"    : "2016-03-13T05:07:19Z",
	"fechaHoraUltimaRevision"    : "2016-03-13T05:07:19Z",

    "estado" : "enruta"
	
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



## Vistas seguimientos rutas

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//_design/seguimientoAsignacionRuta/_view/seguimientoAsignacionRutaPorEstado
function(doc){
	if(doc.tipoDato == "seguimientoAsignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.estado],null);
	}
}

//_design/seguimientoAsignacionRuta/_view/seguimientoAsignacionRutaPorAsignacionRuta
function(doc){
	if(doc.tipoDato == "seguimientoAsignacionRuta" && doc.activo && !doc.eliminado){
		emit([doc.idAsignacionRuta],null);
	}
}


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##===================Inicio Seguridad vial===========================================

NOTA 1: para limpiar todos los registros de:

1. Encendido y apagado ejecutar el script limpiarEncendidoApagado.py
2. Pausa activa ejecutar el script limpiarPausaActiva.py
3  Conduccion continua ejecutar el script limpiarConduccionContinua.py

NOTA 2: Para la seguridad vial ejecutar los script:

1. evaluarEncendidoApagado.py
2. evaluarPausaActiva.py
3. evaluarConduccionContinua.py


*Documentos:*
//Para la conduccion agresiva
```
//Aceleracion
{
    "tipoDato"        : "aceleracion",
    "creadoEn"        : "2016-03-12T08:07:19Z", ##creado por el sistema
    "horaRegistrada"  : "2017-08-15T08:07:19Z",
    "ubicacion"       : "Tocaima-Viota, Cundinamarca",
    "idConductor"     : "b672a041cd1582c3b51d6c7c250019c5",
    "idVehiculo"      : "9114de62e4a98b11669dd37ff5a40c71",  
    "activo"          : true
}

//Frenadas abruptas
{
    "tipoDato"          : "frenadas",
    "creadoEn"          : "2017-08-15T08:07:19Z",
    "horaRegistrada"    : "2017-08-15T08:07:19Z",
    "ubicacion"         : "Tocaima-Viota, Cundinamarca",
    "idConductor"       : "b672a041cd1582c3b51d6c7c250019c5",
    "idVehiculo"        : "9114de62e4a98b11669dd37ff5a40c71",
    "intensidadFrenada" : "48",  
    "activo"            : true
}

//Movimientos abruptos
{
    "tipoDato"              : "movimientoAbrupto",
    "creadoEn"              : "2017-08-12T08:07:19Z",
    "horaRegistrada"        : "2017-08-15T08:07:19Z",
    "ubicacion"             : "Tocaima-Viota, Cundinamarca",
    "idConductor"           : "b672a041cd1582c3b51d6c7c250019c5",
    "idVehiculo"            : "9114de62e4a98b11669dd37ff5a40c71",
    "intensidadMovimiento"  : "56",  
    "activo"                : true
}

//Excesos de velocidad
{
    "tipoDato"        : "excesoVelocidad",
    "creadoEn"        : "2017-08-12T08:07:19Z",
    "horaRegistrada"  : "2017-08-15T08:07:19Z",
    "ubicacion"       : "Tocaima-Viota, Cundinamarca",
    "idConductor"     : "b672a041cd1582c3b51d6c7c250019c5",
    "idVehiculo"      : "9114de62e4a98b11669dd37ff5a40c71",  
    "activo"          : true
}

//Para los eventos de encendido y apagado
//"Encendido y Apagado"
{
    "tipoDato"        : "encendidoApagado",
    "creadoEn"        : "2017-08-12T08:07:19Z",
    "evento"          : "Encendido", 
    "horaInicio"      : "2017-08-15T08:07:19Z",
    "horaFin"         : "2017-08-15T08:07:19Z",
    "idVehiculo"      : "3cdfc1d5e1eabb7b8578b07043a2428e",  
    "activo"          : true
}

//Encendido y apagado
{
    "tipoDato"        : "encendidoApagado",
    "creadoEn"        : "2017-08-12T08:07:19Z",
    "evento"          : "Apagado",
    "horaInicio"      : "2017-08-15T08:07:19Z",
    "horaFin"         : "2017-08-15T08:07:19Z",
    "idVehiculo"      : "3cdfc1d5e1eabb7b8578b07043a2428e",  
    "activo"          : true
}

//Pausa activa
{
    "tipoDato"        : "pausaActiva",
    "creadoEn"        : "2017-08-12T08:07:19Z",
    "fechaInfraccion" : "2017-08-18T08:07:19Z",
    "fechaFin"        : "2017-08-18T08:07:19Z",
    "conduceDesde"    : "2017-08-17T08:07:19Z",
    "idVehiculo"      : "9114de62e4a98b11669dd37ff5a40c71",
    "idConductor"     : "b672a041cd1582c3b51d6c7c250019c5", 
    "activo"          : true
}

//Conduccion continua
  {
      "tipoDato"        : "conduccionContinua",
      "creadoEn"        : "2017-08-12T08:07:19Z",
      "fechaInfraccion" : "2017-08-18T08:07:19Z",
      "fechaFin"        : "2017-08-18T08:07:19Z",      
      "conduceDesde"    : "2017-08-17T11:07:19Z",
      "idVehiculo"      : "9114de62e4a98b11669dd37ff5a40c71",
      "idConductor"     : "b672a041cd1582c3b51d6c7c250019c5", 
      "activo"          : true
  }


### vista seguridad vial
```
{
   "_id": "_design/seguridadVial",
   "views": {
       "listarAceleracionPorConductor": {
           "map": "function(doc){if(doc.tipoDato == \"aceleracion\"){ emit([doc.idConductor, doc.horaRegistrada], null );}}"
       },
       "listarAceleracionPorVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"aceleracion\"){ emit([doc.idVehiculo,doc.horaRegistrada], null );}}"
       },
       "listarFrenadasPorConductor": {
           "map": "function(doc){if(doc.tipoDato == \"frenadas\"){ emit([doc.idConductor,doc.horaRegistrada], null );}}"
       },
       "listarFrenadasPorVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"frenadas\"){ emit([doc.idVehiculo,doc.horaRegistrada], null );}}"
       },
       "listarMovimientoAbruptoConductor": {
           "map": "function(doc){if(doc.tipoDato == \"movimientoAbrupto\"){ emit([doc.idConductor,doc.horaRegistrada], null );}}"
       },
       "listarMovimientoAbruptoPorVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"movimientoAbrupto\"){ emit([doc.idVehiculo,doc.horaRegistrada], null );}}"
       },
       "listarExcesoVelocidadPorConductor": {
           "map": "function(doc){if(doc.tipoDato == \"excesoVelocidad\"){ emit([doc.idConductor,doc.horaRegistrada], null );}}"
       },
       "listarExcesoVelocidadPorVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"excesoVelocidad\"){ emit([doc.idVehiculo,doc.horaRegistrada], null );}}"
       },
       "listarEncendidoApagadoPorVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"encendidoApagado\"){ emit([doc.idVehiculo,doc.horaInicio], null );}}"
       },
       "listarPausaActiva": {
           "map": "function(doc){if(doc.tipoDato == \"pausaActiva\"){ emit([doc.fechaInfraccion], null );}}"
       },
       "listarConduccionContinua": {
           "map": "function(doc){if(doc.tipoDato == \"conduccionContinua\"){ emit([doc.fechaInfraccion], null );}}"
       },
       "listarFechasRevision": {
           "map": "function(doc){if(doc.tipoDato == \"fechasRevision\"){ emit([doc.tipoRevision, doc.idVehiculo], null );}}"
       },
       "listarSeguimientoPausaActiva": {
           "map": "function(doc){if(doc.tipoDato == \"seguimientoPausaActiva\"){ emit([doc.idVehiculo], null );}}"
       },
       "listarSeguimientoConduccionContinua": {
           "map": "function(doc){if(doc.tipoDato == \"seguimientoConduccionContinua\"){ emit([doc.idVehiculo], null );}}"
       },
       "listarPausaActivaPorVehiculo": {
           "map": "function(doc){if(doc.tipoDato == \"pausaActiva\"){ emit([doc.idVehiculo, doc.fechaInfraccion], null );}}"
       }
   }
}
```

##===================================================================================

##GEOCODER==========================================================================



# Geocoder

Estos documentos tiene base de datos aparte para compartirlas entre todos los tenants.

*Documentos geocoder:*
```
//Geocoder
{
    "tipoDato"      : "geocoder",
    "creadoEn"      : "2016-03-12T08:07:19Z",
	"activo"        : true,
	
	"latitud"       : "-77.2812819212",
	"longitud"      : "44.12128192",
	"direccion"     : "Cra 123 # 456 - 980, Cali Colombia"
}

//Municipios
{
	"tipoDato"      : "puntoreferencia",
	"creadoEn"      : "2016-03-12T08:07:19Z",
	"activo"        : true,
	
	"latitud"        : "-77.2812819212",
	"longitud"       : "44.12128192",
	"tipoReferencia" : "municipio" 
	"nombre"         : "Cali",
	"departamento"   : "Valle del Cauca"
	
}

//Peajes
{
	"tipoDato"      : "puntoreferencia",
	"creadoEn"      : "2016-03-12T08:07:19Z",
	"activo"        : true,
	
	"latitud"        : "-77.2812819212",
	"longitud"       : "44.12128192",
	"tipoReferencia" : "peaje", 
	"nombre"         : "MEDIACANOA",
	"departamento"   : "Valle del Cauca",
	"sector"         : "Yumbo - mediacanoa"
	
}

//Poste
{
	"tipoDato"      : "puntoreferencia",
	"creadoEn"      : "2016-03-12T08:07:19Z",
	"activo"        : true,
	
	"latitud"        : "-77.2812819212",
	"longitud"       : "44.12128192",
	"tipoReferencia" : "poste" 
	"nombre"         : "11",
	"tramo"          : "Troncal",
	"sector"         : "Yumbo - mediacanoa"
	
}

//Ubicacion direccion ip
{
  "tipoDato"       : "ubicacionDireccionIp",
	"creadoEn"      : "2016-03-12T08:07:19Z",
	"activo"        : true,
  "direccionIp"    : "127.125.85.00",
  "latitud"           : "-77.2812819212",
	"longitud"          : "44.12128192",
  "direccionCompleta"  : "calle 14 barrio German",
  "ciudad"            : "Cali"
}
```

*Vistas geocoder*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//_design/geocoder/_view/direcciones
function(doc){
	for(doc.tipoDato == "geocoder" && doc.activo){
		var latitud  = parseFloat(latitud).toFixed(4);
		var longitud = parseFloat(longitud).toFixed(4); 
		emit([latitud, longitud],doc.direccion)
	}
}
//_design/geocoder/_view/puntosreferencialatitud
function(doc){
	if( doc.tipoDato == "puntoreferencia"  && doc.activo){
		emit([doc.latitud, doc.tipoReferencia], null)
	}
}

//_design/geocoder/_view/puntosreferencialongitud
function(doc){
	if( doc.tipoDato == "puntoreferencia"  && doc.activo){
		emit([doc.longitud, doc.tipoReferencia], null)
	}
}

//_design/geocoder/_view/latitudportiporeferencia
function(doc){
	if( doc.tipoDato == "puntoreferencia"  && doc.activo){
		emit([doc.tipoReferencia, doc.latitud], null)
	}
}

//_design/geocoder/_view/UbicacionDireccionIpPorIp
function(doc){
	if( doc.tipoDato == "ubicacionDireccionIp"  && doc.activo){
		emit([doc.direccionIp], null)
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## GEOCODER webservices

### Buscar puntos referecnias

*Nombre:* wsBuscarPuntosReferencias

*URL:* `http://localhost:8080/ws/buscarPuntosReferencias`

En caso de encontrar un punto de referencia no se retorna.

*Descripción:* ws que busca puntos de referencia como peajes, postes y
municipios cercanos, adicionalmente se pretente que también retorne la
dirección pero queda pendiente por implementar

- *buscarDireccion:* si es True se busca en geocoder la dirección, de
  lo contrario no.

- *distancia:* en metros al centro del punto de referencia.

- *direccion:* el externo es "cra tal" el interno indica utiizando los
  4 puntos cardinales a que dirección se encuentra el punto e
  referencia con respecto al vehículo

~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
//Petición
{
    "autenticacion" : {
      "usuario" : "admin",
      "token" : "5776d71ff8f8442ca8326d04987a9bdc",
      "tenant" : "exxonmobil"
    },
    "data" : {
		"latitud"         : 3.753776,
		"longitud"        : -76.410214,
		"buscarDireccion" : false 
    }
}

//Respuesta
{
  "success" : true,
  "data"    : {
	"direccion" : "cra 123 # 456-789",
	"municipio" : {
		"nombre"       : "Cali",
		"departamento" : "Valle del Cauca",
		"distancia"    : 1200,
		"direccion"    : "Suroccidente"
	},
	"peaje" : {
		"nombre"         : "MEDIACANOA",
		"departamento"   : "Valle del Cauca",
		"sector"         : "Yumbo - mediacanoa",
		"distancia"      : 1200,
		"direccion"      : "Suroccidente"
	},
	"poste" : {
		"nombre"         : "11",
		"tramo"          : "Troncal",
		"sector"         : "Yumbo - mediacanoa",
		"distancia"      : 1200,
		"direccion"      : "Suroccidente"
	}
  }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 




-------------------------- ws ------------------------------------------


#Registrar posiciones aceleración  del vehiculo usando el GPS

*Nombre:* wsregistrarAceleracionVehiculoGPS

*URL:* `http://localhost:8080/ws/registrarAceleracionVehiculoGPS`

*Descripción:* ws que registra la aceleracion de forma repentina de un vehiculo y registra los datos en el documento "aceleracion"

```
//Petición
{
    "autenticacion" : {
      "usuario" : "admin",
      "token" : "5776d71ff8f8442ca8326d04987a9bdc",
      "tenant" : "exxonmobil"
    },
    "data" : {
    "latitud"        : "3.4206",
    "longitud"       : "-76.5222",
    "horaRegistrada" :  "2017-08-24T08:07:19Z",       
    "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```
```
//Petición
{
    "autenticacion" : {
      "usuario" : "admin",
      "token" : "5776d71ff8f8442ca8326d04987a9bdc",
      "tenant" : "exxonmobil"
    },
    "data" : {
    "latitud"        : "",
    "longitud"       : "-76.5222",
    "horaRegistrada" :  "2016-08-19T08:07:19Z",       
    "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```


//Frenadas abruptas
{
    "tipoDato"        : "frenadas",
    "creadoEn"        : "2017-08-15T08:07:19Z",
    "horaRegistrada"  : "2017-08-15T08:07:19Z",
    "ubicacion"       : "Tocaima-Viota, Cundinamarca",
    "idConductor"     : "b672a041cd1582c3b51d6c7c250019c5",
    "idVehiculo"      : "9114de62e4a98b11669dd37ff5a40c71",  
    "activo"          : true
}

#Registrar posiciones de las frenadas abruptas del vehiculo usando el GPS

*Nombre:* wsRegistrarFrenadasVehiculoGPS

*URL:* `http://localhost:8080/ws/registrarFrenadasVehiculoGPS`

*Descripción:* ws que registra las frenadas abruptas de un vehiculo y registra los datos en el documento "frenadas"

```
//Petición
{
    "autenticacion" : {
      "usuario" : "admin",
      "token" : "5776d71ff8f8442ca8326d04987a9bdc",
      "tenant" : "exxonmobil"
    },
    "data" : {
    "latitud"           : "3.4206",
    "longitud"          :  "-76.5222",
    "horaRegistrada"    :  "2017-08-24T08:07:19Z", 
    "intensidadFrenada" :  "48",     
    "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```


#Registrar posiciones de los movimientos abruptos del vehiculo usando el GPS

*Nombre:* wsRegistrarMovimientosAbruptosVehiculoGPS

*URL:* `http://localhost:8080/ws/registrarMovimientosAbruptosVehiculoGPS`

*Descripción:* ws que registra los movimientos abruptos de un vehiculo y registra los datos en el documento "movimientoAbrupto"

```
//Petición
{
    "autenticacion" : {
      "usuario" : "admin",
      "token" : "5776d71ff8f8442ca8326d04987a9bdc",
      "tenant" : "exxonmobil"
    },
    "data" : {
    "latitud"           : "3.4206",
    "longitud"          :  "-76.5222",
    "horaRegistrada"    :  "2017-08-24T08:07:19Z", 
    "intensidadMovimiento" :  "56",     
    "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```

------------------------- ws ------------------------------------------
 #Para el algoritmo de registro de encendido y apagado se utilizara el campo del documento es: estaEncendidoMotor

*Documentos:*
//Fechas Revision. Este documento registra las ultimas fechas de revision de encendidoApagado, pausaActiva,conduccionContinua, excesosVelocidad.

Para hacer una nueva revision se actualiza el campo revisado a false y fechaHoraRegistrada a la actual
Registro carro andres 16/08/2017 04:00 pm

  {
      "tipoDato"                : "fechasRevision",
      "tipoRevision"            : "encendidoApagado",
      "fechaHoraRegistrada"     : "2017-08-16T16:45:19",
      "idVehiculo"              : "95ea81741bbfba959550827b15005700",
      "activo"              : true
  }


{
    "tipoDato"      : "posicionVehiculos",
    "creadoEn"      : "2017-08-16T17:00:47.363597",
    "modificadoEn"  : "2017-08-16T17:00:47.363597",
    "modificadoPor" : "Pablo Solarte",
    "horaRegistrada": "2017-08-29T15:55:42.243596",
    "horaRecibida"  : "2017-08-16T15:52:47.363597",
    "latitud"       : "-30.37812817283",
    "longitud"      : "70.6271265342323",
    "velocidad"     : "30.35 km/h",
    "idVehiculo"    : "95ea81741bbfba959550827b15005700",
    "estado"        : "activo",
    "activo"        : true,
    "ultimaPosicion": true,
    "zonaAlarmas" : [],
    "programacionVigilancia" : [],
    "idParada"          : "",
    "idFragmentoParada" : "",
    "estaEncendidoMotor" : true,
  "complementosEstadisticas" : {
    "metrosRecorridos" : 10,
    "idPrimerPuntoExcesoVelocidad" : "12981928192",        
    "segundosAlPuntoAnterior" : 130,
    "idPrimerPuntoCambioEncendido" : "2819281928"   
  }

}  

#En _design/seguridadVial
 "listarFechasRevision": {
     "map": "function(doc){if(doc.tipoDato == \"fechasRevision\"){ emit([doc.tipoRevision, doc.idVehiculo], null );}}"
 }

------------------------- ws ------------------------------------------
 #Para el algoritmo de registro de pausa activa se utilizara el campo del documento es: pausaActiva

{
    "tipoDato"                : "fechasRevision",
    "tipoRevision"            : "pausaActiva",
    "fechaHoraRegistrada"     : "2017-08-16T16:45:19",
    "idVehiculo"              : "95ea81741bbfba959550827b15005700",
    "activo"              : true
}


#Documento seguimientoPausaActiva

{
    "tipoDato"                  : "seguimientoPausaActiva",
    "fechaHoraResetPausa"       : "2017-08-16T16:45:19",
    "fechaHoraUltimoEncendido"  : "2017-08-16T16:45:19",
    "idVehiculo"                : "95ea81741bbfba959550827b15005700",
    "idPausaActiva"             : "",
    "activo"                    : true
}

#Documento seguimientoConduccionContinua

{
    "tipoDato"                  : "seguimientoConduccionContinua",
    "fechaHoraResetPausa"       : "2017-08-16T16:45:19",
    "fechaHoraUltimoEncendido"  : "2017-08-16T16:45:19",
    "idVehiculo"                : "95ea81741bbfba959550827b15005700",
    "idConduccionContinua"      : "",
    "activo"                    : true
}


Los Cron ejecutables son:

evaluarEncendidoApagado
evaluarPausaActiva
evaluarConduccionContinua
##===================Fin Seguridad vial===========================================


##===================PEGASO=======================================================

# Documentación PEGASO

## Documentos PEGASO

### Seguimiento pegaso

- *fechaHoraUltimaRevision:* indica la fecha del ultimo punto enviado a pegaso.
- *metrosRecorridossDia:* la cantidad de metros recorridos desde el inicio del día
- *fechaMetrosRecorridosDia:* indica la fecha a la cual pertenecen los metrosRecorridosDia, en caso de cambiar de fecha se resetea fecha.

- *ultimoNumeroSecuencia:* indica el últiumo número de secuencia utilizado.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
{
    "tipoDato"        : "seguimientoPegaso",
	
    "creadoEn"        : "2016-03-12T08:07:19Z",
    "modificadoEn"    : "2016-03-13T05:07:19Z",
    "modificadoPor"   : "Pablo Solarte",
    "activo"          : true,
    "eliminado"       : false,
	
	"idVehiculo"                 : "182018291820192",
	"fechaHoraUltimaRevision"    : "2016-03-13T05:07:19Z",
    "metrosRecorridosDia"        : 1023,
	"fechaMetrosRecorridosDia"   : "2016-03-13",
	"ultimoNumeroSecuencia"      : 65535
	
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Vistas PEGASO

### Pegaso Views _design/pegaso

- *Nombre:* `_design/pegaso`

~~~~~~~~~~~~~~~~~~~{.javascript}
//_view/seguimientoPegaso
function(doc){
	if(doc.tipoDato == "seguimientoPegaso" && doc.activo){
		emit([doc.idVehiculo],fechaHoraUltimaRevision)
	}
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



##===================Fin PEGASO===========================================

2017-08-29T15:00:19


##=======Inicio GENERADORES DE CÓGIGO PARA GENERADORES DE CARGA====================

*Documento codigosGenerados:*

{
    "tipoDato"        : "codigosGenerados",
    "creadoEn"        : "2017-08-12T08:07:19Z",
    "modificadoEn"    : "2017-08-12T08:07:19Z",
    "modificadoPor"   : "usuario",
    "codigo"          : "RT75255",
    "fechaGeneracion" : "2017-08-12T08:07:19Z",
    "fechaCaducidad"  : "2017-08-12T08:07:19Z",
    "descripcion"     : "codigo para exxonMovil",
    "vehiculos"       : ["15456532323311313","54454564646464646"],
    "anulado"         : True, False
    "tenant"		  : "ExxonMobil"
    "activo"          : true
}


### vista generadores de carga
```
{
   "_id": "_design/generadoresDeCarga",
   "views": {
       "listarCodigosGenerados": {
           "map": "function(doc){if(doc.tipoDato == \"codigosGenerados\" && doc.activo){ emit([doc.fechaGeneracion], null );}}"
       },
       "listarCodigoGeneradoPorCodigoAcceso": {
           "map": "function(doc){if(doc.tipoDato == \"codigosGenerados\"){ emit([doc.codigo], null );}}"
       }
   }
}
```

#Para el registro de datos para el generador de carga. se realizará en la base de datos llamada 'fleetbigeneradorescarga'. por lo tanto el tenant será 'generadorescarga' 


*Documento generadoresDeCarga:*

{
    "tipoDato"        : "generadoresDeCarga",
    "creadoEn"        : "2017-08-12T08:07:19Z",
    "modificadoEn"    : "2017-08-12T08:07:19Z",
    "nombreGenerador" : "ecopetrol",
    "email"			  : "ecopetrol@ecopetrol.com",
    "contrasena"	  : "396d6174f78903caed6218a115202a72",
    "activo"          : true
}

*Documento autenticacion:*

{
	"tipoDato"              : "autenticacion",
	"creadoEn"              : "2017-08-12T08:07:19Z",
	"loginUsuario"          : "ecopetrol@ecopetrol.com",
  "token"                 : "5776d71ff8f8442ca8326d04987a9bdc",
  "activo"                : True,
  "tipoSesion"            : "fleetBiWeb", "FleetBiAndroid", "FleetBiIos",
  "idUsuario"             : "5776d71ff8f8442ca8326d04987a946546",
  "identificadorSesion"   : "107.02.45.2.31", "12211221132", Nota: direccion ip o identificador telefono 
  "dispositivo"           : "Linux", "androrid", "androidNativo", "iosNativo",
  "latitud"               : 4.5981,
  "longitud"              : -74.0758,
  "direccionCompleta"     : "Cra. 7 #11-10, Bogotá, Colombia",
  "ciudad"                : "Bogota",
  "ultimaSesion"          : True,
  validadoMultipleCiudad  : False
}

#el tipoSesion(web, android, ios) se pasa como parametro desde el formulario de acceso

*Documentacion alertasSesion:*

{
  "tipoDato"                    : "alertasSesion",
	"creadoEn"                    : "2017-08-12T08:07:19Z",
  "usuario"                     : "Raul"
  "idUsuario"                   : "154556444444444444444466578",
  "tipoUsuario"                 : "Cliente"
  "tipoSesion"                  : "fleetBiWeb",
  "identificadorAnteriorSesion" : "127.0.0.78",
  "dispositivoAnteriorSesion"   : "Linux",
  "fechaHoraAnteriorSesion"     : "2017-08-12T08:07:19Z",
  "direccionAnteriorSesion"     : "Cra. 7 #11-10, Bogotá, Colombia",
  "ciudadAnteriorSesion"        : "Bogota",
  "latitudAnteriorSesion"       :  4.5981,
  "longitudAnteriorSesion"      : -74.0758,
  "identificadorActualSesion"   : "127.0.0.78",
  "dispositivoActualSesion"     : "Windows",
  "fechaHoraActualSesion"       : "2017-08-12T08:07:19Z",
  "direccionActualSesion"       : "Cra. 7 #11-10, Bogotá, Colombia",
  "latitudActualSesion"         :  4.5981,
  "longitudActualSesion"        : -74.0758,
  "concepto"                    : "Sesion simultanea",
  "observaciones"               : "Multiple sesión en la misma dirección Ip",
  "activo"                      : True  
}


*Documento recuperacionContrasena 'generadorescarga' 


### recuperacionContrasena:
*Documentos:*
```
{
    "tipoDato"      : "recuperacionContrasena",
    "token" 		: "",
    "estaUsado"		: true,
    "usuario"		: "terpel@terpel.com",
    "creadoEn"		: "2016-03-12T08:07:19Z",
    "activo"        : true
}
```

*Documento codigosAcceso 'generadorescarga' 


### codigosAcceso:
*Documentos:*
```
{
    "tipoDato"      				: "codigosAcceso",
    "idDocCodAcceso" 				: "4d6c34900fab29c5e7101d7186001c97",
    "tenantDelCodGenerado"			: "exxonmobil",
    "idGeneradorCarga"				: "3d6c34900fab29c5e7101d7186001c94",
    "codigo"						: "AHOOPP"
    "creadoEn"						: "2016-03-12T08:07:19Z",
    "activo"        				: true
}
```


### vista generadores de carga en el tenant 'generadorescarga'
```
{
   "_id": "_design/generadoresDeCarga",
   "views": {
       "listarGeneradoresCarga": {
           "map": "function(doc){if(doc.tipoDato == \"generadoresDeCarga\" && doc.activo){ emit([doc.email], null );}}"
       },
       "generadoresCargaPorContrasena": {
           "map": "function(doc){if(doc.tipoDato == \"generadoresDeCarga\" && doc.activo){ emit([doc.email, doc.contrasena], null);}}"
       },
       "listarVehiculosPorId": {
           "map": "function(doc){if(doc.tipoDato == \"vehiculos\" && doc.activo){ emit([doc._id], null);}}"
       }
   }
}
```
## Autenticacioes  en el tenant 'generadorescarga'

```
{
   "_id": "_design/autenticaciones",
   "views": {
       "autenticacion": {
           "map": "function(doc){if(doc.tipoDato == \"autenticacion\"){ emit([doc.loginUsuario, doc.token], null );}}"
       }
   }
}
```

### vista recuperacionContrasena  para los generadoresCarga
```
{
   "_id": "_design/recuperacionContrasena",
   "views": {
       "recuperacionPorToken": {
           "map": "function(doc){if(doc.tipoDato == \"recuperacionContrasena\" && doc.activo){ emit([doc.token], null );}}"
       },
        "recuperacionPorTokenYuso": {
           "map": "function(doc){if(doc.tipoDato == \"recuperacionContrasena\" && doc.activo){ emit([doc.token, doc.estaUsado], null );}}"
       }        
   }
}
```

### vista codigosAcceso de carga en el tenant 'generadorescarga'
```
{
   "_id": "_design/codigosAcceso",
   "views": {
       "listarCodigosAcceso": {
           "map": "function(doc){if(doc.tipoDato == \"codigosAcceso\" && doc.activo){ emit([doc.idGeneradorCarga], null );}}"
       },
       "listarCodigosAccesoPorCodigo": {
           "map": "function(doc){if(doc.tipoDato == \"codigosAcceso\" && doc.activo){ emit([doc.codigo, doc.idGeneradorCarga], null );}}"
       }
   }
}
```
##========Fin GENERADORES DE CÓGIGO PARA GENERADORES DE CARGA======================


#pruebas encio de puntos za y boton de panico diciembre 2017

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

*Nombre:* wsregistrarBotonPanicoGPS 

*URL:* `http://54.243.219.114:56899/ws/botonPanicoGPS`
*URL:* `http://localhost:8080/ws/botonPanicoGPS`

*Descripción:* ws que registra un botón de pánico, latitud y longitud
puede ser "0", igual se recibe y se usa el punto mas reciente que
existe en fleet.

```
//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
     "token" : "5776d71ff8f8442ca8326d04987a9bdc",
     "tenant" : "exxonmobil"
    },
    "data" : {
    "latitud"        : 6.2527,
    "longitud"       : -75.5859,
    "velocidad"      : 30,
    "horaRegistrada" :  "2017-12-11T10:15:20Z",       
    "identificadorGPS"  : "11235556"
    }
}
```


# Documentos CadenaFrio 


### puntoCadenaFrio:
*Documentos:*
```
{
    "tipoDato"       : "puntoCadenaFrio",
    "idVehiculo"     : "2918290182012",
    "horaRegistrada" : "2016-03-12T08:07:19Z",
    "horaRecibida"   : "2016-03-12T08:07:19Z",
    "temperatura"    : 30,
    "activo"         : true
}
```

~~~~~~~~~~{javascript}
{
    "tipoDato"          : "cadenaFrioAlarma",
	"fechahoraInicio"   : "2017-12-18T12:03:28",
	"fechahoraFin"      : "2017-12-18T12:03:45",
    "estado"            : "finalizada",
    "tempMaxima"        : 38,
    "tempMinima"        : 18,
    "tempLimSuperior"   : 30,
    "tempLimInferior"   : 20,
    "tipoAlarma"        : "inferiorSuperado",
    "idVehiculo"        : "a6a9368d6c64bb1cdbab24cd05bec5ed",
    "activo"         : true
}
~~~~~~~~~~~~~~~~~~~~~~~




### Design 'cadenaFrio'

~~~~~~~~~~{javascript}

//puntosCadenaFrio
function(doc){
  if(doc.tipoDato == "puntoCadenaFrio" && doc.activo){
      emit([doc.idVehiculo, doc.horaRegistrada], doc.temperatura);
  }
}
//reduce: _stats

//alarmasCadenaFrio
function(doc){
  if(doc.tipoDato == "cadenaFrioAlarma" && doc.activo){
      emit([doc.idVehiculo, doc.fechahoraInicio], null);
  }
}
//reduce: 


~~~~~~~~~~~~~~~~~~~~~~~



##================== Cadena de frio ============================

# listadoAlarmasCadenaFrio
*Nombre:* wsListadoAlarmasCadenaFrio
*URL:* `http://localhost:8080/ws/listadoAlarmasCadenaFrio`
*Descripcion:* Trae el listado de alarmas en un rango de fechas


- fechahoraInicio: inicio de la alarma
- fechahoraFin: fin de la alarma, "" cuando está e curso
- estado: "encurso" cuando no se ha acabado, "finalizada" cuando se
  completó el evento
- tempMaxima: temperatura ma´xima alcanzada en el rango de fechas
- tempMinima: temperatura mínima alcancazada en el rango de fechas
- tempLimSuperior: límite superior definido
- tempLimInferior: límite inferior definido,
- tipoAlarma : "inferiorSuperado" cuando se supera por abajo (muy
  frio), "superiorSuperado" cuadno se supera por arriba (muy
  caliente),

```
//Petición
{
  "autenticacion":{
      "usuario":"transcolombia",
      "token":"3b318d2e4b864c5eb0745dc6ad37eedc",
      "tenant":"transcolombia"
  },

  "data" : {
      "idVehiculo"  : "a6a9368d6c64bb1cdbab24cd05bec5ed",
      "fechaInicio" : "2017-12-18T12:02:51-05:00",
      "fechaFin"    : "2017-12-19T12:02:51-05:00"
  }
}

//REspuesta:
{
  "success" : true,
  "data"    : [
    {
        "idAlarmaCadenaFrio" : "1829018281290182012",
        "latitud"           : 4.696926666666666,
		"fechahoraInicio"   : "2017-12-18T12:03:28",
		"fechahoraFin"      : "2017-12-18T12:03:45",
		"longitud"          : -74.17124833333334,
        "estado"            : "finalizada",
        "tempMaxima"      : 38,
        "tempMinima"      : 18,
        "tempLimSuperior" : 30,
        "tempLimInferior" : 20,
        "tipoAlarma"      : "inferiorSuperado",
    }
  ]

}
```

# listadoPuntosCadenaFrio
*Nombre:* wsListadoPuntosCadenaFrio
*URL:* `http://localhost:8080/ws/listadoPuntosCadenaFrio`
*Descripcion:* Trae el listado de puntos de la cadena de frio registradas

- fechahoraInicio: inicio de la alarma
- fechahoraFin: fin de la alarma, "" cuando está e curso
- estado: "encurso" cuando no se ha acabado, "finalizada" cuando se
  completó el evento
- tempMaxima: temperatura ma´xima alcanzada en el rango de fechas
- tempMinima: temperatura mínima alcancazada en el rango de fechas
- tempLimSuperior: límite superior definido
- tempLimInferior: límite inferior definido,
- tipoAlarma : "inferiorSuperado" cuando se supera por abajo (muy
  frio), "superiorSuperado" cuadno se supera por arriba (muy
  caliente),

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil" 
  },

  "data" : {
      "idVehiculo"  : "11235556",
      "fechaInicio" : "2017-12-18T12:02:51-05:00",
      "fechaFin"    : "2017-12-19T12:02:51-05:00"
  }
}

//REspuesta:
{
  "success" : true,
  "data"    : {
    "tempMaxima" : 38,
    "tempMinima" : 17,
    "temperaturas" : [
        {
            "fechahora"       : "2017-12-18T12:03:28",
            "temperatura"     : 30,
        }
      ]
  }

}
```

# actualizarAlarmaCadenaFrio
*Nombre:* wsActualizarAlarmaCadenaFrio
*URL:* `http://localhost:8080/ws/actualizarAlarmaCadenaFrio`
*Descripcion:* Actualiza la alarma de cadena de frio indicando si es esta activada o no.

- estaAlarmaCadenaFrioActivada: true or false para indica si está activa la alarma.

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil" 
  },

  "data" : {
      "idVehiculo"  : "11235556",
      "estaAlarmaCadenaFrioActivada" : true,
      "tempLimSuperior"              : 30,
      "tempLimInferior"              : 20,
  }
}

//Respuesta:
{
  "success" : true,
  "data"    : {
    
  }

}
```

# listadoVehiculosCadenaFrio
*Nombre:* wsListadoVehiculosCadenaFrio
*URL:* `http://localhost:8080/ws/listadoVehiculosCadenaFrio`
*Descripcion:* Trae el listado de alarmas en un rango de fechas


- fechahoraInicio: inicio de la alarma
- fechahoraFin: fin de la alarma, "" cuando está e curso
- estado: "encurso" cuando no se ha acabado, "finalizada" cuando se
  completó el evento
- tempMaxima: temperatura ma´xima alcanzada en el rango de fechas
- tempMinima: temperatura mínima alcancazada en el rango de fechas
- tempLimSuperior: límite superior definido
- tempLimInferior: límite inferior definido,
- tipoAlarma : "inferiorSuperado" cuando se supera por abajo (muy
  frio), "superiorSuperado" cuadno se supera por arriba (muy
  caliente).

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil" 
  },

  "data" : {
      "idVehiculo"  : "11235556",
      "fechaInicio" : "2017-12-18T12:02:51-05:00",
      "fechaFin"    : "2017-12-19T12:02:51-05:00"
  }
}

//REspuesta:
{
  "success" : true,
  "data"    : [
    {
        "idVehiculo"                   : "129018201829102",
        "placaVehiculo"                : "TTY123"
        "latitud"                      : 4.696926666666666,
        "longitud"                     : -74.17124833333334,
		"fechaHora"                    : "2017-12-18T12:03:28"
        "estaAlarmaCadenaFrioActivada" : true,
        "temperatura"                  : 30,
        "tempLimSuperior" : 30,
        "tempLimInferior" : 20,
        
    }
  ]

}
```

# reporteTemperaturaVehiculos
*Nombre:* wsReporteTemperaturaVehiculos
*URL:* `http://localhost:8080/ws/reporteTemperaturaVehiculos`
*Descripcion:* Muestra el reporte de temperatura de vehiculos.


- fechahoraInicio: inicio de la alarma
- fechahoraFin: fin de la alarma, "" cuando está e curso
- estado: "encurso" cuando no se ha acabado, "finalizada" cuando se
  completó el evento
- tempMaxima: temperatura ma´xima alcanzada en el rango de fechas
- tempMinima: temperatura mínima alcancazada en el rango de fechas
- tempLimSuperior: límite superior definido
- tempLimInferior: límite inferior definido,
- tipoAlarma : "inferiorSuperado" cuando se supera por abajo (muy
  frio), "superiorSuperado" cuadno se supera por arriba (muy
  caliente).

```
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token"   : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant"  : "exxonmobil" 
  },

  "data" : {
      "idVehiculo"  : "11235556",
      "fechaInicio" : "2017-12-18T12:02:51-05:00",
      "fechaFin"    : "2017-12-19T12:02:51-05:00"
  }
}

//REspuesta:
{
  "success" : true,
  "data"    : [
    {
        "idVehiculo"                   : "129018201829102",
        "placaVehiculo"                : "TTY123"
        "latitud"                      : 4.696926666666666,
        "longitud"                     : -74.17124833333334,
		"fechaHora"                    : "2017-12-18T12:03:28"
        "estaAlarmaCadenaFrioActivada" : true,
        "temperatura"                  : 30,
        "tempLimSuperior" : 30,
        "tempLimInferior" : 20,
        
    }
  ]

}
```

##==============================================================
Permisos platamorma por super admin

// Array para el select picker super administrador opciones a visualizar cliente en la plataforma por vehiculo
var opcionesAdicionalesPlataforma = [
	{ idOpcionPlataforma: "1", descripcionOpcion: "Imagen manual" },
	{ idOpcionPlataforma: "2", descripcionOpcion: "Audio manual" },
	{ idOpcionPlataforma: "3", descripcionOpcion: "Rutas" },
	{ idOpcionPlataforma: "4", descripcionOpcion: "Seguridad Vial" },
	{ idOpcionPlataforma: "5", descripcionOpcion: "Reportes estadísticos" },
	{ idOpcionPlataforma: "6", descripcionOpcion: "Reporte paradas vehículos - zonas" },
	{ idOpcionPlataforma: "7", descripcionOpcion: "Reporte kilometraje por hora" },
	{ idOpcionPlataforma: "8", descripcionOpcion: "Reporte calificación conductores" },
	{ idOpcionPlataforma: "9", descripcionOpcion: "Reporte conducción fuera horario permitido" },
	{ idOpcionPlataforma: "10", descripcionOpcion: "Generadores de carga" },
	{ idOpcionPlataforma: "11", descripcionOpcion: "Imagen botón de panico" },
	{ idOpcionPlataforma: "12", descripcionOpcion: "Audio botón de panico" },
	{ idOpcionPlataforma: "13", descripcionOpcion: "Imagen zona alarma" },
	{ idOpcionPlataforma: "14", descripcionOpcion: "Audio zona alarma" },
	{ idOpcionPlataforma: "15", descripcionOpcion: "Imagen programacion vigilancia" },
	{ idOpcionPlataforma: "16", descripcionOpcion: "Audio programacion vigilancia" },
	{ idOpcionPlataforma: "17", descripcionOpcion: "Llamada automatica botón de panico" },
	{ idOpcionPlataforma: "18", descripcionOpcion: "Mensaje automatico SMS botón de panico" },
	{ idOpcionPlataforma: "19", descripcionOpcion: "Cadena de Frio" }
]