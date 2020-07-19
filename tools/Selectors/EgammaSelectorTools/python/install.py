

__all__ = ["installTrigEgammaL2CaloSelectors", 
           "installTrigEgammaElectronSelectors"]


# Install the T2Calo selector used between 2015 and 2018 in the ATLAS
# trigger fast calo system.
def installTrigEgammaL2CaloSelectors( toolname = "EgammaEmulation" ):

  from EgammaSelectorTools import TrigEgammaL2CaloSelectorTool
  selectors = [
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloTight"   , IDinfo='lhtight'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloMedium"  , IDinfo='lhmedium' ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloLoose"   , IDinfo='lhloose'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloVLoose"  , IDinfo='lhvloose' ) ,
    ]
  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool+=sel
  else:
    raise RuntimeError("%s not found into the ToolSvc." % toolname)





# Install the LH HLT selector
def installTrigEgammaElectronSelectors( toolname = "EgammaEmulation" ):

  from EgammaSelectorTools import TrigEgammaElectronSelectorTool
  selectors = [
      TrigEgammaElectronSelectorTool('HLT__isLHTight'         , branch = 'trig_EF_el_lhtight'   ),
      TrigEgammaElectronSelectorTool('HLT__isLHMedium'        , branch = 'trig_EF_el_lhmedium'  ),
      TrigEgammaElectronSelectorTool('HLT__isLHLoose'         , branch = 'trig_EF_el_lhloose'   ),
      TrigEgammaElectronSelectorTool('HLT__isLHVLoose'        , branch = 'trig_EF_el_lhvloose'  ),
      TrigEgammaElectronSelectorTool('HLT__isLHTightCaloOnly' , branch = 'trig_EF_calo_lhtight' ),
      TrigEgammaElectronSelectorTool('HLT__isLHMediumCaloOnly', branch = 'trig_EF_calo_lhmedium'),
      TrigEgammaElectronSelectorTool('HLT__isLHLooseCaloOnly' , branch = 'trig_EF_calo_lhloose' ),
      TrigEgammaElectronSelectorTool('HLT__isLHVLooseCaloOnly', branch = 'trig_EF_calo_lhvloose'),
      ]
  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool+=sel
  else:
    raise RuntimeError("%s not found into the ToolSvc." % toolname)







