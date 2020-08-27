
import argparse
from Gaugi import ToolSvc, ToolMgr
from Gaugi.messenger import Logger


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
alg = PileupCorrectionTool( 'PileupCorrection' )

targets = [
            Target( 'L2_Tight' , 'T0HLTElectronRingerTight_v5' , "T0HLTElectronT2CaloTight"  , "TrigL2CaloRingerElectronTightThresholds.root"    ) , 
            Target( 'L2_Medium', 'T0HLTElectronRingerTight_v5' , "T0HLTElectronT2CaloMedium" , "TrigL2CaloRingerElectronMediumThresholds.root"   ) ,
            Target( 'L2_Loose' , 'T0HLTElectronRingerTight_v5' , "T0HLTElectronT2CaloLoose"  , "TrigL2CaloRingerElectronLooseThresholds.root"    ) ,
            Target( 'L2_VLoose', 'T0HLTElectronRingerTight_v5' , "T0HLTElectronT2CaloVLoose" , "TrigL2CaloRingerElectronVeryLooseThresholds.root") ,
          ]
       

scale     = [0.0, 0.1, 0.2, 0.25]

for idx, t in enumerate(targets):
  t.expertAndExperimentalMethods().scaleParameter = scale[idx]
  alg.addTarget( t )





import numpy as np
barrel          = np.arange(16.5,40.5+1,1).tolist()
longbarrel      = np.arange(16.5,40.5+1,1).tolist()
crack           = np.arange(16.5,40.5+1,1).tolist()
endcap          = np.arange(16.5,40.5+1,1).tolist()
lastendcap      = np.arange(16.5,40.5+1,1).tolist()
res_ybins       = [[ barrel, longbarrel, crack, endcap, lastendcap] for _ in range(5)]
res_xbins       = [[0.001]*5]*5



#if args.doEgam7:
etbins  = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
#etbins=[15.0,20.0]
#etabins=[0.0,0.8]
#alg.setHistogram2DRegion( -1, 1, 16.5, 40.5, res_xbins, res_ybins )
alg.setHistogram2DRegion( -1, 1, 16.5, 40.5, 0.02, 1.5 )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )
alg.doTrigger = True
alg.storeSvc = sg
ToolSvc += alg

dirname = 'plot_correction_data16_13TeV_EGAM1_probes_lhmedium.JF17_vetolhvloose_with_tansig'
pdfname = 'plot_correction_data16_13TeV_EGAM1_probes_lhmedium.JF17_vetolhvloose_with_tansig.pdf'
pdftitle = 'data16 13TeV EGAM1 probes (lhmedium) and JF17 (vetolhvloose) with tansig'
alg.plot(dirname, pdftitle, pdfname)


