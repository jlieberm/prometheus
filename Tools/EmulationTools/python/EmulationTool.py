
__all__ = ['EmulationTool']


from Gaugi import Algorithm, StatusCode
from Gaugi.messenger.macros import *
from Gaugi.enumerations import Dataframe as DataframeEnum

class EmulationTool( Algorithm ):

  _ph_selector = {}
  _el_selector = {}
  _fc_selector = {}

  def __init__(self, name):
    Algorithm.__init__(self, name)


  def addElectronSelector( self, name, tool ):
    self._el_selector[name] = tool

  def addPhotonSelector( self, name, tool ):
    self._ph_selector[name] = tool

  def addFastCaloSelector( self, name, tool ):
    self._fc_selector[name] = tool


  def initialize(self):

    ### Electron Selectors
    for key, tool in self._el_selector.iteritems():
      MSG_INFO( self, 'Initializing %s tool',key)
      if tool.initialize().isFailure():
        MSG_ERROR( self, 'Can not initialize %s',tool.name)
 
    ### Photon Selectors
    for key, tool in self._ph_selector.iteritems():
      MSG_INFO( self, 'Initializing %s tool',key)
      if tool.initialize().isFailure():
        MSG_ERROR( self, 'Can not initialize %s',tool.name)
 
    ### FastCalo selectors  
    for key, tool in self._fc_selector.iteritems():
      MSG_INFO( self, 'Initializing %s tool',key)
      if tool.initialize().isFailure():
        MSG_ERROR( self, 'Can not initialize %s',tool.name)
    
    return StatusCode.SUCCESS



  def execute(self, context):
    
    event = context.getHandler("EventInfoContainer")
    el    = context.getHandler("ElectronContainer")
    MSG_DEBUG( self, "execute e/g emulation tool")
    # Build each selector for electrons and decorate
    # the Offline electron with the Likelihood decision
    for key, tool in self._el_selector.iteritems():
      passed = tool.accept(el, event.nvtx() )
      el.setDecor( key, passed )
      if type(tool) is LHSelectorTool:
        el.setDecor( key+'_discriminant', tool.likelihood() )
      elif type(tool) is RingerSelectorTool:
        el.setDecor( key+'_discriminant', tool.getNNOutput() )


    #TODO: this is only used in physval_v2 dataframe. This needed to be expand
    # to the offline (skimmed) fro future.
    if self.dataframe is DataframeEnum.PhysVal_v2:
      hlt_el= context.getHandler("HLT__ElectronContainer")
      fc    = context.getHandler("HLT__FastCaloContainer")
      # Build each selector for FastCalo (only ringer) and decorate
      # the HLT electron with the Fast Ringer decision
      for key, tool in self._fc_selector.iteritems():
        passed = tool.accept(fc, event.avgmu() )
        hlt_el.setDecor( key, passed )      
        if hasattr(tool, "getDiscriminant"):
          # set the neural network output as a decoration
          hlt_el.setDecor( key+'_discriminant', tool.getDiscriminant() )
      # helper accessor function
      def getDecision( container, branch ):
        passed=False
        for it in container:
          if it.accept(branch):  passed=True;  break;
        return passed

      # Decorate the HLT electron with all final decisions
      hlt_el.setDecor('HLT__isLHTight'         , getDecision(hlt_el, 'trig_EF_el_lhtight')   )
      hlt_el.setDecor('HLT__isLHMedium'        , getDecision(hlt_el, 'trig_EF_el_lhmedium')  )
      hlt_el.setDecor('HLT__isLHLoose'         , getDecision(hlt_el, 'trig_EF_el_lhloose')   )
      hlt_el.setDecor('HLT__isLHVLoose'        , getDecision(hlt_el, 'trig_EF_el_lhvloose')  )
      hlt_el.setDecor('HLT__isLHTightCaloOnly' , getDecision(hlt_el, 'trig_EF_calo_lhtight') )
      hlt_el.setDecor('HLT__isLHMediumCaloOnly', getDecision(hlt_el, 'trig_EF_calo_lhmedium'))
      hlt_el.setDecor('HLT__isLHLooseCaloOnly' , getDecision(hlt_el, 'trig_EF_calo_lhloose') )
      hlt_el.setDecor('HLT__isLHVLooseCaloOnly', getDecision(hlt_el, 'trig_EF_calo_lhvloose'))
    
    
    elif self.dataframe is Dataframe.SkimmedNtuple_v2:
      fc = context.getHandler("HLT__FastCaloContainer")
      for key, tool in self._fc_selector.iteritems():
        passed = tool.accept(fc, event.avgmu() )
        fc.setDecor( key, passed )      
        if hasattr(tool, "getDiscriminant"):
          # set the neural network output as a decoration
          fc.setDecor( key+'_discriminant', tool.getDiscriminant() )
 

    return StatusCode.SUCCESS



  def finalize(self):
    ### Electron Selectors
    for key, tool in self._el_selector.iteritems():
      MSG_INFO( self, 'Finalizing %s tool',key)
      if tool.finalize().isFailure():
        MSG_ERROR( self, 'Can not finalizing %s',tool.name)

    ### Photon Selectors
    for key, tool in self._ph_selector.iteritems():
      MSG_INFO( self, 'Finalizing %s tool',key)
      if tool.finalize().isFailure():
        MSG_ERROR( self, 'Can not finalizing %s',tool.name)

    ### FastCalo selectors  
    for key, tool in self._fc_selector.iteritems():
      MSG_INFO( self, 'Finalizing %s tool',key)
      if tool.finalize().isFailure():
        MSG_ERROR( self, 'Can not finalizing %s',tool.name)
 


    return StatusCode.SUCCESS





