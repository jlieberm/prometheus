
__all__ = ['EmulationTool']


from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi.messenger.macros import *
from prometheus import Dataframe as DataframeEnum


class EmulationTool( Algorithm ):


  def __init__(self):
    Algorithm.__init__(self, "Emulator")
    self._selector = {}


  def __add__( self, tool ):
    self._selector[tool.name()] = tool
    return self


  def initialize(self):

    for key, tool in self._selector.items():
      MSG_INFO( self, 'Initializing %s tool',key)
      tool.dataframe = self.dataframe
      tool.setContext( self.getContext() )
      tool.level = self.level
      if tool.initialize().isFailure():
        MSG_ERROR( self, 'Can not initialize %s',tool.name)

    return StatusCode.SUCCESS



  def execute(self, context):
    return StatusCode.SUCCESS



  def accept( self, context, key ):

    if key in self._selector.keys():
      return self._selector[key].accept( context )
    else:
      MSG_FATAL( self, "The key %s is not in the emulation" , key )



  def finalize(self):

    for key, tool in self._selector.items():
      MSG_INFO( self, 'Finalizing %s tool',key)
      if tool.finalize().isFailure():
        MSG_ERROR( self, 'Can not finalizing %s',tool.name)

    return StatusCode.SUCCESS



  def isValid(self, key ):
    return True if key in self._selector.keys() else False



