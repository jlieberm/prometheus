
__all__ = ['TrigEgammaElectronHypoTool']

from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi import retrieve_kw
from EventAtlas import Accept
from prometheus.enumerations import Dataframe as DataframeEnum



#
# Hypo tool
#
class TrigEgammaElectronHypoTool( Algorithm ):

  __property = [
                "Branch"
                ]

  #
  # Constructor
  #
  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)

    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)

  #
  # Initialize method
  #
  def initialize(self):
    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  # 
  def accept(self, context):

    el= context.getHandler("HLT__ElectronContainer")
  
    branch = self.getProperty("Branch")

    if not el.checkBody( branch ):
      MSG_FATAL( self, "The branch %s is not found into the HLT electron body.", branch )


    # helper accessor function
    def getDecision( container, branch ):
      passed=False
      current = container.getPos()
      for it in container:
        if it.accept(branch):  passed=True;  break;
      container.setPos(current) # to avoid location fail
      return passed

    # Decorate the HLT electron with all final decisions
    passed =  getDecision(el, branch)

    return Accept( self.name(), [ ("Pass", passed) ] )


  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS




#
# Configure the hypo tool from trigger name
#
def configure( trigger ):

  from TrigEgammaEmulationTool import TriggerInfo
  info = TriggerInfo( trigger )
  etthr = info.etthr()

  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve("Emulator")
  pidname = info.pidname()
  name = 'Hypo__HLT__' + info.signature()[0]+str(int(etthr)) + '_' + info.pidname()

  if not emulator.isValid(name):
    hypo  = TrigEgammaElectronHypoTool(name, Branch = 'trig_EF_el_'+info.pidname() )
    emulator+=hypo

  return name





