
__all__ = ['EventSimulator']

from Gaugi.messenger import Logger, LoggingLevel
from Gaugi.messenger.macros import *
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi import StatusCode
from Gaugi.types import NotSet


# Import all root classes
import ROOT

# get the unique identification
def uniqueid():
  import random
  seed = 0
  while True:
    yield seed
    seed += 1
unique_sequence = uniqueid()


# The main framework base class for SIM analysis.
# This class is responsible to build all containers object and
# manager the storegate and histogram services for all classes.
class EventSimulator( Logger ):
    
  def __init__(self, name, **kw):
    # Retrieve all information needed
    Logger.__init__(self, **kw)
    from Gaugi.utilities import retrieve_kw
    self._fList      = retrieve_kw( kw, 'inputFiles', NotSet                          )
    self._ofile      = retrieve_kw( kw, 'outputFile', "histos.root"                   )
    self._treePath   = retrieve_kw( kw, 'treePath'  , NotSet                          )
    self._dataframe  = retrieve_kw( kw, 'dataframe' , DataframeEnum.Geant           )
    self._nov        = retrieve_kw( kw, 'nov'       , -1                              )
    self._name       = name
    self._level = LoggingLevel.retrieve( retrieve_kw(kw, 'level', LoggingLevel.INFO ) )
    if self._fList:
      from Gaugi.utilities import csvStr2List, expandFolders
      self._fList = csvStr2List ( self._fList )
      self._fList = expandFolders( self._fList )
    
    # Loading libraries
    if ROOT.gSystem.Load('libEventGeantLib') < 0:
       MSG_FATAL( self, "Could not load prometheus library", ImportError)

    self._containersSvc = {}
    self._storegateSvc = NotSet
    self._id = unique_sequence.next()
 
  def name(self):
    return self._name


  def __getRunNumber(self,d):
    from ROOT import TFile
    f=TFile(d,'r')
    name = f.GetListOfKeys()[0].GetName()
    try:
      f.Close(); del f
      return name
    except:
      MSG_WARNING( self, 'Can not retrieve the run number')

  # Initialize all services
  def initialize( self ):

    MSG_INFO( self, 'Initializing EventReader...')

    # Use this to hold the fist good 
    metadataInputFile = None
    from Gaugi.utilities import progressbar
    ### Prepare to loop:
    self._t = ROOT.TChain()
    for inputFile in progressbar(self._fList, len(self._fList), prefix= "Creating collection tree ", logger=self._logger):
      # Check if file exists
      self._f  = ROOT.TFile.Open(inputFile, 'read')
      if not self._f or self._f.IsZombie():
        MSG_WARNING( self, 'Couldn''t open file: %s', inputFile)
        continue
      # Inform user whether TTree exists, and which options are available:
      self._logger.debug("Adding file: %s", inputFile)
      try: 
        # Custon directory token
        if '*' in self._treePath:
          dirname = self._f.GetListOfKeys()[0].GetName()
          treePath = self._treePath.replace('*',dirname)
        else:
          treePath=self._treePath
      except:
        MSG_WARNING( self, "Couldn't retrieve TTree (%s) from GetListOfKeys!", treePath)
        continue

      obj = self._f.Get(treePath)
      if not obj:
        MSG_WARNING( self, "Couldn't retrieve TTree (%s)!", treePath)
        MSG_INFO( self, "File available info:")
        self._f.ReadAll()
        self._f.ReadKeys()
        self._f.ls()
        continue
      elif not isinstance(obj, ROOT.TTree):
        MSG_FATAL( self, "%s is not an instance of TTree!", treePath, ValueError)
      self._t.Add( inputFile+'/'+treePath )
    # Turn all branches off.

    self._t.SetBranchStatus("*", False)

    # RingerPhysVal hold the address of required branches
    if self._dataframe is DataframeEnum.Geant:
      #self._t.SetBranchStatus("*", False)
      from ROOT import edm
      self._event = edm.Geant()
      self._t.GetEntry(0)
    elif self._dataframe is DataframeEnum.Delphes:
      try:
        ROOT.gSystem.Load("libDelphes")
      except:
        MSG_FATAL( self, "Can not import Delphes library. You should install delphes before! Bye...")
      try:
        ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
        ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
      except:
        MSG_WARNING( self, "Can not include DelphesClasses/ExRootTreeReader.")
      self._event = NotSet
      self._t = ROOT.ExRootTreeReader(self._t)
      self._t.ReadEntry(0)
    else:
      return StatusCode.FATAL

    # Ready to retrieve the total number of events

    ## Allocating memory for the number of entries
    self._entries = self._t.GetEntries()
    MSG_INFO( self, "Creating containers...")
    # Allocating containers
    if self._dataframe is DataframeEnum.Geant:
      from EventGeant import CaloCells, CaloRings, ShowerShapes
    elif self._dataframe is DataframeEnum.Delphes:
      from EventDelphes import CaloTowers
    else:
      pass
    
    #from prometheus.dataframe.simulator import CaloCells
    # Initialize the base of this container. 
    # Do not change this key names!
    import collections
    self._containersSvc  = collections.OrderedDict()
    # NOTE: Do not change this order.
    # we must retrieve the cells first and the reco other features
    # event dataframe containers
    self._containersSvc['CaloCellsContainer']    = CaloCells() 
    self._containersSvc['CaloRingsContainer']    = CaloRings()
    self._containersSvc['ShowerShapesContainer'] = ShowerShapes()
                           
    from Gaugi import EventContext
    self._context = EventContext(self._t)

    # configure all EDMs needed
    for key, edm in self._containersSvc.iteritems():
      # attach the EDM pointer into the context list
      self.getContext().setHandler(key,edm)
      
      # add properties
      edm.dataframe = self._dataframe
      edm.tree  = self._t
      edm.level = self._level
      edm.event = self._event
      edm.setContext(self.getContext())
      
      # If initializations is failed, we must remove this from the container 
      # service
      if(edm.initialize().isFailure()):
        MSG_WARNING( self, 'Impossible to create the EDM: %s',key)


    # Create the StoreGate service
    if not self._storegateSvc:
      MSG_INFO( self, "Creating StoreGate...")
      from Gaugi.storage import StoreGate
      self._storegateSvc = StoreGate( self._ofile , level = self._level)
    else:
      MSG_INFO( self, 'The StoraGate was created for ohter service. Using the service setted by client.')

    self.getContext().initialize()

    return StatusCode.SUCCESS

  def execute(self):
    for key, edm in self._containersSvc.iteritems():
      if edm.execute().isFailure():
        MSG_WARNING( self,  'Can not execute the edm %s', key )
    return StatusCode.SUCCESS

  def finalize(self):
    MSG_INFO( self, 'Finalizing StoreGate service...')
    self._storegateSvc.write()
    del self._storegateSvc
    MSG_DEBUG( self, "Finalizing file...")
    self._f.Close()
    del self._f
    MSG_DEBUG( self, "Finalizing Event...")
    del self._event
    MSG_DEBUG( self, "Finalizing tree...")
    del self._t
    return StatusCode.SUCCESS

  def getEntries(self):
    return self._entries

  def getEntry( self, entry ):
    if self._dataframe is DataframeEnum.Geant:
      self._t.GetEntry( entry )
    elif self._dataframe is DataframeEnum.Delphes:
      self._t.ReadEntry( entry )
    else:
      self._t.GetEntry( entry )

  def getContext(self):
    return self._context

  # get the storegate pointer
  def getStoreGateSvc(self):
    return self._storegateSvc

  # set the storegate from another external source
  def setStoreGateSvc(self, store):
    self._storegateSvc = store

  # number of event
  @property
  def nov(self):
    if self._nov < 0:
      return self.getEntries()
    else:
      return self._nov

  # return the framework identification
  def id(self):
    return self._id


