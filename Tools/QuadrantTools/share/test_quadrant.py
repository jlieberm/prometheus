



from Gaugi import EventATLASLoop
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from Gaugi import ToolSvc, ToolMgr


datapath = '/afs/cern.ch/work/j/jodafons/public/data_samples/PhysVal/user.jodafons.data17_13TeV.00329835.physics_Main.deriv.DAOD_EGAM1.f843_m1824_p3336.Physval.GRL_v97.r7000_GLOBAL'

ToolMgr += EventATLASLoop(  "EventATLASLoop",
                            inputFiles = datapath, 
                            treePath = '*/HLT/Physval/Egamma/probes', 
                            nov = 1000,
                            dataframe = DataframeEnum.PhysVal_v2, 
                            outputFile = 'test_output.root',
                            level = LoggingLevel.DEBUG
                          )



from EventSelectionTool import EventSelection, SelectionType, EtCutType

evt = EventSelection('EventSelection')
evt.setCutValue( SelectionType.SelectionOnlineWithRings )
evt.setCutValue( SelectionType.SelectionPID, "el_lhtight" ) 
evt.setCutValue( EtCutType.L2CaloAbove , 15)
ToolSvc += evt


from EmulationTools import EmulationTool
ToolSvc += EmulationTool( "EgammaEmulation" )

from QuadrantTools import QuadrantTool

alg = QuadrantTool("Quadrant")
alg.doTrigger  = True
alg.add_quadrant( 'HLT_e28_lhtight_nod0_noringer_ivarloose'  , "TDT__HLT__e28_lhtight_nod0_noringer_ivarloose", # T2Calo
                  'HLT_e28_lhtight_nod0_ivarloose'           , "TDT__HLT__e28_lhtight_nod0_ivarloose") # Ringer
etlist = [15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,50000.0] 
etalist= [ 0.0, 0.6, 0.8, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47 ]
alg.setEtBinningValues(etlist)
alg.setEtaBinningValues(etalist)
ToolSvc += alg



from Gaugi import job
job.initialize()
job.execute()
job.finalize()



