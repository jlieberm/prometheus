

__all__ =  [
            "installElectronL2CaloRingerSelector_v5", 
            "installElectronL2CaloRingerSelector_v6",
            "installElectronL2CaloRingerSelector_v8",
           ]
import os



# same as ringer v6 but use the output after the tansig TF function in 
# the last neuron
def installElectronL2CaloRingerSelector_v5( toolname = "EgammaEmulation" ):

  from RingerSelectorTools import RingerSelectorTool
  # do not change this paths...
  #calibpath = 'RingerSelectorTools/TrigL2_20170505_v6'
  calibpath = os.environ['PRT_PATH'] + '/tools/Selectors/RingerSelectorTools/data/TrigL2_20170505_v6'

  selectors = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v5", 
                          calibpath+'/TrigL2CaloRingerElectronTightConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronTightThresholds.json',
                          remove_last_activation=False ), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v5", 
                          calibpath+'/TrigL2CaloRingerElectronMediumConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronMediumThresholds.json', 
                          remove_last_activation=False ), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v5", 
                          calibpath+'/TrigL2CaloRingerElectronLooseConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronLooseThresholds.json', 
                          remove_last_activation=False ), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v5", 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseThresholds.json', 
                          remove_last_activation=False ), 

    ]

  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool.addFastCaloSelector( sel.name(), sel )
  else:
    raise RuntimeError( "%s not found into the ToolSvc." % toolname )





###########################################################
################## Official 2017 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v6( toolname = "EgammaEmulation" ):

  from RingerSelectorTools import RingerSelectorTool
  # do not change this paths...
  #calibpath = 'RingerSelectorTools/TrigL2_20170505_v6'
  calibpath = os.environ['PRT_PATH'] + '/tools/Selectors/RingerSelectorTools/data/TrigL2_20170505_v6'

  selectors = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v6", 
                          calibpath+'/TrigL2CaloRingerElectronTightConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronTightThresholds.json'), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v6", 
                          calibpath+'/TrigL2CaloRingerElectronMediumConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronMediumThresholds.json'), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v6", 
                          calibpath+'/TrigL2CaloRingerElectronLooseConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronLooseThresholds.json'), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v6", 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseThresholds.json'), 

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
  #calibpath = 'RingerSelectorTools/TrigL2_20180125_v8'
  calibpath = os.environ['PRT_PATH'] + '/tools/Selectors/RingerSelectorTools/data/TrigL2_20180125_v8'

  selectors = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v8", 
                          calibpath+'/TrigL2CaloRingerElectronTightConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronTightThresholds.json'), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v8", 
                          calibpath+'/TrigL2CaloRingerElectronMediumConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronMediumThresholds.json'), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v8", 
                          calibpath+'/TrigL2CaloRingerElectronLooseConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronLooseThresholds.json'), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v8", 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseConstants.json', 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseThresholds.json'), 

    ]

  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool.addFastCaloSelector( sel.name(), sel )
  else:
    raise RuntimeError( "%s not found into the ToolSvc." % toolname )



  







