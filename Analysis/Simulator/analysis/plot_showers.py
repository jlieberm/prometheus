



from prometheus import EventSimulatorLoop
from prometheus.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger import LoggingLevel
from prometheus import ToolSvc, ToolMgr
from monet.AtlasStyle import SetAtlasStyle
SetAtlasStyle()

datapath   = 'monitoring.root'

from Gaugi.storage import  restoreStoreGate
sg =  restoreStoreGate( datapath )


from SimValidationTools.drawers import PlotCells, PlotShowers




PlotCells( sg.histogram("electron/CaloView/layer_0"), "cells_electron_first_em_layer.pdf")
PlotCells( sg.histogram("electron/CaloView/layer_1"), "cells_electron_second_em_layer.pdf")
PlotCells( sg.histogram("electron/CaloView/layer_2"), "cells_electron_third_em_layer.pdf")
PlotCells( sg.histogram("electron/CaloView/layer_3"), "cells_electron_first_had_layer.pdf")
PlotCells( sg.histogram("electron/CaloView/layer_4"), "cells_electron_second_had_layer.pdf")
PlotCells( sg.histogram("electron/CaloView/layer_5"), "cells_electron_third_had_layer.pdf")

PlotCells( sg.histogram("jets/CaloView/layer_0"), "cells_jets_first_em_layer.pdf")
PlotCells( sg.histogram("jets/CaloView/layer_1"), "cells_jets_second_em_layer.pdf")
PlotCells( sg.histogram("jets/CaloView/layer_2"), "cells_jets_third_em_layer.pdf")
PlotCells( sg.histogram("jets/CaloView/layer_3"), "cells_jets_first_had_layer.pdf")
PlotCells( sg.histogram("jets/CaloView/layer_4"), "cells_jets_second_had_layer.pdf")
PlotCells( sg.histogram("jets/CaloView/layer_5"), "cells_jets_third_had_layer.pdf")






PlotShowers( sg.histogram("electron/ShowerShapes/eratio2"), sg.histogram("jets/ShowerShapes/eratio2"), 'e^{-}','jets','E_{ratio}_{EM2}','eratio_em2.pdf')
PlotShowers( sg.histogram("electron/ShowerShapes/reta"), sg.histogram("jets/ShowerShapes/reta"), 'e^{-}','jets','R_{#eta}','reta.pdf')
PlotShowers( sg.histogram("electron/ShowerShapes/rphi"), sg.histogram("jets/ShowerShapes/rphi"), 'e^{-}','jets','R_{#phi}','rphi.pdf')
PlotShowers( sg.histogram("electron/ShowerShapes/f1"), sg.histogram("jets/ShowerShapes/f1"), 'e^{-}','jets','f_{1}','f1.pdf')

PlotShowers( sg.histogram("electron/Rings/ring_profile"), sg.histogram("jets/Rings/ring_profile"), 'e^{-}','jets','Ring#','rings.pdf',ylabel='Energy Average [MeV]')
PlotShowers( sg.histogram("electron/Rings/ring_profile"), sg.histogram("jets/Rings/ring_profile"), 'e^{-}','jets','Ring#','rings_nolog.pdf',
    doLogY=False,ylabel='Energy Average [MeV]')




