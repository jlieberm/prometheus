
__all__ = ['TrigEgammaElectronSelectorTool']

from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi import retrieve_kw
from EventAtlas import Accept
from prometheus.enumerations import Dataframe as DataframeEnum


class TrigEgammaElectronSelectorTool( Algorithm ):


  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    self._branch = retrieve_kw( kw, 'branch', '')


  def initialize(self):
   
      
    return StatusCode.SUCCESS


  def accept(self, context):

    if self.dataframe is DataframeEnum.PhysVal_v2:
      el= context.getHandler("HLT__ElectronContainer")
      # helper accessor function
      def getDecision( container, branch ):
        passed=False
        current = container.getPos()
        for it in container:
          if it.accept(branch):  passed=True;  break;
        container.setPos(current) # to avoid location fail
        return passed

      # Decorate the HLT electron with all final decisions
      passed = getDecision(el, self._branch)
      accept = Accept( self.name )
      accept.setCutResult( 'Pass', passed )
      return accept
    else:
      MSG_FATAL( self, "It's not possible to emulate the HLT since the dataframe is not reconized")




  def finalize(self):
    return StatusCode.SUCCESS






