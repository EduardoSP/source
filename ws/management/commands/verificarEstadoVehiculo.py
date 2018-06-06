from django.core.management.base import NoArgsCommand
from django.conf              import settings
from ws.serviciosweb.modulos.conexion import conexion
from datetime                 import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
#Verifica si esta activo o inactivo un vehiculo: por un tiempo definido
#si ha pasado mucho tiempo en reportar el dispositivo GPS 
# -*- encoding: utf-8 -*- 
#==========================================================================
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
      tenants = buscarTenants()
      for tenant in tenants:
        verificarEstadoVehiculo(tenant)


def verificarEstadoVehiculo(tenant):
  db = conexion.getConexionTenant(tenant)
  if db == None:
    print "No existe bd"
  try:
    filas = db.view('_design/posicionVehiculos/_view/ultimaPosicionGuardada',
                include_docs  = True,
                startkey      = [True, 0],
                endKey = [True, {}])
    print len(filas)
    for fila in filas:
        key                 = fila.key
        value               = fila.value
        doc                 = fila.doc
        horaRegistrada      = doc.get('horaRegistrada')
        horaAdecuada        = validarHoras(horaRegistrada)
        if not(horaAdecuada):
          #doc["estado"] = "inactivo"
          db.save(doc)
  except ValueError:
    print "error"

def validarHoras(horaRegistrada):
  respuesta       = True
  fechaHoraActual = datetime.now()
  horaReg         = datetime.strptime(horaRegistrada, '%Y-%m-%dT%H:%M:%S')
  restaHoras      = fechaHoraActual - horaReg
  segundosDefecto = settings.TIEMPO_MININO_DATOS_GPS * 60
  if restaHoras.seconds > segundosDefecto:
    respuesta     = False
  return respuesta
  

def buscarTenants():
  #funcion que busca los tenants en la bd fleetbi
  dbFleet = conexion.getConexionFleet()
  listaTenants = []
  if dbFleet == None:
    return { 'success' : False, 'mensaje': "existe el bd" }
  try:
    dataRaw = {}
    filas = dbFleet.view('_design/tenant/_view/visualizarTenants',
              include_docs  = True)
    for fila in filas:
      key           = fila.key
      value           = fila.value
      doc           = fila.doc
      urlTenant         = doc.get('urlTenant')    
      listaTenants.append(urlTenant)
    return listaTenants
  except ValueError:
    pass
