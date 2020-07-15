
from ProfileTools import StandardQuantitiesDrawer, RingerQuantitiesDrawer, BasicInfoDrawer


etbins  = [15.0, 20.0, 30.0, 40.0, 50.0, 1000000.0]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
#etabins = [0.0, 0.8, 1.37, 1.54, 2.50]


dataLegend = "data16, Z#rightarrowee"

import gc
kwargs = { 
           'outputPath' : "plot_quantities_EGAM1_2016_probes_lhmedium"
         , 'dataLegend' : dataLegend
         , 'etBins'     : etbins
         , 'etaBins'    : etabins
         #, 'filePath'   : '../phd_data/analysis/commissioning/quantities_v6_mc15_Zee_probes_lhmedium/mc15_13TeV.Zee_probes.lhmedium.profiles.root'
         , 'filePath'   : '../phd_data/quantities_EGAM1_2016_probes_lhmedium/data16_13TeV.EGAM1.probes_lhmedium.profiles.root'
         }

pDrawer = StandardQuantitiesDrawer( **kwargs ) 
pDrawer.plot()
del pDrawer
gc.collect()
pDrawer = RingerQuantitiesDrawer( **kwargs ) 
pDrawer.plot()
del pDrawer
gc.collect()
pDrawer = BasicInfoDrawer( **kwargs ) 
pDrawer.plot()
del pDrawer
gc.collect()

