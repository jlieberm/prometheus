

__init__ = ["ToolSvc", "ToolMgr"]

from Gaudi.messenger import Logger
from Gaugi.messenger.macros import *

class Service( Logger ):

  def __init__(self, name):
    Logger.__init__(self)
    import collections
    self._name = name
    self._tools = collections.OrderedDict()
    MSG_INFO("Creating %s as Service...", name)

  def get(self, name):
    return self._tools[name]

  def put(self, tool):
    self._tools[ tool.name() ] =  tool


  def disable(self):
    for name, tool in self._tools.iteritems():
      MSG_DEBUG( self, "Disable %s tool", name)
      tool.disable()

  def enable(self):
    for name, tool in self._tools.iteritems():
      MSG_DEBUG( self, "Enable %s tool", name)
      tool.enable()

  def __iter__(self):
    for name, tool in self._tools.iteritems():
      yield tool 

  def __add__(self, tool):
    self._tools[ tool.name() ] =  tool

  def clear(self):
    self._tools.clear()

  def resume(self):
    MSG_INFO( self, "Service: %s", self.name())
    for name, tool in self._tools.iteritems():
      MSG_INFO( self, " * %s as tool", tool.name())
    

# Use this to attach all tools 
ToolSvc = Service("ToolSvc")

# Use this to attach all event loop manager
ToolMgr = Service("ToolMgr")


