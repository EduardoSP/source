
//======================Vehiculos==================================//
```
{
    "tipoDato"      : "vehiculos",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Luis Antonio Ramos",
    "placa"         : "XMT814",
    "marca"         : "KEnworth",
    "modelo"        : "2010",
    "activo"        : true,
	 "referencia"    : "",
	 "marcaMotor"      : "cummins",
	 "referenciaMotor" : "IPS400",
	 "consumoGalKm"    : 40.15,
   "conductor"       : "5444288881",
   "cargado"         : true 

}
```
```
{
    "tipoDato"      : "vehiculos",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Luis Antonio Ramos",
    "placa"         : "PQR524",
    "marca"         : "KEnworth",
    "modelo"        : "2013",
    "activo"        : true,
     "referencia"    : "",
     "marcaMotor"      : "cummins",
     "referenciaMotor" : "IPS400",
     "consumoGalKm"    : 40.15,
   "conductor"       : "5444288881",
   "cargado"         : true 

}
```


// Identificadores GPS a vehiculos

SZZ623   -> 20170302
KIQ095   -> 20160302
PQR524   -> 511331
XMT814   -> 2012123456 // estara en  Bogota
SKY250   -> 14191992992 //estara en barranquilla
SPL782   -> 1123555 //estara en cartagena


//================================================================================
//Posicion en Cartagena
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://52.55.0.240/ws/registrarPosicionesGPS`

//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
       "token" : "5776d71ff8f8442ca8326d04987a9bdc",
       "tenant" : "exxonmobil"
    },

  "data" : {
    "posiciones"            : [
            {"latitud": "10.391141", "longitud": "-75.479501","velocidad": "30.35 km/h", "horaRegistrada":   "2017-06-14T14:00:19Z"}
        ],
    "identificadorGPS"  : "1123555"    
  }
}

//=============================================================================


//============================================================================
//Posicion Barranquilla
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://52.55.0.240/ws/registrarPosicionesGPS`

//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
       "token" : "5776d71ff8f8442ca8326d04987a9bdc",
       "tenant" : "exxonmobil"
    },

  "data" : {
    "posiciones"            : [
            {"latitud": "11.009154", "longitud": "-74.805486","velocidad": "30.35 km/h", "horaRegistrada":   "2017-06-14T14:23:19Z"}
        ],
    "identificadorGPS"  : "14191992992"    
  }
}

//=============================================================================

//============================================================================
//Posicion Bogota
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://52.55.0.240/ws/registrarPosicionesGPS`

//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
       "token" : "5776d71ff8f8442ca8326d04987a9bdc",
       "tenant" : "exxonmobil"
    },

  "data" : {
    "posiciones"            : [
            {"latitud": "4.564808", "longitud": "-74.136931","velocidad": "30.35 km/h", "horaRegistrada":   "2017-06-14T14:26:19Z"}
        ],
    "identificadorGPS"  : "511331"    
  }
}


//============================================================================


//============================================================================
//Posicion Bogota
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://52.55.0.240/ws/registrarPosicionesGPS`

//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
       "token" : "5776d71ff8f8442ca8326d04987a9bdc",
       "tenant" : "exxonmobil"
    },

  "data" : {
    "posiciones"            : [
            {"latitud": "4.711178", "longitud": "-74.071951","velocidad": "30.35 km/h", "horaRegistrada":   "2017-06-14T14:32:19Z"}
        ],
    "identificadorGPS"  : "2012123456"    
  }
}

//============================================================================

//============================================================================
//Posicion Cali
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://52.55.0.240/ws/registrarPosicionesGPS`

//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
       "token" : "5776d71ff8f8442ca8326d04987a9bdc",
       "tenant" : "exxonmobil"
    },

  "data" : {
    "posiciones"            : [
            {"latitud": "3.450280", "longitud": "-76.533294","velocidad": "30.35 km/h", "horaRegistrada":   "2017-06-14T14:32:19Z"}
        ],
    "identificadorGPS"  : "20160302"    
  }
}

//============================================================================

//============================================================================
//Posicion Cali
*Nombre:* wsregistrarPosicionesGPS
*URL:* `http://52.55.0.240/ws/registrarPosicionesGPS`

//Petición
{
    "autenticacion" : {
        "usuario" : "admin",
       "token" : "5776d71ff8f8442ca8326d04987a9bdc",
       "tenant" : "exxonmobil"
    },

  "data" : {
    "posiciones"            : [
            {"latitud": "3.761553", "longitud": "-76.664046","velocidad": "30.35 km/h", "horaRegistrada":   "2017-06-14T14:26:19Z"}
        ],
    "identificadorGPS"  : "20170302"    
  }
}

//============================================================================
