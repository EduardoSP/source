# -*- coding: utf-8 -*-
"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import pytz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '88uya2v@1h7=%5l^gkc7j7q!$3rlab48g68^@t71ptk3mapj^x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'webfleetbigui',
    'ws',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

#      'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     #'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),        
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL  = '/static/'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = '/Users/leilly/Documents/imagenes'

# Configuracion general: ---------------------------------------
BASE_URL            = 'http://localhost'
COUCHDB_URL         = 'http://localhost:3000'
BASEDB              = 'fleetbi'

CERTIOSPUSHJEFEDEV = "/Users/fasozu/irengines/proyectos/emergencia/src/ambulanciasWebAdmin/llaves/apns-dev-jefe.pem"
CERTIOSPUSHJEFE = "/Users/fasozu/irengines/proyectos/emergencia/src/ambulanciasWebAdmin/llaves/apns-jefe.pem"

CERTIOSPUSHDEV = "/Users/fasozu/irengines/proyectos/emergencia/src/ambulanciasWebAdmin/llaves/apns-dev.pem"
CERTIOSPUSH = "/Users/fasozu/irengines/proyectos/emergencia/src/ambulanciasWebAdmin/llaves/apns.pem"

SENDFILE_BACKEND    = 'sendfile.backends.development'
NISABU_CACHE_DIR    = '/var/www/fleetbi/fleet2/Fleetbiweb/nodeServiceGPS/gpsserver/nodejs-meiligao-master/examples/fotos/fotosNisabu'
NISABU_IMAGE_URL    = 'http://54.243.219.114:56899/nisabu/image/'

TWILIO_TIEMPO_LLAMADA   = 10 #valor donde se especifica el tiempo de la llamada
TWILIO_NUMERO     = "+573233636572" #Numero registrado para la aplicacion FLEET
TWILIO_ACCOUNT_SID = "ACcd85262f050496f5d315d26714d64e55" # se configura decauerdo a la cuenta
TWILIO_AUTH_TOKEN  = "9bfd538741cd20925d23447302ff1c48"#se configura decauerdo a la cuenta

GPS_RUTA_FOTO      = "/var/www/fleetbi/fleet2/Fleetbiweb/nodeServiceGPS/gpsserver/nodejs-meiligao-master/examples/fotos/"

# cada 30 minutos por defecto va a ser el tiempo minimo que transmite datos el GPS 
TIEMPO_MININO_DATOS_GPS = 30    

EST = pytz.timezone('America/Bogota')

#funcion solicitarTomarFoto de integracionGPS.py
URL_SOLICITAR_FOTO  = "http://localhost:5006/ws/solicitarTomarFoto"

# funcion leerArchivoJpg examinarImagenesPendientes.py
RUTA_ARCHIVO_JPG   = "/var/www/fleetbi/fleet2/Fleetbiweb/nodeServiceGPS/gpsserver/nodejs-meiligao-master/examples/fotos/{}.jpg" 

RUTA_ARCHIVO_JSON   = "/var/www/fleetbi/fleet2/Fleetbiweb/nodeServiceGPS/gpsserver/nodejs-meiligao-master/examples/fotos/{}.json" 

# funcion guardarDocumentoCapturaImagenes de archivo examinarImagenes.py
RUTA_ARCHIVO_NISABU = "http://54.243.219.114:56899/nisabu/image/{}"

