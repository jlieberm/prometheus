

__all__ =  [
            #"installElectronL2CaloRingerSelector_v5", 
            "installElectronL2CaloRingerSelector_v6",
            "installElectronL2CaloRingerSelector_v8",
            "installElectronL2CaloRingerSelector_v10",
            #jpsiee
            'installLowEnergyElectronL2CaloRingerSelector_v1',
            'installLowEnergyElectronL2CaloRingerSelector_v1_vmedium',
            'installLowEnergyElectronL2CaloRingerSelector_v1_freeRinger',
            'installLowEnergyElectronL2CaloRingerSelector_v1_sameCutBased',
            'installLowEnergyElectronL2CaloRingerSelector_v1_athena'
           ]
import os



###########################################################
################## Official 2017 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v6( toolname = "Emulator" ):

  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/zee/TrigL2_20170505_v6'


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
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/zee/TrigL2_20180125_v8'

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
  from RingerSelectorTools import norm1 as norm
  # do not change this paths...
  #calibpath = 'RingerSelectorTools/TrigL2_20180125_v8'
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/zee/TrigL2_20200715_v10'


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v10"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v10"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v10"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v10", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm), 
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
################### jpsiee v1 tuning  #####################
###########################################################
def installLowEnergyElectronL2CaloRingerSelector_v1( toolname = "Emulator" ):

  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  # do not change this paths...
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/jpsiee/TrigL2_20200805_v1'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm), 
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
################### jpsiee v1 legacy  #####################
###########################################################

def installLowEnergyElectronL2CaloRingerSelector_v1_athena( toolname = "Emulator" ):
  '''
  This tuning was emulated in athena and was adjusted to minimize the impact at the final of HLT.
  '''
  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  # do not change this paths...
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/jpsiee/final_tuning_09032019_athena_onnx'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_ath"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1_ath"    , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1_ath"     , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1_ath" , ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm), 
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names

def installLowEnergyElectronL2CaloRingerSelector_v1_sameCutBased( toolname = "Emulator" ):
  '''
  This tuning was adjust in rDev to have the same efficiency as CutBased with respect to a subset of EGAM2 (lh medium) and EGAM7 (!veryloose)
  '''
  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  # do not change this paths...
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/jpsiee/final_tuning_28022019_sameCutBased_onnx'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_cutbased"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1_cutbased"    , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1_cutbased"     , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1_cutbased" , ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm), 
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names

def installLowEnergyElectronL2CaloRingerSelector_v1_freeRinger( toolname = "Emulator" ):
  '''
  This tuning was adjusted in order to have the operation points around of the max SP point.
  '''
  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  # do not change this paths...
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/jpsiee/final_tuning_28022019_puroRinger_onnx'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_freeRinger"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1_freeRinger"    , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1_freeRinger"     , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1_freeRinger" , ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm), 
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names


def installLowEnergyElectronL2CaloRingerSelector_v1_vmedium( toolname = "Emulator" ):
  '''
  This tuning is the very medium tuning which was adjusted to operate in the knee of the ROC curve given the best balance between PD and FR.
  '''
  from RingerSelectorTools import RingerSelectorTool
  from RingerSelectorTools import norm1 as norm
  # do not change this paths...
  calibpath = os.environ['PRT_PATH'] + '/tools/trigger/RingerSelectorTools/data/jpsiee/final_tuning_28022019_vmedium_onnx'

  # very medum has only one operation point alocate in tight
  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_vmedium"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm),
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names