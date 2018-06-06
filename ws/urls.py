# -*- coding: utf-8 -*-
from django.conf.urls        import url
from ws.serviciosweb.modulos import wsautenticacion
from ws.serviciosweb.modulos import wscuentausuario
from ws.serviciosweb.modulos import wsvehiculos
from ws.serviciosweb.modulos import wsconductores
from ws.serviciosweb.modulos import wsalarmas
from ws.serviciosweb.modulos import wsvigilancias
from ws.serviciosweb.modulos import wsintegracionGPS
from ws.serviciosweb.modulos import wsregistrarBotonPanicoGPS
from ws.serviciosweb.modulos import wsTenants
from ws.serviciosweb.modulos import wsgps
from ws.serviciosweb.modulos import wsadministracion
from ws                      import nisabuUtils                      
from ws.serviciosweb.modulos import wsmicuenta
from ws.serviciosweb.modulos import wsreportes
from ws.serviciosweb.modulos import wsConfiguracion
from ws.serviciosweb.modulos import wsRutas
from ws.serviciosweb.modulos import wsAsignacionRutas
from ws.serviciosweb.modulos import wsSeguridadVial 
from ws.serviciosweb.modulos import wsSeguimientoAsignacionRutas
from ws.serviciosweb.modulos import wsGeocoder
from ws.serviciosweb.modulos import wsGeneradoresCarga
from ws.serviciosweb.modulos import wsCadenaFrio

urlpatterns = [ 
    
    #Autenticaciones -----------------------------------------------------------
    url(r'^autenticar$',                   wsautenticacion.wsAutenticar,                   name='wsautenticar'),
    url(r'^autenticarUnificado$',          wsautenticacion.wsAutenticarUnificado,          name='wsAutenticarUnificado'),
    url(r'^verificarCredenciales$',        wsautenticacion.wsVerificarCredenciales,        name='wsverificarcredenciales'),
    url(r'^recuperarContrasena$',          wsautenticacion.wsRecuperarContrasena,          name='wsRecuperarContrasena'),
    url(r'^recuperarContrasenaUnificado$', wsautenticacion.wsRecuperarContrasenaUnificado, name='wsRecuperarContrasenaUnificado'),
    url(r'^cambiarContrasena$',            wsautenticacion.wsCambiarContrasena,            name='wsCambiarContrasena'),
    url(r'^actualizarCerrarSesion$',       wsautenticacion.wsActualizarCerrarSesion,       name='wsActualizarCerrarSesion'),
 
    #Mi cuenta------------------------------------------------------------------
    url(r'^detalleClienteTenant$',  wsmicuenta.wsdetalleClienteTenant,  name='wsdetalleClienteTenant'),
    url(r'^actualizarDatosCuenta$', wsmicuenta.wsactualizarDatosCuenta, name='wsactualizarDatosCuenta'),

    #Configuración -------------------------------------------------------------
    url(r'^listarConfiguraciones$',   wsConfiguracion.wsListarConfiguraciones,   name='wsListarConfiguraciones'),
    url(r'^actualizarConfiguracion$', wsConfiguracion.wsActualizarConfiguracion, name='wsActualizarConfiguracion'),
    
    #Vehiculos -----------------------------------------------------------------
    url(r'^listadoMapaVehiculos$',            wsvehiculos.wslistarMapaVehiculos,             name='wslistarMapaVehiculos'),
    url(r'^listadoVehiculos$',                wsvehiculos.wslistarVehiculos,                 name='wslistarVehiculos'),
    url(r'^listadoParadaVehiculo$',           wsvehiculos.wslistarParadaVehiculo,            name='wslistarParadaVehiculo'),   	
    url(r'^listadoDetalleVehiculo$',          wsvehiculos.wslistarDetalleVehiculo,           name='wslistarDetalleVehiculo'),
    url(r'^posicionVehiculoRangoFecha$',      wsvehiculos.wsposicionVehiculoRangoFecha,      name='wsposicionVehiculoRangoFecha'),
    url(r'^vehiculoRangoFechaCapturaImagen$', wsvehiculos.wsvehiculoRangoFechaCapturaImagen, name='wsvehiculoRangoFechaCapturaImagen'),
    url(r'^vehiculoRangoFechaCapturaAudio$',  wsvehiculos.wsvehiculoRangoFechaCapturaAudio,  name='wsvehiculoRangoFechaCapturaAudio'),
    url(r'^vehiculoRangoFechaAlarma$',        wsvehiculos.wsvehiculoRangoFechaAlarma,        name='wsvehiculoRangoFechaAlarma'),
    url(r'^ultimaPosicionVehiculo$',          wsvehiculos.wsultimaPosicionVehiculo,          name='wsultimaPosicionVehiculo'),
    url(r'^listVehiculos$',                   wsvehiculos.wslistVehiculos,                   name='wslistVehiculos'),
    url(r'^solicitarCapturaAudio$',           wsvehiculos.wssolicitarCapturaAudio,           name='wssolicitarCapturaAudio'),
    url(r'^detenerCapturaAudio$',             wsvehiculos.wsdetenerCapturaAudio,             name='wsdetenerCapturaAudio'),
    url(r'^verificarEstadoLlamada$',          wsvehiculos.wsverificarEstadoLlamada,          name='wsverificarEstadoLlamada'),
    url(r'^buscarLlamadaActivaDirecta$',      wsvehiculos.wsbuscarLlamadaActivaDirecta,      name='wsbuscarLlamadaActivaDirecta'),
    url(r'^actualizarEstadoCarga$',           wsvehiculos.wsActualizarEstadoCarga,           name='wsActualizarEstadoCarga'),
        
    #Conductores -----------------------------------------------------------------
    url(r'^listadoConductores$', wsconductores.wslistarConductores, name='wslistarConductores'),
    url(r'^crearConductor$',     wsconductores.wscrearConductor,    name='wscrearConductor'),
    url(r'^eliminarConductor$',  wsconductores.wsEliminarConductor, name='wsEliminarConductor'),
    url(r'^detalleConductor$',   wsconductores.wsDetalleConductor,  name='wsDetalleConductor'),
    url(r'^editarConductor$',    wsconductores.wsEditarConductor,   name='wsEditarConductor'),

    url(r'^descargarArchivoCsvConductores/(?P<usuario>[-\w]+)/(?P<tenant>[-\w]+)$',
                                 wsconductores.wsDescargarArchivoCsvConductores,
                                                                    name='wsDescargarArchivoCsvConductores'),

    url(r'^cargarArchivoCsvConductores$', wsconductores.wsCargarArchivoCsvConductores, name='wsCargarArchivoCsvConductores'),        
    url(r'^pickerConductores$',           wsconductores.wsPickerConductores,           name='wsPickerConductores'),
    url(r'^asignarConductor$',            wsconductores.wsAsignarConductor,            name='wsAsignarConductor'),
    url(r'^verificarConductorAsignado$',  wsconductores.wsVerificarConductorAsignado,  name='wsVerificarConductorAsignado'),
    url(r'^reAsignarConductor$',          wsconductores.wsReAsignarConductor,          name='wsReAsignarConductor'),
    
    #Vigilancias -----------------------------------------------------------------    
    url(r'^monitoreoZonas$',                 wsvigilancias.wsmonitoreoZonas,                 name='wsmonitoreoZonas'),  
    url(r'^listarVigilancias$',              wsvigilancias.wslistarVigilancias,              name='wslistarVigilancias'),
    url(r'^crearZonas$',                     wsvigilancias.wscrearZonas,                     name='wscrearZonas'), 
    url(r'^eliminarZonas$',                  wsvigilancias.wseliminarZonas,                  name='wseliminarZonas'),
    url(r'^crearProgramacion$',              wsvigilancias.wscrearProgramacion,              name='wscrearProgramacion'),
    url(r'^listadoProgramacionVigilancia$',  wsvigilancias.wslistarProgramacionVigilancia,   name='wslistarProgramacionVigilancia'),
    url(r'^eliminarProgramacionVigilancia$', wsvigilancias.wsEliminarProgramacionVigilancia, name='wsEliminarProgramacionVigilancia'),
    url(r'^validarAudioImagenVehiculo$',     wsvigilancias.wsValidarAudioImagenVehiculo,     name='wsValidarAudioImagenVehiculo'), 
    #revisar
    url(r'^zonaAlarmas$',                    wsvigilancias.wszonaAlarmas,                    name='wszonaAlarmas'),
    #====
    url(r'^listadoDetalleZona$',                  wsvigilancias.wslistarDetalleZona,                  name='wslistarDetalleZona'),
    url(r'^editarZona$',                          wsvigilancias.wseditarZona,                         name='wseditarZona'), 
    url(r'^listadoDetalleZonaAlarma$',            wsvigilancias.wslistarDetalleZonaAlarma,            name='wslistarDetalleZonaAlarma'),
    url(r'^listadoDetalleVehiculoZonaAlarma$',    wsvigilancias.wslistarDetalleVehiculoZonaAlarma,    name='wslistarDetalleVehiculoZonaAlarma'),
    url(r'^listadoPosicionZonaAlarma$',           wsvigilancias.wslistarPosicionZonaAlarma,           name='wslistarPosicionZonaAlarma'),
    url(r'^listadoCapturaImagenesZonaAlarma$',    wsvigilancias.wslistarCapturaImagenesZonaAlarma,    name='wslistarCapturaImagenesZonaAlarma'),
    url(r'^listadoCapturaAudiosZonaAlarma$',      wsvigilancias.wslistarCapturaAudiosZonaAlarma,      name='wslistarCapturaAudiosZonaAlarma'),
    url(r'^crearProgramacionVigilancia$',         wsvigilancias.wscrearProgramacionVigilancia,        name='wscrearProgramacionVigilancia'),
    url(r'^listadoPosicionesVehiculoVigilancia$', wsvigilancias.wslistarPosicionesVehiculoVigilancia, name='wslistarPosicionesVehiculoVigilancia'),

    url(r'^listadoDetalleVehiculoProgramacionVigilancia$',
                                                  wsvigilancias.wslistarDetalleVehiculoProgramacionVigilancia,
                                                                                                      name='wslistarDetalleVehiculoProgramacionVigilancia'),
    url(r'^listadoImagenesProgramacionVigilancia$',
                                                  wsvigilancias.wslistarImagenesProgramacionVigilancia,
                                                                                                      name='wslistarImagenesProgramacionVigilancia'),
    url(r'^listadoAudiosProgramacionVigilancia$', wsvigilancias.wslistarAudiosProgramacionVigilancia, name='wslistarAudiosProgramacionVigilancia'),
    url(r'^listadoParadaPorRangoFecha$',          wsvigilancias.wsparadaPorRangoFecha,                name='wslistarParadaPorRangoFecha'),

    url(r'^crearTipoZona$',    wsvigilancias.wsCrearTipoZona,    name='wsCrearTipoZona'),
    url(r'^detalleTipoZona$',  wsvigilancias.wsDetalleTipoZona,  name='wsDetalleTipoZona'),
    url(r'^editarTipoZona$',   wsvigilancias.wsEditarTipoZona,   name='wsEditarTipoZona'),
    url(r'^listarTiposZonas$', wsvigilancias.wsListarTiposZonas, name='wsListarTiposZonas'),    
    url(r'^eliminarTipoZona$', wsvigilancias.wsEliminarTipoZona, name='wsEliminarTipoZona'),
    
    #Alarmas =============================================================
    url(r'^listadoAlarmas$',              wsalarmas.wslistarAlarmas,               name='wslistarAlarmas'),
    url(r'^listarUltimasAlarmas$',        wsalarmas.wsListarUltimasAlarmas,        name='wsListarUltimasAlarmas'),
    url(r'^listadoDetalleAlarmaPanico$',  wsalarmas.wslistarDetalleAlarmaPanico,   name='wslistarDetalleAlarmaPanico'),
    url(r'^listadoCapturaImagenesPanico$',wsalarmas.wslistarCapturaImagenesPanico, name='wslistarCapturaImagenesPanico'),   
    url(r'^listadoCapturaAudiosPanico$',  wsalarmas.wslistarCapturaAudiosPanico,   name='wslistarCapturaAudiosPanico'), 
    url(r'^listadoAlarmasPorVehiculo$',   wsalarmas.wslistarAlarmasPorVehiculo,    name='wslistarAlarmasPorVehiculo'),    

    #actualiza el ultimo ingreso de la alarma de un usuario
    url(r'^actualizarIngresoAlarmasUsuario$',  wsalarmas.wsactualizarIngresoAlarmasUsuario,           name='wsactualizarIngresoAlarmasUsuario'),    
    
    url(r'^wsmostrarAlarmasNoVistasUsuario$',  wsalarmas.wsmostrarAlarmasNoVistasUsuario    ,           name='wsmostrarAlarmasNoVistasUsuario'),   
    
    #  Urls integración GPS
    url(r'^listadoGPS$',             wsintegracionGPS.wslistadoGPS,             name='wslistadoGPS'),
    url(r'^solicitarCapturaImagen$', wsintegracionGPS.wssolicitarCapturaImagen, name='wssolicitarCapturaImagen'),
    url(r'^registrarPosicionesGPS$', wsintegracionGPS.wsregistrarPosicionesGPS, name='wsregistrarPosicionesGPS'),

    #Urls boton de panico
    url(r'^botonPanicoGPS$', wsregistrarBotonPanicoGPS.wsregistrarBotonPanicoGPS, name='wsregistrarBotonPanicoGPS'),

    # Urls SuperAdministracion TODO FABIO unificar estas interfaces con administracion
    url(r'^pickerTenants$',
        wsTenants.wsPickerTenants,
        name='wsPickerTenants'),

    #Clientes fleetbi -----------------------------------------------------------------
    url(r'^listadoTenants$',                wsadministracion.wslistadoTenants,             name='wslistarTenants'),
    url(r'^crearTenant$',                   wsadministracion.wsCrearTenant,                name='wsCrearTenant'),
    url(r'^detalleTenant$',                 wsadministracion.wsDetalleTenant,              name='wsDetalleTenant'),
    url(r'^editarTenant$',                  wsadministracion.wsEditarTenant,               name='wsEditarTenant'),
    url(r'^crearUsuarioAdminTenant$',       wsadministracion.wsCrearUsuarioAdminTenant,    name='wsCrearUsuarioAdminTenant'),
    url(r'^detalleUsuarioAdminTenant$',     wsadministracion.wsDetalleUsuarioAdminTenant,  name='wsDetalleUsuarioAdminTenant'),
    url(r'^editarUsuarioAdminTenant$',      wsadministracion.wsEditarUsuarioAdminTenant,   name='wsEditarUsuarioAdminTenant'),
    url(r'^eliminarUsuarioAdminTenant$',    wsadministracion.wsEliminarUsuarioAdminTenant, name='wsEliminarUsuarioAdminTenant'),
    url(r'^activarPermisosPlataforma$',     wsadministracion.wsActivarPermisosPlataforma,  name='wsActivarPermisosPlataforma'),
    url(r'^desactivarPermisosPlataforma$',  wsadministracion.wsDesactivarPermisosPlataforma,    name='wsDesactivarPermisosPlataforma'),

    #Gps fleetbi -----------------------------------------------------------------
    url(r'^listadoGps$',                    wsgps.wslistadoGps,                            name='wslistadoGps'),
    url(r'^crearGps$',                      wsgps.wsCrearGps,                              name='wsCrearGps'),
    url(r'^detalleGps$',                    wsgps.wsDetalleGps,                            name='wsDetalleGps'),
    url(r'^editarGps$',                     wsgps.wsEditarGps,                             name='wsEditarGps'),
    url(r'^pickerGps$',                     wsgps.wsPickerGps,                               name='wsPickerGps'),
    
    #Vehiculos fleetbi -----------------------------------------------------------------
    url(r'^crearVehiculoAdminTenant$',   wsvehiculos.wsCrearVehiculoAdminTenant,    name='wsCrearVehiculoAdminTenant'),
    url(r'^detalleVehiculoAdminTenant$', wsvehiculos.wsDetalleVehiculoAdminTenant,  name='wsDetalleVehiculoAdminTenant'),
    url(r'^editarVehiculoAdminTenant$',  wsvehiculos.wsEditarVehiculoAdminTenant,   name='wsEditarVehiculoAdminTenant'),
    url(r'^pickerVehiculos$',            wsvehiculos.wsPickerVehiculos,             name='wsPickerVehiculos'),

    url(r'^enviarImagen$',             nisabuUtils.guardarImagen,                   name='guardarImagen'),    
    url(r'^enviarArchivo$',            nisabuUtils.guardarArchivo,                  name='guardarArchivo'),
    
    #Rrportes fleetbi ------------------------------------------------------------------
    url(r'^reporteEstadisticasVehiculos$',          wsreportes.wsReporteEstadisticasVehiculos,          name='wsReporteEstadisticasVehiculos'),
    url(r'^reporteEstadisticasVehiculoPorDia$',     wsreportes.wsReporteEstadisticasVehiculoPorDia,     name='wsReporteEstadisticasVehiculoPorDia'),
    url(r'^reporteParadasVehiculo$',                wsreportes.wsReporteParadasVehiculo,                name='wsReporteParadasVehiculo'),
    url(r'^reporteGraficoVehiculosPorEstadistica$', wsreportes.wsReporteGraficoVehiculosPorEstadistica, name='wsReporteGraficoVehiculosPorEstadistica'),
    url(r'^reporteGraficoVehiculoEstadisticaPorFecha$', wsreportes.wsReporteGraficoVehiculoEstadisticaPorFecha, name='wsReporteGraficoVehiculoEstadisticaPorFecha'),
    url(r'^reporteParadasVehiculosEnZonas$',    wsreportes.wsReporteParadasVehiculosEnZonas,    name='wsReporteParadasVehiculosEnZonas'),
    url(r'^reporteMapaCalorActividadVehiculo$', wsreportes.wsReporteMapaCalorActividadVehiculo, name='wsReporteMapaCalorActividadVehiculo'),
    url(r'^reporteCalificacionConductores$',    wsreportes.wsReporteCalificacionConductores,    name='wsReporteCalificacionConductores'),
    url(r'^reporteConduccionPorFueraDeHorario$',    wsreportes.wsReporteConduccionPorFueraDeHorario,    name='wsReporteConduccionPorFueraDeHorario'),
    url(r'^reportesCadenaFrio$',    wsreportes.wsReportesCadenaFrio,    name='wsReportesCadenaFrio'),
    
    #Rutas -----------------------------------------------------------------
    url(r'^crearRuta$',                 wsRutas.wsCrearRuta,                name='wsCrearRuta'), 
    url(r'^editarRuta$',                wsRutas.wsEditarRuta,               name='wsEditarRuta'),
    url(r'^editarPuntoControlRuta$',    wsRutas.wsEditarPuntosCrontrolRuta, name='wsEditarPuntoControlRuta'),
    url(r'^editarPuntoVelocidadRuta$',  wsRutas.wsEditarPuntosVelocidadRuta,name='wsEditarPuntoVelocidadRuta'),
    url(r'^editarPuntoInteresRuta$',    wsRutas.wsEditarPuntosInteresRuta,  name='wsEditarPuntosInteresRuta'),
    url(r'^detalleRuta$',               wsRutas.wsDetalleRuta,              name='wsDetalleRuta'),
    url(r'^detallePuntoControlRuta$',   wsRutas.wsDetallePuntoControlRuta,  name='wsDetallePuntoControlRuta'),
    url(r'^detallePuntoVelocidadRuta$', wsRutas.wsDetallePuntoVelocidadRuta,name='wsDetallePuntoVelocidadRuta'),
    url(r'^detallePuntoInteresRuta$',   wsRutas.wsDetallePuntoInteresRuta,  name='wsDetallePuntoInteresRuta'),
    url(r'^listarRutas$',               wsRutas.wsListarRutas,              name='wsListarRutas'),
    url(r'^buscarDireccion$',           wsRutas.wsBuscarDireccion,          name='wsBuscarDireccion'),
    url(r'^eliminarRuta$',              wsRutas.wsEliminarRuta,             name='wsEliminarRuta'),
    url(r'^crearPuntosControl$',        wsRutas.wsCrearPuntosControl,       name='wsCrearPuntosControl'),
    url(r'^crearPuntosVelocidad$',      wsRutas.wsCrearPuntosVelocidad,     name='wsCrearPuntosVelocidad'),
    url(r'^crearPuntosInteres$',        wsRutas.wsCrearPuntosInteres,       name='wsCrearPuntosInteres'),
    url(r'^pickerRutas$',               wsRutas.wsPickerRutas,              name='wsPickerRutas'),
    
    #Asignación de rutas -------------------------------------------------------
    url(r'^listarAsignacionesRutas$', wsAsignacionRutas.wsListarAsignacionesRutas, name='wsListarAsignacionesRutas'),
    url(r'^crearAsignacionRuta$',     wsAsignacionRutas.wsCrearAsignacionRuta,     name='wsCrearAsignacionRuta'),
    url(r'^detalleAsignacionRuta$',   wsAsignacionRutas.wsDetalleAsignacionRuta,   name='wsDetalleAsignacionRuta'),
    url(r'^editarAsignacionRuta$',    wsAsignacionRutas.wsEditarAsignacionRuta,    name='wsEditarAsignacionRuta'),
    url(r'^eliminarAsignacionRuta$',  wsAsignacionRutas.wsEliminarAsignacionRuta,  name='wsEliminarAsignacionRuta'),
    url(r'^abortarAsignacionRuta$',   wsAsignacionRutas.wsAbortarAsignacionRuta,   name='wsAbortarAsignacionRuta'),
    url(r'^detalleSeguimientoAsignacionRuta$',
                                      wsSeguimientoAsignacionRutas.wsDetalleSeguimientoAsignacionRuta,
                                                                                   name='wsDetalleSeguimientoAsignacionRuta'),
    #Tipo Zona -----------------------------------------------------------------
    #url(r'^crearTipoZona$',             wsTipoZona.wsCrearTipoZona,         name='wsCrearTipoZona'),

    #Seguridad Vial -------------------------------------------------------
    url(r'^consultarConduccionAgresiva$', wsSeguridadVial.wsConsultarConduccionAgresiva, name='wsConsultarConduccionAgresiva'),
    url(r'^consultarDetalleAceleracion$', wsSeguridadVial.wsConsultarDetalleAceleracion, name='wsConsultarDetalleAceleracion'),
    url(r'^consultarDetalleFrenadas$', wsSeguridadVial.wsConsultarDetalleFrenadas, name='wsConsultarDetalleFrenadas'),
    url(r'^consultarMovimientosAbruptos$', wsSeguridadVial.wsConsultarDetalleMovimientosAbruptos, name='wsConsultarDetalleMovimientosAbruptos'),
    url(r'^consultarDetalleExcesosVelocidad$', wsSeguridadVial.wsConsultarDetalleExcesosVelocidad, name='wsConsultarDetalleExcesosVelocidad'),
    url(r'^consultarEncendidoApagado$', wsSeguridadVial.wsConsultarEncendidoApagado, name='wsConsultarEncendidoApagado'),
    url(r'^consultarPausaActiva$', wsSeguridadVial.wsConsultarPausaActiva, name='wsConsultarPausaActiva'),
    url(r'^consultarConduccionContinua$', wsSeguridadVial.wsConsultarConduccionContinua, name='wsConsultarConduccionContinua'),

    url(r'^registrarAceleracionVehiculoGPS$', wsSeguridadVial.wsRegistrarAceleracionVehiculoGPS, name='wsRegistrarAceleracionVehiculoGPS'),
    url(r'^registrarFrenadasVehiculoGPS$', wsSeguridadVial.wsRegistrarFrenadasVehiculoGPS, name='wsRegistrarFrenadasVehiculoGPS'),
    url(r'^registrarMovimientosAbruptosVehiculoGPS$', wsSeguridadVial.wsRegistrarMovimientosAbruptosVehiculoGPS, name='wsRegistrarMovimientosAbruptosVehiculoGPS'),

    #Geocoder -----------------------------------------------------------------
    url(r'^buscarPuntosReferencias$', wsGeocoder.wsBuscarPuntosReferencias, name='wsBuscarPuntosReferencias'),

    #Generadores de código -------------------------------------------------------
    url(r'^listarCodigosGenerados$', wsGeneradoresCarga.wsListarCodigosGenerados, name='wsListarCodigosGenerados'),
    url(r'^consultarDetalleVehiculosCodigoGenerado$', wsGeneradoresCarga.wsConsultarDetalleVehiculosCodigoGenerado, name='wsConsultarDetalleVehiculosCodigoGenerado'),
    url(r'^anularCodigoGenerado$', wsGeneradoresCarga.wsAnularCodigoGenerado, name='wsAnularCodigoGenerado'),
    url(r'^generarCodigoAcceso$', wsGeneradoresCarga.wsGenerarCodigoAcceso, name='wsGenerarCodigoAcceso'),
    url(r'^crearCodigoAcceso$', wsGeneradoresCarga.wsCrearCodigoAcceso, name='wsCrearCodigoAcceso'),
    url(r'^autenticarGeneradorCarga$', wsGeneradoresCarga.wsAutenticarGeneradorCarga, name='wsAutenticarGeneradorCarga'),
    url(r'^autenticarGeneradorCargaLogin$', wsGeneradoresCarga.wsAutenticarGeneradorCargaLogin, name='wsAutenticarGeneradorCargaLogin'),
    url(r'^recuperarContrasenaGeneradorCarga$', wsGeneradoresCarga.wsRecuperarContrasenaGeneradorCarga, name='wsRecuperarContrasenaGeneradorCarga'),
    url(r'^listarCodigosAgregados$', wsGeneradoresCarga.wsListarCodigosAgregados, name='wsListarCodigosAgregados'),
    url(r'^agregarCodigoAcceso$', wsGeneradoresCarga.wsAgregarCodigoAcceso, name='wsAgregarCodigoAcceso'),
    url(r'^actualizarDatosCuentaGeneradorCarga$', wsGeneradoresCarga.wsActualizarDatosCuentaGeneradorCarga, name='wsActualizarDatosCuentaGeneradorCarga'),
    url(r'^clientesCodGenerados$', wsGeneradoresCarga.wsClientesCodGenerados, name='wsClientesCodGenerados'),

    #Cadena de frio --------------------------------------------------------------
    url(r'^listadoAlarmasCadenaFrio$',    wsCadenaFrio.wsListadoAlarmasCadenaFrio,    name='wsListadoAlarmasCadenaFrio'),
    url(r'^listadoPuntosCadenaFrio$',     wsCadenaFrio.wsListadoPuntosCadenaFrio,     name='wsListadoPuntosCadenaFrio'),
    url(r'^actualizarAlarmaCadenaFrio$',  wsCadenaFrio.wsActualizarAlarmaCadenaFrio,  name='wsActualizarAlarmaCadenaFrio'),
    url(r'^listadoVehiculosCadenaFrio$',  wsCadenaFrio.wsListadoVehiculosCadenaFrio,  name='wsListadoVehiculosCadenaFrio'),
    url(r'^reporteTemperaturaVehiculos$', wsCadenaFrio.wsReporteTemperaturaVehiculos, name='wsReporteTemperaturaVehiculos'),
    url(r'^listarVehiculosCadenaFrio$',   wsCadenaFrio.wsListarVehiculosCadenaFrio, name='wsListarVehiculosCadenaFrio'),
    url(r'^activarDesactivarCadenaFrioVehiculos$',  wsCadenaFrio.wsActivarDesactivarCadenaFrioVehiculos, name='wsActivarDesactivarCadenaFrioVehiculos'),

]
