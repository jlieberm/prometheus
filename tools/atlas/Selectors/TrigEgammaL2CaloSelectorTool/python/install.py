

__all__ = ["installTrigEgammaL2CaloSelectors"]


# Install the T2Calo selector used between 2015 and 2018 in the ATLAS
# trigger fast calo system.
def installTrigEgammaL2CaloSelectors( toolname = "EgammaEmulation" ):

  from TrigEgammaL2CaloSelectorTool import TrigEgammaL2CaloSelectorTool
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
      tool.addFastCaloSelector(sel.name(), sel)
  else:
    raise RuntimeError("%s not found into the ToolSvc." % toolname)



