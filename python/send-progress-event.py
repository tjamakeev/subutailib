#!/usr/bin/python
import httplib, json, urllib
from progresspayload import ProgressPayload
from progressevent import ProgressEvent

def getconnection():
  return httplib.HTTPConnection("10.10.10.1:8080")
  
def gettoken(ip):
  conn = getconnection()
  conn.request("GET","/rest/v1/metadata/token/"+ip)
  response = conn.getresponse()
  conn.close()
  return response
  
def readtoken():
  with open("/etc/subutai/jwttoken", "r") as tokenFile:
    return tokenFile.read().replace("\n","")

def getip():
  return "172.20.71.2"

def sendevent(event):
  conn = getconnection()
  headers = {"Content-type": "application/json", "Authorization": "Bearer "+ readtoken()}
  params = json.dumps(event, default=jsonDefault)
  print(params)
  conn.request("POST", "/rest/v1/metadata/event", params, headers=headers)
  response = conn.getresponse()
  conn.close()
  return response

def jsonDefault(object):
  return object.__dict__

r = gettoken(getip())

if r.status == 204:
  payload = ProgressPayload("Initial step", "Script started...", 10.0)

  print(json.dumps(payload.__dict__))

  progressevent= ProgressEvent(payload, "BLUEPRINT")
  print(json.dumps(progressevent, default=jsonDefault))
  r = sendevent(progressevent)
  print(r.status)
else:
  print("Error on requiesting JWT tokein:"+ r.reason)

