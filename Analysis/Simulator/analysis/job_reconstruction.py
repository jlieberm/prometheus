



from prometheus import EventSimulatorLoop
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from prometheus import ToolSvc, ToolMgr


#datapath   = 'data/generator_electron100GeV_1evt_deposit.root'
datapath   = 'data/generator_electron100GeV_500evt.root'
#datapath   = 'data/generator_jets_1evt_deposit.root'
#datapath   = 'data/generator_jets_500evt.root'
outputfile = 'monitoring.root'

ToolMgr += EventSimulatorLoop(  "EventLorenzetLoop",
                                inputFiles = datapath, 
                                treePath = 'generator', 
                                nov = -1,
                                dataframe = DataframeEnum.Lorenzet, 
                                outputFile = outputfile,
                                level = LoggingLevel.INFO
                              )


from SimValidationTools import *

ToolSvc += StandardQuantityProfiles( "ShowerShapes", basepath = "electron")
ToolSvc += RingProfiles("Rings" , basepath = "electron")
ToolSvc += CaloView("CaloView", basepath = "electron" )

from prometheus import job
job.initialize()
job.execute()
job.finalize()




