

__all__ = ['BasicInfoProfiles']
from prometheus.core                                  import StatusCode
from prometheus.tools.atlas.profiles.ProfileToolBase  import ProfileToolBase
from prometheus.tools.atlas.common.constants          import (  basicInfoNBins, basicInfoLowerEdges, basicInfoHighEdges, 
                                                                default_etabins, coarse_etbins, nvtx_bins )





class BasicInfoProfiles( ProfileToolBase ):

  def __init__(self, name, **kw):
    ProfileToolBase.__init__(self, name, **kw)
    from prometheus.tools.atlas.common.constants import basicInfoNBins
    self.basicInfos = basicInfoNBins.keys()

  def initialize(self):
    sg = self.getStoreGateSvc()
    from ROOT import TH1F
    # Fill all histograms needed
    from prometheus.tools.atlas.common.constants import basicInfoLatexStr
    for etBinIdx in range(len(self._etBins)-1):
      for etaBinIdx in range(len(self._etaBins)-1):
        # if doSpecialBins
        path = self.getPath(etBinIdx, etaBinIdx)
        sg.mkdir( path )
        self._debug('Initializing path: %s', path)
        for var in self.basicInfos:
          latexvar = basicInfoLatexStr(var)
          if var == 'eta':
            lb = self._etaBins[etaBinIdx]; ub = self._etaBins[etaBinIdx+1]; nbins = 10
          elif var == 'et':
            lb = self._etBins[etBinIdx]; ub = self._etBins[etBinIdx+1]; nbins = 10
            if etBinIdx+2 == len(self._etBins) and self._etBins[etBinIdx+1] >= 13000:
              ub = 200; nbins = 20
          else:
            lb = basicInfoLowerEdges[var]; ub = basicInfoHighEdges[var]; nbins = basicInfoNBins[var]
          sg.addHistogram(TH1F(var + "_" + self.binStr(etBinIdx,etaBinIdx), latexvar + ' profile;' + latexvar + ';Counts/bin', nbins, lb, ub ))
    import numpy as np
    path_integrated = self.getPath()
    sg.mkdir( path_integrated )
    self._debug('Initializing path: %s', path_integrated)
    for var in self.basicInfos:
      latexvar = basicInfoLatexStr( var )
      if var == 'eta':
        sg.addHistogram(TH1F(var + "_" + self.binStr(), latexvar + ' profile;' + latexvar + ';Counts/bin', len(default_etabins)-1, np.array(default_etabins) ))
      elif var == 'et':
        sg.addHistogram(TH1F(var + "_" + self.binStr(), latexvar + ' profile;' + latexvar + ' [GeV];Counts/bin', len(coarse_etbins)-1, np.array(coarse_etbins) ))
      else:
        nBins = basicInfoNBins[var]
        lb = basicInfoLowerEdges[var]
        ub = basicInfoHighEdges[var]
        sg.addHistogram(TH1F(var + "_" + self.binStr(), latexvar + ' profile;' + latexvar + ';Counts/bin', nbins, lb, ub ))
    return StatusCode.SUCCESS

  def execute(self, context):
    sg = self.getStoreGateSvc()
    if self._doTrigger:
      obj = context.getHandler('HLT__FastCaloContainer')
    else:
      obj = context.getHandler('ElectronContainer')

    # If is trigger, the position must use the trigger et/eta positions.
    from prometheus.tools.atlas.common.constants import GeV
    etBinIdx, etaBinIdx = self._retrieveBinIdx( obj.et()/GeV, abs(obj.eta()) )
    if etBinIdx is None or etaBinIdx is None:
      self._warning("Ignoring event with none index. Its et[GeV]/eta is: %f/%f", obj.et()/GeV, obj.eta())
      return StatusCode.SUCCESS

    # Force this to be the offline object
    el =context.getHandler('ElectronContainer')
    eventInfo = context.getHandler( "EventInfoContainer" )
    # Fill binned information 
    path = self.getPath(etBinIdx, etaBinIdx)
    path_integrated = self.getPath()
    for var in self.basicInfos:
      try:
        value = getattr(el,var)()
      except:
        value = getattr(eventInfo,var)()
      if var == "et": value /= GeV
      try:
        sg.histogram(path+'/'+var+"_"+self.binStr(etBinIdx,etaBinIdx)).Fill(value)
      except AttributeError, e:
        self._fatal("Couldn't fill histogram. Reason: %s", e)
      try:
        sg.histogram(path_integrated+'/'+var+"_"+self.binStr()).Fill(value)
      except AttributeError, e:
        self._fatal("Couldn't fill histogram. Reason: %s", e)

    return StatusCode.SUCCESS

  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS
