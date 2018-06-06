var polyline3 = null;
var listaPuntosLimiteVelocidad = [];//guarda las posiciones ordenadas de la informacion de los limites de vel que se enviaran ws
var pestanaPrimeraVez = true;
var primerLimiteInicial = {location: {lat: 0, lng: 0, direccion : "", velocidadCarga : "", velocidadDescarga : ""}}; //almacena las velocidades (carga y descarga) del primer punto inicial se envia como primer limite para enviar ws
function pintarRutaLimitesVelocidad(){
      if(pestanaPrimeraVez){
        $("#right-panel3-table3").empty();
        //pintarPanelPuntosLimitesVelocidad(origen.lat(), origen.lng(), direccionOrigen,"/static/images/origenCirculo.png", 0, destino.lat(), destino.lng(), direccionDestino, "/static/images/destinoCirculo.png" , 0);
        //pinta punto origen velocidad
        pintarTemplateLimiteVelocidadInicial(origen.lat(), origen.lng(), direccionOrigen,"/static/images/origenCirculo.png", "Punto Origen", primerLimiteInicial.location.velocidadCarga, primerLimiteInicial.location.velocidadDescarga);
        pintarTemplateLimiteVelocidadFinal(destino.lat(), destino.lng(), direccionDestino,"/static/images/destinoCirculo.png", "Punto Destino");
        //pinta punto final velocidad
        pestanaPrimeraVez = false;
      }else{
        // pinta la ruta de los limites de velocidad
          borraIconosPosIniFinalMapa3(null);
          borrarMarkersMapaLimitesVelocidad();
          ordenarPuntosLineaLimitesVelocidad();
          pintarPanelListaOrdenadaLimitesVelocidad(false);
      }
      //Borra puntos de control que estan fuera de la ruta
      evaluarLimitesVelocidadEnRuta();

      if(polyline3 != null){
        polyline3.setMap(null);
      } 

      polyline3 = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
      });

      var bounds = new google.maps.LatLngBounds();
      var legs = directionsDisplay.getDirections().routes[0].legs;
      for (i=0;i<legs.length;i++) {
          var steps = legs[i].steps;
          for (j=0;j<steps.length;j++) {
            var nextSegment = steps[j].path;
            for (k=0;k<nextSegment.length;k++) {
              polyline3.getPath().push(nextSegment[k]);
              bounds.extend(nextSegment[k]);
            }
          }
      }
      polyline3.setMap(map3);
      makeMarkerRutaLimiteVelocidad( origen, guiImagePuntoControl+"/static/images/origenPin.png", "Origen" );
      
      makeMarkerRutaLimiteVelocidad( destino, guiImagePuntoControl+"/static/images/destinoPin.png", 'Destino' );

}

var markersRutaLimitesVelocidadIniFin = [];
function makeMarkerRutaLimiteVelocidad( position, icon, title ) {
 var marker = new google.maps.Marker({
  position: position,
  map: map3,
  icon: icon,
  title: title
 });
 markersRutaLimitesVelocidadIniFin.push(marker);
}

//funciones que pintan los puntos en el panel3 derecho
function pintarPanel3Origen(latitud, longitud, direccion){
  $("#right-panel3-tableOrigenDestino3").empty();
  //punto origen
  var filaRenderizadaOrigen = Mustache.render(templateOrigenDestino, 
    {
      imagen    : "/static/images/origenCirculo.png",
      titulo    : "Punto Origen",
      direccion : direccionOrigen,
      posicion  : "("+latitud+", "+longitud+")",
      lat       : latitud,
      lng       : longitud
    }
    );
  $("#right-panel3-tableOrigenDestino3").append(filaRenderizadaOrigen);

}

function pintarPanel3Destino(latitud, longitud, direccion){
    var filaRenderizadaDestino = Mustache.render(templateOrigenDestino, 
      {
        imagen   : "/static/images/destinoCirculo.png",
        titulo    : "Punto Destino",
        direccion : direccion,
        posicion  : "("+latitud+", "+longitud+")",
        lat       : latitud,
        lng       : longitud
      }
      );
  $("#right-panel3-tableOrigenDestino3").append(filaRenderizadaDestino);
}


// Sets the map on all markers in the array.
function borraIconosPosIniFinalMapa3(map) {
  for (var i = 0; i < markersRutaLimitesVelocidadIniFin.length; i++) {
    markersRutaLimitesVelocidadIniFin[i].setMap(map);
  }
} 

function evaluarLimitesVelocidadEnRuta(){
  //funcion que evalua los limites de velocidad y borra los que se encuentran fuera de la ruta
  borrarMarkersMapaLimitesVelocidad();
  ordenarPuntosLineaLimitesVelocidad();
  pintarPanelListaOrdenadaLimitesVelocidad(false);
  pintarPanelRangosVelocidad();
}

var infowindow3  = null;
function agregarListanerDerechoMap3(){
  // agrega el evento click derecho al map 3
  google.maps.event.addListener(map3, "rightclick", function(event) {
    var lat = event.latLng.lat();
    var lng = event.latLng.lng();
    //funcion que verifica la parada si es de carga o descarga
    if(infowindow3 != null){
      infowindow3.close();
    }
    var contentString = '<a href='+'javascript:puntoLimiteVelocidad('+lat+','+lng+');'+'>Agregar limite velocidad</a>';
    infowindow3 = new google.maps.InfoWindow({
      content: contentString
    });    
    var a = new google.maps.MVCObject();
    a.setValues({position: event.latLng });
    infowindow3.open(map3,a);
    
  });
}



var listaConfiguracionPuntosLimiteVelocidad= []; //lista que guardara las configuraciones de los puntos de interes
function puntoLimiteVelocidad(lat, lng){  
  var posicion = null;
  posicion = evaluarPosicionParada(lat, lng);
  infowindow3.close();
  //funcion que ordena los puntos en la linea recibe latitud y longitud
  buscarDireccionPunto("puntoLimiteVelocidad", posicion[1], posicion[2]);
}

function AsignarDireccionLimiteVelocidad(latitud, longitud, direcc){
    obtenerValoresCamposTexto(); // obtiene los valores iniciales antes de ordenarlos ----
    listaPuntosLimiteVelocidad.push({location: {lat: latitud, lng: longitud, direccion : direcc, velocidadCarga : "", velocidadDescarga : ""}});
    ordenarPuntosLineaLimitesVelocidad();
    evaluarPosicionesVacias();
    pintarPanelListaOrdenadaLimitesVelocidad(false);
    pintarPanelRangosVelocidad(); // pinta en el panel derecho los limites de velocidad

}

/* julian :D */
// traer_datos_punto_control ({{tenant}}, "{{idRuta}}", "{% url 'wsDetallePuntoVelocidadRuta' %}")
function traer_datos_velocidad (tenant, idRuta, ws) {

  var legs        = directionsDisplay.getDirections().routes[0].legs[0]
  var latOrigen   = legs.start_location.lat();
  var lngOrigen   = legs.start_location.lng();

  var peticion    = { 'autenticacion': {  'usuario' : config.getUsuarioLogin(),
                                          'token'   : config.getToken(),
                                          'tenant'  : tenant,
                                              
                                            },
                        'data'         : { 
                                  'id'            : idRuta,
                                  /*  En el caso de no encontrar el documento en la db, se deba crear uno 
                                      nuevo para poder cargar la pagina actual */
                                  'idRuta'          : idRuta,
                                  'idPuntosRuta'    : idPuntosRutaDefinida,    
                                  'puntosVelocidad' : [[latOrigen, lngOrigen, direccionOrigen, "0" , "0"]]
                                      
                                 }
                      };
  
    var request = $.ajax({
            type: "POST",
            url   : ws,
            data  : {
                        request: JSON.stringify(peticion)
             },
             dataType: "json"
        });
    request.done(function(respuesta){
      obtenerValoresCamposTexto(); // obtiene los valores iniciales antes de ordenarlos ----

      var puntos_velocidad    = respuesta.data.puntosVelocidad;
      id_punto_velocidad_ruta = respuesta.data.id;
      for (i = 1; i < puntos_velocidad.length; i++) { 
        var index                     = i;

        var latitud_temp              = puntos_velocidad[index][0];
        var longitud_temp             = puntos_velocidad[index][1];
        var direccion_tenmp           = puntos_velocidad[index][2];
        var velocidad_cargado_temp    = puntos_velocidad[index][3];
        var velocidad_descargado_temp = puntos_velocidad[index][4];
        listaPuntosLimiteVelocidad.push({location: {  lat               : latitud_temp, 
                                                      lng               : longitud_temp, 
                                                      direccion         : direccion_tenmp, 
                                                      velocidadCarga    : velocidad_cargado_temp, 
                                                      velocidadDescarga : velocidad_descargado_temp
                                                    }});
        
      }
      /* Esto es para setear las velocidades el punto de origen */
      $('#formPuntosVelocidadCarga'     +0+'').val(puntos_velocidad[0][3]);
      $('#formPuntosVelocidadDescarga'  +0+'').val(puntos_velocidad[0][4]);
      // console.log (listaPuntosLimiteVelocidad [0]);
      ordenarPuntosLineaLimitesVelocidad();
      evaluarPosicionesVacias();
      pintarPanelListaOrdenadaLimitesVelocidad(false);
      pintarPanelRangosVelocidad();

      /* Dejamos seleccionada la petana Rutas */
      // $('#tabPestana1').tab('show');

    });

    request.fail(function(jqXHR, textStatus){ });
};

function evaluarPosicionesVacias(){
  //evalua las velocidades vacias. De serlo asi se le asigna las velocidades del punto anterior
  //editando
  var idTextoCargaInicial    = $('#formPuntosVelocidadCarga0').val();
  var idTextoDescargaInicial = $('#formPuntosVelocidadDescarga0').val();
  primerLimiteInicial = {location: {lat: Number(origen.lat()), lng: Number(origen.lng()), direccion : direccionOrigen, velocidadCarga : idTextoCargaInicial, velocidadDescarga : idTextoDescargaInicial}};
  for (var i = 0; i < listaPuntosLimiteVelocidad.length; i++) {
    var index= i +1;
    var idTextoCarga    = listaPuntosLimiteVelocidad[i].location.velocidadCarga;
    var idTextoDescarga = listaPuntosLimiteVelocidad[i].location.velocidadDescarga;
    if(i == 0){
      //si no tiene velocidad de carga o descarga se asigna el de la inicial
      if(idTextoCarga == ""){
        idTextoCarga = idTextoCargaInicial; 
        idTextoDescarga = idTextoDescarga; 
      }
      if(idTextoDescarga==""){
        idTextoCarga   = idTextoCarga; 
        idTextoDescarga = idTextoDescargaInicial; 
      }
    }else{
      if(idTextoCarga == ""){
        idTextoCarga = listaPuntosLimiteVelocidad[i-1].location.velocidadCarga; 
        idTextoDescarga = idTextoDescarga; 
      }
      if(idTextoDescarga==""){
        idTextoCarga   = idTextoCarga; 
        idTextoDescarga = listaPuntosLimiteVelocidad[i-1].location.velocidadDescarga; 
      }
    }
    listaPuntosLimiteVelocidad[i] = {location: {lat: listaPuntosLimiteVelocidad[i].location.lat, lng: listaPuntosLimiteVelocidad[i].location.lng, direccion : listaPuntosLimiteVelocidad[i].location.direccion, velocidadCarga : idTextoCarga, velocidadDescarga : idTextoDescarga}};
  }
}



function obtenerValoresCamposTexto(){
  //mantiene los nombre digitados por el usuario
  var idTextoCargaInicial    = $('#formPuntosVelocidadCarga0').val();
  var idTextoDescargaInicial = $('#formPuntosVelocidadDescarga0').val();
  primerLimiteInicial = {location: {lat: Number(origen.lat()), lng: Number(origen.lng()), direccion : direccionOrigen, velocidadCarga : idTextoCargaInicial, velocidadDescarga : idTextoDescargaInicial}};
  for (var i = 0; i < listaPuntosLimiteVelocidad.length; i++) {
    var index= i +1;
    var idTextoCarga    = $('#formPuntosVelocidadCarga'+index+'').val();
    var idTextoDescarga = $('#formPuntosVelocidadDescarga'+index+'').val();
    listaPuntosLimiteVelocidad[i] = {location: {lat: listaPuntosLimiteVelocidad[i].location.lat, lng: listaPuntosLimiteVelocidad[i].location.lng, direccion : listaPuntosLimiteVelocidad[i].location.direccion, velocidadCarga : idTextoCarga, velocidadDescarga : idTextoDescarga}};
  }
}


function pintarPanelRangosVelocidad(){
  $("#right-panel3-table3").empty();
  pintarTemplateLimiteVelocidadInicial(origen.lat(), origen.lng(), direccionOrigen,"/static/images/origenCirculo.png", "Punto Origen", primerLimiteInicial.location.velocidadCarga, primerLimiteInicial.location.velocidadDescarga);


  for (var i = 0; i < listaPuntosLimiteVelocidad.length; i++) {

      pintarPanelPuntosLimitesVelocidad(listaPuntosLimiteVelocidad[i].location.lat, listaPuntosLimiteVelocidad[i].location.lng, listaPuntosLimiteVelocidad[i].location.direccion, "/static/images/velocidadCirculo.png", i, listaPuntosLimiteVelocidad[i].location.velocidadCarga, listaPuntosLimiteVelocidad[i].location.velocidadDescarga);
  }

  pintarTemplateLimiteVelocidadFinal(destino.lat(), destino.lng(), direccionDestino,"/static/images/destinoCirculo.png", "Punto Destino");
}



function ordenarPuntosLineaLimitesVelocidad(){
  var listasPuntosLimiteVelocidadTemp = [];
  //agrega el punto al final de la lista
  var legs  = directionsDisplay.getDirections().routes[0].legs;
  //ciclo para obtener los puntos de la ruta
    for (i=0;i<legs.length;i++) {
        var steps = legs[i].steps;
        for (j=0;j<steps.length;j++) {
          var nextSegment = steps[j].path;
          for (k=0;k< nextSegment.length-1;k++) {
            //--------punto inicial y final de los segmentos de la linea
            latPrimera = nextSegment[k].lat();
            lngPrimera = nextSegment[k].lng();
            latSegundo = nextSegment[k+1].lat();
            lngSegundo = nextSegment[k+1].lng();

            var listaPuntosLimiteVelocidadEnLinea = [];
            for (var i = 0; i < listaPuntosLimiteVelocidad.length; i++) {

              //punto esta en el segemento
              if(listaPuntosLimiteVelocidad[i] != null){
                var estaEnLinea = evaluarPuntoEnLinea(listaPuntosLimiteVelocidad[i].location.lat, listaPuntosLimiteVelocidad[i].location.lng, latPrimera, lngPrimera, latSegundo, lngSegundo);
                if(estaEnLinea){
                  listaPuntosLimiteVelocidadEnLinea.push(listaPuntosLimiteVelocidad[i]);
                  listaPuntosLimiteVelocidad.splice(i, 1);
                  i--;
                }

              }
              
            }  

            if(listaPuntosLimiteVelocidadEnLinea.length == 1){
              listasPuntosLimiteVelocidadTemp.push(listaPuntosLimiteVelocidadEnLinea[0]);

            }else if (listaPuntosLimiteVelocidadEnLinea.length > 1){
               listaPuntosLimiteVelocidadEnLinea = bubbleSort(listaPuntosLimiteVelocidadEnLinea, latPrimera, lngPrimera);
               
               for (var i = 0; i < listaPuntosLimiteVelocidadEnLinea.length; i++) {
                     listasPuntosLimiteVelocidadTemp.push(listaPuntosLimiteVelocidadEnLinea[i]);
               }

            }


          }

        }

    }
    listaPuntosLimiteVelocidad = listasPuntosLimiteVelocidadTemp;

}

function pintarPanelListaOrdenadaLimitesVelocidad(borroCampo){
  //borrar panel
  //$("#right-panel3-table3").empty();
  for (var i = 0; i < listaPuntosLimiteVelocidad.length; i++) {
    posicion = evaluarPosicionParada(listaPuntosLimiteVelocidad[i].location.lat, listaPuntosLimiteVelocidad[i].location.lng);
    var numPuntoLimiteVelocidad = i+1;
    makeMarkerPuntosLimiteVelocidad({lat: posicion[1], lng: posicion[2]}, "/static/images/velocidadPin.png", "Límite velocidad "+numPuntoLimiteVelocidad,i);
  }

}


var markerPuntosLimitePuntosVelocidad   = [];
function makeMarkerPuntosLimiteVelocidad( position, icon, title, idMarker) {   
 var marker = new google.maps.Marker({
  position : position,
  map      : map3,
  icon     : icon,
  title    : title,
  type     : "Limite velocidad",
  id       : idMarker
 });
 markerPuntosLimitePuntosVelocidad.push(marker);

}


function pintarPanelPuntosLimitesVelocidad(latitud, longitud, direccion, imagen, id, valorCarga, valorDescarga){
 	numVelocidad = id+1;
  //Pinta el panel del punto de control
    var filaRenderizada = Mustache.render(templateLimiteVelocidad, 
      {
        id            : numVelocidad,
        imagen        : imagen,
        titulo        : "Límite de velocidad "+numVelocidad,
        direccion     : direccion,
        posicion      : "("+latitud+", "+longitud+")",
        lat           : latitud,
        lng           : longitud,
        valorCarga    : valorCarga,
        valorDescarga : valorDescarga

      }
      );
    $("#right-panel3-table3").append(filaRenderizada);

}


function pintarTemplateLimiteVelocidadInicial(latitud, longitud, direccion, imagen, titulo, velocidadCarga, velocidadDescarga){
  //Pinta el panel del punto de control
    var filaRenderizada = Mustache.render(templateLimiteVelocidadInicial, 
      {
        imagen                : imagen,
        titulo                : titulo,
        direccion             : direccion,
        posicion              : "("+latitud+", "+longitud+")",
        lat                   : latitud,
        lng                   : longitud,
        valorCargaInicial     : velocidadCarga,
        valorDescargaInicial  : velocidadDescarga

      }
      );
    $("#right-panel3-table3").append(filaRenderizada);

}

function pintarTemplateLimiteVelocidadFinal(latitud, longitud, direccion, imagen, titulo){
    var filaRenderizada = Mustache.render(templateLimiteVelocidadFinal, 
      {
        imagen    : imagen,
        titulo    : titulo,
        direccion : direccion,
        posicion  : "("+latitud+", "+longitud+")",
        lat       : latitud,
        lng       : longitud

      }
      );
    $("#right-panel3-table3").append(filaRenderizada);

}

function borrarMarkersMapaLimitesVelocidad(){
  for (var i = 0; i < markerPuntosLimitePuntosVelocidad.length; i++) {
    markerPuntosLimitePuntosVelocidad[i].setMap(null);
  }
}