
import argparse
from prometheus import EventATLAS
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc, ToolMgr


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

parser.add_argument('--Zee', action='store_true', 
    dest='doZee', required = False, 
    help = "Do Zee collection.")

parser.add_argument('--EGAM7', action='store_true', 
    dest='doEGAM7', required = False, 
    help = "The colelcted sample came from EGAM7 skemma.")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


acc = EventATLAS( "EventATLASLoop",
                  inputFiles = args.inputFiles, 
                  #treePath= '*/HLT/Physval/Egamma/fakes' if args.doEgam7 else '*/HLT/Physval/Egamma/probes',
                  treePath= '*/HLT/Egamma/Egamma/fakes' if args.doFakes else '*/HLT/Egamma/Egamma/probes',
                  dataframe = DataframeEnum.Electron_v1, 
                  outputFile=args.outputFile,
                  nov = args.nov,
                  level = LoggingLevel.INFO)


from EventSelectionTool import EventSelection, SelectionType, EtCutType
evt = EventSelection('EventSelection')
evt.setCutValue( SelectionType.SelectionOnlineWithRings )

# Do not change this!
if args.doEGAM7:
  #pidname = '!VeryLooseLLH_DataDriven_Rel21_Run2_2018'
  pidname = '!el_vlhloose'
else:
  #pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
  pidname = 'el_lhtight'

evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += evt




from TrigEgammaEmulationTool import Chain


triggerList = [
                Chain( "EMU_e28_tight_noringer"      , "L1_EM3", "HLT_e28_tight_noringer"  ),
                Chain( "EMU_e28_tight_ringerss_v1"     , "L1_EM3", "HLT_e28_tight_ringerss_v1" ),
              ]

# Add all chains into the emulator
emulator = ToolSvc.retrieve( "Emulator" )
for chain in triggerList:
  print(chain.name())
  if not emulator.isValid( chain.name() ):
    emulator+=chain



from QuadrantTools import QuadrantTool
alg = QuadrantTool("Quadrant")
alg.add_quadrant( 'HLT_e28_tight_noringer'  , "EMU_e28_tight_noringer", # T2Calo
                  'HLT_e28_tight_ringerss_v1' , "EMU_e28_tight_ringerss_v1") # Ringer v1


etlist = [15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,50000.0] 
etalist= [ 0.0, 0.6, 0.8, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47 ]
alg.setEtBinningValues(etlist)
alg.setEtaBinningValues(etalist)
ToolSvc += alg


acc.run(args.nov)


