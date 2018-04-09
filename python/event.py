import time

class Event:
  def __init__(self, meta, payload):
    self.payload = payload
    self.metaData = meta
    self.timestamp = int(round(time.time() * 1000))

  def jsonDefault(object):
    return object.__dict__


