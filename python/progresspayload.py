class ProgressPayload(object):
  def __init__(self, step, message, value):
    self.type="progress"
    self.step = step
    self.message = message
    self.value = value
