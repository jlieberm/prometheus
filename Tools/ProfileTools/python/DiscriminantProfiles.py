__all__ = ['DiscriminantProfiles']
from prometheus.tools.atlas.profiles.ProfileToolBase  import ProfileToolBase
from prometheus.core                                  import StatusCode

class DiscriminantProfiles( ProfileToolBase ):
  def __init__(self, name, **kw):
    ProfileToolBase.__init__(self, name, **kw)

  def initialize(self):
    
    sg = selg.getStoreGateSvc()
    # Fill all histograms needed
    # Loop over main dirs
    from ROOT import TH2F
    import numpy as np
    from prometheus.tools.atlas.common.constants import nvtx_bins
    for etBinIdx in range(len(self._etBins)-1):
      for etaBinIdx in range(len(self._etaBins)-1):
        for algname in self._discrList:
          path = self.getPath(etBinIdx, etaBinIdx) + '/' + algname
          sg.mkdir( path )
          # create neural network histograms
          sg.addHistogram(TH2F('discriminantVsNvtx', 
            'Offline Pileup as function of the discriminant;discriminant;nvtx;Count',
            1000, -12,8,len(nvtx_bins)-1,np.array(nvtx_bins)) ) 
          sg.addHistogram(TH2F('discriminantVsMu'  , 
            'Online Pileup as function of the discriminant;discriminant;nvtx;Count' ,
            1000, -12,8,100 - 1,0,100) ) 
    return StatusCode.SUCCESS

  def execute(self, context):

    sg = selg.getStoreGateSvc()
    if self._doTrigger: # Online
      obj = context.getHandler( "HLT__FastCaloContainer" )
    else: # Offline
      obj = context.getHandler('ElectronContainer')

    from prometheus.tools.atlas.common.constants import GeV
    etBinIdx, etaBinIdx = self._retrieveBinIdx( obj.et()/GeV, abs(obj.eta()) )
    if etBinIdx is None or etaBinIdx is None:
      self._warning("Ignoring event with none index. Its et[GeV]/eta is: %f/%f", obj.et/GeV, obj.eta)
      return StatusCode.SUCCESS
    # make the et/eta string path
    eventInfo = context.getHandler( "EventInfoContainer" )
    nvtx = eventInfo.nvtx()
    avgmu = eventInfo.avgmu()
 
    for algname in self._discrList:
      path = self.getPath(etBinIdx, etaBinIdx) + '/' + algname
      try:
        if self.dataframe is Dataframe.PhysVal_v2:
          obj = context.getHandler( "HLT__ElectronContainer" )
        elif self.dataframe is Dataframe.SkimmedNtuple_v2:
          obj = context.getHandler( "HLT__FastCaloContainer" )
        # get the ringer RNN discriminant
        discriminant = obj.getDecor(algname+'_discriminant')

        try:
          sg.histogram(path+'/discriminantVsMu').Fill(discriminant,avgmu)
        except AttributeError:
          self._fatal("Couldn't fill histogram at path: %s", path + '/discriminantVsMu')
        sg.histogram(path+'/discriminantVsNvtx').Fill(discriminant,nvtx)
      except:
        pass
    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS
  
