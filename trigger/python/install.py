

__all__ =  [
            # Old T2Calo selector
           "installTrigEgammaL2CaloSelectors",

            #"installElectronL2CaloRingerSelector_v5", 
            "installElectronL2CaloRingerSelector_v6",
            "installElectronL2CaloRingerSelector_v8",
            "installElectronL2CaloRingerSelector_v10",
            
            #jpsiee
            'installLowEnergyElectronL2CaloRingerSelector_v1',
            'installLowEnergyElectronL2CaloRingerSelector_v1_vmedium',
            'installLowEnergyElectronL2CaloRingerSelector_v1_freeRinger',
            'installLowEnergyElectronL2CaloRingerSelector_v1_sameCutBased',
            'installLowEnergyElectronL2CaloRingerSelector_v1_athena',
            
            # install helper
            'installElectronRingerZeeFromVersion',
            'installElectronRingerJpsieeFromVersion',
            'installPhotonRingerZeegFromVersion',
           ]




# this dict is used to avoid a lot of elifs into the Menu.
def installElectronRingerZeeFromVersion( key , useOnnx=False):
  
  versions =  {
                  # Zee
                  "v6"                 : installElectronL2CaloRingerSelector_v6(useOnnx),
                  "v8"                 : installElectronL2CaloRingerSelector_v8(useOnnx),
                  "v10"                : installElectronL2CaloRingerSelector_v10(useOnnx),
              }
  return versions[key]




# this dict is used to avoid a lot of elifs into the Menu.
def installElectronRingerJpsieeFromVersion( key , useOnnx=False):
  
  versions =  {
                  # Jpsiee
                  'v1'                 : installLowEnergyElectronL2CaloRingerSelector_v1(useOnnx),
                  'v1_vmedium'         : installLowEnergyElectronL2CaloRingerSelector_v1_vmedium(useOnnx), 
                  'v1_freeRinger'      : installLowEnergyElectronL2CaloRingerSelector_v1_freeRinger(useOnnx),  
                  'v1_sameCutBased'    : installLowEnergyElectronL2CaloRingerSelector_v1_sameCutBased(useOnnx),
                  'v1_athena'          : installLowEnergyElectronL2CaloRingerSelector_v1_athena(useOnnx),
              }
  return versions[key]



# this dict is used to avoid a lot of elifs into the Menu.
def installPhotonRingerZeegFromVersion( key , useOnnx=False):
  
  versions =  {
              }
  return versions[key]




#
# Normalize all rings by the abs total energy
#
def norm1( data ):
  return (data/abs(sum(data))).reshape((1,100))




# Install the LH HLT selector
def installTrigEgammaL2CaloSelectors():

  from TrigEgammaEmulationTool import TrigEgammaL2CaloSelectorTool
  hypos = [
        # L2Calo selector only (backward)
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloTight"   , OperationPoint ='lhtight'  ) ,
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloMedium"  , OperationPoint ='lhmedium' ) ,
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloLoose"   , OperationPoint ='lhloose'  ) ,
        TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloVLoose"  , OperationPoint ='lhvloose' ) ,
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
################## Official 2017 tuning ###################
###########################################################
def installElectronL2CaloRingerSelector_v6( useOnnx=False ):

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20170505_v6'
  
  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v6"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     , 
        Preproc = norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v6"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    , 
        Preproc = norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v6"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     , 
        Preproc = norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v6", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' , 
        Preproc = norm1, UseOnnx=useOnnx), 
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
def installElectronL2CaloRingerSelector_v8( useOnnx=False ):

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20180125_v8'

  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v8"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     , Preproc = norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v8"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    , Preproc = norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v8"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     , Preproc = norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v8", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' , Preproc = norm1, UseOnnx=useOnnx), 
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
def installElectronL2CaloRingerSelector_v10( useOnnx=False ):

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20200715_v10'


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v10"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v10"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v10"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v10", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm1, UseOnnx=useOnnx), 
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
def installLowEnergyElectronL2CaloRingerSelector_v1( useOnnx=False ):

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/jpsiee/TrigL2_20200805_v1'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1"    , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1"   , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1"    , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1", ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,Preproc=norm1, UseOnnx=useOnnx), 
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

def installLowEnergyElectronL2CaloRingerSelector_v1_athena():
  '''
  This tuning was emulated in athena and was adjusted to minimize the impact at the final of HLT.
  '''
  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/jpsiee/test/final_tuning_09032019_athena_onnx'

  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_ath"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1_ath"    , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1_ath"     , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1_ath" , ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,
        Preproc=norm1, UseOnnx=useOnnx), 
    ]

  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names

def installLowEnergyElectronL2CaloRingerSelector_v1_sameCutBased( useOnnx=False ):
  '''
  This tuning was adjust in rDev to have the same efficiency as CutBased with respect to a subset of EGAM2 (lh medium) and EGAM7 (!veryloose)
  '''
  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/jpsiee/test/final_tuning_28022019_sameCutBased_onnx'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_cutbased"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1_cutbased"    , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1_cutbased"     , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1_cutbased" , ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,
        Preproc=norm1, UseOnnx=useOnnx), 
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names



def installLowEnergyElectronL2CaloRingerSelector_v1_freeRinger():
  '''
  This tuning was adjusted in order to have the operation points around of the max SP point.
  '''
  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/jpsiee/test/final_tuning_28022019_puroRinger_onnx'


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_freeRinger"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1_freeRinger"    , ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1_freeRinger"     , ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ,
        Preproc=norm1, UseOnnx=useOnnx), 
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1_freeRinger" , ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ,
        Preproc=norm1, UseOnnx=useOnnx), 
    ]


  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names




def installLowEnergyElectronL2CaloRingerSelector_v1_vmedium(useOnnx=False):
  '''
  This tuning is the very medium tuning which was adjusted to operate in the knee of the ROC curve given the best balance between PD and FR.
  '''
  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/jpsiee/test/final_tuning_28022019_vmedium_onnx'

  # very medum has only one operation point alocate in tight
  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1_vmedium"     , ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf',
        Preproc=norm1, UseOnnx=useOnnx),
    ]

  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names





