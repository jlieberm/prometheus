


from prometheus import EventATLAS
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc
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

parser.add_argument('--egam7', action='store_true', 
    dest='doEgam7', required = False, 
    help = "Only for EGAM7/background samples..")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = EventATLAS( "EventATLASLoop",
                  inputFiles = args.inputFiles, 
                  #treePath= '*/HLT/Physval/Egamma/fakes' if args.doEgam7 else '*/HLT/Egamma/Egamma/probes',
                  treePath= '*/HLT/Egamma/Egamma/fakes' if args.doEgam7 else '*/HLT/Egamma/Egamma/probes',
                  dataframe = DataframeEnum.Electron_v1, 
                  outputFile = args.outputFile,
                  level = LoggingLevel.INFO
                  )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection', dataframe = DataframeEnum.Electron_v1)
evt.setCutValue( SelectionType.SelectionOnlineWithRings )

# Do not change this!
if args.doEgam7:
  #pidname = '!VeryLooseLLH_DataDriven_Rel21_Run2_2018'
  pidname = '!el_lhvloose'
else:
  #pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
  pidname = 'el_lhmedium'


evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove, 3.)
evt.setCutValue( EtCutType.L2CaloBelow, 15.)
evt.setCutValue( EtCutType.OfflineAbove, 2.)



ToolSvc += evt


# Install ringer v1
from RingerSelectorTools import installLowEnergyElectronL2CaloRingerSelector_v1
installLowEnergyElectronL2CaloRingerSelector_v1() 

# intall trigger e/g fastcalo cut-based selector (T2Calo)
from TrigEgammaEmulationTool import installTrigEgammaL2CaloSelectors
installTrigEgammaL2CaloSelectors()


from PileupCorrectionTools import PileupCorrectionTool, Target
alg = PileupCorrectionTool( 'PileupCorrection' , IsBackground = True if args.doEgam7 else False,  dataframe = DataframeEnum.Electron_v1)

targets = [
            Target( 'L2_Tight_v1' , 'T0HLTLowEnergyElectronRingerTight_v1'  , "T0HLTElectronT2CaloTight"  ) , 
            Target( 'L2_Medium_v1', 'T0HLTLowEnergyElectronRingerTight_v1'  , "T0HLTElectronT2CaloMedium"  ) , 
            Target( 'L2_Loose_v1' , 'T0HLTLowEnergyElectronRingerTight_v1'  , "T0HLTElectronT2CaloLoose"  ) , 
            Target( 'L2_VLoose_v1', 'T0HLTLowEnergyElectronRingerTight_v1'  , "T0HLTElectronT2CaloVLoose" ) ,

          ]
       
for t in targets:
  alg.addTarget( t )


etbins  = [3.0, 7.0, 10.0, 15.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]




alg.setHistogram2DRegion( -6, 6, 0, 70, 0.02, 0.5 )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )

ToolSvc += alg
acc.run(args.nov)








