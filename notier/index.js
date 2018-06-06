var app        = require('express')();
var http       = require('http').Server(app);
var io         = require('socket.io')(http);
var request    = require('request');
var bodyParser = require('body-parser');


app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

app.get('/', function(req, res){
    res.sendfile('index.html');
});

app.get('/enviarMensaje', function(req, res){
    io.to('comercial').emit('chat message', 'MENSAJE DE COMERCIAL');
    res.send('<h1>Mensaje Enviado</h1>');
});

app.post('/enviarNotificaciones', function (req, res) {
    console.log("NOTICICAIONES-------------------------");
    console.log(req.body.request);
    console.log("--------------------------------------");

    var resultado = {"success":true};    
//    try {
        var peticion = JSON.parse(req.body.request);


        
        var sala = peticion.tenant;
        console.log("Mandando notificacion a sala: "+sala)
        io.to(sala).emit('notificacion', JSON.stringify(peticion) );
        
        resultado = {"success":true};    
    // }
    // catch(err) {
    //     resultado = {"success":false};            
    // }

    res.send( JSON.stringify( resultado ) );
});

app.get('/validarAutenticacion', function(req, res){
    console.log('Validando autenticación')
    var peticion = {
        "usuario"  : "admin",
	"token"    : "1f49ad26a56445f696a105545cb9a5f7",
        "tenant"   : "exxonmobil"
    };
    var peticionJson = JSON.stringify(peticion);
    request.post(
    'http://localhost:8080/ws/verificarCredenciales',
    { form: { request: peticionJson } },
        function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body)
            }else{
                console.log("ERROR")
            }
            res.send('<h1>revisado Enviado</h1>');
        }
    );
});

io.on('connection', function(socket){
   
    //Realizo la sucripcion a la sala:
    console.log('a user connected');
    var usuario = socket.request._query['usuario'];
    var tenant  = socket.request._query['tenant'];
    var token   = socket.request._query['token'];
    console.log(usuario);
    console.log(token);
/*
    socket.join(tenant);  */    

    var peticion = {
        "usuario" : usuario,
        "token"   : token,
        "tenant"   : tenant
    };

    
    var peticionJson = JSON.stringify(peticion);
    request.post(
    'http://localhost:8080/ws/verificarCredenciales',
    { form: { request: peticionJson } },
        function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body)
                var respuesta = JSON.parse(body);
                if(respuesta["success"]){                    
                    socket.join(tenant);                                        
                }                
            }else{
                console.log("ERROR")
            }            
        }
    );

    //Fin de la suscrbicion a la sala.
    //===================================================
        
    socket.on('disconnect', function(){
        console.log('user disconnected');
    });
    /*
    socket.on('chat message', function(msg){
        console.log('message: ' + msg);
        io.emit('chat message', msg);
    });
    */
});

io.on('connection', function(socket){
        
    socket.on('disconnect', function(){
        console.log('user disconnected');
    });
    
    socket.on('chat message', function(msg){
        console.log('message: ' + msg);
        io.emit('chat message', msg);
    });
    
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});
