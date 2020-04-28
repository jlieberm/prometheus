



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
                                nov = 5,
                                dataframe = DataframeEnum.Lorenzett_v1, 
                                outputFile = outputfile,
                                level = LoggingLevel.INFO
                              )


from ValidationTool import Profiles

ToolSvc += Profiles( "Profiles", basepath = "Zee" )

from ValidationTool import CollectorTool


ToolSvc += CollectorTool( "CollectorTool" )
#ToolSvc += Profiles( "Profiles", basepath = "JF17" )



acc.run()

