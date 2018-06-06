
#----------------------------------------------------------------
#Documentos para registrar el boton de panico

# El campo 'idImagen' pertenece al documento 'inspeccionImagen' se puede ver en el docIntegracionGPS.md
# El campo 'idLlamada' pertenece al documento 'llamadas' donde esta el sidLLamada que provee twilio se puede ver en el doc.md

{
    "tipoDato"        : "alarmasBotonPanico",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "-30.37812817283",
    "longitud"        : "70.6271265342323",
    "idVehiculo"      : "ca759f5632ec30e319570ba94b000743",
    "activo"          : true,
    "timeStamp"       : 1482355653.846376
}
```

```
{
    "tipoDato"      : "capturaImagenesBotonPanico",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "modificadoEn"  : "2016-03-13T05:07:19Z",
    "modificadoPor" : "Pablo Solarte",
    "horaRegistrada"       : "2016-03-12T08:07:19Z",
    "latitud"              : "-30.37812817283",
    "longitud"             : "70.6271265342323",
    "idVehiculo"           : "ca759f5632ec30e319570ba94b000743",
    "idImagen"             : "1911e9b72f67bf6ac72b6ace06002cef",
    "idAlarmaBotonPanico"  : "ca759f5632ec30e319570ba94b000743",
    "activo"          : true

}
```

```
{
    "tipoDato"      : "capturaAudioBotonPanico",
    "creadoEn"      : "2016-03-12T08:07:19Z",
    "horaRegistrada"  : "2016-03-12T08:07:19Z",
    "latitud"         : "3.41306",
    "longitud"        : "-76.3511",
    "duracion"        : "6000",
    "idLlamada"       : "131239183719271382", #id Doc llamadas
    "idVehiculo"      : "95ea81741bbfba959550827b15005700",
    "estado"          : "En curso", "Finalizado"
    "activo"          : true,
    "idAlarmaBotonPanico" : "026b8e0d73b1739a3871cda683004e7e"
}
```

#----------------------------------------------------------------


##vistas

##Vista TenantPorTenant: se encuentra elñ nombre del tenant segun el tenant
```
{
   "_id": "_design/tenantPorTenant",
   "views": {
       "tenantPorTenant": {
           "map": "function(doc){if(doc.tipoDato == \"tenant\" && doc.activo){ emit([doc.urlTenant ], null );}}"
       }
   }
}



##Vista botonPanico
```
{
   "_id": "_design/botonPanico",
   "views": {
       "listarAlarmasBotonPanico": {
           "map": "function(doc){if(doc.tipoDato == \"alarmasBotonPanico\" && doc.activo){ emit([doc._id], null );}}"
       },
        "listarCapturaAudioBotonPanico": {
           "map": "function(doc){if(doc.tipoDato == \"capturaAudioBotonPanico\" && doc.activo){ emit([doc.idVehiculo], null );}}"
       }
   }
}



#Registrar Posiciones boton de pánico del GPS

*Nombre:* wsregistrarBotonPanicoGPS 

*URL:* `http://54.243.219.114:56899/ws/botonPanicoGPS`
*URL:* `http://localhost/ws/botonPanicoGPS`

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
    "latitud"        : "3.4206",
    "longitud"       : "-76.5222",
    "velocidad"      : "30.35 km/h",
    "horaRegistrada" :  "2016-08-19T08:07:19Z",       
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
        "latitud"        : "3.450332",
        "longitud"       : "-76.533648",
        "velocidad"      : "30.35 km/h",
        "horaRegistrada" :  "2016-08-19T20:07:19Z",       
        "identificadorGPS"  : "20160302"
    }
}


//Respuesta
{
  "success" : true
}
```

#====================================================================================
#prueba posicion 3.423328, -76.541170 Calle 6 #38-44 a 38-90 Cali, Valle del Cauca, Colombia

*URL:* `http://localhost/ws/botonPanicoGPS`

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
        "latitud"        : "3.423328",
        "longitud"       : "-76.541170",
        "velocidad"      : "30.35 km/h",
        "horaRegistrada" :  "2016-08-19T08:07:19Z",       
        "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```
#====================================================================================
#prueba boton de panico para notier

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
        "latitud"        : "3.423328",
        "longitud"       : "-76.541170",
        "velocidad"      : "30.35 km/h",
        "horaRegistrada" :  "2016-12-27T12:07:19Z",       
        "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```


#====================================================================================
#prueba boton de panico para notier servidor

*URL:* `http://http://52.55.0.240/ws/botonPanicoGPS`

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
        "latitud"        : "3.423328",
        "longitud"       : "-76.541170",
        "velocidad"      : "30.35 km/h",
        "horaRegistrada" :  "2016-12-27T12:07:19Z",       
        "identificadorGPS"  : "20160302"
    }
}

//Respuesta
{
  "success" : true
}
```