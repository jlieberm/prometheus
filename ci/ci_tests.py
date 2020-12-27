

from prometheus import EventATLAS
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc, ToolMgr
import argparse
logger = Logger.getModuleLogger("job")
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

parser.add_argument('-t','--test', action='store',
    dest='test', required = True, default = 'q221',
    help = "The test tag.")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


#
# setup event
#
acc = EventATLAS( "EventATLASLoop",
                  inputFiles = args.inputFiles,
                  treePath= '*/HLT/Physval/Egamma/probes',
                  dataframe = DataframeEnum.Electron_v1,
                  outputFile = args.outputFile,
                  level = LoggingLevel.INFO
                  )

from EventSelectionTool import EventSelection, SelectionType, EtCutType
event_cuts = EventSelection('EventSelection')
event_cuts.setCutValue( SelectionType.SelectionOnlineWithRings )
event_cuts.setCutValue( SelectionType.SelectionPID, 'el_lhmedium' )
event_cuts.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += event_cuts



if args.test == 'q221':

  from TrigEgammaEmulationTool import Chain, Group, TDT

  triggerList = [
                # e28 lhtight
                Group( TDT( "TDT_e28_lhtight_nod0_noringer_ivarloose" , "HLT_e28_lhtight_nod0_noringer_ivarloose"   ), "el_lhtight", 28 ),
                Group( Chain( "EMU_e28_lhtight_nod0_noringer_ivarloose"       , "L1_EM24VHI", "HLT_e28_lhtight_nod0_noringer_ivarloose"   ), "el_lhtight", 28 ),
                Group( Chain( "EMU_e28_lhtight_nod0_ringer_v8_ivarloose"      , "L1_EM24VHI", "HLT_e28_lhtight_nod0_ringer_v8_ivarloose"  ), "el_lhtight", 28 ),
              ]

  from EfficiencyTools import EfficiencyTool
  tool = EfficiencyTool( "Efficiency" )
  for group in triggerList:
    tool.addGroup( group )
  ToolSvc += tool


elif args.test == 'q222':


  from TrigEgammaEmulationTool import Chain

  triggerList = [
                Chain( "EMU_e28_lhtight_nod0_noringer_ivarloose"       , "L1_EM24VHI", "HLT_e28_lhtight_nod0_noringer_ivarloose"   ),
                Chain( "EMU_e28_lhtight_nod0_ringer_v8_ivarloose"      , "L1_EM24VHI", "HLT_e28_lhtight_nod0_ringer_v8_ivarloose"  ),
              ]

  emulator = ToolSvc.retrieve( "Emulator" )
  for chain in triggerList:
    if not emulator.isValid( chain.name() ):
      emulator+=chain

  from QuadrantTools import QuadrantTool
  tool = QuadrantTool("Quadrant")
  tool.add_quadrant( 'HLT_e28_lhtight_nod0_noringer_ivarloose'  , "EMU_e28_lhtight_nod0_noringer_ivarloose",
                    'HLT_e28_lhtight_nod0_ringer_v8_ivarloose' , "EMU_e28_lhtight_nod0_ringer_v8_ivarloose")


  etlist = [15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,50000.0]
  etalist= [ 0.0, 0.6, 0.8, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47 ]
  tool.setEtBinningValues(etlist)
  tool.setEtaBinningValues(etalist)
  ToolSvc += tool


else:
  logger.fatal("test %s not supported.")


# Run it!
acc.run(args.nov)













