




from prometheus import EventATLASLoop
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from prometheus import ToolSvc, ToolMgr
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

parser.add_argument('--Zee', action='store_true', 
    dest='doZee', required = False, 
    help = "Do Zee collection.")

parser.add_argument('--egam7', action='store_true', 
    dest='doEgam7', required = False, 
    help = "The colelcted sample came from EGAM7 skemma.")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



ToolMgr += EventATLASLoop(  "EventATLASLoop",
                            inputFiles = args.inputFiles, 
                            treePath= '*/HLT/Physval/Egamma/fakes' if args.doEgam7 else '*/HLT/Physval/Egamma/probes',
                            #treePath= '*/HLT/Egamma/Egamma/fakes' if args.doEgam7 else '*/HLT/Egamma/Egamma/probes',
                            nov = args.nov,
                            dataframe = DataframeEnum.PhysVal_v2, 
                            #outputFile = args.outputFile,
                            outputFile = 'dummy.root',
                            level = LoggingLevel.INFO
                          )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection')
evt.setCutValue( SelectionType.SelectionOnlineWithRings )

# Do not change this!
if args.doEgam7:
  #pidname = '!VeryLooseLLH_DataDriven_Rel21_Run2_2018'
  pidname = '!el_lhvloose'
else:
  #pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
  pidname = 'el_lhtight'


evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += evt


from EmulationTools import EmulationTool
ToolSvc += EmulationTool( "EgammaEmulation" )

from RingerSelectorTools import installElectronL2CaloRingerSelector_v8
installElectronL2CaloRingerSelector_v8() 

from TrigEgammaL2CaloSelectorTool import installTrigEgammaL2CaloSelectors
installTrigEgammaL2CaloSelectors()


from CollectorTool import Collector
alg = Collector( 'Collector' , outputname = args.outputFile.replace('.root','.pic'), doTrack = True )

etbins  = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )
alg.SaveThisBin( 'et2_eta0' )
#alg.SaveThisBin( 'et0_eta0' )
alg.doTrigger  = True



alg.AddFeature( "T0HLTElectronT2CaloTight"        )
alg.AddFeature( "T0HLTElectronT2CaloMedium"       )
alg.AddFeature( "T0HLTElectronT2CaloLoose"        )
alg.AddFeature( "T0HLTElectronT2CaloVLoose"       )
alg.AddFeature( "T0HLTElectronRingerTight_v8"     )
alg.AddFeature( "T0HLTElectronRingerMedium_v8"    )
alg.AddFeature( "T0HLTElectronRingerLoose_v8"     )
alg.AddFeature( "T0HLTElectronRingerVeryLoose_v8" )
alg.AddFeature( "el_lhtight"                      )
alg.AddFeature( "el_lhmedium"                     )
alg.AddFeature( "el_lhloose"                      )
alg.AddFeature( "el_lhvloose"                     )

ToolSvc += alg

from prometheus import job
job.initialize()
job.execute()
job.finalize()








