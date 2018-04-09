#!/usr/bin/python
import httplib, json, urllib
from payload import ProgressPayload, LogPayload, LogLevel
from metadata import MetaData
from event import Event
from jwt import JwtToken

def getconnection():
  return httplib.HTTPConnection("10.10.10.1:8080")

def gettoken(ip):
  conn = getconnection()
  conn.request("GET","/rest/v1/metadata/token/"+ip)
  response = conn.getresponse()
  conn.close()
  return response
  
def readJwtToken():
  with open("/etc/subutai/jwttoken", "r") as tokenFile:
    return JwtToken(tokenFile.read().replace("\n",""))

def getip():
  return "172.20.71.2"

def sendevent(jwtToken, event):
  conn = getconnection()
  headers = {"Content-type": "application/json", "Authorization": "Bearer "+ jwtToken}
  params = json.dumps(event, default=jsonDefault)
  conn.request("POST", "/rest/v1/metadata/event", params, headers=headers)
  response = conn.getresponse()
  conn.close()
  return response

def jsonDefault(object):
  return object.__dict__

r = gettoken(getip())

if r.status == 204:
  jwtToken = readJwtToken()
  origin = jwtToken.subutaiId
  sourceType = MetaData.BLUEPRINT
  sourceName = "my-cool-cassandra-script"
  metadata = MetaData(origin, sourceType, sourceName)
  metadata.add("OS", "debian")
  payload = ProgressPayload("Initial step", "Script started...", 10.0)

  progressevent= Event(metadata, payload)
  print(json.dumps(progressevent, default=jsonDefault))
  r = sendevent(jwtToken.value, progressevent)
  print(r.status)
  print(r.read())
  logevent = Event(metadata,LogPayload("LogPayload.TRACE", "source","trace info"))
  print(json.dumps(logevent, default=jsonDefault))
  r = sendevent(jwtToken.value, logevent)
  print(r.status)
  print(r.read())
else:
  print("Error on requiesting JWT tokein:"+ r.reason)

