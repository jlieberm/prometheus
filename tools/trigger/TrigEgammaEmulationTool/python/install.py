

__all__ = [
           "installTrigEgammaL2CaloSelectors",
           ]


# Install the LH HLT selector
def installTrigEgammaL2CaloSelectors( toolname = "Emulator" ):

  from TrigEgammaEmulatorTool import TrigEgammaL2CaloSelectorTool
  
  selectors = [
        # L2Calo selector only (backward)
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloTight"   , OperationPoint ='lhtight'  ) ,
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloMedium"  , OperationPoint ='lhmedium' ) ,
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloLoose"   , OperationPoint ='lhloose'  ) ,
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloVLoose"  , OperationPoint ='lhvloose' ) ,
      ]
  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool+=sel
  else:
    raise RuntimeError("%s not found into the ToolSvc." % toolname)




