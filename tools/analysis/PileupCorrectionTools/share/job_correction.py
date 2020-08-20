




from Gaugi import EventATLASLoop
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from Gaugi import ToolSvc, ToolMgr

parser.add_argument('--Zee', action='store_true',
    dest='doZee', required = False,
    help = "Do Zee collection.")

parser.add_argument('--Jpsi', action='store_true',
    dest='doJpsi', required = False,
    help = "Do Jpsi collection.")

parser.add_argument('--Zrad', action='store_true',
    dest='doZrad', required = False,
    help = "Do Zrad collection.")

if args.doZee or args.doJpsi:
  signature = 'electron'
elif args.doZrad:
  signature = 'photon'
else:
  signature = 'electron'

datapath = '/afs/cern.ch/work/j/jodafons/public/data_samples/PhysVal/user.jodafons.data17_13TeV.00329835.physics_Main.deriv.DAOD_EGAM1.f843_m1824_p3336.Physval.GRL_v97.r7000_GLOBAL'

ToolMgr += EventATLASLoop(  "EventATLASLoop",
                            inputFiles = datapath, 
                            treePath = '*/HLT/Physval/Egamma/probes', 
                            nov = 1000,
                            dataframe = DataframeEnum.Electron_v1 if signature == 'electron' else DataframeEnum.Photon_v1,
                            outputFile = 'test_output.root',
                            level = LoggingLevel.INFO
                          )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection', dataframe = DataframeEnum.Electron_v1 if signature == 'electron' else DataframeEnum.Photon_v1)
evt.setCutValue( SelectionType.SelectionOnlineWithRings )
evt.setCutValue( SelectionType.SelectionPID, "el_lhtight" ) 
evt.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += evt


from EmulationTools import EmulationTool
ToolSvc += EmulationTool( "EgammaEmulation" )

# Install ringer v6
from RingerSelectorTools import installElectronL2CaloRingerSelector_v6
installElectronL2CaloRingerSelector_v6() 

# intall trigger e/g fastcalo cut-based selector (T2Calo)
from TrigEgammaL2CaloSelectorTool import installTrigEgammaL2CaloSelectors
installTrigEgammaL2CaloSelectors()


from PileupCorrectionTools import PileupCorrectionTool, Target
alg = PileupCorrectionTool( 'PileupCorrection' , dataframe = DataframeEnum.Electron_v1 if signature == 'electron' else DataframeEnum.Photon_v1)

targets = [
            Target( 'L2_Tight' , 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloTight"  ) , 
            Target( 'L2_Medium', 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloMedium" ) ,
            Target( 'L2_Loose' , 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloLoose"  ) ,
            Target( 'L2_VLoose', 'T0HLTElectronRingerTight_v6' , "T0HLTElectronT2CaloVLoose" ) ,
          ]
       

for t in targets:
  alg.addTarget( t )




#if args.doEgam7:
etbins  = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]

alg.setHistogram2DRegion( -12, 8, 0, 100, 0.02, 0.5 )
alg.setEtBinningValues( etbins   )
alg.setEtaBinningValues( etabins )
alg.doTrigger  = True


ToolSvc += alg



from Gaugi import job
job.initialize()
job.execute()
job.finalize()