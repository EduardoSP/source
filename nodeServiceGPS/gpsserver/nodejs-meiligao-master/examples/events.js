//Configuracion:
var GPSTrackerUsuario = "gps";
var GPSTrackerToken   = "123456";
var GPSTestImage      = "/Users/fasozu/Downloads/800106002609.jpg"; 
var meiligao = require('../index.js');
var request  = require('request');
// Set up server
var server = new meiligao.Server().listen(56806, function(error) {
    if (error) {
	throw error;
    }
    console.log('gps server is listening');
});
// Handle server connections
var listadoGPS = { };
server.on('connect', function(tracker) {
    var gpsTracker = tracker;
    
    
    gps = tracker; //Me saco ua copia del traclker, en teoría debería mandarlo a listado.
    console.log('tracker has connected');
    /**
     * Tracker events
     */
    // Tracker requested login (and it was confirmed)
    tracker.on('login', function(tracker) {
		
	console.log("IDTRACKER");
	console.log(gpsTracker.trackerId);
	var idGps      = gpsTracker.trackerId;
	console.log("Registrando gps --"+idGps+"--");
	if(! (idGps in listadoGPS) ){
	    
	    listadoGPS[idGps] = {
		"fotos"   : {}
	    };
	}
	listadoGPS[idGps]["tracker"] = gpsTracker;
	//Solicitar por una nueva foto.
	
	/*
	gps.getPhoto(function(err, data) {
	    if (err) {
		console.log('GET PHOTO ERROR: ', err);
	    } else {
		console.log('GET PHOTO DATA: ', data);
	    }
	});*/
	
	
    });
    tracker.on('uploadPhoto', function(dataHexPhoto, tracker){
	
	console.log('Tracker sent uploadPhoto');
	
	var idPhoto      = dataHexPhoto["idPhoto"];
	var idPacket     = dataHexPhoto["idPacket"];
	var totalPackets = dataHexPhoto["totalPackets"];
	var idGps        = dataHexPhoto["idGps"];
	idGps            = parseInt(idGps, 10).toString(10)
	var dataHexPhoto = dataHexPhoto["dataHexPhoto"];
	console.log("PHOTO --- antes if");
	console.log("---"+idGps+"---");
	console.log(listadoGPS);
	if(! (idGps in listadoGPS) ){
	    console.log("PHOTO --- in IF");
	    listadoGPS[idGps] = {
		"fotos" : {},
		"tracker" : tracker
	    };
	}
	console.log("PHOTO --- after IF");
	
	var posGps = listadoGPS[idGps];
	
	if(! (idPhoto in posGps["fotos"]) ){
	    console.log("PHOTO --- new photo");
	    posGps["fotos"][idPhoto] = [];
	}
	console.log("PHOTO --- agregando parte foto");
	partesFoto = posGps["fotos"][idPhoto];
	partesFoto.push({
	    "idPacket"     : idPacket,
	    "dataHexPhoto" : dataHexPhoto 
	});
	console.log("PHOTO --- parte foto agregada");
	console.log("PHOTO --- calculando paquetes");
	var intTotalPackets = parseInt(totalPackets,16);
	console.log("PHOTO --- verificando si tengo todas las foto");
	console.log(intTotalPackets);
	console.log("comparando "+partesFoto.length+" "+intTotalPackets);
	if( partesFoto.length >= intTotalPackets ){
	    console.log("PHOTO --- Tengo todos lso paquetes");
	    //armar archivoFoto.
	    var dataFoto = ""
	    for(var i = 0 ; i < partesFoto.length ; i++ ){
		console.log("PHOTO --- agregando parte foto "+i);
		var parteFoto = partesFoto[i];
		dataFoto = dataFoto+parteFoto["dataHexPhoto"];
	    }
	    var idFoto = posGps["idFoto"] ;
	    var rutaFoto = posGps["rutaFoto"];
	    var fotoDestino  = rutaFoto+idFoto+".jpg";
	    var hexDestino   = rutaFoto+idFoto+".hex";
	    var jsonDestino  = rutaFoto+idFoto+".json";
	    
	    var bufferBinario = new Buffer(dataFoto, "hex");
	    
	    console.log("PHOTO --- creando binario");
	    var wstream = fs.createWriteStream(fotoDestino);	    
	    wstream.write(bufferBinario);	    
	    wstream.end();
	    console.log("PHOTO --- binario creado");
	    fs.writeFile(
		hexDestino,
		dataFoto				
	    );
	    
	    var fechaHoy = new Date();
	    
	    fs.writeFile(
		jsonDestino,
		JSON.stringify({
		    "capturaImagen":[
			{
			    "creadoEn": fechaHoy.toISOString()
			}
		    ]
		})	
	    );
	    
	    console.log("PHOTO --- hex creado");	    	    
	}
	
    });
    
    // Heartbeat packets
    tracker.on('heartbeat', function(tracker) {
	console.log('tracker sent heartbeat');		
	
    });
    // Most useful thing: alarms & reports
    tracker.on('message', function(message, tracker) {
	console.log('tracker sent message: [' + meiligao.Message.getMessageTypeByCode(message.type) + ']', message);
	console.log("*****");
	console.log(message.data.latitude);
	console.log(message.data.longitude);
	console.log(message.data.date.toISOString() );
	console.log( (typeof message.data.date) );
	console.log(message.trackerId);
	console.log(gpsTracker.trackerId);
	console.log(this.trackerId);
	console.log("*****");
	if(meiligao.Message.getMessageTypeByCode(message.type) == "ALARM_SOS_RELEASED"){
	    var dataCompleto = { 
		"autenticacion" : {
		    "usuario" : "admin",
		    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
		    "tenant" : "exxonmobil"        
		},    
		"data" : {
		    "latitud"           : message.data.latitude.toString(), 
		    "longitud"          : message.data.longitude.toString(),
		    "velocidad"         : (message.data.speed * 1.852).toString(), 
		    "horaRegistrada"    : message.data.date.toISOString(),
		    "identificadorGPS"  : this.trackerId          
		}		    
	    };
	    console.log(JSON.stringify(dataCompleto));
	    console.log(":):):):):):):):):):):):):):):):):):):)");
	    
	    
	    request.post(
		{
		    url:'http://localhost/ws/botonPanicoGPS', 
		    form: {
			request:JSON.stringify(dataCompleto)
		    }
		}, function(err,httpResponse,body){ 
		    //console.log(body);
		    console.log("RESPEUSTA BOTON PANICO");
		}
	    );
	    
	}else{
	    var dataCompleto = { 
		"autenticacion" : {
		    "usuario" : "admin",
		    "token" : "5776d71ff8f8442ca8326d04987a9bdc",
		    "tenant" : "exxonmobil"        
		},    
		"data" : {        
 		 "posiciones" : [
		     { "latitud"        : message.data.latitude.toString(), 
		       "longitud"       : message.data.longitude.toString(),
		       "velocidad"      : (message.data.speed * 1.852), 
		       "horaRegistrada" : message.data.date.toISOString()}
		  ],
		    "identificadorGPS"  : this.trackerId          
		}
	    };
	     console.log("-----------------------------------------------------------------------------");
	    if(message.data.latitude != 0){
		console.log(JSON.stringify(dataCompleto));
		console.log("LASDKASJDASDJASDKJHASKDHASJKDHAKSDHJ");
		console.log(dataCompleto);
		request.post(
		    {
			url:'http://localhost/ws/registrarPosicionesGPS', 
			form: {
			    request:JSON.stringify(dataCompleto)
			}
		    }, function(err,httpResponse,body){ 
			//console.log(body);
		    }
		);
	    }
	}
	
	
	    
    });
    // Useful for debugging
    tracker.on('packet.in', function(packet, tracker) {
	console.log('incoming packet:', packet.toString());
    });
    tracker.on('packet.out', function(packet, tracker) { 
	console.log('outgoing packet:', packet.toString());
    });
    // Handle errors
    tracker.on('error', function(error, buffer) { 
	console.log('error parsing message:', error, buffer);
    });
    // Handle disconnects
    tracker.on('disconnect', function() {
	console.log('tracker disconnected (tracker.disconnect)');
    });
});
// Handle disconnects
server.on('disconnect', function(tracker) { 
    console.log('tracker disconnected (server.disconnect)'); 
});
//---------------------------------------------------------------------
//Servidor otro.
var fs      = require('fs');
var express = require('express');
var app     = express();
var bodyParser = require('body-parser')
//app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
    type : "application/x-www-form-urlencoded",
    extended: true
}));
app.get('/', function (req, res) {
  res.send('Hello World!');
});
app.post('/ws/solicitarTomarFoto', function (req, res) {
    var respuesta = {};    
    if('request' in req.body){
	
	var peticion      = JSON.parse(req.body.request);
	var autenticacion = peticion.autenticacion;
	
	if(
	    autenticacion.usuario == GPSTrackerUsuario &&
	    autenticacion.token   == GPSTrackerToken 
	){
	    var dataPeticion = peticion.data;
	    var idFoto       = dataPeticion.idFoto;
	    var rutaFoto     = dataPeticion.rutaFoto;
	    var idGps        = dataPeticion.idGps;
	    console.log("Buscando el gps Para foto --"+idGps+"--");
	    if(! (idGps in listadoGPS) ){		
		console.log("No encontré nada");
		listadoGPS[idGps] = {
		    "fotos"   : {},
		    "tracker" : null
		};
	    }
	    listadoGPS[idGps]["idFoto"]   = idFoto;
	    listadoGPS[idGps]["rutaFoto"] = rutaFoto;
	    
	    var tracker = listadoGPS[idGps]["tracker"];
	    if(tracker != null){
		
		if( true /* tracker.status == 1*/ ){ //Waiting
		    console.log("Intentando tomar foto con status: "+tracker.status);
		    tracker.getPhoto(function(err, data) {
			console.log("Tomando foto");
			if (err) {
			    console.log('GET PHOTO ERROR: ', err);
			} else {
			    console.log('GET PHOTO DATA: ', data);
			}
		    });
		    respuesta = {
			"success"  : true
		    };
		}else{
		    respuesta = {
			"success"  : false,
			"errorMsg" : "El dispositivo se encuentra ocupado."
		    };
		}						
	    }else{
		respuesta = {
		    "success" : false,
		    "errorMsg" : "El dispositivo ni se ha logueado"
 		}
	    }
	    
	    
	    /*
	    var dataJson = {
		"capturaImagen":[
		    {
			"creadoEn":"2016-03-12T08:07:19Z",
			"latitud":"4.5981",
			"longitud":"-74.0758"
		    }
		]
	    };
	    
	    var fotoDestino  = rutaFoto+idFoto+".jpg";
	    var jsonDestino  = rutaFoto+idFoto+".json";
	    
	    fs.createReadStream(GPSTestImage).pipe(fs.createWriteStream(fotoDestino));
	    fs.writeFile(
		jsonDestino,
		JSON.stringify(dataJson),
		function(err) {
		if(err) {
		    //return console.log(err);
		}				
	    });
	    */
	    
   
	}else{
	    respuesta = {
		"success"  : false,
		"errorMsg" : ""
	    };
	}			
    }else{
	respuesta = {
	    "success"  : false,
	    "errorMsg" : "No hay request"	    
	};
    }
    console.log(respuesta);
    res.send( JSON.stringify( respuesta ) );
    
});
app.listen(5006, function () {
});
//---------------------------------------------------------------------