__all__ = ['BasicInfoDrawer']

from prometheus.drawers.DrawerBase import *
from prometheus.tools.atlas.common import *
from RingerCore import retrieve_kw, ensureExtension

class BasicInfoDrawer(DrawerBase):

  def __init__(self, **kw):
    DrawerBase.__init__(self, kw)

  def plot(self, **kw):
    from RingerCore import mkdir_p
    mkdir_p( self.outputPath )
    self.plotBasicInfo(**kw)

  def plotBasicInfo(self, **kw):
    from prometheus.drawers.functions import basicInfoLatexStr
    #self.defaultPlotProfiles("BasicInfo", basicInfoLatexStr, logPrefix="Drawing basic info", norm=False)
    self.defaultPlotProfiles("BasicInfo", basicInfoLatexStr, logPrefix="Drawing basic info" )
