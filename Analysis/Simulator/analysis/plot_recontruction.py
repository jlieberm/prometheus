



from prometheus import EventSimulatorLoop
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from prometheus import ToolSvc, ToolMgr
from monet.AtlasStyle import SetAtlasStyle
SetAtlasStyle()

datapath   = 'monitoring.root'

from Gaugi.storage import  restoreStoreGate
sg =  restoreStoreGate( datapath )


from SimValidationTools.drawers import PlotDeposit, PlotCells

PlotDeposit( sg.histogram( "calorimeter/CaloView/lateral_view"), 'lateral_view.eps')



