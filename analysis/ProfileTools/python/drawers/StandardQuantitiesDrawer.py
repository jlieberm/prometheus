__all__ = ['StandardQuantitiesDrawer']

from .DrawerBase import *
from Gaugi import retrieve_kw, ensureExtension

class StandardQuantitiesDrawer(DrawerBase):

  def __init__(self, **kw):
    DrawerBase.__init__(self, kw)

  def plot(self, **kw):
    from Gaugi import mkdir_p
    mkdir_p( self.outputPath )
    self.plotStandardQuantityProfiles(**kw)

  def plotStandardQuantityProfiles(self, **kw):
    from ProfileTools.constants import electronLatexStr, specialElectronBins
    self.defaultPlotProfiles("StandardQuantities", electronLatexStr, logPrefix="Drawing standard quantities"
                            , entriesMap = specialElectronBins)
