# -*- coding: utf-8 -*-
from twilio.rest import TwilioRestClient
from django.conf import settings

def crearLlamada(client, destino, origen):
    #call = client.calls.create(url="http://fleetbi.cloud/llamada.xml",
    call = client.calls.create(url="{}/webfleetbigui/llamarGPS/".format(settings.RUTA_BASE_FLEETBI),
        to=destino,
        from_= origen, record=True)
    return call.sid

def terminarLlamada(client, sid):
    call = client.calls.update(sid, status="completed")

#Obtiene la url del audio
def consultarUrlGrabacion(callSid, client):
    call = client.calls.get(callSid)
    accountSid = call.account_sid
    if len(call.recordings.list()) > 0:
        recording = call.recordings.list()[0]
        recording = client.recordings.get(sid = recording.sid)
        return "https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Recordings/{RecordingSid}".format(AccountSid = accountSid, RecordingSid = recording.sid)
    else:
        return ""
