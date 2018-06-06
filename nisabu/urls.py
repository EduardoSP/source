from django.conf.urls   import  url
from nisabu import views

urlpatterns = [
    url(r'^image/(?P<imageId>[-\w\W]+)_thumbnail$',  views.getThumbnail,    name='thumbnail'),     #Obtiene la foto.
    url(r'^image/(?P<imageId>[-\w\W]+)_medianita$',  views.getMedianita,    name='medianita'),     #Obtiene la foto.
    url(r'^image/(?P<imageId>[-\w\W]+)_grandecita$',  views.getGrandecita,  name='grandecita'),     #Obtiene la foto.
    url(r'^image/(?P<imageId>[-\w\W]+)$',            views.getImage,        name='image'),     #Obtiene la foto.
    url(r'^saveImage$',                              views.saveImage,       name='saveImage'), #Guarda la foto en el servidor.
    url(r'^archivo/(?P<archivoId>[-\w\W]+)/(?P<archivoName>[-\w\W]+)$',            views.getArchivo,        name='archivo'),     #Obtiene la foto.

]
