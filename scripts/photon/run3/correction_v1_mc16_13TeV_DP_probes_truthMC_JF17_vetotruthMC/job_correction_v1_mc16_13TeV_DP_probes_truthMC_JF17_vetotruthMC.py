

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

parser.add_argument('--Zrad', action='store_true', 
    dest='doZrad', required = False, 
    help = "Do Zrad collection.")

parser.add_argument('--fakes', action='store_true', 
    dest='doFakes', required = False, 
    help = "The colelcted sample came from JF17 skemma.")

import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = EventATLAS( "EventATLASLoop",
                  inputFiles = args.inputFiles, 
                  treePath= '*/HLT/PhysVal/Egamma/fakes' if args.doFakes else '*/HLT/PhysVal/Egamma/photons',
                  dataframe = DataframeEnum.Photon_v1, 
                  outputFile = args.outputFile,
                  level = LoggingLevel.INFO
                  )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection')
evt.setCutValue( SelectionType.SelectionOnlineWithRings )

# Do not change this!
if args.doFakes:
  #pidname = '!VeryLooseLLH_DataDriven_Rel21_Run2_2018'
  pidname = '!ph_loose'
else:
  #pidname = 'MediumLLH_DataDriven_Rel21_Run2_2018'
  pidname = 'ph_medium'


# evt.setCutValue( SelectionType.SelectionPID, pidname ) 
evt.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += evt



# Install ringer v6
from TrigEgammaEmulationTool import installPhotonL2CaloRingerSelector_v1
installPhotonL2CaloRingerSelector_v1()

# Install ringer v6
# from RingerSelectorTools import installElectronL2CaloRingerSelector_v6
# installElectronL2CaloRingerSelector_v6() 

# # Install ringer v8
# from RingerSelectorTools import installElectronL2CaloRingerSelector_v8
# installElectronL2CaloRingerSelector_v8() 

# Install ringer v6
#from RingerSelectorTools import installElectronL2CaloRingerSelector_v10
#installElectronL2CaloRingerSelector_v10() 

# intall trigger e/g fastcalo cut-based selector (T2Calo)
from TrigEgammaEmulationTool import installTrigEgammaL2CaloSelectors
installTrigEgammaL2CaloSelectors()


from PileupCorrectionTools import PileupCorrectionTool, Target
alg = PileupCorrectionTool( 'PileupCorrection' , IsBackground = True if args.doFakes else False )

targets = [
            #Target( 'L2_Tight_v6' , 'T0HLTElectronRingerTight_v6'  , "T0HLTElectronT2CaloTight"  ) , 
            #Target( 'L2_Mediun_v6' , 'T0HLTElectronRingerTight_v6'  , "T0HLTElectronT2CaloMedium"  ) , 
            #Target( 'L2_Loose_v6' , 'T0HLTElectronRingerTight_v6'  , "T0HLTElectronT2CaloLoose"  ) , 
            #Target( 'L2_VLoose_v6', 'T0HLTElectronRingerTight_v6'  , "T0HLTElectronT2CaloVLoose" ) ,

            Target( 'L2_Tight_v1' , 'T0HLTPhotonRingerTight_v1' , "T0HLTElectronT2CaloTight"  ) , 
            Target( 'L2_Medium_v1', 'T0HLTPhotonRingerMedium_v1' , "T0HLTElectronT2CaloMedium" ) ,
            Target( 'L2_Loose_v1' , 'T0HLTPhotonRingerLoose_v1' , "T0HLTElectronT2CaloLoose"  ) ,
            


            # set v8 to be like the legacy cutbased
            # Target( 'L2_Tight_v8_cutbasedLike' , 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloTight"  ) , 
            # Target( 'L2_Medium_v8_cutbasedLike', 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloMedium" ) ,
            # Target( 'L2_Loose_v8_cutbasedLike' , 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloLoose"  ) ,
            # Target( 'L2_VLoose_v8_cutbasedLike', 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloVLoose" ) ,


          ]
       
for t in targets:
  alg.addTarget( t )


etbins  = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
alg.setHistogram2DRegion( -12, 8, 0, 70, 0.02, 0.5 )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )

ToolSvc += alg

acc.run(args.nov)








