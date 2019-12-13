



from prometheus import EventSimulatorLoop
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from prometheus import ToolSvc, ToolMgr


datapath   = 'energy_shots.root'
outputfile = 'resolution.root'

ToolMgr += EventSimulatorLoop(  "EventLorenzetLoop",
                                inputFiles = datapath, 
                                treePath = 'fancy_tree', 
                                nov = -1,
                                dataframe = DataframeEnum.Lorenzet, 
                                outputFile = outputfile,
                                level = LoggingLevel.INFO
                              )


from SimValidationTools import *
ToolSvc += ResolutionTool( "ResolutionTool", energy_bins =[ 2,10,15,20,50,100] )


from prometheus import job
job.initialize()
job.execute()
job.finalize()




