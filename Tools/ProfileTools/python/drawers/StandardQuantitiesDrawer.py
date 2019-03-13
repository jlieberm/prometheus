__all__ = ['StandardQuantitiesDrawer']

from DrawerBase import *
from Gaugi.utilites import retrieve_kw, ensureExtension

class StandardQuantitiesDrawer(DrawerBase):

  def __init__(self, **kw):
    DrawerBase.__init__(self, kw)

  def plot(self, **kw):
    from Gaugi.utilities import mkdir_p
    mkdir_p( self.outputPath )
    self.plotStandardQuantityProfiles(**kw)

  def plotStandardQuantityProfiles(self, **kw):
    from CommonTools.constants import electronLatexStr, specialElectronBins
    self.defaultPlotProfiles("StandardQuantities", electronLatexStr, logPrefix="Drawing standard quantities"
                            , entriesMap = specialElectronBins)
