
__all__ = ['TrigEgammaL2ElectronSelectorTool']

from Gaugi import GeV
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi.messenger.macros import *
from EventAtlas import Accept



#
# Selector tool
#
class TrigEgammaL2ElectronSelectorTool( Algorithm ):


  #
  # Contructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)
    # List of hypos in this selector
    self.__hypos = None



  #
  # Initialize method
  #
  def initialize(self):

    # take from hypo config
    from TrigEgammaEmulationTool import TrigEgammaL2ElectronHypoTool
    self.__hypo = TrigEgammaL2ElectronHypoTool(name,
                                        EtCut                =   0,
                                        TrackPt              =   1*GeV,
                                        CaloTrackdETA        =   0.2  ,
                                        CaloTrackdPHI        =   0.3  ,
                                        CaloTrackdEoverPLow  =   0    ,
                                        CaloTrackdEoverPHigh =   999  ,
                                        TRTRatio             =   -999 )

    if self.__hypo.initialize().isFailure():
      return StatusCode.FAILURE

    self.init_lock()
    return StatusCode.SUCCESS



  #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):

    fc = context.getHandler( "HLT__TrigElectronContainer" )
    et = fc.et()
    passed = False

    if et < 15*GeV:
      self.__hypo.TrackPt = 1*GeV
      self.__hypo.CaloTrackdETA = 0.2
      self.__hypo.CaloTrackdPHI = 0.3
      passed = self.__hypos.accept(context)
    elif et>=15*GeV and et < 20*GeV:
      self.__hypo.TrackPt = 2*GeV
      self.__hypo.CaloTrackdETA = 0.2
      self.__hypo.CaloTrackdPHI = 0.3
      passed = self.__hypos.accept(context)
    elif et>=20*GeV and et < 50*GeV:
      self.__hypo.TrackPt = 3*GeV
      self.__hypo.CaloTrackdETA = 0.2
      self.__hypo.CaloTrackdPHI = 0.3
      passed = self.__hypos.accept(context)
    else: # > 50GeV
      self.__hypo.TrackPt = 5*GeV
      self.__hypo.CaloTrackdETA = 999
      self.__hypo.CaloTrackdPHI = 999
      passed = self.__hypos.accept(context)

    return passed


  #
  # Finalize method
  #
  def finalize(self):
    if hypo.finalize().isFailure():
      return StatusCode.FAILURE
    return StatusCode.SUCCESS










