




from Gaugi.messenger import Logger
from Gaugi.messenger.macros import *


class InstallRingerSelector( Logger ):

  def __init__( self, **kw ):

    Logger.__init__(self, **kw)


  def getToolSvc( self ):
    from Gaugi import ToolSvc as toolSvc
    return toolSvc

  def __call__(  ):
    return StatusCode.SUCCESS





###########################################################
################## Official 2017 tuning ###################
###########################################################
def installElectronRingerSelector_v6( toolname = "EventEmulation" ):

  from RingerSelectorTools import RingerSelectorTool
  # do not change this paths...
  calibpath = 'RingerSelectorTools/TrigL2_20170505_v6'

  selectors = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v6", 
                          calibpath+'/TrigL2CaloRingerElectronTightContants.root', 
                          calibpath+'/TrigL2CaloRingerElectronTightThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerMedium_v6", 
                          calibpath+'/TrigL2CaloRingerElectronMediumContants.root', 
                          calibpath+'/TrigL2CaloRingerElectronMediumThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerLoose_v6", 
                          calibpath+'/TrigL2CaloRingerElectronLooseContants.root', 
                          calibpath+'/TrigL2CaloRingerElectronLooseThresholds.root'), 
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v6", 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseContants.root', 
                          calibpath+'/TrigL2CaloRingerElectronVeryLooseThresholds.root'), 

    ]

  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  for sel in selectors:
    tool.addFastCaloSelector( sel.name(), sel )



#def install_HLTElectronRinger_v7( tool ):
#
#  from prometheus.tools.atlas import RingerSelectorTool,ElectronRingerPid
#  # do not change this paths...
#  #calibPath = 'RingerSelectorTools/TrigL2_20170505_v6'
#  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/trigger/data17_20171212_v7'
#  configFiles = [
#    ("T0HLTElectronRingerTight_v7"  , calibPath, ElectronRingerPid.Tight    ),
#    ("T0HLTElectronRingerMedium_v7" , calibPath, ElectronRingerPid.Medium   ),
#    ("T0HLTElectronRingerLoose_v7"  , calibPath, ElectronRingerPid.Loose    ),
#    ("T0HLTElectronRingerVLoose_v7" , calibPath, ElectronRingerPid.VeryLoose),
#    ]
#
#  for config in configFiles:
#    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
#    tool.addFastCaloSelector(config[0], selector)


###########################################################
################## Official 2018 tuning ###################
###########################################################
def install_HLTElectronRinger_v8( tool ):

  from prometheus.tools.atlas import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = 'RingerSelectorTools/TrigL2_20180125_v8'
  #calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/trigger/data17_20180125_v8'
  configFiles = [
    ("T0HLTElectronRingerTight_v8"  , calibPath, ElectronRingerPid.Tight    ),
    ("T0HLTElectronRingerMedium_v8" , calibPath, ElectronRingerPid.Medium   ),
    ("T0HLTElectronRingerLoose_v8"  , calibPath, ElectronRingerPid.Loose    ),
    ("T0HLTElectronRingerVLoose_v8" , calibPath, ElectronRingerPid.VeryLoose),
    ]

  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addFastCaloSelector(config[0], selector)


  







