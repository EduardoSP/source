# -*- coding: utf-8 -*-
from django.conf.urls import  url
from webfleetbigui import views

#NOTA:..........preguntar a scrum master las siguientes lineas
urlpatterns = [
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/login',
            views.login,
           name='loginUsuarios'),

    url(r'^webfleetbigui/login$',
            views.loginUnificado,
           name='loginUnificado'),

    url(r'^$',
            views.loginUnificado,
           name='loginUnificado'),    
    
    url(r'^webfleetbigui/recuperarContrasena/(?P<tenant>[-\w]+)/(?P<token>[-\w]+)$',
            views.recuperarContrasena,
            name='recuperarContrasena'),

    url(r'^webfleetbigui/loginGeneradorCarga',
            views.loginGeneradorCarga,
           name='loginGeneradorCarga'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/codigosAccesoGenerador',
            views.codigosAccesoGenerador,
           name='codigosAccesoGenerador'),    
                        
    #Administrador--------------------------------------------------------------                   
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminVistaGeneral$',
            views.adminVistaGeneral,
            name='adminVistaGeneral'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminVehiculos',
            views.adminVehiculos,
            name='adminVehiculos'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminConductores',
            views.adminConductores,
            name='adminConductores'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminRutas',
            views.adminRutas,
            name='adminRutas'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleVehiculo/(?P<idVehiculo>[-\w]+)/(?P<pestanaActivada>[-\w]+)',
            views.adminDetalleVehiculo,
            name='adminDetalleVehiculo'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminVigilancia$',
            views.adminVigilancia,
            name='adminVigilancia'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminVigilanciaCrearZona/(?P<latitud>[-\.\w]+)/(?P<longitud>[-\.\w]+)',
            views.adminVigilanciaCrearZona,
            name='adminVigilanciaCrearZona'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleZona/(?P<idZona>[-\w]+)',
            views.adminDetalleZona,
            name='adminDetalleZona'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleZonaAlarma/(?P<idZonaAlarma>[-\w]+)',
            views.adminDetalleZonaAlarma,
            name='adminDetalleZonaAlarma'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminVigilanciaCrearProgramacion$',
            views.adminVigilanciaCrearProgramacion,
            name='adminVigilanciaCrearProgramacion'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleProgramacionVigilancia/(?P<idProgramacion>[-\w]+)',
            views.adminDetalleProgramacionVigilancia,
            name='adminDetalleProgramacionVigilancia'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminAlarmas$',
            views.adminAlarmas,
            name='adminAlarmas'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminSeguridadVial$',
            views.adminSeguridadVial,
            name='adminSeguridadVial'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminGeneradorCodigo$',
            views.adminGeneradorCodigo,
            name='adminGeneradorCodigo'),

    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminCadenaFrio$',
            views.adminCadenaFrio,
            name='adminCadenaFrio'),

    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminCrearCodigoGeneradorCarga$',
            views.adminCrearCodigoGeneradorCarga,
            name='adminCrearCodigoGeneradorCarga'),    
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleAlarmaPanico/(?P<idAlarmaPanico>[-\w]+)',
            views.adminDetalleAlarmaPanico,
            name='adminDetalleAlarmaPanico'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/miCuenta$',
            views.miCuenta,
            name='miCuenta'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/miCuentaGeneradorCarga$',
            views.miCuentaGeneradorCarga,
            name='miCuentaGeneradorCarga'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminConfiguracion$',
            views.adminConfiguracion,
            name='adminConfiguracion'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminCrearConductor$',
            views.adminCrearConductor,
            name='adminCrearConductor'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleConductor/(?P<idConductor>[-\w]+)',
            views.adminDetalleConductor,
            name='adminDetalleConductor'),
    
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminCrearRuta$',
            views.adminCrearRuta,
            name='adminCrearRuta'),

    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminEditarRuta/(?P<idRuta>[-\w]+)',
            views.adminEditarRuta,
            name='adminEditarRuta'),
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminListadoAsignacionesRutas$',
            views.adminListadoAsignacionesRutas,
            name='adminListadoAsignacionesRutas'),
               
   url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminDetalleAsignacionRuta/(?P<idAsignacionRuta>[-\w]+)/(?P<idRuta>[-\w]+)',
            views.adminDetalleAsignacionRuta,
            name='adminDetalleAsignacionRuta.html'),

    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminCrearTipoZona$',
            views.adminCrearTipoZona,
            name='adminCrearTipoZona'),

    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminTipoZona$',
            views.adminTipoZona,
            name='adminTipoZona'),

    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminEditarTipoZona/(?P<idTipozona>[-\w]+)',
            views.adminEditarTipoZona,
            name='adminEditarTipoZona'),
    
    # url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminComunicaciones',
    #         views.adminComunicaciones,
    #         name='adminComunicaciones'),
               
    #Super Administrador--------------------------------------------------------------                   
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/administrador$',
            views.superAdministradorTenants,
            name='superAdministradorTenants'), 
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorCrearTenant$',
            views.superAdministradorCrearTenant,
            name='superAdministradorCrearTenant'),
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorDetalleTenant/(?P<idTenant>[-\w]+)',
            views.superAdministradorDetalleTenant,
            name='superAdministradorDetalleTenant'),
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorCrearUsuarioTenant/(?P<idTenant>[-\w]+)',
            views.superAdministradorCrearUsuarioTenant,
            name='superAdministradorCrearUsuarioTenant'),   
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorDetalleUsuarioTenant/(?P<idUsuario>[-\w]+)/(?P<idTenant>[-\w]+)$',
        views.superAdministradorDetalleUsuarioTenant,
        name='superAdministradorDetalleUsuarioTenant'),           
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorGps',
            views.superAdministradorGps,
            name='superAdministradorGps'), 
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorCrearGps$',
            views.superAdministradorCrearGps,
            name='superAdministradorCrearGps'),
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorDetalleGps/(?P<idGps>[-\w]+)',
            views.superAdministradorDetalleGps,
            name='superAdministradorDetalleGps'),
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorCrearVehiculoTenant/(?P<idTenant>[-\w]+)',
            views.superAdministradorCrearVehiculoTenant,
            name='superAdministradorCrearVehiculoTenant'),   
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/superAdministradorDetalleVehiculoTenant/(?P<idVehiculo>[-\w]+)/(?P<idTenant>[-\w]+)$',
        views.superAdministradorDetalleVehiculoTenant,
        name='superAdministradorDetalleVehiculoTenant'),
               
    #Reportes--------------------------------------------------------------                              
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminReportes$',
            views.adminReportes,
            name='adminReportes'),        
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminReporteParadasVehiculosZonas$',
            views.adminReporteParadasVehiculosZonas,
            name='adminReporteParadasVehiculosZonas'),  
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminReporteActividadVehiculos$',
            views.adminReporteActividadVehiculos,
            name='adminReporteActividadVehiculos'),         
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminReporteCalificacionConductores$',
            views.adminReporteCalificacionConductores,
            name='adminReporteCalificacionConductores'),     
               
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminReporteConduccionHorarioPermitido$',
            views.adminReporteConduccionHorarioPermitido,
            name='adminReporteConduccionHorarioPermitido'),    
                     
    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/adminReportesCadenaFrio$',
            views.adminReportesCadenaFrio,
            name='adminReportesCadenaFrio'),    


    url(r'^webfleetbigui/(?P<tenant>[-\w]+)/llamada/(?P<placa>[-\w]+)$',views.llamada, name='llamada'),

    url(r'^webfleetbigui/llamarGPS/$',views.llamarGPS, name='llamadarGPS'),

    #se puede borrar :D           
    url(r'^webfleetbigui/pruebaImagen$',      views.pruebaImagen,   name='pruebaImagen'),
    url(r'^enviarImagen$',                    views.enviarImagen,   name='enviarImagen'),

    
    #Mapa sin restricciones para visualizar la posicion de un vehiculo--------------------------------------
    url(r'^webfleetbigui/mapaVerPosicionLink/(?P<horaRegistrada>[-\:\.\w]+)/(?P<latitud>[-\:\.\w]+)/(?P<longitud>[-\:\.\w]+)$',
            views.mapaVerPosicionLink,
            name='mapaVerPosicionLink'),   
    
                          
]

