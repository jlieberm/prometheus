
__all__ = ['Algorithm']

from Gaugi.messenger import  Logger
from Gaugi.messenger.macros import *
from Gaugi import EnumStringification, NotSet
from Gaugi import StatusCode
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.enumerations import StatusTool, StatusWatchDog


# Base class used for all tools for this framework
class Algorithm( Logger ):

  def __init__(self, name):
    Logger.__init__(self)
    self._name = name
    self._wtd  = StatusWatchDog.DISABLE
    self._status = StatusTool.ENABLE
    self._initialized = StatusTool.NOT_INITIALIZED
    self._finalized = StatusTool.NOT_FINALIZED
    self._ids = []
    self._eventName = NotSet
    self._context   = NotSet
    self._storegateSvc = NotSet
    self._dataframe = NotSet

  def name(self):
    return self._name

  @property
  def dataframe(self):
    return self._dataframe

  @dataframe.setter
  def dataframe(self,v):
    self._dataframe = v


  def setContext( self, context ):
    self._context = context

  def getContext(self):
    return self._context

  def setStoreGateSvc(self,sg):
    self._storegateSvc=sg

  def getStoreGateSvc(self):
    return self._storegateSvc


  @property
  def storeSvc(self):
    if self._storegateSvc is not None:
      return self._storegateSvc
    else:
      MSG_FATAL( self, "Attempted to access storeSvc which wasn't set.")

  @storeSvc.setter
  def storeSvc(self, s):
    from Gaugi.storage import StoreGate
    if not isinstance(s, StoreGate):
      PRH_MSG_FATAL( self, "Attempted to set StoreGate to instance of non StoreGate type")
    self._storegateSvc=s

  def initialize(self):
    return StatusCode.SUCCESS

  def execute(self, context):
    self.setContext(context)
    self._wtd = StatusWatchDog.DISABLE
    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS

  @property
  def wtd(self):
    "Retrieve the watch dog status"
    return self._wtd

  @wtd.setter
  def wtd(self, v):
    self._wtd = StatusWatchDog.retrieve(v)

  @property
  def status(self):
    return self._status

  def disable(self):
    MSG_INFO( self, 'Disable %s tool service.',self._name)
    self._status = StatusTool.DISABLE

  def enable(self):
    MSG_INFO( self, 'Enable %s tool service.',self._name)
    self._status = StatusTool.ENABLE

  def init_lock(self):
    self._initialized = StatusTool.IS_INITIALIZED

  def fina_lock(self):
    self._finalized = StatusTool.IS_FINALIZED

  def setEventName(self, event):
    from Gaugi import EventATLAS, EventSimulator
    if isinstance(event, (EventATLAS,EventSimulator)):
      self._eventName = event.name
    else:
      self._eventName = event

  def plot(self):
    return StatusCode.SUCCESS

  def isInitialized(self):
    if self._initialized is StatusTool.IS_INITIALIZED:
      return True
    else:
      return False

  def isFinalized(self):
    if self._finalized is StatusTool.IS_FINALIZED:
      return True
    else:
      return False

  def setId(self, id):
    from Gaugi import EventATLAS, EventSimulator
    if isinstance(id, int):
      self._ids.append(id)
    elif isinstance(id, (EventATLAS,EventSimulator)):
      self._ids.append(id.id())
    else:
      MSG_ERROR( self, "Attempted to add id of unknown type.")
      MSG_ERROR( self, "id %r ignored.", id)

  def checkId(self, id):
    if id in self._ids:
      return True
    else:
      return False

