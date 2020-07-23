
__all__ = ['TrigEgammaL2CaloSelectorTool']

from Gaugi import GeV
from Gaugi import StatusCode
from Gaugi import Algorithm
from EventAtlas import Accept



#
# Hypo tool
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
    
    Algorithm.__init__(self, name, self.__property)

    # List of hypos in this selector
    self.__hypos = list()

    # configure all properties
    for key, value in kw.items():
      if key in self.__property:
        self.setProperty( key, value )



  #
  # Initialize method
  #
  def initialize(self):

    # take from hypo config
    from TrigEgammaHypo import TrigEgammaL2CaloHypoTool, L2CaloCutMaps
    thrs = [0.0, 15.0, 28] # dummy thrsholds to select the energy range inside of L2CaloCutMaps

    def same(value):
      return [value]*9

    for idx, threshold in enumerate(thrs):
      cuts = L2CaloCutMaps(threshold)
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

      self._hypos.append(hypo)


    self.init_lock()
    return StatusCode.SUCCESS



  #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):
    fc = context.getHandler( "HLT__FastCaloContainer" )
    et = fc.et()
    passed = False
    
    if et < 12*GeV:
      passed = self.__hypos[0].accept(context)
    elif et>=12*GeV and et < 22*GeV:
      passed = self.__hypos[1].accept(context)
    else:
      passed =  self.__hypos[2].accept(context)
    
    return Accept( self.name(), [("Pass", passed)] )


  #
  # Finalize method
  #
  def finalize(self):
    for hypo in self.__hypos:
      if hypo.finalize().isFailure():
        return StatusCode.FAILURE

    return StatusCode.SUCCESS










