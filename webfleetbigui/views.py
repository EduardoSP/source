# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http        import HttpResponse
from ws.nisabuUtils        import guardarImagen
from ws.serviciosweb.modulos.autenticacion import autenticacion
import logging
from django.conf              import settings
#from django.views.decorators.clickjacking import xframe_options_exempt

#@xframe_options_exempt
def login(request, tenant):
    context = { 
       "tenant" : tenant,
     }
    return render(request, 'webfleetbigui/login.html', context)

#@xframe_options_exempt
def loginUnificado(request):
    context = {        
     }
    return render(request, 'webfleetbigui/loginUnificado.html', context)

#@xframe_options_exempt
def loginGeneradorCarga(request):
    context = {        
     }
    return render(request, 'webfleetbigui/loginGeneradorCarga.html', context)

#@xframe_options_exempt
def codigosAccesoGenerador(request, tenant):
    context = { 
       "tenant" : tenant,
        "pintarPestana" : "pestanaGeneradorCodigosAcceso",        
     }
    return render(request, 'webfleetbigui/codigosAccesoGenerador.html', context)


#@xframe_options_exempt
def recuperarContrasena(request, tenant, token):
    estadoToken = autenticacion.getEstadoToken(tenant, token)
    context = {
        'usuario'  : estadoToken['usuario'],
        'esValido' : 'true' if estadoToken['esValido'] else 'false',
        'token'    : token,
        'tenant'   : tenant        
    }
    return render(request, 'webfleetbigui/recuperarContrasena.html', context)


#@xframe_options_exempt
def miCuenta(request, tenant):
    context = { 
       "tenant" : tenant,
       "baseTemplate"  : getBaseTemplate(tenant)
     }
    return render(request, 'webfleetbigui/miCuenta.html', context)

#@xframe_options_exempt
def miCuentaGeneradorCarga(request, tenant):
    context = { 
       "tenant" : tenant,
       "baseTemplate"  : getBaseTemplate(tenant)
     }
    return render(request, 'webfleetbigui/miCuentaGeneradorCarga.html', context)

#Administrador-------------------------------------------------------------- 
#@xframe_options_exempt
def adminVistaGeneral(request, tenant):
     context = { 
     	 "tenant" : tenant,
         "pintarPestana" : "pestanaAdminVistaGeneral",
         "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminVistaGeneral.html', context)

#@xframe_options_exempt
def adminVehiculos(request, tenant):
     context = { 
     	"tenant" : tenant,
        "pintarPestana"     : "pestanaAdminTransporte",
        "pintarSubPestana"  : "pestanaAdminVehiculos",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminVehiculos.html', context)

#@xframe_options_exempt
def adminDetalleVehiculo(request, tenant, idVehiculo, pestanaActivada):
    paquete = getPaqueteTenant(tenant) 
    context = { 
     	"tenant"            : tenant,
        "pestanaActivada"   : pestanaActivada,
        "idVehiculo"        : idVehiculo,
        "baseTemplate"      : getBaseTemplate(tenant),
        "paquete"           : paquete
    }
    return render(request, 'webfleetbigui/adminDetalleVehiculo.html', context)

#@xframe_options_exempt
def adminVigilancia(request, tenant):
     context = { 
        "tenant"            : tenant,
        "pintarPestana"     : "pestanaAdminVigilancia",
        "pintarSubPestana"  : "pestanaAdminVigilancia",
         "baseTemplate"     : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminVigilancia.html', context)

#@xframe_options_exempt
def adminVigilanciaCrearZona(request, tenant, latitud, longitud):
    paquete = getPaqueteTenant(tenant) 
    context = { 
        "tenant" : tenant,
        "latitud" : latitud,
        "longitud": longitud,
        "baseTemplate"  : getBaseTemplate(tenant),
        "paquete" : paquete
    }
    return render(request, 'webfleetbigui/adminVigilanciaCrearZona.html', context)

#@xframe_options_exempt
def adminDetalleZona(request, tenant, idZona):
    paquete = getPaqueteTenant(tenant) 
    context = { 
        "tenant" : tenant,
        "idZona" : idZona,
        "baseTemplate"  : getBaseTemplate(tenant),
        "paquete" : paquete
    }
    return render(request, 'webfleetbigui/adminDetalleZona.html', context)

#@xframe_options_exempt
def adminDetalleZonaAlarma(request, tenant, idZonaAlarma):
     context = { 
        "tenant" : tenant,
        "idZonaAlarma" : idZonaAlarma,
         "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminDetalleZonaAlarma.html', context)

#@xframe_options_exempt
def adminVigilanciaCrearProgramacion(request, tenant):
    paquete = getPaqueteTenant(tenant) 
    context = { 
        "tenant"        : tenant,
        "baseTemplate"  : getBaseTemplate(tenant),
        "paquete"       : paquete
    }
    return render(request, 'webfleetbigui/adminVigilanciaCrearProgramacion.html', context)

#@xframe_options_exempt
def adminDetalleProgramacionVigilancia(request, tenant, idProgramacion):
    paquete = getPaqueteTenant(tenant) 
    context = { 
        "tenant" : tenant,
        "idProgramacion" : idProgramacion,
        "baseTemplate"  : getBaseTemplate(tenant),
        "paquete" : paquete
    }
    return render(request, 'webfleetbigui/adminDetalleProgramacionVigilancia.html', context)
 
#@xframe_options_exempt
def adminAlarmas(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"  : "pestanaAdminAlarmas",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminAlarmas.html', context)
 

#@xframe_options_exempt
def adminSeguridadVial(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"     : "pestanaAdminVigilancia",
        "pintarSubPestana"  : "pestanaAdminSeguridadVial",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminSeguridadVial.html', context)
 
#@xframe_options_exempt
def adminGeneradorCodigo(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"  : "pestanaAdminGeneradoresDeCodigo",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminGeneradoresDeCodigo.html', context)


def adminCadenaFrio(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"  : "pestanaAdminCadenaFrio",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminCadenaFrio.html', context)

#@xframe_options_exempt
def adminCrearCodigoGeneradorCarga(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaAdminGeneradoresDeCodigo"
     }
     return render(request, 'webfleetbigui/adminCrearCodigoGeneradorCarga.html', context)     

# @xframe_options_exempt
# def adminGeneradoresDeCodigo(request, tenant):
#      context = { 
#         "tenant"         : tenant,
#         "pintarPestana"  : "pestanaAdminGeneradoresDeCodigo",
#         "baseTemplate"  : getBaseTemplate(tenant)
#      }
#      return render(request, 'webfleetbigui/adminGeneradoresDeCodigo.html', context)

 
#@xframe_options_exempt
def adminDetalleAlarmaPanico(request,tenant, idAlarmaPanico):
    paquete = getPaqueteTenant(tenant) 
    context = { 
        "tenant" : tenant,
        "idAlarmaPanico" : idAlarmaPanico,
        "baseTemplate"  : getBaseTemplate(tenant),
        "paquete" : paquete
    }
    return render(request, 'webfleetbigui/adminDetalleAlarmaPanico.html', context)


#@xframe_options_exempt
def llamada(request, tenant, placa):

    logging.warning(placa)
    palabra = ""
    for c in placa:
        logging.warning(c)
        #palabra += '</Say><Pause length="1" /><Say voice="alice" language="es-ES">{}'.format(letraVoz(c))
        palabra += u'</Say><Say voice="alice" language="es-ES">{}'.format(letraVoz(c))
    palabra += '</Say><Pause length="1" /><Say voice="alice" language="es-ES">'
    logging.warning(palabra)

    context = { 
        "tenant" : tenant, 
        "placa" : palabra
    }
    return render(request, 'webfleetbigui/llamada.xml', context)  

#@xframe_options_exempt def llamarGPS(request, tenant):
#@xframe_options_exempt
def llamarGPS(request):
    context = { 
        #"tenant" : tenant
    }
    return render(request, 'webfleetbigui/llamarGPS.xml', context)  


#@xframe_options_exempt
def letraVoz(letra):
    logging.warning(u"LEtravoz--{}--".format(letra))
    listado = {
        "a" : u"Alfa",
        "b" : u"Barco",
        "c" : u"Charli",
        "d" : u"Delta",
        "e" : u"Eco",
        "f" : u"Fócstrot",
        "g" : u"Golf",
        "h" : u"Hotel",
        "i" : u"Índia",
        "j" : u"Julia",
        "k" : u"kilo",
        "l" : u"Lima",
        "m" : u"Mamá",
        "n" : u"Noviembre",
        "ñ" : u"Ñoño",
        "o" : u"Óscar",
        "p" : u"Papá",
        "q" : u"Quebéc",
        "r" : u"Romeo",
        "s" : u"Sierra",
        "t" : u"Tango",
        "u" : u"Ultra",
        "v" : u"Victor",
        "w" : u"Whisky",
        "x" : u"Equis",
        "y" : u"Yanqui",
        "z" : u"Zulu",
        "1" : u"uno",
        "2" : u"dos",
        "3" : u"tres",
        "4" : u"cuatro",
        "5" : u"cinco",
        "6" : u"seis",
        "7" : u"siete",
        "8" : u"ocho",
        "9" : u"nueve",
        "0" : u"cero",
        " " : u" "
    }
    #logging.warning(listado[letra])
    palabras = listado.get(letra,"")
    return palabras

def adminConductores(request, tenant):
     context = { 
        "tenant" : tenant,
        "pintarPestana"     : "pestanaAdminTransporte",
        "pintarSubPestana"  : "pestanaAdminConductores",
         "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminConductores.html', context)

def adminCrearConductor(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaAdminConductores"
     }
     return render(request, 'webfleetbigui/adminCrearConductor.html', context)

def adminDetalleConductor(request, tenant, idConductor):
     context = { 
        "tenant"        : tenant,
        "idConductor"   : idConductor,  
        "pintarPestana" : "pestanaAdminConductores"
     }
     return render(request, 'webfleetbigui/adminDetalleConductor.html', context)

def adminRutas(request, tenant):
     context = { 
        "tenant" : tenant,
        "pintarPestana" : "pestanaAdminRutas",
        "pintarSubPestana"  : "pestanaAdminRutas",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminRutas.html', context)
     
def adminCrearRuta(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaAdminRutas",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminCrearRuta.html', context)
     
#@xframe_options_exempt
def adminEditarRuta(request, tenant, idRuta):
     context = { 
        "idRuta"        : idRuta,
        "tenant"        : tenant, 
        "pintarPestana" : "pestanaAdminRutas",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminEditarRuta.html', context)     
  
def adminListadoAsignacionesRutas(request, tenant):
     context = { 
        "tenant" : tenant,
        "pintarPestana" : "pestanaAdminRutas",
        "pintarSubPestana"  : "pestanaAdminAsignacionesRutas",
         "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminListadoAsignacionesRutas.html', context)

def adminDetalleAsignacionRuta(request, tenant, idAsignacionRuta, idRuta):
     context = { 
        "idAsignacionRuta"        : idAsignacionRuta,
        "idRuta"        : idRuta,
        "tenant" : tenant,
        "pintarPestana" : "pestanaAdminRutas",
        "pintarSubPestana"  : "pestanaAdminAsignacionesRutas",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     #return render(request, 'webfleetbigui/adminDetalleAsignacionRuta.htmlFABIO', context)
     return render(request, 'webfleetbigui/adminDetalleAsignacionRuta.html', context)


#@xframe_options_exempt
def adminConfiguracion(request, tenant):
     context = { 
     	 "tenant"        : tenant,
         "pintarPestana" : "",
         "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminConfiguracion.html', context)


#Super Administrador-------------------------------------------------------------- 

#@xframe_options_exempt
def superAdministradorTenants(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaSuperAdminTenants",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/superAdministradorTenants.html', context)
 
#@xframe_options_exempt
def superAdministradorCrearTenant(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaSuperAdminTenants"
     }

     return render(request, 'webfleetbigui/superAdministradorCrearTenant.html', context)
 
#@xframe_options_exempt
def superAdministradorDetalleTenant(request, tenant, idTenant):
     context = { 
        "tenant" : tenant,
        "idTenant" : idTenant,  
        "pintarPestana" : "pestanaSuperAdminTenants"
     }
     return render(request, 'webfleetbigui/superAdministradorDetalleTenant.html', context)  
 
#@xframe_options_exempt
def superAdministradorCrearUsuarioTenant(request, tenant, idTenant):
     context = { 
        "tenant" : tenant, 
        "idTenant" : idTenant,  
        "pintarPestana" : "pestanaSuperAdminTenants"
     }
     return render(request, 'webfleetbigui/superAdministradorCrearUsuarioTenant.html', context)
 

#@xframe_options_exempt
def superAdministradorDetalleUsuarioTenant(request, tenant, idUsuario, idTenant):
     context = { 
        "tenant" : tenant, 
        "idUsuario" : idUsuario,  
        "idTenant" : idTenant,  
        "pintarPestana" : "pestanaSuperAdminTenants"
     }
     return render(request, 'webfleetbigui/superAdministradorDetalleUsuarioTenant.html', context)
  
 
#@xframe_options_exempt
def superAdministradorGps(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaSuperAdminGps"
     }
     return render(request, 'webfleetbigui/superAdministradorGps.html', context)

#@xframe_options_exempt
def superAdministradorCrearGps(request, tenant):
     context = { 
        "tenant" : tenant, 
        "pintarPestana" : "pestanaSuperAdminGps"
     }
     return render(request, 'webfleetbigui/superAdministradorCrearGps.html', context)
 
#@xframe_options_exempt
def superAdministradorDetalleGps(request, tenant, idGps):
     context = { 
        "tenant" : tenant,
        "idGps" : idGps,  
        "pintarPestana" : "pestanaSuperAdminGps"
     }
     return render(request, 'webfleetbigui/superAdministradorDetalleGps.html', context)  

#@xframe_options_exempt
def superAdministradorCrearVehiculoTenant(request, tenant, idTenant):
     context = { 
        "tenant" : tenant, 
        "idTenant" : idTenant,  
        "pintarPestana" : "pestanaSuperAdminTenants"
     }
     return render(request, 'webfleetbigui/superAdministradorCrearVehiculoTenant.html', context)
 
 
#@xframe_options_exempt
def superAdministradorDetalleVehiculoTenant(request, tenant, idVehiculo, idTenant):
     context = { 
        "tenant"        : tenant, 
        "idVehiculo"    : idVehiculo,  
        "idTenant"      : idTenant,  
        "pintarPestana" : "pestanaSuperAdminTenants"
     }
     return render(request, 'webfleetbigui/superAdministradorDetalleVehiculoTenant.html', context)

#Reportes-------------------------------------------------------------- 
#@xframe_options_exempt
def adminReportes(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"  : "pestanaAdminReportes",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminReportes.html', context)


def adminReporteParadasVehiculosZonas(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"  : "pestanaAdminReportes",
        "pintarSubPestana"  : "pestanaAdminParadasVehiculos",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminReporteParadasVehiculosZonas.html', context)
 
 
def adminReporteActividadVehiculos(request, tenant):
     context = { 
        "tenant"         : tenant,
        "pintarPestana"  : "pestanaAdminReportes",
        "pintarSubPestana"  : "pestanaAdminActividadVehiculos",
        "baseTemplate"  : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminReporteActividadVehiculos.html', context) 
 
def adminReporteCalificacionConductores(request, tenant):
     context = { 
        "tenant"            : tenant,
        "pintarPestana"     : "pestanaAdminReportes",
        "pintarSubPestana"  : "pestanaAdminCalificacionConductores",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminReporteCalificacionConductores.html', context) 
 
def adminReporteConduccionHorarioPermitido(request, tenant):
     context = { 
        "tenant"            : tenant,
        "pintarPestana"     : "pestanaAdminReportes",
        "pintarSubPestana"  : "pestanaAdminConduccionHorarioPermitido",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminReporteConduccionHorarioPermitido.html', context) 


def adminReportesCadenaFrio(request, tenant):
     context = { 
        "tenant"            : tenant,
        "pintarPestana"     : "pestanaAdminReportes",
        "pintarSubPestana"  : "pestanaAdminReportesCadenaFrio",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminReportesCadenaFrio.html', context)

  
#se puede borrar era una prueba
#@xframe_options_exempt
def pruebaImagen(request):
    context = {
                "imagenLogo" : "images/fleetbi.png" }
    return render(request, 'webfleetbigui/pruebaImagen.html', context) 
 
#@xframe_options_exempt
def enviarImagen(request):
    logging.warning(request.POST['request'])
    archivo = request.FILES['archivo']
    logging.warning(archivo.name)
    identificador = guardarImagen(archivo)
    logging.warning(identificador)
    dataRaw = {"success" : True}
    data = json.dumps(dataRaw)
    return HttpResponse(data, content_type='application/json')
 

def getBaseTemplate(tenant):
    template = ""
    if tenant == settings.TENANT_ADMINISTRACION:
        template = "webfleetbigui/baseSuperAdministrador.html"
    elif tenant == settings.TENANT_GENERADOR_CARGA:
        template = "webfleetbigui/baseGeneradorCarga.html"
    else:
        template = "webfleetbigui/baseAdminTenant.html"
    return template    


def getPaqueteTenant(tenant):
    resultado = "basico"
    if tenant == "exxonmobil":
        #resultado =  "avanzado"
        resultado = "basico"
    elif tenant == "demouno":
        resultado = "basico"
    return resultado

# Tipo Zona ==================================================================== //

def adminCrearTipoZona(request, tenant):
     context = { 
        "tenant"            : tenant,
        "pintarPestana"     : "pestanaAdminVigilancia",
        "pintarSubPestana"  : "pestanaAdminTipoZona",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminCrearTipoZona.html', context)

def adminTipoZona(request, tenant):
     context = { 
        "tenant"            : tenant,
        "pintarPestana"     : "pestanaAdminVigilancia",
        "pintarSubPestana"  : "pestanaAdminTipoZona",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminTipoZona.html', context)     

def adminEditarTipoZona(request, tenant, idTipozona):
     context = { 
        "tenant"            : tenant,
        "idTipozona"        : idTipozona,
        "pintarPestana"     : "pestanaAdminVigilancia",
        "pintarSubPestana"  : "pestanaAdminTipoZona",
        "baseTemplate"      : getBaseTemplate(tenant)
     }
     return render(request, 'webfleetbigui/adminEditarTipoZona.html', context)       

#Mapa sin restricciones para visualizar la posicion de un vehiculo =====================================     

def mapaVerPosicionLink(request, horaRegistrada, latitud, longitud):
     context = { 
        "horaRegistrada"    : horaRegistrada,
        "latitud"           : latitud,
        "longitud"          : longitud

     }
     return render(request, 'webfleetbigui/mapaVerPosicionLink.html', context)