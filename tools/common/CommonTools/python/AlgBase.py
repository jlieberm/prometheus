

__all__ = ['AlgBase']


from Gaugi import Algorithm



class AlgBase( Algorithm ):

  def __init__(self, name):
    Algorithm.__init__(self,name)
    self._doTrigger = False
    self._doJpsiee = False


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


  def doJpsiee(self):
    return self._doJpsiee

  def doTrigger(self):
    self._doTrigger


  def accept( self, name ):
    dec = self.getContext().getHandler( "MenuContainer" )
    return dec.accept(name)


 



