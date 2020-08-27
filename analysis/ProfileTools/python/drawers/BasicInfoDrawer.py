__all__ = ['BasicInfoDrawer']

from .DrawerBase import *
from Gaugi import retrieve_kw, ensureExtension

class BasicInfoDrawer(DrawerBase):

  def __init__(self, **kw):
    DrawerBase.__init__(self, kw)

  def plot(self, **kw):
    from Gaugi import mkdir_p
    mkdir_p( self.outputPath )
    self.plotBasicInfo(**kw)

  def plotBasicInfo(self, **kw):
    from CommonTools.constants import basicInfoLatexStr
    #self.defaultPlotProfiles("BasicInfo", basicInfoLatexStr, logPrefix="Drawing basic info", norm=False)
    self.defaultPlotProfiles("BasicInfo", basicInfoLatexStr, logPrefix="Drawing basic info" )
