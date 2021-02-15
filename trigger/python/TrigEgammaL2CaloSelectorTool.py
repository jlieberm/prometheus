
__all__ = ['TrigEgammaL2CaloSelectorTool']

from Gaugi import GeV
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi.messenger.macros import *
from EventAtlas import Accept



#
# Selector tool
#
class TrigEgammaL2CaloSelectorTool( Algorithm ):

  # Allo properties for this tool
  __property = [
                "OperationPoint",
               ]

  #
  # Contructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)

    # List of hypos in this selector
    self.__hypos = list()

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

    # take from hypo config
    from TrigEgammaEmulationTool import TrigEgammaL2CaloHypoTool, L2CaloCutMaps, L2CaloPhotonCutMaps
    from prometheus import Dataframe as DataFrameEnum

    if self._dataframe is DataFrameEnum.Electron_v1:
      thrs = [0.0, 15.0, 28] # dummy thrsholds to select the energy range inside of L2CaloCutMaps
    elif self._dataframe is DataFrameEnum.Photon_v1:
      thrs = [0.0, 12.0,17.0,22.0,32.0,44.0]
    
    def same(value):
      return [value]*9

    for idx, threshold in enumerate(thrs):
      if self._dataframe is DataFrameEnum.Electron_v1:
         cuts = L2CaloCutMaps(threshold)
      elif self._dataframe is DataFrameEnum.Photon_v1:
         cuts = L2CaloPhotonCutMaps(threshold)
      else:
         MSG_FATAL( self, "Unrecognized dataframe information ")

      hypo  = TrigEgammaL2CaloHypoTool(self._name+"_"+str(idx),
                                        dETACLUSTERthr = 0.1,
                                        dPHICLUSTERthr = 0.1,
                                        EtaBins        = [0.0, 0.6, 0.8, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47],
                                        F1thr          = same(0.005),
                                        ETthr          = same(0),
                                        ET2thr         = same(90.0*GeV),
                                        HADET2thr      = same(999.0),
                                        #HADETthr       = [0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058],
                                        WETA2thr       = same(99999.),
                                        WSTOTthr       = same(99999.),
                                        F3thr          = same(99999.),
                                        HADETthr       = cuts.MapsHADETthr[self.getProperty("OperationPoint")],
                                        CARCOREthr     = cuts.MapsCARCOREthr[self.getProperty("OperationPoint")],
                                        CAERATIOthr    = cuts.MapsCAERATIOthr[self.getProperty("OperationPoint")],
                                      )
      if hypo.initialize().isFailure():
        return StatusCode.FAILURE

      self.__hypos.append(hypo)

    self.init_lock()
    return StatusCode.SUCCESS



  #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):
    from prometheus import Dataframe as DataFrameEnum

    fc = context.getHandler( "HLT__TrigEMClusterContainer" )
    et = fc.et()
    passed = False
    if(self._dataframe is DataFrameEnum.Electron_v1):
      if et < 12*GeV:
        passed = self.__hypos[0].accept(context)
      elif et>=12*GeV and et < 22*GeV:
        passed = self.__hypos[1].accept(context)
      else:
        passed =  self.__hypos[2].accept(context)

    elif(self._dataframe is DataFrameEnum.Photon_v1):
      if et < 10*GeV:
        passed = self.__hypos[0].accept(context)
      elif et>=10*GeV and et < 15*GeV:
        passed = self.__hypos[1].accept(context)
      elif et>=15*GeV and et < 20*GeV:
        passed = self.__hypos[2].accept(context)
      elif et>=20*GeV and et < 30*GeV:
        passed = self.__hypos[3].accept(context)
      elif et>=30*GeV and et < 40*GeV:
        passed = self.__hypos[4].accept(context)
      else:
        passed =  self.__hypos[5].accept(context)

    return passed


  #
  # Finalize method
  #
  def finalize(self):
    for hypo in self.__hypos:
      if hypo.finalize().isFailure():
        return StatusCode.FAILURE

    return StatusCode.SUCCESS










