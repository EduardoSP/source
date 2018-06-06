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


#Prueba audio con la programacion vigilancia --------------
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-04T10:08:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


#Pruebas guardar audio zona alarma
Caso 1:

Llamadas zona alarma el mismo punto. pasa la prueba mantiene la llamada. pasa prueba

caso 2.
Sale del punto debe terminar la llamada. Se presentaba un problema al colgar la llamada
cuando sale de la zona alarma. Solucionado 

caso 3
Terminar llamada cuando pasa el tiempo usando el archivo colgarLlamada.py. 
pasa la prueba
observacion: se noto que cuando vuelvo a ingresar a la zona alarma no me crea la llamada
por lo que se crea un nuevo caso de prueba

caso 4.
Grabar llamada reingreso zona alarma:
Solucionado se modifica una la funcion buscarPuntoAnterior.

caso 5.

Guardando foto y audio zona alarma. La zona alarma audio imagen ha sido evaluada

#Pruebas guardar audio programacion vigilancia

caso 6.

Guardando audio programacion vigilancia.


#Prueba audio con la programacion vigilancia --------------
# llamada dia 4  de nov del 2016
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-04T10:08:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}

#Prueba audio con la programacion vigilancia --------------
# llamada dia 5  de nov del 2016
{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-05T10:08:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


caso 6.

Probando audio programacion vigilancia nuevos parametros

{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-04T21:30:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


{
  "autenticacion" : {
    "usuario" : "admin",
    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
    "tenant" : "exxonmobil" 
  },

  "data" : {
  "posiciones"      : [
        {"latitud": "3.5833", "longitud": "-76.25","velocidad": "30.35 km/h", "horaRegistrada":   "2016-11-05T21:30:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}


#------------------------------------------------

#Entra
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
        {"latitud": "3.517", "longitud": "-76.3","velocidad": "30.35 km/h", "horaRegistrada":   "2016-12-26T12:19Z"}
      ],
    "identificadorGPS"  : "20160302"  
  }
}