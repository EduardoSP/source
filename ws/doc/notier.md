#Notier

## Autenticacion:

Desde cada html se puede conectar al servicio de socket realizando el siguiente llamado para conectarse.

~~~~~~~~~~~~~~~~~~~~~~~~~~~{.javascript}
socket = io(notierbase, { query: "usuario="+config.getUsuarioLogin()+"&token="+config.getToken()+"&tenant="+config.getTennant()+"" });

socket.on('notificacion', function(msg){
    console.log(msg);            
});
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Enviar notificación:

*Nombre* enviarNotificaciones
*URL:* http://localhost:3000/enviarNotificaciones
    *Descripción:* Se debe enviar de la misma forma que los post de los webservices. Los campos obligatorios son `tipo`, `salas` y `parametros`, el `tipo` indica el tipo de notificación el segundo indica a cuales salsa enviar. el campo parmatros se usarán como parametros, a cada cliente le llega la petición completa y decidirá que hacer con ella.

```
//Petición
{
   "tipo"  : "botonpanico",
   "salas" : ["exxonmobil", "administracion"],
   "parametros" : {
       "placa" : "ytf773" 
   }
   
}

```
