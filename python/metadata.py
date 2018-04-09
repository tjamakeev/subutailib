class SourceType(object):
  CONTAINER, BLUEPRINT = range(2)

  def __init__(self, source):
    if source < 0 or source > 1:
      raise ValueError("Invalid event source.")
    self.value = source

  def __str__(self):
    if self.value == SourceType.CONTAINER:
      return "CONTAINER"
    else:
      return "BLUEPRINT"


class MetaData(object):
  CONTAINER = "CONTAINER"
  BLUEPRINT = "BLUEPRINT"

  def __init__(self, origin, source):
    if type(origin) != OriginMeta:
      raise ValueError("Invalid origin.")

    if type(source) != SourceMeta:
      raise ValueError("Invalid source.")
    self.origin = origin
    self.source = source
    self.items = []

  def add(self, name, value):
    self.items.append(CustomMeta(name,value))

class OriginMeta(object):

  def __init__(self, id):
    self.type = "origin"
    self.id = id

class SourceMeta(object):
  CONTAINER = SourceType(SourceType.CONTAINER)
  BLUEPRINT = SourceType(SourceType.BLUEPRINT)

  def __init__(self, Type, name):
    print type(Type)
    if type(Type) != SourceType:
      raise ValueError("Invalid source type.")
    self.type = "source"
    self.value = str(Type)
    self.name = name

class CustomMeta(object):
  def __init__(self,key,value):
    self.type = "custom"
    self.key = key
    self.value = value

