



from prometheus import EventSimulator
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from Gaugi import ToolSvc, ToolMgr


datapath = 'zee.reco.root'
outputfile = 'zee_hists.root'

#datapath = 'jf17.reco.root'
#outputfile = 'jf17_hists.root'


acc = EventSimulator(  "EventLorenzettLoop",
                       inputFiles = datapath, 
                       treePath = 'events', 
                       nov = -1,
                       dataframe = DataframeEnum.Lorenzett_v1, 
                       outputFile = outputfile,
                       level = LoggingLevel.INFO )



from SimCollectorTool import Collector

ToolSvc += Collector( "CollectorTool" , outputname = "Zee")
#ToolSvc += Collector( "CollectorTool" , outputname = "JF17")



acc.run()

