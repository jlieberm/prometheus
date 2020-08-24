
__all__ = ["Menu", "EmulationTool","Accept"]



from Gaugi import EDM
from Gaugi import ToolSvc
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi.messenger.macros import *
from prometheus import Dataframe as DataframeEnum
from EventAtlas import DecisionCore, AcceptType
import collections



#
# EDM Menu
#
class Menu(EDM):
    
  #
  # Constructor
  #
  def __init__(self):
    EDM.__init__(self)


  #
  # Initialize method
  #
  def initialize(self):

    if not ToolSvc.retrieve("Emulator"):
      MSG_FATAL( self, "The emulator tool is not in the ToolSvc" )

    return StatusCode.SUCCESS

  
  #
  # Execute method
  #
  def execute(self):
    MSG_DEBUG( self, "Clear all decorations..." )
    self.clearDecorations()
    return StatusCode.SUCCESS
  

  #
  # Finalize method
  #
  def finalize(self):
    return StatusCode.SUCCESS

  
  #
  # Accept method
  #
  def accept( self, key ):

    # is in cache?
    if key in self.decorations():
      # decision in cache
      return self.getDecor( key )

    # get the accept decision from the TDT metadata
    elif (self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1) and key.startswith('TDT__'):
      #  TDT__HLT__e28_lhtight_nod0_ivarloose
      #  TDT__EFCalo__e28_lhtight_nod0_ivarloose
      tdt = self.getContext().getHandler("HLT__TDT")
      trigInfo = key.split('__')
      tdt.core(DecisionCore.TriggerDecisionTool) # athena core
      # TDT__AcceptType__trigItem
      passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      accept = Accept( key )
      accept.setCutResult( 'pass', passed )
      self.setDecor( key, accept )
      return accept
    # get the accept decision from the Emulation metadata
    elif (self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1) and key.startswith('EMU__'):
      #  EMU__HLT__e28_lhtight_nod0_ivarloose
      tdt = self.getContext().getHandler("HLT__TDT")
      trigInfo = key.split('__')
      tdt.core(DecisionCore.TrigEgammaEmulationTool) # athena emulation e/g core
      # EMU__AcceptType__trigItem
      passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      accept = Accept( key )
      accept.setCutResult( 'pass', passed )
      self.setDecor( key, accept )
      return accept
    
    # This name is not in metadata and not in cache, let's access the emulation svc and run it!
    else:  
      emulator = ToolSvc.retrieve( "Emulator" )
      if emulator.isValid( key ):
        accept = emulator.accept( self.getContext(), key )
        self.setDecor( key, accept )
        return accept
      else:
        MSG_FATAL( self, "It's is not possble to interpreter the key: %s.", key )



#
# Emulator
#
class EmulationTool( Algorithm ):

  
  #
  # Constructor
  #
  def __init__(self):
    Algorithm.__init__(self, "Emulator")
    self.__tools = {}


  #
  # Add a selector to the list
  #
  def __add__( self, tool ):
    self.__tools[tool.name()] = tool
    return self

  #
  # Get the hypo tool
  #
  def retrieve(self, key):
    return self.__tools[key] if self.isValid(key) else None
    


  #
  # Initialize method
  #
  def initialize(self):

    tools = [ tool for _, tool in self.__tools.items() ]

    for tool in tools:
      MSG_INFO( self, 'Initializing %s tool',tool.name())
      tool.dataframe = self.dataframe
      tool.setContext( self.getContext() )
      tool.level = self.level
      if tool.initialize().isFailure():
        MSG_ERROR( self, 'Can not initialize %s',tool.name())

    return StatusCode.SUCCESS

  
  #
  # Execute method
  #
  def execute(self, context):
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept( self, context, key ):

    if self.isValid(key):
      return self.__tools[key].accept( context )
    else:
      MSG_FATAL( self, "The key %s is not in the emulation" , key )


  #
  # Finalized method
  #
  def finalize(self):

    for key, tool in self.__tools.items():
      MSG_INFO( self, 'Finalizing %s tool',key)
      if tool.finalize().isFailure():
        MSG_ERROR( self, 'Can not finalizing %s',tool.name)

    return StatusCode.SUCCESS


  #
  # Check if the selector is installed
  #
  def isValid(self, key ):
    return True if key in self.__tools.keys() else False



#
# Add the emulator tool into the tool service
#
ToolSvc += EmulationTool()



#
# Accept
#
class Accept( object ):

  #
  # Constructor
  #
  def __init__(self, name, results=[] ):
    self.__name = name
    self.__results = collections.OrderedDict()
    for (key,value) in results:
      self.__results[key] = value

    self.__decoration = {}

  #
  # Get the accept name
  #
  def name(self):
    return self.__name


  #
  # Add new cut
  #
  def addCut( self, key ):
    self.__results[key] = False


  #
  # Set cut result value
  #
  def setCutResult( self, key, value ):
    self.__results[key] = value


  #
  # Get cut result value
  #
  def getCutResult( self, key ):
    try:
      return self.__results[key]
    except KeyError as e:
      print( e )


  #
  # Is passed
  #
  def __bool__(self):
    x = [v for _, v in self.__results.items()]
    return all( [value for _, value in self.__results.items()] )


  #
  # Add decoration
  #
  def setDecor( self, key, value ):
    self.__decoration[key] = value

  
  #
  # Get decoration
  #
  def getDecor( self, key ):
    return self.__decoration[key]


