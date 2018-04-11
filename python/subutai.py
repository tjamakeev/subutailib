#!/usr/bin/python
import httplib, json, urllib, socket, sys, datetime
from payload import ProgressPayload, LogPayload, LogLevel, CustomPayload
from metadata import MetaData, SourceMeta, OriginMeta
from event import Event
from jwt import JwtToken
import argparse

class Subutai(object):
  def getconnection(self):
    return httplib.HTTPConnection("10.10.10.1:8080")

  def requesttoken(self):
    conn = self.getconnection()
    ip = self.getip()
    conn.request("GET","/rest/v1/metadata/token/"+ip)
    response = conn.getresponse()
    conn.close()
    return response

  def readJwtToken(self):
    try:
      with open("/etc/subutai/jwttoken", "r") as tokenFile:
        return JwtToken(tokenFile.read().replace("\n",""))
    except:
      return None

  def getJwtToken(self):
    token = self.readJwtToken()

    if token == None:
      self.requesttoken()
      print("There is no JWT token at all. Token requested. Please run this script again.")
      sys.exit()

    n = datetime.datetime.now()

    exp = datetime.datetime.fromtimestamp(token.expire)

    if (exp-n).total_seconds() < 100:
      self.requesttoken()
      print "JWT token expired. Token requested. Please run this script again."
      sys.exit()

    return self.readJwtToken()

  def getip(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.10.10.1', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

  def sendevent(self, event):
    jwtToken = self.getJwtToken()
    conn = self.getconnection()
    headers = {"Content-type": "application/json", "Authorization": "Bearer "+ jwtToken.value}
    params = json.dumps(event, default=jsonDefault)
    conn.request("POST", "/rest/v1/metadata/event", params, headers=headers)
    response = conn.getresponse()
    conn.close()
    return response

  def newMetadata(self, sourceType, sourceName):
    jwtToken = self.getJwtToken()
    parts = list(jwtToken.subutaiId.split("."))
    return MetaData(OriginMeta(parts[0], parts[1], parts[2]),SourceMeta(sourceType, sourceName))

def jsonDefault(object):
    return object.__dict__

def sendTestEvents():
  subutai = Subutai()
  sourceName = "my-cool-cassandra-script"
  metadata = subutai.newMetadata(SourceMeta.BLUEPRINT, sourceName)
  metadata.add("OS", "debian")
  payload = ProgressPayload("Initial step", "Script started...", 10.0)

  progressevent= Event(metadata, payload)
  print(json.dumps(progressevent, default=jsonDefault))
  r = subutai.sendevent(progressevent)
  print(r.status)
  print(r.read())

  metadata.add("now", str(datetime.datetime.now()))
  logevent = Event(metadata,LogPayload(LogPayload.TRACE, "source","trace info"))
  print(json.dumps(logevent, default=jsonDefault))
  r = subutai.sendevent(logevent)
  print(r.status)
  print(r.read())

  metadata.add("now", str(datetime.datetime.now()))
  customevent = Event(metadata,CustomPayload("custom payload"))
  print(json.dumps(logevent, default=jsonDefault))
  r = subutai.sendevent(customevent)
  print(r.status)
  print(r.read())

def sendProgressEvent(step, message, value):
  subutai = Subutai()
  sourceName = "MY-BLUEPRINT"
  metadata = subutai.newMetadata(SourceMeta.BLUEPRINT, sourceName)
  payload = ProgressPayload(step,message, value)

  progressevent= Event(metadata, payload)
  print(json.dumps(progressevent, default=jsonDefault))
  r = subutai.sendevent(progressevent)
  print(r.status)
  print(r.read())

if __name__ == "__main__":
  # sendTestEvents()
  parser = argparse.ArgumentParser()
  parser.add_argument("step")

  parser.add_argument("message")

  parser.add_argument("value")
  args = parser.parse_args()

  sendProgressEvent(args.step, args.message,args.value)
