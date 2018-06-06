# -*- coding: utf-8 -*-
from ..autenticacion import autenticacion

def validacionPermisos(permiso, peticion):

    autenticaData = peticion["autenticacion"]
    usuario       = autenticacion.getUsuario(autenticaData.get('usuario'), autenticaData.get('perfil'))
    if usuario == None:
        return {
            'success' : False,
            'errormsg' : u"Usuario no válido"
        }

    print u"El usuario es: {}".format(usuario)
    if permiso == "wslistarMapaVehiculos":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }    

    elif permiso == "wslistarVehiculos":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }     

    elif permiso == "wslistarConductores":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' } 
    
    elif permiso == "wslistarDetalleVehiculo":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wsvehiculoRangoFechaCapturaImagen":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
   
    elif permiso == "wsvehiculoRangoFechaCapturaAudio":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wsvehiculoRangoFechaAlarma":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsmonitoreoZonas":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wslistarVigilancias":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wscrearZonas":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wseliminarZonas":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wscrearProgramacion":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wsEliminarprogramacionVigilancia":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wsultimaPosicionVehiculo":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
            
    elif permiso == "wszonaAlarmas":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarDetalleZona":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarDetalleZonaAlarma":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
                
    elif permiso == "wslistarDetalleVehiculoZonaAlarma":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarCapturaAudiosZonaAlarma":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarProgramacionVigilancia":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistVehiculos":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarPosicionVehiculosVigilancia":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarDetalleVehiculoProgramacionVigilancia":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarImagenesProgramacionVigilancia":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wslistarAudiosProgramacionVigilancia":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsparadaPorRangoFecha":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wssolicitarCapturaImagen":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wslistadoGPS":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsregistrarPosicionesGPS":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wslistarParadaVehiculo":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wssolicitarCapturaAudio":
        if usuario.get('perfil')  == 'administradores':
            return { 'success' : True }
        else:
            return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsdetenerCapturaAudio":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsverificarEstadoLlamada":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wscrearConductor":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsEliminarConductor":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsDetalleConductor":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsEditarConductor":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsCargarArchivoCsvConductores":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsPickerConductores":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsAsignarConductor":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsVerificarConductorAsignado":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsReAsignarConductor":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsActualizarEstadoCarga":
                if usuario.get('perfil')  == 'administradores':
                    return { 'success' : True }
                else:
                    return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    #Permisos boton de panico------------------------------------------
    elif permiso == "wsregistrarBotonPanicoGPS":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wslistarDetalleAlarmaPanico":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }   
    elif permiso == "wslistarCapturaImagenesPanico":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    #Permisos para miCuenta --------------------------------            
    elif permiso == "wsdetalleClienteTenant":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' } 
                
    elif permiso == "wsactualizarDatosCuenta":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }                                                                

    elif permiso == "wsactualizarIngresoAlarmasUsuario":
            if usuario.get('perfil')  == 'administradores':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }                                                                

    #Permisos para SuperAdministradores --------------------------------
    elif permiso == "wsPickerTeants":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsCrearTenant":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    #------------------------------------------------------                                                                
    #Permisos para Rutas --------------------------------
    elif permiso == "wscrearRuta":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsListarRutas":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsBuscarDireccion":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsEliminarRuta":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsCrearPuntosControl":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsCrearPuntosVelocidad":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }
    elif permiso == "wsCrearPuntosInteres":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }



    
    elif permiso == "wsEditarRuta":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wsEditarPuntosCrontrolRuta":
            if usuario.get('perfil')  == 'superAdministrador':
                return { 'success' : True }
            else:
                return { 'success' : False , 'mensaje' : 'usuario no autorizado' }

    elif permiso == "wsEditarPuntosVelocidadRuta":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}

    elif permiso == "wsEditarPuntosInteresRuta":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}      

    elif permiso == "wsDetalleRuta":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'} 

    elif permiso == "wsDetallePuntoControlRuta":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}   

    elif permiso == "wsDetallePuntoVelocidadRuta":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'} 

    elif permiso == "wsDetallePuntoInteresRuta":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}   
    #perminos seguridad vial            
    elif permiso == "wsConsultarConduccionAgresiva":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}            
    elif permiso == "wsConsultarDetalleAceleracion":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}            
    elif permiso == "wsConsultarDetalleFrenadas":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}            
    elif permiso == "wsConsultarDetalleMovimientosAbruptos":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsConsultarDetalleExcesosVelocidad":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsConsultarEncendidoApagado":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsConsultarPausaActiva":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsConsultarConduccionContinua":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsRegistrarAceleracionVehiculoGPS":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsRegistrarFrenadasVehiculoGPS":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsRegistrarMovimientosAbruptosVehiculoGPS":
            if usuario.get('perfil') == 'superAdministrador':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}
    #permisos generadores de carga                                 
    elif permiso == "wsListarCodigosGenerados":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsConsultarDetalleVehiculosCodigoGenerado":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsAnularCodigoGenerado":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsGenerarCodigoAcceso":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsCrearCodigoAcceso":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsListarCodigosAgregados":
            if usuario.get('perfil') == 'generadoresCarga':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsAgregarCodigoAcceso":
            if usuario.get('perfil') == 'generadoresCarga':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsactualizarDatosCuentaGeneradorCarga":
            if usuario.get('perfil') == 'generadoresCarga':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsDetalleVehiculosTenant":
            if usuario.get('perfil') == 'generadoresCarga':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsOpcionesPlataformaTenant":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsValidarAudioImagenVehiculo":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsActivarPermisosPlataforma":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsDesactivarPermisosPlataforma":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsListarVehiculosCadenaFrio":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsActivarCadenaFrioVehiculos":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}                 
    elif permiso == "wsReportesCadenaFrio":
            if usuario.get('perfil') == 'administradores':
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'usuario no autorizado'}
    #------------------------------------------------------

    #------------------------------------------------------
    
    return {
        'success' : False,
        'errormsg' : u"No se encontró el permiso"
    }
    
