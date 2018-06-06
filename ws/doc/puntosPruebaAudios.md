#Para terminar las llamadas  segun un tiempo establecido se estara ejecutando un archivo 
# para verificar las llamadas en curso y que se ha superado el tiempo
##---puntos  de prueba para verificar el algoritmo de 
##grabacion de Audios para las zonas alarmas y la programacion vigilancia

//================================================================================
Prueba 1
prueba para registrar audios segun zona alarma
#prueba puntos verificando zonaAlarmas
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
  			{"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-09-28T10:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

Con este punto donde hay una zona alarma pasa la prueba

//==============================================================
#Prueba 2
Otro punto prueba dos zonas alarmas
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "3.359153", "longitud": "-76.539222","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-09-28T10:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

Ok pasa prueba
//==============================================================

#prueba 3
# Punto en el que sale de una zona alarma para terminar la llamada

{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
 	"posiciones" 			: [
  			{"latitud": "5.0671", "longitud": "-75.5183","velocidad": "30.35 km/h", "horaRegistrada": 	"2016-09-28T10:07:19Z"}
  		],
  	"identificadorGPS"	: "sajljallk22112"	
  }
}

//=================================================================

#Prueba 4
//===========pruebas para la programacion vigilancia=============

prueba para registrar audios segun zona alarma
#prueba puntos verificando zonaAlarmas
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
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-06T12:40:19Z"}
      ],
    "identificadorGPS"  : "sajljallk22112"  
  }
}


#Prueba 5
#Nota: El GPS envia la Z para que el algoritmo no falle 
#prueba para registrar la programacion vigilancia
prueba para registrar audios segun una programacion vigilancia
#prueba puntos verificando Programacion vigilancia
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
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-13T17:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

#Prueba 6
#Dos zonas alarmas
#Nota: El GPS envia la Z para que el algoritmo no falle 
#prueba para registrar la programacion vigilancia
prueba para registrar audios segun una programacion vigilancia
#prueba puntos verificando Programacion vigilancia
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
        {"latitud": "3.361207", "longitud": "-76.540354","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-13T17:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

# Punto en el que sale de una zona alarma para terminar la llamada
#Punto donde evaluo la programacion vigilancia
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "5.0671", "longitud": "-75.5183","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-20T10:11:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

#puntos prueba 

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
        {"latitud": "3.361207", "longitud": "-76.540354","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-20T17:18Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

#Prueba grabar audio

#Entra
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
        {"latitud": "3.4193", "longitud": "-76.5167","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-20T05:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}





#sale zona alarma
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "5.0671", "longitud": "-75.5183","velocidad": "30.35 km/h", "horaRegistrada":   "2016-09-28T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}



#Prueba audio con la programacion vigilancia
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-23T10:08:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}
