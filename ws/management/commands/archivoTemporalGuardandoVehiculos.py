from django.core.management.base import NoArgsCommand
from django.conf              import settings
from ws.serviciosweb.modulos.conexion import conexion
from datetime                 import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
from twilio.rest import TwilioRestClient
import time
# -*- encoding: utf-8 -*- 
#==========================================================================
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
    	#Nota: No se ha hecho una prueba con una llamada Real
		#Buscar documento colgar 
    	#llamada si se encuentran las llamadas en curso
    	#Extraer el limite y el campo creadoEn del doc llamadas
    	# el limite debe estar en minutos
		tenants = buscarTenants()
		for tenant in tenants:
			colgarLlamadaEnCurso(tenant)


