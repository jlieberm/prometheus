



from prometheus import EventSimulatorLoop
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from prometheus import ToolSvc, ToolMgr


datapath   = 'resolution.root'

from Gaugi.storage import  restoreStoreGate
sg =  restoreStoreGate( datapath )

from SimValidationTools import *
tool = ResolutionTool( "ResolutionTool", energy_bins =[ 5,10,15,20,50,100] )

tool.plot(sg,'reso.pdf')




