__all__ = ['ProfileToolBase']

from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import retrieve_kw
 


class ProfileToolBase( Algorithm ):

  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    from ProfileTools.constants import ringer_tuning_etbins, ringer_tuning_etabins
    self._etBins   = ringer_tuning_etbins
    self._etaBins  = ringer_tuning_etabins

  @property
  def basepath( self ):
    eventName = self._eventName
    if eventName: eventName = '/' + eventName
    return 'Profiles/' + self.name + eventName

  def setEtBins( self, etbins):
    self._etBins = etbins

  def setEtaBins( self, etabins):
    self._etaBins = etabins

  def setDiscriminantList( self, d ):
    self._discrList = d

  def initialize(self):
    Algorithm.initialize()
    return StatusCode.SUCCESS

  def execute(self, context):
    return StatusCode.SUCCESS

  def finalize(self):
    Algorithm.finalize()
    return StatusCode.SUCCESS

  def binStr(self, etBinIdx = None, etaBinIdx = None):
    if etBinIdx is None and etaBinIdx is None:
      binstr = 'integrated'
    else:
      binstr = ('et%d_eta%d') % (etBinIdx, etaBinIdx)
    return binstr
  
  def getPath( self, etBinIdx = None, etaBinIdx = None ):
    return self.basepath + '/' + self.binStr(etBinIdx, etaBinIdx)

  # (Private method) retrieve the correct bin range
  def _retrieveBinIdx(self,et, eta):
    found = False
    for etBinIdx in range(len(self._etBins)-1):
      if et >= self._etBins[etBinIdx] and  et <= self._etBins[etBinIdx+1]:
        found = True
        break
    if not found: etBinIdx = None
    # Fix eta value if > 2.5
    for etaBinIdx in range(len(self._etaBins)-1):
      if eta >= self._etaBins[etaBinIdx] and  eta <= self._etaBins[etaBinIdx+1]:
        break
    return etBinIdx, etaBinIdx
