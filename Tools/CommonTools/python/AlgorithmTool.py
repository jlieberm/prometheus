

__all__ = ['AlgorithmTool']


from Gaugi import Algorithm

class AlgorithmTool( Algorithm ):

  def __init__(self, name):
    Algorithm.__init__(self,name)
    self._doTrigger = False
    self._doJpsiee = False

  def initialize(self):
    from EventSelectionTool import Interpreter
    self._re = Interpreter("Interpreter")
    self._re.dataframe = self._dataframe
    # syncronizaion with the base
    self._re.setStoreGateSvc( self.getStoreGateSvc() )
    self._re.setContext( self.getContext() )
    self._re.level = self._level

  @property
  def doTrigger(self):
    return self._doTrigger

  @property
  def doJpsiee(self):
    return self._doJpsiee
 
  @doTrigger.setter
  def doTrigger(self, v):
    self._doTrigger = v
  
  @doJpsiee.setter
  def doJpsiee(self, v):
    self._doJpsiee = v


  def accept( self, expression ):
    return self._re.apply(expression)

  # get the regex interpreter
  def re(self):
    return self._re

 



