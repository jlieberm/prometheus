__all__ = ['StandardQuantitiesDrawer']

from prometheus.drawers.DrawerBase import *
from RingerCore import retrieve_kw, ensureExtension

class StandardQuantitiesDrawer(DrawerBase):

  def __init__(self, **kw):
    DrawerBase.__init__(self, kw)

  def plot(self, **kw):
    from RingerCore import mkdir_p
    mkdir_p( self.outputPath )
    self.plotStandardQuantityProfiles(**kw)

  def plotStandardQuantityProfiles(self, **kw):
    from prometheus.drawers.functions import electronLatexStr
    from prometheus.tools.atlas.common import *
    self.defaultPlotProfiles("StandardQuantities", electronLatexStr, logPrefix="Drawing standard quantities"
                            , entriesMap = specialElectronBins)
