

__all__ =  [
            #"installElectronL2CaloRingerSelector_v5", 
            "installElectronL2CaloRingerSelector_v6",
            "installElectronL2CaloRingerSelector_v8",
            "installElectronL2CaloRingerSelector_v10",
           ]
import os



###########################################################
################## Official 2017 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v6( toolname = "Emulator" ):

  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/TrigL2_20170505_v6'


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v6"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v6"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v6"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v6", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' , Preproc = norm), 
    ]

  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names




###########################################################
################## Official 2018 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v8( toolname = "Emulator" ):

  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/TrigL2_20180125_v8'

  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v8"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v8"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v8"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v8", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' , Preproc = norm), 
    ]

  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names



  
###########################################################
################## Testing 2020 tuning  ###################
###########################################################
def installElectronL2CaloRingerSelector_v10( toolname = "Emulator" ):

  from RingerSelectorTools import RingerSelectorTool
  # do not change this paths...
  #calibpath = 'RingerSelectorTools/TrigL2_20180125_v8'
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/TrigL2_20200715_v10'

  # specif normalization procedure  
  def norm( data ):
      return (data/abs(sum(data))).reshape((1,100, 1))

  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v10"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v10"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v10"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     , Preproc = norm), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v10", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' , Preproc = norm), 
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names



