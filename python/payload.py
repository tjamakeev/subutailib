class ProgressPayload(object):
  def __init__(self, step, message, value):
    self.type="progress"
    self.step = step
    self.message = message
    self.value = value

class LogLevel(object):
    TRACE, DEBUG, INFO, WARN, ERROR, FATAL = range(6)
    def __init__(self, Type):
        self.value = Type

    def __str__(self):
      if self.value == LogLevel.TRACE:
        return 'TRACE'
      if self.value == LogLevel.DEBUG:
        return 'DEBUG'
      if self.value == LogLevel.INFO:
        return 'INFO'
      if self.value == LogLevel.WARN:
        return 'WARN'
      if self.value == LogLevel.ERROR:
        return 'ERROR'
      if self.value == LogLevel.FATAL:
        return 'FATAL'

    def __eq__(self,y):
       return self.value==y.value

class LogPayload(object):
  TRACE = LogLevel(LogLevel.TRACE)
  DEBUG = LogLevel(LogLevel.DEBUG)
  INFO = LogLevel(LogLevel.INFO)
  WARN = LogLevel(LogLevel.WARN)
  ERROR = LogLevel(LogLevel.ERROR)
  FATAL = LogLevel(LogLevel.FATAL)

  def __init__(self, level, source,  message):
    self.type="log"
    if type(level) != LogLevel:
	raise ValueError('Invalid log level.')    
    self.level = str(level)
    self.source = source
    self.message = message

class CustomPayload(object):
  def __init__(self, key, value):
    self.type="custom"
    self.key = key
    self.value = value
