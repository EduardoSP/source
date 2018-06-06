from django.conf.urls   import patterns, url
from nisabu import views

urlpatterns = patterns('',
    url(r'^image/(?P<imageId>[-\w\W]+)_thumbnail$',  views.getThumbnail,    name='thumbnail'),     #Obtiene la foto.
    url(r'^image/(?P<imageId>[-\w\W]+)_medianita$',  views.getMedianita,    name='medianita'),     #Obtiene la foto.
    url(r'^image/(?P<imageId>[-\w\W]+)_grandecita$',  views.getGrandecita,  name='grandecita'),     #Obtiene la foto.
    url(r'^image/(?P<imageId>[-\w\W]+)$',            views.getImage,        name='image'),     #Obtiene la foto.
    url(r'^saveImage$',                              views.saveImage,       name='saveImage'), #Guarda la foto en el servidor.




)
