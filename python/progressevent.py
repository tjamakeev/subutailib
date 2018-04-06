class ProgressEvent:
  def __init__(self, payload, source):
    self.type="progress"
    self.payload = payload
    self.source = source
    self.timestamp = 0

  def jsonDefault(object):
    return object.__dict__


