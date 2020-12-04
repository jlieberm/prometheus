
import argparse
import numpy as np
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
alg = PileupCorrectionTool( 'PileupCorrection', IsBackground = False )


targets = [
          
            Target( 'L2_Tight_v1' , 'T0HLTPhotonRingerTight_v1' , "T0HLTPhotonRingerTight_v1"  ) , 
            Target( 'L2_Medium_v1', 'T0HLTPhotonRingerMedium_v1' , "T0HLTPhotonRingerMedium_v1" ) ,
            Target( 'L2_Loose_v1' , 'T0HLTPhotonRingerLoose_v1' , "T0HLTPhotonRingerLoose_v1"  ) ,
          ]
 
scale     = [0.0, 0.1, 0.2, 0.25]

for idx, t in enumerate(targets):
  t.expertAndExperimentalMethods().scaleParameter = scale[idx]
  alg.addTarget( t )



barrel = np.arange(1.,24.5,1.).tolist() + np.arange(24.5,32.5,.5).tolist() + np.arange(32.5,40.5,1.).tolist() + np.arange(40.5,45.5,2.5).tolist() + [45.5,50.5,60.5,70.5]
longbarrel = np.arange(1.,24.5,4.).tolist() + np.arange(24.5,32.5,2.).tolist() + np.arange(32.5,40.5,4.).tolist() + np.arange(40.5,45.5,5.).tolist() + [45.5,70.5]
longbarrelhigherE = np.arange(1.,24.5,4.).tolist() + np.arange(24.5,32.5,4.).tolist() + np.arange(32.5,40.5,8.).tolist() + [40.5,70.5]
#longbarrelhigherE = longbarrel
crack =  np.arange(1.,40.5,10.).tolist() + [40.5,70.5]
endcap = longbarrel
endcaphigherE = crack
lastendcap = [1.,20.5,30.5,60.5,70.5]
  
res_ybins = [[ barrel, longbarrel, crack, endcap, lastendcap] for _ in range(3)]
res_ybins[1][0] = longbarrel
res_ybins[1][1] = longbarrelhigherE
res_ybins[2][0] = longbarrelhigherE
res_ybins[2][1] = longbarrelhigherE
res_ybins[2][3] = endcaphigherE
res_ybins[2][2] = crack

etbins = [15, 20, 30, 40, 50, 10000000]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.5]



alg.setHistogram2DRegion( -6, 6, 0,  70, 0.02, res_ybins )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )
alg.storeSvc = sg
ToolSvc += alg

dirname = 'plot_correction_v1_mc16_13TeV_DP_probes_truthMC.JF17_vetotruthMC'
pdfname = 'plot_correction_v1_mc16_13TeV_DP_probes_truthMC.JF17_vetotruthMC.pdf'
pdftitle = 'mc16 13TeV DP probes (truthMC) and JF17 (truthMC)'
alg.plot(dirname, pdftitle, pdfname)


