var polyline4 = null;
var listaPuntosInteres = [];//lista que se guarda la informacion de los puntos de interes que se enviaran ws
var inicializar__editar_datos_panel = false;


function pintarRutaPuntosInteres(){
      //pinta la direccion origen y la direccion destino en el panel
      pintarPanel4Origen(origen.lat(), origen.lng(), direccionOrigen);
      pintarPanel4Destino(destino.lat(), destino.lng(), direccionDestino);

      // pinta la ruta de los limites de velocidad
        borraIconosPosIniFinalMapa4(null);
      //Borra puntos de interes que estan fuera de la ruta
        //evaluarPuntosInteresEnRuta();

      if(polyline4 != null){
        polyline4.setMap(null);
      } 

      polyline4 = new google.maps.Polyline({
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
              polyline4.getPath().push(nextSegment[k]);
              bounds.extend(nextSegment[k]);
            }
          }
      }
      polyline4.setMap(map4);
      makeMarkerRutaPuntosInteres( origen, guiImagePuntoControl+"/static/images/origenPin.png", "Origen" );
      
      makeMarkerRutaPuntosInteres( destino, guiImagePuntoControl+"/static/images/destinoPin.png", 'Destino' );

}


//funciones que pintan los puntos en el panel3 derecho
function pintarPanel4Origen(latitud, longitud, direccion){
  $("#right-panel4-tableOrigenDestino4").empty();
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
  $("#right-panel4-tableOrigenDestino4").append(filaRenderizadaOrigen);

}

function pintarPanel4Destino(latitud, longitud, direccion){
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
  $("#right-panel4-tableOrigenDestino4").append(filaRenderizadaDestino);

}

var markersRutaPuntosInteresIniFin = [];
function makeMarkerRutaPuntosInteres( position, icon, title ) {
 var marker = new google.maps.Marker({
  position: position,
  map: map4,
  icon: icon,
  title: title
 });
 markersRutaPuntosInteresIniFin.push(marker);
}


var infowindow4  = null;
function agregarListanerDerechoMap4(){
// agrega el evento click derecho al map 4
  google.maps.event.addListener(map4, "rightclick", function(event) {

    var lat = event.latLng.lat();
    var lng = event.latLng.lng();
    //funcion que verifica la parada si es de carga o descarga
    if(infowindow4 != null){
      infowindow4.close();
    }
    var contentString = '<a href='+'javascript:puntoInteres('+lat+','+lng+');'+'>Agregar punto de interes</a>';
      infowindow4 = new google.maps.InfoWindow({
    content: contentString
      });    
      var a = new google.maps.MVCObject();
      a.setValues({position: event.latLng });
      infowindow4.open(map4,a);
    
  });
}

var listaConfiguracionPuntosInteres= []; //lista que guardara las configuraciones de los puntos de interes
function puntoInteres(lat, lng){  
  var posicion = null;
  infowindow4.close();
  //funcion que ordena los puntos en la linea recibe latitud y longitud
  buscarDireccionPunto("puntoInteres", lat, lng);
}

function AsignarDireccionPuntoInteres(latitud, longitud, direcc){
    listaPuntosInteres.push({location: {lat: latitud, lng: longitud, direccion : direcc, nombre : ""}});
    //ordenarPuntosInteres();
    pintarPanelListaOrdenadaPuntosInteres(false);
}

/* julian :D */
function traer_datos_interes (tenant, idRuta, ws) {
  var peticion    = { 'autenticacion': {  'usuario' : config.getUsuarioLogin(),
                                          'token'   : config.getToken(),
                                          'tenant'  : tenant,  
                                        },
                        'data'         : { 
                                  'id': idRuta,
                                  /*  En el caso de no encontrar el documento en la db, se deba crear uno 
                                      nuevo para poder cargar la pagina actual */
                                  'idRuta'        : idRuta,
                                  'idPuntosRuta'  : idPuntosRutaDefinida,    
                                  'puntosInteres' : []
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
      var puntos_interes    = respuesta.data.puntosInteres;
      id_punto_interes_ruta = respuesta.data.id;
      for (i = 0; i < puntos_interes.length; i++) { 
        var latitud_temp              = puntos_interes[i][0];
        var longitud_temp             = puntos_interes[i][1];
        var direccion_tenmp           = puntos_interes[i][2];
        var nombre                    = puntos_interes[i][3];

        listaPuntosInteres.push({location: {  lat               : latitud_temp, 
                                              lng               : longitud_temp, 
                                              direccion         : direccion_tenmp, 
                                              nombre            : nombre
                                            }});
        
      }
      // console.log ("puntos de interes" + JSON.stringify(listaPuntosInteres, null, 3));
      inicializar__editar_datos_panel = true;
      pintarPanelListaOrdenadaPuntosInteres(false);
      inicializar__editar_datos_panel = false;

      /* Dejamos seleccionada la petana Rutas */
      // $('#tabPestana1').tab('show');

    });
    request.fail(function(jqXHR, textStatus){ });
};

function pintarPanelListaOrdenadaPuntosInteres(borroCampo) {
	//mantiene los nombre digitados por el usuario
	if(!borroCampo){	
		for (var i = 0; i < listaPuntosInteres.length; i++) {
		  var idTexto = ""; // = $('#formNombreInteres'+i+'').val();

      if (inicializar__editar_datos_panel) {
          idTexto = listaPuntosInteres[i].location.nombre;
          console.log ("puntos interes: paso por inicializar__editar_datos_panel");
      } else {
          idTexto = $('#formNombreInteres'+i+'').val();
          console.log ("puntos interes: paso por la secuencia normal");
      }

		  listaPuntosInteres[i] = { 
        location: {
          lat       : listaPuntosInteres[i].location.lat, 
          lng       : listaPuntosInteres[i].location.lng, 
          direccion : listaPuntosInteres[i].location.direccion, 
          nombre    : idTexto}
        }
		}	
	}
  //borrar panel
  $("#right-panel4-table4").empty();
  for (var i = 0; i < listaPuntosInteres.length; i++) {
    //posicion = evaluarPosicionParada(listaPuntosInteres[i].location.lat, listaPuntosInteres[i].location.lng);
    var numPuntosInteres = i+1;
    makeMarkerPuntosInteres({
      lat: Number(listaPuntosInteres[i].location.lat), 
      lng: Number(listaPuntosInteres[i].location.lng)}, 
      "/static/images/interesPin.png", 
      "Punto Interes "+numPuntosInteres,
      i
      );
    pintarPanelPuntoInteres(
      listaPuntosInteres[i].location.lat, 
      listaPuntosInteres[i].location.lng, 
      listaPuntosInteres[i].location.direccion, 
      listaPuntosInteres[i].location.nombre, 
      i
      );
  }
}

var markerPuntosInteres   = [];
function makeMarkerPuntosInteres( position, icon, title, idMarker) {   
 var marker = new google.maps.Marker({
  position : position,
  map      : map4,
  icon     : icon,
  title    : title,
  type     : "Punto interes",
  id       : idMarker
 });
 markerPuntosInteres.push(marker);

}

function pintarPanelPuntoInteres(latitud, longitud, direccion, nombre, id){
  numPunto = id+1;
  //Pinta el panel del punto de control
    var filaRenderizada = Mustache.render(templatePuntosInteres, 
      {
        id        : id,
        imagen    : "/static/images/interesCirculo.png",
        titulo    : "Punto de interes "+numPunto,
        direccion : direccion,
        posicion  : "("+latitud+", "+longitud+")",
        lat       : latitud,
        lng       : longitud,
        nombre	  : nombre

      }
      );
    $("#right-panel4-table4").append(filaRenderizada);
/*    var formInteres = $('#formInteres');
    $('#formInteres').validator('update');*/

}


// Sets the map on all markers in the array.
function borraIconosPosIniFinalMapa4(map) {
  for (var i = 0; i < markersRutaPuntosInteresIniFin.length; i++) {
    markersRutaPuntosInteresIniFin[i].setMap(map);
  }
} 


/*function evaluarPuntosInteresEnRuta(){
  //funcion que evalua los limites de velocidad y borra los que se encuentran fuera de la ruta
  //ordenarPuntosInteres();
  //borrarMarkersPuntosInteres();
  pintarPanelListaOrdenadaPuntosInteres();
}*/

function borrarMarkersPuntosInteres(){
  for (var i = 0; i < markerPuntosInteres.length; i++) {
    markerPuntosInteres[i].setMap(null);
  }
}