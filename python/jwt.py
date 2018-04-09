import base64, json

class JwtToken(object):
  def __init__(self, value):
    self.value = value
    self.parse()

  def parse(self):
    data = self.value.split(".")[1]
    self.data = base64.decodestring(data)
    self.payload = json.loads(self.data)
    self.subutaiId = self.payload["sub"]
    self.expire = self.payload["exp"]

  def __str__(self):
    return self.data
