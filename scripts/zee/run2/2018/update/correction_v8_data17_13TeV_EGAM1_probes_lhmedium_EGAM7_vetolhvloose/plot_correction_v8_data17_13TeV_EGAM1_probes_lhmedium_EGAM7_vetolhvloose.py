
import argparse
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc, ToolMgr



mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFile', action='store',
    dest='inputFile', required = True,
    help = "The input files that will be used to generate the plots")

parser.add_argument('-r','--referenceFile', action='store',
    dest='refFile', required = False, default=None,
    help = "The input files that will be used to generate the reference points")

parser.add_argument('-o','--outputFile', action='store',
    dest='outputFile', required = False, default = None,
    help  = 'output file')


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

from Gaugi.storage import  restoreStoreGate
sg =  restoreStoreGate( args.inputFile )

from PileupCorrectionTools import PileupCorrectionTool, Target
alg = PileupCorrectionTool( 'PileupCorrection',  dataframe = DataframeEnum.Electron_v1)

targets = [
          
            
            Target( 'L2_Tight_v8' , 'T0HLTElectronRingerTight_v8' , "T0HLTElectronRingerTight_v6"  ) , 
            Target( 'L2_Medium_v8', 'T0HLTElectronRingerTight_v8' , "T0HLTElectronRingerMedium_v6" ) ,
            Target( 'L2_Loose_v8' , 'T0HLTElectronRingerTight_v8' , "T0HLTElectronRingerLoose_v6"  ) ,
            Target( 'L2_VLoose_v8', 'T0HLTElectronRingerTight_v8' , "T0HLTElectronRingerVeryLoose_v6" ) ,

            # set v8 to be like the legacy cutbased
            #Target( 'L2_Tight_v8_cutbasedLike' , 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloTight"  ) , 
            #Target( 'L2_Medium_v8_cutbasedLike', 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloMedium" ) ,
            #Target( 'L2_Loose_v8_cutbasedLike' , 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloLoose"  ) ,
            #Target( 'L2_VLoose_v8_cutbasedLike', 'T0HLTElectronRingerTight_v8'  , "T0HLTElectronT2CaloVLoose" ) ,


            
            ]
       

scale     = [0.0, 0.1, 0.2, 0.25]

for idx, t in enumerate(targets):
  t.expertAndExperimentalMethods().scaleParameter = scale[idx]
  alg.addTarget( t )



#if args.doEgam7:
etbins  = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
#etbins=[15.0,20.0]
#etabins=[0.0,0.8]
#alg.setHistogram2DRegion( -8, 4, 16.5, 40.5, res_xbins, res_ybins )
alg.setHistogram2DRegion( -12, 8, 16, 60, 0.02, 0.5 )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )
alg.storeSvc = sg
ToolSvc += alg

dirname = 'plot_correction_v8_data17_13TeV_EGAM1_probes_lhmedium.JF17_vetolhvloose'
pdfname = 'plot_correction_v8_data17_13TeV_EGAM1_probes_lhmedium.JF17_vetolhvloose.pdf'
pdftitle = 'data17 13TeV EGAM1 probes (lhmedium) and EGAM7 (vetolhvloose)'
alg.plot(dirname, pdftitle, pdfname)


