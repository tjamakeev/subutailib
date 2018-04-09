class MetaData(object):
  CONTAINER = "CONTAINER"
  BLUEPRINT = "BLUEPRINT"

  def __init__(self, originId, sourceType, sourceName ):
    self.origin = OriginMeta(originId)
    self.source = SourceMeta(sourceType, sourceName)
    self.items = []

  def add(self, name, value):
    self.items.append(CustomMeta(name,value))

class OriginMeta(object):

  def __init__(self, id):
    self.type = "origin"
    self.id = id

class SourceMeta(object):
  def __init__(self, type, name):
    self.type = "source"
    self.value = type
    self.name = name

class CustomMeta(object):
  def __init__(self,key,value):
    self.type = "custom"
    self.key = key
    self.value = value