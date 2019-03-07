



from Gaugi import EventSimulatorLoop
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from Gaugi import ToolSvc, ToolMgr


datapath = '/afs/cern.ch/work/j/jodafons/public/data_samples/ci_test/valid_calocells.G4.eplus.simulator.root'

ToolMgr += EventSimulatorLoop(  "EventGeantLoop",
                                inputFiles = datapath, 
                                treePath = 'fancy_tree', 
                                nov = -1,
                                dataframe = DataframeEnum.Geant, 
                                outputFile = 'test_output.root',
                                level = LoggingLevel.DEBUG
                              )


from Gaugi import Algorithm
ToolSvc += Algorithm( "AlgTest" )

from Gaugi import job
job.initialize()
job.execute()
job.finalize()


