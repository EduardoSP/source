var polyline2 = null;
var listaPuntosControl = []; //lista que se guarda la informacion de los puntos de control  se enviaran ws
function pintarRutaPuntoControl(){
      //pinta la direccion origen y la direccion destino en el panel
      pintarPanel2Origen  (origen.lat(),  origen.lng(),   direccionOrigen);
      pintarPanel2Destino (destino.lat(), destino.lng(),  direccionDestino);
      // pinta la ruta de los puntos de control
      //if(makeMarkerRutaPuntoControl.length != 0){
        borraIconosPosIniFinalMapa2(null);
        //Borra puntos de control que estan fuera de la ruta
        evaluarPuntosControlEnRuta();
      //}

      if(polyline2 != null){
        polyline2.setMap(null);
      } 

      polyline2 = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
      });

      var bounds = new google.maps.LatLngBounds();
      var legs = directionsDisplay.getDirections().routes[0].legs;
      //console.log (legs);
      //console.log (directionsDisplay);
      //console.log (directionsDisplay.map.zoom);
      var direccionDisplay_get =  directionsDisplay.getDirections();
      //console.log (direccionDisplay_get);

      for (i=0;i<legs.length;i++) {
          var steps = legs[i].steps;
          for (j=0;j<steps.length;j++) {
            var nextSegment = steps[j].path;
            for (k=0;k<nextSegment.length;k++) {
              polyline2.getPath().push(nextSegment[k]);
              //console.log (nextSegment[k]);
              bounds.extend(nextSegment[k]);
            }
          }
      }
      polyline2.setMap(map2);
      //makeMarkerRutaPuntoControl( origen, "file:localhost:8080/Fleetbiweb/webfleetbigui/static/images/origenPin.png", "Origen" );
      makeMarkerRutaPuntoControl( origen, guiImagePuntoControl+"/static/images/origenPin.png", "Origen" );
      
      makeMarkerRutaPuntoControl( destino, guiImagePuntoControl+"/static/images/destinoPin.png", 'Destino' );
      //console.log(markersRutaPuntoControlIniFin);

}


var markersRutaPuntoControlIniFin = [];
function makeMarkerRutaPuntoControl( position, icon, title ) {
 var marker = new google.maps.Marker({
  position: position,
  map: map2,
  icon: icon,
  title: title
 });
 markersRutaPuntoControlIniFin.push(marker);
}

// Sets the map on all markers in the array.
function borraIconosPosIniFinalMapa2(map) {
  for (var i = 0; i < markersRutaPuntoControlIniFin.length; i++) {
    markersRutaPuntoControlIniFin[i].setMap(map);
  }
}  

var infowindow2  = null;
function agregarListanerDerechoMap2(){
// agrega el evento click derecho al map 2
  google.maps.event.addListener(map2, "rightclick", function(event) {

    var lat = event.latLng.lat();
    var lng = event.latLng.lng();
    //funcion que verifica la parada si es de carga o descarga
    if(infowindow2 != null){
      infowindow2.close();
    }
    var contentString = '<a href='+'javascript:puntoControl('+lat+','+lng+');'+'>Agregar punto control</a>';
      infowindow2 = new google.maps.InfoWindow({
        content: contentString
      });    
      var a = new google.maps.MVCObject();
      a.setValues({position: event.latLng });
      infowindow2.open(map2,a);
    
  });
}


var markerPuntosControl     = [];
//var idMarkerControl         = 0;
var markerOprimidoControl   = null;
function makeMarkerPuntosControl( position, icon, title, idMarkerControl) {   
 var marker = new google.maps.Marker({
  position : position,
  map      : map2,
  icon     : icon,
  title    : title,
  type     : "Punto control",
  id       : idMarkerControl
 });
 markerPuntosControl.push(marker);

}


var listaConfiguracionPuntoControl= []; //lista que guardara las configuraciones de los puntos de control
function puntoControl(lat, lng){  
  var posicion = null;
  posicion = evaluarPosicionParada(lat, lng);
  infowindow2.close();
  //funcion que ordena los puntos en la linea recibe latitud y longitud
  buscarDireccionPunto("puntoControl", posicion[1], posicion[2]);
}

function AsignarDireccionPuntoControl(latitud, longitud, direcc){
    listaPuntosControl.push({location: {lat: latitud, lng: longitud, direccion : direcc}});
    ordenarPuntosLinea();
    pintarPanelListaOrdenada();
}

/* julian :D */
// traer_datos_punto_control ({{tenant}}, "{{idRuta}}", "{% url 'wsDetallePuntoControlRuta' %}")
function traer_datos_punto_control (tenant, idRuta, ws) {
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
                                  'puntosControl' : []
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
      // pintarTablaRutas(respuesta["data"]);
      // console.log(respuesta);
      var puntosControl     = respuesta.data.puntosControl;
      id_punto_control_ruta = respuesta.data.id 
      for (i = 0; i < puntosControl.length; i++) {
        var latitud_temp    = puntosControl[i][0];
        var longitud_temp   = puntosControl[i][1];
        var direccion_tenmp = puntosControl[i][2];
        listaPuntosControl.push({location: {  lat: latitud_temp, 
                                              lng: longitud_temp, 
                                              direccion : direccion_tenmp
                                            }});
      }
      ordenarPuntosLinea();
      pintarPanelListaOrdenada();

      /* Dejamos seleccionada la petana Rutas */
      // $('#tabPestana1').tab('show');

    });
    request.fail(function(jqXHR, textStatus){ });
};

function pintarPanelListaOrdenada(){
  //borrar panel
  $("#right-panel2-table2").empty();
  for (var i = 0; i < listaPuntosControl.length; i++) {
    posicion = evaluarPosicionParada(listaPuntosControl[i].location.lat, listaPuntosControl[i].location.lng);
    var numPuntoControl = i+1;
    makeMarkerPuntosControl({lat: posicion[1], lng: posicion[2]}, "/static/images/controlPin.png", "Punto Control "+numPuntoControl,i);
    pintarPanelPuntoControl(listaPuntosControl[i].location.lat, listaPuntosControl[i].location.lng, listaPuntosControl[i].location.direccion, i);
  }
}

function borrarMarkersMapa(){
  for (var i = 0; i < markerPuntosControl.length; i++) {
    markerPuntosControl[i].setMap(null);
  }
}


function evaluarPuntosControlEnRuta(){
  //funcion que evalua los puntos de control y borra los que se encuentran fuera de la ruta
  ordenarPuntosLinea();
  borrarMarkersMapa();
  pintarPanelListaOrdenada();
}


function evaluarPuntoEnLinea(currPointX, currPointY, point1X, point1Y, point2X, point2Y){
  //https://stackoverflow.com/questions/11907947/how-to-check-if-a-point-lies-on-a-line-between-2-other-points
  dxc = currPointX - point1X;
  dyc = currPointY- point1Y;
  dxl = point2X - point1X;
  dyl = point2Y - point1Y;
  cross = dxc * dyl - dyc * dxl;
  if (Math.abs(cross) >= 0.0000000001){
    return false;
  }else{
    if (Math.abs(dxl) >= Math.abs(dyl))
      return dxl > 0 ? 
        point1X <= currPointX && currPointX <= point2X :
        point2X <= currPointX && currPointX <= point1X;
        else
          return dyl > 0 ? 
            point1Y <= currPointY&& currPointY<= point2Y :
            point2Y <= currPointY&& currPointY<= point1Y;
  }

}

function swap(myArr, indexOne, indexTwo){
  var tmpVal = myArr[indexOne];
  myArr[indexOne] = myArr[indexTwo];
  myArr[indexTwo] = tmpVal;
  return myArr;
}

function bubbleSort(myArr, latitud, longitud){
  //ordenamiento por burbuja
  //http://www.etnassoft.com/2011/10/17/ordenacion-basica-de-datos-en-javascript/
  var size = myArr.length;
 
  for( var pass = 1; pass < size; pass++ ){ // outer loop
    for( var left = 0; left < (size - pass); left++){ // inner loop
      var right = left + 1;

      var dlatIzq = latitud - myArr[left].location.lat;
      var dlngIzq = longitud - myArr[left].location.lng;
      var dlatDer = latitud - myArr[right].location.lat;
      var dlngDer = longitud -myArr[right].location.lng;
      var distanciaIzq = Math.sqrt(dlatIzq * dlatIzq + dlngIzq * dlngIzq);
      var distanciaDer = Math.sqrt(dlatDer * dlatDer + dlngDer * dlngDer);

      if( distanciaIzq > distanciaDer ){
        swap(myArr, left, right);
      }
    }
  }
 
  return myArr;
}


var listaPuntosSegmento = [];

function ordenarPuntosLinea(){
  var listasPuntosControlOrdenadosTemp = [];
  //var listaFinal = [];
  //var numSegmentos = 0;
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

            var listaPuntosControlEncontradosEnLinea = [];
            for (var i = 0; i < listaPuntosControl.length; i++) {

              //punto esta en el segemento
              if(listaPuntosControl[i] != null){
                var estaEnLinea = evaluarPuntoEnLinea(listaPuntosControl[i].location.lat, listaPuntosControl[i].location.lng, latPrimera, lngPrimera, latSegundo, lngSegundo);
                if(estaEnLinea){
                  listaPuntosControlEncontradosEnLinea.push(listaPuntosControl[i]);
                  listaPuntosControl.splice(i, 1);
                  i--;
                }

              }
              
            }  

            if(listaPuntosControlEncontradosEnLinea.length == 1){
              listasPuntosControlOrdenadosTemp.push(listaPuntosControlEncontradosEnLinea[0]);

            }else if (listaPuntosControlEncontradosEnLinea.length > 1){
               listaPuntosControlEncontradosEnLinea = bubbleSort(listaPuntosControlEncontradosEnLinea, latPrimera, lngPrimera);
               
               for (var i = 0; i < listaPuntosControlEncontradosEnLinea.length; i++) {
                     listasPuntosControlOrdenadosTemp.push(listaPuntosControlEncontradosEnLinea[i]);
               }

            }


          }

        }

    }
    listaPuntosControl = listasPuntosControlOrdenadosTemp;

}


function pintarPanelPuntoControl(latitud, longitud, direccion, id){
  numPuntoControl = id+1;
  //Pinta el panel del punto de control
    var filaRenderizada = Mustache.render(templatePuntosControl, 
      {
        id        : id,
        imagen    : "/static/images/controlCirculo.png",
        titulo    : "Punto de control "+numPuntoControl,
        direccion : direccion,
        posicion  : "("+latitud+", "+longitud+")",
        lat       : latitud,
        lng       : longitud

      }
      );
    $("#right-panel2-table2").append(filaRenderizada);

}


//funciones que pintan los puntos en el panel2 derecho

function pintarPanel2Origen(latitud, longitud, direccion){
  $("#right-panel2-tableOrigenDestino2").empty();
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
  $("#right-panel2-tableOrigenDestino2").append(filaRenderizadaOrigen);

}

function pintarPanel2Destino(latitud, longitud, direccion){
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
  $("#right-panel2-tableOrigenDestino2").append(filaRenderizadaDestino);

}