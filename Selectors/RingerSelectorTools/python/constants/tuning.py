


__all__ = [
           ### Trigger
           'install_HLTElectronLikelihood_rel21_20170217',
           'install_HLTElectronLikelihood_CaloOnly_rel21_20170217',
           'install_HLTElectronCutBased_L2Calo',
           'install_HLTElectronRinger_v6',
           #'install_HLTElectronRinger_v7',
           'install_HLTElectronRinger_v8',
           'install_HLTElectronRinger_v9',
           'install_HLTElectronRinger_v9_nohad',
           

           ### Offline
           'install_ElectronLikelihood_v11',
           'install_ElectronLikelihoodCaloOnly_test',
           'install_ElectronRinger_v6',
           'install_ElectronTrack_v6',
           'install_ElectronRinger_CutBasedRef_v6',
           'install_ElectronRinger_ExClTrk_v6',
           'install_ElectronRinger_ExClSSTrk_v6',

           ]


import os
basepath = os.environ['ROOTCOREBIN']+'/..'


def install_HLTElectronCutBased_L2Calo( tool ):

  from rDev.tools.emulation.selector import T2CaloSelectorTool
  configs = {
      "T0HLTElectronT2CaloTight"  : T2CaloSelectorTool("T2CaloTight" , IDinfo='lhtight' ) ,
      "T0HLTElectronT2CaloMedium" : T2CaloSelectorTool("T2CaloMedium", IDinfo='lhmedium') ,
      "T0HLTElectronT2CaloLoose"  : T2CaloSelectorTool("T2CaloLoose" , IDinfo='lhloose' ) ,
      "T0HLTElectronT2CaloVLoose" : T2CaloSelectorTool("T2CaloVLoose", IDinfo='lhvloose') ,
            }
  for key, selector in configs.iteritems():
    tool.addFastCaloSelector(key, selector)




def install_HLTElectronLikelihood_rel21_20170217( tool ):

  from rDev.tools.emulation.selector import LHSelectorTool
  # do not change this paths...
  calibPath = "ElectronPhotonSelectorTools/trigger/rel21_20170217"
  configFiles = [
     ( "T0HLTTightElectronSelector" ,calibPath+"/ElectronLikelihoodTightTriggerConfig.conf"    ),
     ( "T0HLTMediumElectronSelector",calibPath+"/ElectronLikelihoodMediumTriggerConfig.conf"   ),
     ( "T0HLTLooseElectronSelector" ,calibPath+"/ElectronLikelihoodLooseTriggerConfig.conf"    ),
     ( "T0HLTVLooseElectronSelector",calibPath+"/ElectronLikelihoodVeryLooseTriggerConfig.conf"),
    ]

  for config in configFiles:
    selector = LHSelectorTool(config[0],ConfigFile=config[1])
    tool.addElectronSelector(config[0],selector)


def install_HLTElectronLikelihood_CaloOnly_rel21_20170217( tool ):

  from rDev.tools.emulation.selector import LHSelectorTool

  # do not change this paths...
  calibPath = "ElectronPhotonSelectorTools/trigger/rel21_20170217"
  configFiles = [
     ( "T0HLTTightElectronSelector_CaloOnly" ,calibPath+"/ElectronLikelihoodTightTriggerConfig_CaloOnly.conf"    ),
     ( "T0HLTMediumElectronSelector_CaloOnly",calibPath+"/ElectronLikelihoodMediumTriggerConfig_CaloOnly.conf"   ),
     ( "T0HLTLooseElectronSelector_CaloOnly" ,calibPath+"/ElectronLikelihoodLooseTriggerConfig_CaloOnly.conf"    ),
     ( "T0HLTVLooseElectronSelector_CaloOnly",calibPath+"/ElectronLikelihoodVeryLooseTriggerConfig_CaloOnly.conf"),
    ]

  for config in configFiles:
    selector = LHSelectorTool(config[0],ConfigFile=config[1], caloOnly = True)
    tool.addElectronSelector(config[0],selector)


###########################################################
################## Official 2017 tuning ###################
###########################################################
def install_HLTElectronRinger_v6( tool ):

  from prometheus.tools.atlas import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = 'RingerSelectorTools/TrigL2_20170505_v6'
  configFiles = [
    ("T0HLTElectronRingerTight_v6"  , calibPath, ElectronRingerPid.Tight    ),
    ("T0HLTElectronRingerMedium_v6" , calibPath, ElectronRingerPid.Medium   ),
    ("T0HLTElectronRingerLoose_v6"  , calibPath, ElectronRingerPid.Loose    ),
    ("T0HLTElectronRingerVLoose_v6" , calibPath, ElectronRingerPid.VeryLoose),
    ]

  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addFastCaloSelector(config[0], selector)



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

def install_HLTElectronRinger_v8_test( tool ):

  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = 'RingerSelectorTools/TrigL2_20180125_v8'
  configFiles = [
    ("T0HLTElectronRingerTight_v8_test"  , calibPath, ElectronRingerPid.Tight    ),
    ("T0HLTElectronRingerMedium_v8_test" , calibPath, ElectronRingerPid.Medium   ),
    ("T0HLTElectronRingerLoose_v8_test"  , calibPath, ElectronRingerPid.Loose    ),
    ("T0HLTElectronRingerVLoose_v8_test" , calibPath, ElectronRingerPid.VeryLoose),
    ]

  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addFastCaloSelector(config[0], selector)




def install_HLTElectronRinger_v9( tool ):

  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180617_v9'
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180701_v9'
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180723_v9'
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180812_v9'
  calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180823_v9'
  configFiles = [
    ("T0HLTElectronRingerTight_v9"  , calibPath, ElectronRingerPid.Tight    ),
    ("T0HLTElectronRingerMedium_v9" , calibPath, ElectronRingerPid.Medium   ),
    ("T0HLTElectronRingerLoose_v9"  , calibPath, ElectronRingerPid.Loose    ),
    ("T0HLTElectronRingerVLoose_v9" , calibPath, ElectronRingerPid.VeryLoose),
    ]

  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addFastCaloSelector(config[0], selector)




def install_HLTElectronRinger_v9_nohad( tool ):

  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180617_v9'
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180701_v9'
  #calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180723_v9'
  calibPath = basepath+'/TuningBook/RingerSelectorTools/trigger/data17_20180812_v9'
  configFiles = [
    ("T0HLTElectronRingerTight_v9"  , calibPath, ElectronRingerPid.Tight    ),
    ("T0HLTElectronRingerMedium_v9" , calibPath, ElectronRingerPid.Medium   ),
    ("T0HLTElectronRingerLoose_v9"  , calibPath, ElectronRingerPid.Loose    ),
    ("T0HLTElectronRingerVLoose_v9" , calibPath, ElectronRingerPid.VeryLoose),
    ]

  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2], UseTileCal=False)
    tool.addFastCaloSelector(config[0], selector)






####################################################################################################
# Offline tuning

def install_ElectronLikelihood_v11( tool ):
  from rDev.tools.emulation.selector import LHSelectorTool
  # do not change this paths...
  calibPath = 'ElectronPhotonSelectorTools/offline/mc15_20150712'
  configFiles = [
     ( "IsLHTight" ,calibPath+"/ElectronLikelihoodTightTriggerConfig.conf"),
     ( "IsLHMedium",calibPath+"/ElectronLikelihoodMediumTriggerConfig.conf"),
     ( "IsLHLoose" ,calibPath+"/ElectronLikelihoodLooseTriggerConfig.conf"),
     ( "IsLHVLoose",calibPath+"/ElectronLikelihoodVeryLooseTriggerConfig.conf"),
    ]

  for config in configFiles:
    selector = LHSelectorTool(config[0],ConfigFile=config[1])
    tool.addElectronSelector(config[0],selector)


def install_ElectronLikelihoodCaloOnly_test( tool ):
  from rDev.tools.emulation.selector import LHSelectorTool
  # do not change this paths...
  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/ElectronPhotonSelectorTools/offline/lhcalo_rel21_data16_smooth'
  configFiles = [
     ( "IsLHTightCaloOnly" ,calibPath+"/ElectronLikelihoodTightOfflineConfigCalo_Smooth.conf"),
     ( "IsLHMediumCaloOnly",calibPath+"/ElectronLikelihoodMediumOfflineConfigCalo_Smooth.conf"),
     ( "IsLHLooseCaloOnly" ,calibPath+"/ElectronLikelihoodLooseOfflineConfigCalo_Smooth.conf"),
     ( "IsLHVLooseCaloOnly",calibPath+"/ElectronLikelihoodVeryLooseOfflineConfigCalo_Smooth.conf"),
    ]

  for config in configFiles:
    selector = LHSelectorTool(config[0],ConfigFile=config[1], caloOnly=True)
    tool.addElectronSelector(config[0],selector)


def install_ElectronTrack_v6( tool ):
  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/offline/mc16a_20180308_v6/mc16a_20180308_tlh_v6'
  configFiles = [
                  ( "IsMediumTrack_v6"    , calibPath, ElectronRingerPid.OfflineMedium      ),
                  ( "IsVeryLooseTrack_v6" , calibPath, ElectronRingerPid.OfflineVeryLoose   ),
                ]
  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addElectronSelector(config[0], selector)


def install_ElectronRinger_CutBasedRef_v6( tool ):
  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/offline/mc16a_20180308_v6/mc16a_20180308_ccutbased_v6'
  configFiles = [
                  ( "IsRingerMedium_CutBasedRef_v6" , calibPath, ElectronRingerPid.OfflineMedium   ),
                ]
  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addElectronSelector(config[0], selector)


def install_ElectronRinger_v6( tool ):
  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/offline/mc16a_20180308_v6/mc16a_20180308_clh_v6'
  configFiles = [
                  ( "IsRingerMedium_v6"    , calibPath, ElectronRingerPid.OfflineMedium      ),
                  ( "IsRingerVeryLoose_v6" , calibPath, ElectronRingerPid.OfflineVeryLoose   ),
                ]
  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addElectronSelector(config[0], selector)


def install_ElectronRinger_ExClTrk_v6( tool ):
  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/offline/mc16a_20180308_v6/mc16a_20180308_ectlh_v6'
  configFiles = [
                  ( "IsRingerTightExClTrk_v6"     , calibPath, ElectronRingerPid.OfflineTight       ),
                  ( "IsRingerMediumExClTrk_v6"    , calibPath, ElectronRingerPid.OfflineMedium      ),
                  ( "IsRingerLooseExClTrk_v6"     , calibPath, ElectronRingerPid.OfflineLoose       ),
                  ( "IsRingerVeryLooseExClTrk_v6" , calibPath, ElectronRingerPid.OfflineVeryLoose   ),
                ]
  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addElectronSelector(config[0], selector)


def install_ElectronRinger_ExClSSTrk_v6( tool ):
  from rDev.tools.emulation.selector import RingerSelectorTool,ElectronRingerPid
  # do not change this paths...
  calibPath = '/home/jodafons/Public/ringer/root/TuningBook/RingerSelectorTools/offline/mc16a_20180308_v6/mc16a_20180308_ecstlh_v6'
  configFiles = [
                  ( "IsRingerMediumExClSSTrk_v6"    , calibPath, ElectronRingerPid.OfflineMedium      ),
                  ( "IsRingerVeryLooseExClSSTrk_v6" , calibPath, ElectronRingerPid.OfflineVeryLoose   ),
                ]
  for config in configFiles:
    selector = RingerSelectorTool( config[0], CalibPath = config[1], WorkingPoint = config[2] )
    tool.addElectronSelector(config[0], selector)









