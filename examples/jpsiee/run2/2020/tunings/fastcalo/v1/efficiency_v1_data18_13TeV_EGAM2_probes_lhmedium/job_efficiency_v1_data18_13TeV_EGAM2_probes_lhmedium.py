

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
                  treePath= '*/HLT/Physval/Egamma/fakes',
                  #treePath= '*/HLT/Egamma/Egamma/probes',
                  #treePath= '*/HLT/Egamma/Egamma/fakes' if args.doEgam7 else '*/HLT/Egamma/Egamma/probes',
                  dataframe = DataframeEnum.Electron_v1, 
                  outputFile = args.outputFile,
                  level = LoggingLevel.INFO
                  )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection', dataframe = DataframeEnum.Electron_v1)
evt.setCutValue( SelectionType.SelectionOnlineWithRings )
#pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
#pidname = 'el_lhmedium'
pidname = '!el_lhvloose'
evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove , 3)
evt.setCutValue( EtCutType.L2CaloBelow , 15)

ToolSvc += evt


from TrigEgammaEmulationTool import Chain, Group, TDT

triggerList = [
                # e17 lhvloose
                #Group( TDT( "TDT_e5_lhloose_nod0" , "HLT_e5_lhloose_nod0"   ), "el_lhloose", 5 ),
                #Group( Chain( "EMU_e5_lhloose_nod0_noringer", "L1_EM3", "HLT_e5_lhloose_nod0_noringer"    ), "el_lhloose", 5 ),
                #Group( Chain( "EMU_e5_lhloose_nod0_ringer_v1", "L1_EM3", "HLT_e5_lhloose_nod0_ringer_v1"    ), "el_lhloose", 5 ),
              
                Group( Chain( "EMU_e5_lhloose_nod0_noringer", "L1_EM3", "HLT_e5_lhloose_nod0_noringer"    ), None, 5 ),
                Group( Chain( "EMU_e5_lhloose_nod0_ringer_v1", "L1_EM3", "HLT_e5_lhloose_nod0_ringer_v1"    ), None, 5 ),
                
                
              ]




from EfficiencyTools import EfficiencyTool
alg = EfficiencyTool( "Efficiency", dataframe = DataframeEnum.Electron_v1 )


for group in triggerList:
  alg.addGroup( group )

ToolSvc += alg

acc.run(args.nov)








