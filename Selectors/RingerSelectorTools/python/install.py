

__all__ =  [
            "installElectronL2CaloRingerSelector_v6",
            "installElectronL2CaloRingerSelector_v8",
           ]



###########################################################
################## Official 2017 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v6( toolname = "EgammaEmulation" ):

  from RingerSelectorTools import RingerSelectorTool
  # do not change this paths...
  calibpath = 'RingerSelectorTools/TrigL2_20170505_v6'

  selectors = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v6", 
                          calibpath+'/TrigL2CaloRingerElectronTightConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronTightThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v6", 
                          calibpath+'/TrigL2CaloRingerElectronMediumConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronMediumThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v6", 
                          calibpath+'/TrigL2CaloRingerElectronLooseConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronLooseThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v6", 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseThresholds.root'), 

    ]

  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool.addFastCaloSelector( sel.name(), sel )
  else:
    raise RuntimeError( "%s not found into the ToolSvc." % toolname )



###########################################################
################## Official 2018 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v8( toolname = "EgammaEmulation" ):

  from RingerSelectorTools import RingerSelectorTool
  # do not change this paths...
  calibpath = 'RingerSelectorTools/TrigL2_20180125_v8'

  selectors = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v8", 
                          calibpath+'/TrigL2CaloRingerElectronTightConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronTightThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v8", 
                          calibpath+'/TrigL2CaloRingerElectronMediumConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronMediumThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v8", 
                          calibpath+'/TrigL2CaloRingerElectronLooseConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronLooseThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v8", 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseConstants.root', 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseThresholds.root'), 

    ]

  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool.addFastCaloSelector( sel.name(), sel )
  else:
    raise RuntimeError( "%s not found into the ToolSvc." % toolname )



  







