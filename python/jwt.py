import base64, json

class JwtToken(object):
  def __init__(self, value):
    self.value = value
    self.parse()

  def parse(self):
    print(self.value)
    data = self.value.split(".")[1]
    payload = json.loads(base64.decodestring(data))
    self.subutaiId = payload["sub"]

