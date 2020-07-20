

__all__ = [
           "installTrigEgammaSelectors",
           ]



# Install the LH HLT selector
def installTrigEgammaSelectors( toolname = "EgammaEmulation" ):

  from EgammaSelectorTools import TrigEgammaL1CaloSelectorTool
  from EgammaSelectorTools import TrigEgammaL2CaloSelectorTool
  from EgammaSelectorTools import TrigEgammaL2ElectronSelectorTool
  from EgammaSelectorTools import TrigEgammaElectronSelectorTool
  
  selectors = [

      # L1Calo selector + et cuts
      TrigEgammaL1CaloSelectorTool('T0HLTElectronL1EM3'                 , L1Item = 'L1_EM3'     ),
      TrigEgammaL1CaloSelectorTool('T0HLTElectronL1EM22VH'              , L1Item = 'L1_EM22VH'  ),
      TrigEgammaL1CaloSelectorTool('T0HLTElectronL1EM22VHI'             , L1Item = 'L1_EM22VHI' ),
      TrigEgammaL1CaloSelectorTool('T0HLTElectronL1EM15VH'              , L1Item = 'L1_EM15VH'  ),
      TrigEgammaL1CaloSelectorTool('T0HLTElectronL1EM15VHI'             , L1Item = 'L1_EM15VHI' ),
      
      # L2Calo selector only
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloTight"           , IDinfo='lhtight'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloMedium"          , IDinfo='lhmedium' ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloLoose"           , IDinfo='lhloose'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloVLoose"          , IDinfo='lhvloose' ) ,
      
      # L2 Electron only
      TrigEgammaL2ElectronSelectorTool('T0HLTElectronL2'),


      # HLT Electron selector only
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHTight'         , branch = 'trig_EF_el_lhtight'   ),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHMedium'        , branch = 'trig_EF_el_lhmedium'  ),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHLoose'         , branch = 'trig_EF_el_lhloose'   ),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHVLoose'        , branch = 'trig_EF_el_lhvloose'  ),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHTightCaloOnly' , branch = 'trig_EF_calo_lhtight' ),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHMediumCaloOnly', branch = 'trig_EF_calo_lhmedium'),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHLooseCaloOnly' , branch = 'trig_EF_calo_lhloose' ),
      TrigEgammaElectronSelectorTool('T0HLTElectronHLTisLHVLooseCaloOnly', branch = 'trig_EF_calo_lhvloose'),
      
      
      ]
  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool+=sel
  else:
    raise RuntimeError("%s not found into the ToolSvc." % toolname)




