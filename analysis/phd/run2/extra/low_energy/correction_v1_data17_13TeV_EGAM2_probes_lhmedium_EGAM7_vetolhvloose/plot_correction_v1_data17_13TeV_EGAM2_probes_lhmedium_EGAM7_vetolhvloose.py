
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
alg = PileupCorrectionTool( 'PileupCorrection' )

targets = [
            Target( 'L2_Tight_v1' , 'T0HLTLowEnergyElectronRingerTight_v10' , "T0HLTElectronT2CaloTight"  ) , 
            Target( 'L2_Medium_v1', 'T0HLTLowEnergyElectronRingerTight_v10' , "T0HLTElectronT2CaloMedium" ) ,
            Target( 'L2_Loose_v1' , 'T0HLTLowEnergyElectronRingerTight_v10' , "T0HLTElectronT2CaloLoose"  ) ,
            Target( 'L2_VLoose_v1', 'T0HLTLowEnergyElectronRingerTight_v10' , "T0HLTElectronT2CaloVLoose" ) ,
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
  
res_ybins = [[ barrel, longbarrel, crack, endcap, lastendcap] for _ in xrange(3)]
res_ybins[1][0] = longbarrel
res_ybins[1][1] = longbarrelhigherE
res_ybins[2][0] = longbarrelhigherE
res_ybins[2][1] = longbarrelhigherE
res_ybins[2][3] = endcaphigherE
res_ybins[2][2] = crack

print ("#"*50)
print ("#"*50)
print ("If you're running this, please review code.")
#####
# TODO: Uncomment the following line, fixing `res_xbins` as it's undeclared before using
# alg.setHistogram2DRegion( -6, 6, 0, 70, res_xbins, res_ybins )
print ("#"*50)
print ("#"*50)

etbins = [3.0, 7.0, 10.0, 15.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.5]


alg.setHistogram2DRegion( -16, 16, 16, 60, 0.02, 0.5 )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )
alg.storeSvc = sg
ToolSvc += alg

dirname = 'plot_correction_v1_data17_13TeV_EGAM2_probes_lhmedium.JF17_vetolhvloose'
pdfname = 'plot_correction_v1_data17_13TeV_EGAM2_probes_lhmedium.JF17_vetolhvloose.pdf'
pdftitle = 'data17 13TeV EGAM2 probes (lhmedium) and EGAM7 (vetolhvloose)'
alg.plot(dirname, pdftitle, pdfname)


