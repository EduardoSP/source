from django.core.management.base import NoArgsCommand
from django.conf              import settings
from ws.serviciosweb.modulos.conexion import conexion
from datetime                 import datetime
from ws.serviciosweb.modulos.autenticacion import autenticacion as moduloAutenticacion
#from ws.serviciosweb.conexion import conexion

class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        db = conexion.getConexionFleet()
        filas = db.view('_design/inspeccionGPS/_view/inspeccionImagen',
                    include_docs  = True)
        for fila in filas:
          key = fila.key
          value = fila.value
          doc = fila.doc
          print key
          db.delete(doc)


