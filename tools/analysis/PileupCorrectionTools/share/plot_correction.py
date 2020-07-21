
from ROOT               import gROOT
from prometheus.core        import *
from prometheus.tools.atlas import *
from prometheus.mainloop    import *
from RingerCore             import Logger, LoggingLevel, BooleanStr
import argparse


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

from RingerCore import  restoreStoreGate
sg1 =  restoreStoreGate( args.inputFile )
alg = PileupLinearCorrectionTool( 'PileupCorrection' )
  
relax     = [0.0, 0.1, 0.2, 0.25]
alg.setEfficiencyTarget( 'L2_Tight' , 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloTight"  , relax[0]) 
alg.setEfficiencyTarget( 'L2_Medium', 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloMedium" , relax[1]) 
alg.setEfficiencyTarget( 'L2_Loose' , 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloLoose"  , relax[2]) 
alg.setEfficiencyTarget( 'L2_VLoose', 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloVLoose" , relax[3]) 

# set resolutions
doSP      = False
etbins    = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins   = [0.0, 0.8, 1.37, 1.54, 2.37, 2.5]
title     = r'data16_13TeV Threshold Correction ($Zee$)'
limits    = [16.5,35,40.5] # do not change this!


import numpy as np
barrel          = np.arange(16.5,40.5,1).tolist()
longbarrel      = np.arange(16.5,40.5,1).tolist()
crack           = np.arange(16.5,40.5,1).tolist()
endcap          = np.arange(16.5,40.5,1).tolist()
lastendcap      = np.arange(16.5,40.5,1).tolist()


res_ybins       = [[ barrel, longbarrel, crack, endcap, lastendcap] for _ in xrange(5)]
res_xbins       = [[0.001]*5]*5
alg.setHistogram2DRegion( -8, 4, 16.5, 40.5, res_xbins, res_ybins )

# set output names 
tuning = {
          'L2_Tight'  : 'TrigL2CaloRingerElectronTightThresholds'     ,
          'L2_Medium' : 'TrigL2CaloRingerElectronMediumThresholds'    ,
          'L2_Loose'  : 'TrigL2CaloRingerElectronLooseThresholds'     ,
          'L2_VLoose' : 'TrigL2CaloRingerElectronVeryLooseThresholds' ,
       }

alg.setEtBinningValues( etbins )
alg.setEtaBinningValues( etabins )
alg.doTrigger = True
alg.storeSvc = sg1

if args.refFile:
  sg2 =  restoreStoreGate( args.refFile )
else:
  sg2=sg1

#from TuningTools.export import TrigMultiVarHypo_v2
alg.plot(tuning,
         pdfoutput=args.outputFile,
         pdftitle=title,
         #exportTool = TrigMultiVarHypo_v2( removeOuptutTansigTF=True, toPickle=True, maxPileupLinearCorrectionValue=40 ),
         limits = limits, # do not change this!
         #excludedEt_EtaBinIdx = excludedEt_EtaBinIdx,
         doSP=False,
         reference=sg2,
         tname='v6',
         runLabelC1='Data 2016',
         runLabelC2='mc15',
         #runLabelC3='Data 2016',
         #runLabelC4='mc15',
         
         )


