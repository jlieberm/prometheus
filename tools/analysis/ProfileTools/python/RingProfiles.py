__all__ = ['RingProfiles']
from ProfileTools import ProfileToolBase
from Gaugi import StatusCode
from Gaugi.messenger.macros import *
from prometheus import Dataframe as DataframeEnum

class RingProfiles( ProfileToolBase ):

  def __init__(self, name, dataframe**kw):
    ProfileToolBase.__init__(self, name, **kw)

  @property
  def doZeros(self):
    self._doZeros

  @doZeros.setter
  def doZeros(self, v):
    self._doZeros=v
    self.bookCaloRings()

  def initialize(self):
    ProfileToolBase.initialize()
    # Fill all histograms needed
    # Loop over main dirs
    sg = selg.getStoreGateSvc()
    from ROOT import TH1F, TH1I
    from CommonTools.constants import ringNBins, ringHighEdges, ringLowerEdges
    for etBinIdx in range(len(self._etBins)-1):
      for etaBinIdx in range(len(self._etaBins)-1):
        path = self.getPath(etBinIdx, etaBinIdx)
        sg.mkdir( path )
        MSG_DEBUG( self, 'Initializing path: %s', path)
        # Loop over all calo rings
        for r, nbins, le, he in zip( range( 100 ), ringNBins, ringLowerEdges, ringHighEdges):
          sg.addHistogram(TH1F('ring_%d_%s' % (r, self.binStr(etBinIdx,etaBinIdx), ),'Ring %d E_{T} Profile;E_T (MeV); Counts/bin' % r, nbins , le, he))
          sg.addHistogram(TH1I('ring_%d_%s_specialBins' % (r, self.binStr(etBinIdx,etaBinIdx), ),'Ring %d Special Bins;Special Bins; Counts/bin' % r, 3 , 0, 3))
        # loop over rings
    path_integrated = self.getPath()
    sg.mkdir( path_integrated )
    MSG_DEBUG( self, 'Initializing path_integrated: %s', path_integrated)
    for r, nbins, le, he in zip( range( 100 ), ringNBins, ringLowerEdges, ringHighEdges):
      sg.addHistogram(TH1F('ring_%d_%s' % (r, self.binStr(), ),'Ring %d E_{T} Profile;E_T (MeV); Counts/bin' % r, nbins , le, he))
      sg.addHistogram(TH1I('ring_%d_%s_specialBins' % (r, self.binStr(), ),'Ring %d Special Bins;Special Bins; Counts/bin' % r, nbins , le, he))
    return StatusCode.SUCCESS

  def execute(self, context):
    if self._doTrigger: # Online
      obj = context.getHandler( "HLT__FastCaloContainer" )
    elif self._dataframe is DataframeEnum.Electron_v1:
      obj   = context.getHandler( "ElectronContainer" )
    elif self._dataframe is DataframeEnum.Photon_v1:
      obj    = context.getHandler( "PhotonContainer" )
    else:
      obj    = context.getHandler( "ElectronContainer" )

    sg = selg.getStoreGateSvc()
    from Gaugi.constants import GeV
    etBinIdx, etaBinIdx = self._retrieveBinIdx( obj.et()/GeV, abs(obj.eta()) )
    if etBinIdx is None or etaBinIdx is None:
      MSG_WARNING( self, "Ignoring event with none index. Its et[GeV]/eta is: %f/%f", obj.et()/GeV, obj.eta())
      return StatusCode.SUCCESS
    path = self.getPath(etBinIdx, etaBinIdx)
    path_integrated = self.getPath()
    # make the et/eta string path
    rings = obj.ringsE()
    for r in range(len(rings)):
      try:
        if rings[r] == 0.:
          sg.histogram( path + '/ring_%d_%s_specialBins' % (r, self.binStr(etBinIdx,etaBinIdx), ) ).Fill( 0. )
          sg.histogram( path_integrated + '/ring_%d_%s_specialBins' % (r, self.binStr(), ) ).Fill( 0. )
        else:
          sg.histogram( path + '/ring_%d_%s' % (r, self.binStr(etBinIdx,etaBinIdx), ) ).Fill(  rings[r] )
          sg.histogram( path_integrated + '/ring_%d_%s' % (r, self.binStr(), ) ).Fill( rings[r] )
      except AttributeError as e:
        MSG_FATAL( self,"Couldn't fill histogram. Reason: %s", e)
    return StatusCode.SUCCESS

  def finalize(self):
    ProfileToolBase.finalize()
    return StatusCode.SUCCESS
