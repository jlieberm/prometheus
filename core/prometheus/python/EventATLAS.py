
__all__ = ['EventATLAS']


from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import Logger, LoggingLevel
from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from Gaugi.gtypes import NotSet
from Gaugi import TEventLoop



class EventATLAS( TEventLoop ):

  def __init__(self, name , **kw):
    # Retrieve all information needed
    TEventLoop.__init__(self, name, **kw)
    import ROOT
    ROOT.gSystem.Load('libprometheus')




  # Initialize all services
  def initialize( self ):

    MSG_INFO( self, 'Initializing EventATLAS...')
    if super(EventATLAS,self).initialize().isFailure():
      MSG_FATAL( self, "Impossible to initialize the TEventLoop services.")



    from ROOT import edm
    # RingerPhysVal hold the address of required branches
    if self._dataframe is DataframeEnum.SkimmedNtuple:
      self._event = edm.SkimmedNtuple()
    elif self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      self._event = edm.SkimmedNtuple_v2()
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      #self._event = ROOT.RingerPhysVal()
      self._event = edm.RingerPhysVal_v2()
    else:
      return StatusCode.FATAL

    MSG_INFO( self, "Creating containers...")
    # Allocating containers
    from EventAtlas import Electron
    from EventAtlas import FastCalo
    from EventAtlas import FastElectron
    from EventAtlas import CaloCluster
    from EventAtlas import TrackParticle
    from EventAtlas import EmTauRoI
    from EventAtlas import EventInfo
    from EventAtlas import MonteCarlo
    from EventAtlas import TDT
    from EventAtlas import Menu
   
    
    # Initialize the base of this container.
    # Do not change this key names!
    self._containersSvc  = {
                            # event dataframe containers
                            'EventInfoContainer'         : EventInfo(),
                            'MonteCarloContainer'        : MonteCarlo(),
                            'ElectronContainer'          : Electron(),
                            'CaloClusterContainer'       : CaloCluster(),
                            'TrackParticleContainer'     : TrackParticle(),
                            'MenuContainer'              : Menu("EgammaEmulation"),
                           }

    self._containersSvc.update({
                            'HLT__FastCaloContainer'     : FastCalo(),
                            'HLT__FastElectronContainer' : FastElectron(),
                            'HLT__ElectronContainer'     : Electron(),
                            'HLT__CaloClusterContainer'  : CaloCluster(),
                            'HLT__TrackParticleContainer': TrackParticle(),
                            'HLT__EmTauRoIContainer'     : EmTauRoI(),
                            })


    if self._dataframe is DataframeEnum.PhysVal_v2:
      self._containersSvc.update({
                            # metadata containers
                            'HLT__TDT'                   : TDT(),
                            })


    # force the event id number for this event looper
    #self._containersSvc['EventInfoContainer'].setId( self.id() )
    # Add decoration for ATLAS event information
    self._containersSvc['EventInfoContainer'].setDecor( "is_fakes", True if 'fakes' in self._treePath else False)



    # configure all EDMs needed
    for key, edm  in self._containersSvc.items():

      self.getContext().setHandler(key,edm)
      # add properties
      edm.dataframe = self._dataframe
      edm.tree  = self._t
      edm.level = self._level
      edm.event = self._event
      edm.setContext(self.getContext())

      # enable hlt property by the container key name
      if 'HLT' in key:
        edm.is_hlt = True

      # set basepath into the root file
      if edm.useMetadataParams():
        edm.setMetadataParams( {'basepath':self._metadataInputFile[1].rsplit('/',1)[0],
                                 'file':self._metadataInputFile[0]} ) # remove the last name after '/' (tree name)
      # If initializations is failed, we must remove this from the container
      # service
      if(edm.initialize().isFailure()):
        MSG_WARNING( self, 'Impossible to create the EDM: %s',key)


    self.getContext().initialize()
    return StatusCode.SUCCESS



