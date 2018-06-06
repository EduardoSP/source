
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
  	"identificadorGPS"	: "20160302"	
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
        {"latitud": "3.364300", "longitud": "-76.539300","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:08:20Z"}
      ],
    "identificadorGPS"  : "20160302"  
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
        {"latitud": "3.364400", "longitud": "-76.539400","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-30T10:10:20Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}


//=================================================================================

# cuarto punto de prueba para saber si esta cerca del anterios
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
        {"latitud": "3.364500", "longitud": "-76.539500","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:20Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}





//=================================================================================

# quinto punto de prueba para saber si esta cerca del anterior
# este punto esta lejos
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
        {"latitud": "10.4137", "longitud": "-75.5336","velocidad": "30.35 km/h", "horaRegistrada":   "2016-09-30T10:07:20Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}


//=================================================================================

# sexto punto de prueba para saber si esta cerca del anterior
# este punto esta lejos
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
        {"latitud": "5.0671", "longitud": "-75.5183","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-30T10:07:20Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}


#=============================================================================
#ejemplos puntos para mapa de calor

Paradas en cali
3.460757, -76.516633

3.466089, -76.513234

3.469481, -76.509835


punto 1
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
        {"latitud": "3.460757", "longitud": "-76.516633","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}


punto 2
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
        {"latitud": "3.466089", "longitud": "-76.513234","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}

punto 3
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
        {"latitud": "3.469481", "longitud": "-76.509835","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}

Puntos en Manizales
5.035369, -75.535374
5.038105, -75.534001
5.040841, -75.532285

punto 1
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
        {"latitud": "5.035369", "longitud": "-75.535374","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}


punto 2
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
        {"latitud": "5.038105", "longitud": "-75.534001","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}

punto 3
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
        {"latitud": "5.040841", "longitud": "-75.532285","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}

//======================================================================================
#casos de prueba 12 de diciembre 2016


punto 1
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
        {"latitud": "5.040841", "longitud": "-75.532285","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T11:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}


punto 2
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
        {"latitud": "5.040841", "longitud": "-75.532285","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T11:08:20Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}

//--------------------------------------------------------------------------
punto 3
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
        {"latitud": "5.040841", "longitud": "-75.532285","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T09:09:00Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}


punto 3.1
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
        {"latitud": "5.040841", "longitud": "-75.532285","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T09:40:00Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

//Respuesta
{
  "success" : true
}

//--------------------------------------------------------------------------



#--------------------------------------------------------------------------

punto 4
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
        {"latitud": "3.364298", "longitud": "-76.539258","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T11:00:00Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}

punto 4.1
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.364298", "longitud": "-76.539258","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T11:20:00Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}



punto 4.2
//Petición
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.364298", "longitud": "-76.539258","velocidad": "30.35 km/h", "horaRegistrada":   "2016-10-16T11:28:00Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}

#--------------------------------------------------------------------------


#prueba con el segundo gps
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
        {"latitud": "3.364298", "longitud": "-76.539258","velocidad": "30.35 km/h", "horaRegistrada":   "2016-08-30T10:07:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


//Respuesta
{
  "success" : true
}



#Guardando ultima posicion
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
        {"latitud": "7.72883", "longitud": "-73.44811666666666","velocidad": " 71.35756", "horaRegistrada":   "2017-03-09T20:03:19Z"}
      ],
    "identificadorGPS"  : "20170302"  
  }
}


//Respuesta
{
  "success" : true
}
