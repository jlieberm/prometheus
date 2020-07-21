

from prometheus import EventATLAS
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc, ToolMgr
import argparse
mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-i','--inputFiles', action='store', 
    dest='inputFiles', required = True, nargs='+',
    help = "The input files that will be used to generate the plots")

parser.add_argument('-o','--outputFile', action='store', 
    dest='outputFile', required = False, default = None,
    help = "The output store name.")

parser.add_argument('-n','--nov', action='store', 
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = EventATLAS( "EventATLASLoop",
                  inputFiles = args.inputFiles, 
                  treePath= '*/HLT/Physval/Egamma/fakes' ,#if args.doEgam7 else '*/HLT/Physval/Egamma/probes',
                  #treePath= '*/HLT/Egamma/Egamma/fakes' if args.doEgam7 else '*/HLT/Egamma/Egamma/probes',
                  dataframe = DataframeEnum.PhysVal_v2, 
                  outputFile = args.outputFile,
                  level = LoggingLevel.INFO
                  )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection')
evt.setCutValue( SelectionType.SelectionOnlineWithRings )

#pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
pidname = 'el_lhmedium'


evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += evt


from EmulationTools import EmulationTool, Chain, Group
ToolSvc += EmulationTool()

# install e/g Run2 staff
from EgammaSelectorTools import installTrigEgammaSelectors_Run2
installTrigEgammaSelectors_Run2()

# Install official ringer v6
from RingerSelectorTools import installElectronL2CaloRingerSelector_v6
installElectronL2CaloRingerSelector_v6() 

# Install official ringer v8
from RingerSelectorTools import installElectronL2CaloRingerSelector_v8
installElectronL2CaloRingerSelector_v8() 

# Install dev ringer v10
from RingerSelectorTools import installElectronL2CaloRingerSelector_v10
installElectronL2CaloRingerSelector_v10() 




groups = [

  Group( Chain( "e17_lhvloose_noringer", Signature    = 'electron', 
                                L1Item       = 'L1_EM15VH', 
                                L2CaloItem   = 'L2Calo_LHVLoose', 
                                L2Item       = 'L2_Electron_15to20GeV',
                                HLTItem      = 'HLT_LHVLoose', 
                                L2CaloEtCut  = 17-3, 
                                EFCaloEtCut  = 17, 
                                HLTEtCut     = 17 ),
         None, 17 ),

  Group( Chain( "e17_lhvloose_ringer_v6", Signature    = 'electron', 
                                L1Item       = 'L1_EM15VH', 
                                L2CaloItem   = 'T0HLTElectronRingerVeryLoose_v6', 
                                L2Item       = 'L2_Electron_15to20GeV',
                                HLTItem      = 'HLT_LHVLoose', 
                                L2CaloEtCut  = 17-3, 
                                EFCaloEtCut  = 17, 
                                HLTEtCut     = 17 ),
         None, 17 ),


  Group( Chain( "e17_lhvloose_ringer_v8", Signature    = 'electron', 
                                L1Item       = 'L1_EM15VH', 
                                L2CaloItem   = 'T0HLTElectronRingerVeryLoose_v8', 
                                L2Item       = 'L2_Electron_15to20GeV',
                                HLTItem      = 'HLT_LHVLoose', 
                                L2CaloEtCut  = 17-3, 
                                EFCaloEtCut  = 17, 
                                HLTEtCut     = 17 ),
         None, 17 ),


  Group( Chain( "e17_lhvloose_ringer_v10", Signature    = 'electron', 
                                L1Item       = 'L1_EM15VH', 
                                L2CaloItem   = 'T0HLTElectronRingerVeryLoose_v10', 
                                L2Item       = 'L2_Electron_15to20GeV',
                                HLTItem      = 'HLT_LHVLoose', 
                                L2CaloEtCut  = 17-3, 
                                EFCaloEtCut  = 17, 
                                HLTEtCut     = 17 ),
         None, 17 ),






  Group( Chain( "e26_lhtight_noringer",  Signature    = 'electron', 
                         L1Item       = 'L1_EM22VH', 
                         L2CaloItem   = 'L2Calo_LHTight', 
                         L2Item       = 'L2_Electron_20to50GeV',
                         HLTItem      = 'HLT_LHTight', 
                         L2CaloEtCut  = 26-3, 
                         EFCaloEtCut  = 26, 
                         HLTEtCut     = 26 ),
         None, 26 ),


  Group( Chain( "e26_lhtight_ringer_v6",  Signature    = 'electron', 
                         L1Item       = 'L1_EM22VH', 
                         L2CaloItem   = 'T0HLTElectronRingerTight_v6', 
                         L2Item       = 'L2_Electron_20to50GeV',
                         HLTItem      = 'HLT_LHTight', 
                         L2CaloEtCut  = 26-3, 
                         EFCaloEtCut  = 26, 
                         HLTEtCut     = 26 ),
         None, 26 ),


  Group( Chain( "e26_lhtight_ringer_v8",  
                         Signature    = 'electron', 
                         L1Item       = 'L1_EM22VH', 
                         L2CaloItem   = 'T0HLTElectronRingerTight_v8', 
                         L2Item       = 'L2_Electron_20to50GeV',
                         HLTItem      = 'HLT_LHTight', 
                         L2CaloEtCut  = 26-3, 
                         EFCaloEtCut  = 26, 
                         HLTEtCut     = 26 ),
         None, 26 ),


  Group( Chain( "e26_lhtight_ringer_v10",  
                         Signature    = 'electron', 
                         L1Item       = 'L1_EM22VH', 
                         L2CaloItem   = 'T0HLTElectronRingerTight_v10', 
                         L2Item       = 'L2_Electron_20to50GeV',
                         HLTItem      = 'HLT_LHTight', 
                         L2CaloEtCut  = 26-3, 
                         EFCaloEtCut  = 26, 
                         HLTEtCut     = 26 ),
         None, 26 ),




]

from EfficiencyTools import EfficiencyTool
alg = EfficiencyTool( "ElectronEfficiency" )
alg.doTrigger  = True


for group in groups:
  alg.addGroup( group )
ToolSvc += alg


acc.run(args.nov)








