# coding: utf-8
from django.db import models
import uuid

#Constantes --------------------------------------------------------------------
ESTADOSUSUARIO= (
    ('activo',      'Activo'),
    ('inactivo',    'Inactivo'),
)


class Usuario(models.Model):
    usuario         = models.CharField(max_length=255)
    contrasena      = models.CharField(max_length=255) #MD5 con sal y limon
    estado          = models.CharField(max_length=100, choices=ESTADOSUSUARIO )
    creadoEn        = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.usuario

    class Meta:
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Autenticacion(models.Model):
    token       = models.CharField(max_length=255)
    usuario     = models.ForeignKey(Usuario)
    creadoEn    = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.token

    class Meta:
        verbose_name        = 'Autencación'
        verbose_name_plural = 'Autenticaciones'

