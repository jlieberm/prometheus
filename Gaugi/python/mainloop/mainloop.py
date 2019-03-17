
__all__ = ['EventATLASLoop', 'EventSimulatorLoop', 'job']

from Gaugi import EventATLAS
from Gaugi import EventSimulator
from Gaugi import StatusCode
from Gaugi import checkForUnusedVars, retrieve_kw, progressbar, LoggingLevel, Logger
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.enumerations import StatusTool, StatusWatchDog
from Gaugi.messenger.macros import *
import ROOT



# main loop for atlas analysis
class EventSimulatorLoop( EventSimulator ):

  def __init__(self, name, **kw):
    EventSimulator.__init__(self, name, **kw)
    self._alg_tools = list()
    self._level = retrieve_kw(kw, 'level', LoggingLevel.INFO)
    # For parallel process
    self._mute_progressbar = retrieve_kw(kw, 'mute_progressbar', False)
    #checkForUnusedVars(kw)
    del kw
    self._initialized = StatusTool.NOT_INITIALIZED
    self._finalized = StatusTool.NOT_FINALIZED
    MSG_INFO( self, 'Created with id (%d)',self._id)


  def initialize( self ):

    if super(EventSimulatorLoop,self).initialize().isFailure():
      MSG_FATAL( self, "Impossible to initialize the EventLooper services.")

    MSG_INFO( self, 'Initializing all tools...')
    # XXX This is just a hack to avoid reimplementing everything
    from Gaugi import ToolSvc as toolSvc
    self._alg_tools = toolSvc.getTools()
    for alg in self._alg_tools:
      if alg.status is StatusTool.DISABLE:
        continue
      # Retrieve all services
      alg.setEventName( self.name )
      alg.level = self._level
      alg.setContext( self.getContext() )
      alg.setStoreGateSvc( self.getStoreGateSvc() )
      alg.dataframe = self._dataframe

      if alg.isInitialized():
        continue
      if alg.initialize().isFailure():
        MSG_FATAL( self, "Impossible to initialize the tool name: %s",alg.name)

    self._init_lock()
    return StatusCode.SUCCESS

  def execute( self ):

    # retrieve values 
    entries = self.getEntries()
    ### Loop over events
    if not self._mute_progressbar:
      step = int(entries/100) if int(entries/100) > 0 else 1
      for entry in progressbar(range(self._entries), entries, step=step, prefix= "Looping over entries ", logger=self._logger):
        if self.nov < entry:
          break
        self.process(entry)
    else:
      for entry in range(self._entries):
        if self.nov < entry:
          break
        self.process(entry)
    return StatusCode.SUCCESS


  def process(self, entry):

    #self.getEntry(entry)
    #if super(EventSimulatorLoop,self).execute().isFailure():
    #  MSG_FATAL( self, "Impossible to initialize the EventLooper services.")


    # retrieve all values from the branches
    context = self.getContext()
    context.setEntry(entry)
    # reading all values from file to EDM pointers.
    # the context hold all EDM pointers
    context.execute()

    # force the reconstruction step running the execute method for each edm...
    #if super(EventSimulatorLoop,self).execute().isFailure() :
    #  MSG_WARNING( self, 'There is an exceptio in the reconstrucion EDM step')

    ### loop over tools...
    for alg in self._alg_tools:
      if alg.status is StatusTool.DISABLE:
        continue
      # Flag which event is being executed by the algorithm:
      alg.setEventName( self.name )
      if alg.execute( context ).isFailure():
        MSG_ERROR( self, 'The tool %s return status code different of SUCCESS',alg.name)
      if alg.wtd is StatusWatchDog.ENABLE:
        self._logger.debug('Watchdog is true in %s. Skip events',alg.name)
        # reset the watchdog since this was used
        alg.wtd = StatusWatchDog.DISABLE
        break


  def finalize( self ):
    MSG_INFO( self, 'Finalizing all tools...')
    if super(EventSimulatorLoop,self).finalize().isFailure():
      MSG_FATAL( self, 'Impossible to finalize the EventLooper services.')

    MSG_DEBUG( self, "Finalizing tools...")
    for alg in self._alg_tools:
      if alg.isFinalized():
        continue
      if alg.finalize().isFailure():
        MSG_ERROR( self, 'The tool %s return status code different of SUCCESS',alg.name)
    MSG_DEBUG( self, "Everything was finished... tchau!")
    return StatusCode.SUCCESS

  def push_back( self, alg ):
    if isinstance(alg, (list,tuple,) ):
      self._alg_tools += alg
    else:
      self._alg_tools.append( alg )

  def __add__(self, alg):
    self.push_back( alg )

  def clear(self):
    self._alg_tools = list()

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

  def _init_lock(self):
    self._initialized = StatusTool.IS_INITIALIZED

  def _fina_lock(self):
    self._finalized = StatusTool.IS_FINALIZED







# main loop for atlas analysis
class EventATLASLoop( EventATLAS ):

  def __init__(self, name, **kw):
    EventATLAS.__init__(self, name, **kw)
    self._alg_tools = list()
    self._level = retrieve_kw(kw, 'level', LoggingLevel.INFO)
    # For parallel process
    self._mute_progressbar = retrieve_kw(kw, 'mute_progressbar', False)
    #checkForUnusedVars(kw)
    del kw
    self._initialized = StatusTool.NOT_INITIALIZED
    self._finalized = StatusTool.NOT_FINALIZED
    MSG_INFO( self, 'Created with id (%d)',self._id)



  def initialize( self ):
    
    if super(EventATLASLoop,self).initialize().isFailure():
      MSG_FATAL( self, "Impossible to initialize the EventLooper services.")
    
    MSG_INFO( self, 'Initializing all tools...')
    # XXX This is just a hack to avoid reimplementing everything
    from Gaugi import ToolSvc as toolSvc
    toolSvc.level = self._level
    toolSvc.enable()
    self._alg_tools = toolSvc.getTools()
    for alg in self._alg_tools:
      if alg.status is StatusTool.DISABLE:
        continue
     # Retrieve all services
      alg.setEventName( self.name )
      alg.level = self._level
      alg.setContext( self.getContext() )
      alg.setStoreGateSvc( self.getStoreGateSvc() )
      alg.dataframe = self._dataframe
      if alg.isInitialized():
        continue
      if alg.initialize().isFailure():
        MSG_FATAL( self, "Impossible to initialize the tool name: %s",alg.name)
    self._init_lock()
    return StatusCode.SUCCESS
 

  def execute( self ):
    # retrieve values 
    entries = self.getEntries()

    ### Loop over events
    if not self._mute_progressbar:
      step = int(entries/100) if int(entries/100) > 0 else 1
      for entry in progressbar(range(self._entries),entries, step=step, prefix= "Looping over entries", logger=self._logger): 
        if self.nov < entry:
          break
        self.process(entry)
    else:
      for entry in range(self._entries):
        if self.nov < entry:
          break
        self.process(entry)
    return StatusCode.SUCCESS


  def process(self, entry):
    
    # retrieve all values from the branches
    context = self.getContext()
    context.setEntry(entry)
    # reading all values from file to EDM pointers.
    # the context hold all EDM pointers
    context.execute()


    # force the reconstruction step running the execute method for each edm...
    if super(EventATLASLoop,self).execute().isFailure() :
      MSG_WARNING( self, 'There is an exceptio in the reconstrucion EDM step')

    ### loop over tools...
    for alg in self._alg_tools:
      if alg.status is StatusTool.DISABLE:
        continue
      # Flag which event is being executed by the algorithm:
      alg.setEventName( self.name )
      if alg.execute(context).isFailure():
        MSG_ERROR( self, 'The tool %s return status code different of SUCCESS',alg.name)
      if alg.wtd is StatusWatchDog.ENABLE:
        MSG_DEBUG( self, 'Watchdog is true in %s. Skip events',alg.name)
        # reset the watchdog since this was used
        alg.wtd = StatusWatchDog.DISABLE
        break
    return StatusCode.SUCCESS


  def finalize( self ):
    MSG_INFO( self, 'Finalizing all tools...')
    if super(EventATLASLoop,self).finalize().isFailure():
      MSG_FATAL( self, 'Impossible to finalize the EventLooper services.')

    for alg in self._alg_tools:
      if alg.isFinalized():
        continue
      if alg.finalize().isFailure():
        MSG_ERROR( self, 'The tool %s return status code different of SUCCESS',alg.name)
    return StatusCode.SUCCESS

  def push_back( self, alg ):
    if isinstance(alg, (list,tuple,) ):
      self._alg_tools += alg
    else:
      self._alg_tools.append( alg )

  def __add__(self, alg):
    self.push_back( alg )

  def clear(self):
    self._alg_tools = list()

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

  def _init_lock(self):
    self._initialized = StatusTool.IS_INITIALIZED

  def _fina_lock(self):
    self._finalized = StatusTool.IS_FINALIZED






class Job(Logger):

  def __init__(self):
    Logger.__init__(self)

  
  def initialize(self):
    from Gaugi import ToolMgr as manager
    print manager
    for evt in manager:
      if evt.initialize().isFailure():
        MSG_FATAL( self, "Can not initialize the event %s", evt.name() )


  def execute(self):
    from Gaugi import ToolMgr as manager
    from Gaugi import ToolSvc as toolSvc
    
    # enable all tools as default

    manager.resume()
    toolSvc.resume()
    for evt in manager:
      #for tool in toolSvc:
      #  # check if the current tool is allow to run in this event
      #  if tool.checkId( evt.id() ):
      #    tool.enable()
      #  else: # if not disable te tool
      #    tool.disable()
      #if not evt.isInitialized():
      #  evt.setStoreSvc(self._eventStack[0].getStoreSvc())
      #  evt.level = self._level
      #  evt.setContext( self.getContext() )
      #  evt.setStoreGateSvc( self.getStoreGateSvc() )
      #  if evt.initialize().isFaiulure():
      #    MSG_FATAL(self, "Can not initialize the event %s", evt.name())
      # execute the event loop
      evt.execute()
    # loop over event reader object

  def finalize(self):
    from Gaugi import ToolMgr as manager
    for evt in manager:
      evt.finalize()


# intance Main object
job = Job()


