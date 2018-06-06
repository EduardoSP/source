//var wsbase     = "http://localhost:8080/ws"; //Raiz de los servicios web.
//var guibase    = "http://localhost/webfleetbigui"; //Raiz de los servicios web.

var wsbase     = "http://localhost:8080/ws"; //Raiz de los servicios web.
var guibase    = "http://localhost/webfleetbigui"; //Raiz de los servicios web.


//Funciones estado de usuario. --------------------------------------------
var config = {
	
	//Funciones.
	setLogueado: function(estado){//indica si el usuario está logueado o no.
		if(estado) { localStorage.setItem('isLogueado','true');  }
		      else { localStorage.setItem('isLogueado','false'); }
	},

	getLogueado: function (){
		var resultado = false;
		if(localStorage.getItem('isLogueado') != 'true'){
			resultado = false;
		}else{
			resultado = true;
		}
		return resultado;
	},

	//Token de autenticación
	setToken: function(nuevo){	localStorage.setItem('usuarioToken', nuevo); 	},
	getToken: function(){ return localStorage.getItem('usuarioToken');	},
	
	//nombre de usuario
	setNombreUsuario: function(nuevo){
		localStorage.setItem('nombreUsuario', nuevo);
		},
	getNombreUsuario: function(){ return localStorage.getItem('nombreUsuario');	},

	//login
	setUsuarioLogin: 	function(nuevo){	localStorage.setItem('usuarioLogin', nuevo); 	},
	getUsuarioLogin: 	function(){return   localStorage.getItem('usuarioLogin'); },
	
	//Perfil de usuario
	setPerfilUsuario: 	function(nuevo){	localStorage.setItem('perfilUsuario', nuevo); 	},
	getPerfilUsuario: 	function(){return localStorage.getItem('perfilUsuario'); },
	
	//Tennat 
	setTennant: function(nuevo){	localStorage.setItem('tennant', nuevo); 	},
	getTennant: function(){ return localStorage.getItem('tennant');	},
	
	//Retorna true si el tenantNombre esta configurado, de lo contrario es false
	isConfigured:		function(){
							var result 		= true;
							var tenantRaw 	= localStorage.getItem('config');
							if( tenant != null ){
								// var tenant = JSON.parse(tenantRaw);
								// config			= tenant.id;
								// config = tenant.nombreCompleto;
								// config.tenantNombreCorto 	= tenant.nombreCorto;
								// config.tenantLogo			= tenant.logo;
								result = true;
							}else{
								result = false;
							}
							return result;
						},

	//Recibe un objeto json con la nueva configuración.
	setConfiguration	: function(nuevaConfiguracion){
								//TODO validar la nueva configuración
								localStorage.setItem('config', JSON.stringify(nuevaConfiguracion));
							},

	//funciòn de padding ceros
	zeroPadding: function(numero){
	    var padding = 4;
	    numero = numero.toString();
	    while( numero.length < padding ){
			numero = "0"+numero;
	    }
	    return numero;
	},
	
	//funcion par configurar el tiempo de recarga mapa vista general
	getTIEMPO_RECARGA_MAPA_VISTA_GENERAL: function(numero){
	    return 10000;
	},	
};


var traduccionDatatables = {
    "lengthMenu"  	: "Mostrar _MENU_ registros por página",
    "zeroRecords" 	: "No se encontraron registros",
    "info"        	: "Mostrando página _PAGE_ de _PAGES_",
    "infoEmpty"   	: "No existen registros disponibles",
    "infoFiltered"	: "(filtrado de _MAX_ registros totales)",
    "search"		: "Buscar:",
    "paginate": {
        "first":      "Primero",
        "last":       "Último",
        "next":       "Siguiente",
        "previous":   "Anterior"
    },
};

function verificarReinicio(respuesta, url){
    if('debeReiniciar' in  respuesta){
        if(respuesta.debeReiniciar){                        
            window.location.href = url;
        }
    }  
}

function verificarEstadoIngreso(perfil, urlsBase, urlLogin){
    if(config.getLogueado()){
        var pefilUsuario = config.getPerfilUsuario();
        if(config.getPerfilUsuario() != perfil){
        	var destino = urlsBase[config.getPerfilUsuario()];
        	if(typeof destino != 'undefined'){
        		window.location.href = urlsBase[config.getPerfilUsuario()];
        	}
        	else{
        		config.setLogueado(false);
        	}
            
        }
    }else{
       window.location.href = urlLogin;
    }    
}

