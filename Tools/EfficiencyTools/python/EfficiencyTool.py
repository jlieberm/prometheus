
__all__ = ['EfficiencyTool', 'EfficiencyMode']

from prometheus.dataframe           import ElectronCandidate
from prometheus.tools.atlas.common  import ATLASBaseTool
from prometheus.core                import StatusCode
from RingerCore                     import EnumStringification
from RingerCore                     import retrieve_kw


class EfficiencyMode(EnumStringification):
  # @brief: Use to apply the same athena trigger approch
  Athena   = 0
  # @brief: Use for selector/cut combinations
  Selector = 1


class EfficiencyTool( ATLASBaseTool ):
  
  _triggerLevels = ['L1Calo','L2Calo','L2','EFCalo','HLT']

  def __init__(self, name, **kw):
    ATLASBaseTool.__init__(self, name)
    # default trigger list
    self._itemList = []
    # Default directory
    self._basepath = 'Event/EfficiencyTool'
    # switch flag between athena/selector
    self._mode = EfficiencyMode.Selector
    from prometheus.tools.atlas.common.constants import scalefactor_etbins, scalefactor_etabins
    self._etBins = scalefactor_etbins
    self._etaBins = scalefactor_etabins



  # Athena:  ( TDT__HLT__e24_lhmedium, e24_medium )
  # Selector: ('Et>15GeV && el_lhtight && TDT__HLT__e60_lhmedium' , 'Medium' )
  def setItem( self, name, expression, mode=EfficiencyMode.Selector ):
    self._itemList.append( (name, expression, mode) )  


  def setEtBinningValues( self, etbins ):
    self._etBins = etbins

  def setEtaBinningValues( self, etabins ):
    self._etaBins = etabins


  def initialize(self):
    
    ATLASBaseTool.initialize(self)
    from prometheus.tools.atlas.common.constants import zee_etbins, jpsiee_etbins, default_etabins, nvtx_bins, high_nvtx_bins
    from ROOT         import TH1F, TH2F, TProfile, TProfile2D
    import numpy as np

    sg = self.getStoreGateSvc()

    #et_bins  = zee_etbins
    eta_bins = default_etabins
    nvtx_bins.extend(high_nvtx_bins)
    #eta_bins = [0,0.6,0.8,1.15,1.37,1.52,1.81,2.01,2.37,2.47]
    
    if self._doJpsiee:
      et_bins = jpsiee_etbins
    else:
      et_bins = [4.,7.,10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,80.,150.] 


    for item in self._itemList:
      self._mode=item[2]
      dirnames = self._triggerLevels if self._mode is EfficiencyMode.Athena else ['Selector']
      for sdir in dirnames:

        sg.mkdir( self._basepath+'/'+item[0]+'/Efficiency/'+sdir )
        sg.addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', len(et_bins)-1, np.array(et_bins)))
        sg.addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(eta_bins)-1, np.array(eta_bins)))
        sg.addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", 20, -3.2, 3.2));
        sg.addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', 20, 0, 100))
        sg.addHistogram(TH1F('nvtx' ,'N_{vtx} distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
        sg.addHistogram(TH1F('match_et','E_{T} matched distribution;E_{T};Count', len(et_bins)-1, np.array(et_bins)))
        sg.addHistogram(TH1F('match_eta','#eta matched distribution;#eta;Count', len(eta_bins)-1, np.array(eta_bins)))
        sg.addHistogram(TH1F("match_phi", "#phi matched distribution; #phi ; Count", 20, -3.2, 3.2));
        sg.addHistogram(TH1F('match_mu' ,'<#mu> matched distribution;<#mu>;Count', 20, 0, 100))
        sg.addHistogram(TH1F('match_nvtx' ,'N_{vtx} matched distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
        sg.addHistogram(TProfile("eff_et", "#epsilon(E_{T}); E_{T} ; Efficiency" , len(et_bins)-1, np.array(et_bins)))
        sg.addHistogram(TProfile("eff_eta", "#epsilon(#eta); #eta ; Efficiency"  , len(eta_bins)-1,np.array(eta_bins)))
        sg.addHistogram(TProfile("eff_phi", "#epsilon(#phi); #phi ; Efficiency", 20, -3.2, 3.2));
        sg.addHistogram(TProfile("eff_mu", "#epsilon(<#mu>); <#mu> ; Efficiency", 20, 0, 100));	
        sg.addHistogram(TProfile("eff_nvtx", "#epsilon(N_{vtx}); N_{vtx} ; Efficiency", len(nvtx_bins)-1, np.array(nvtx_bins)));	
        sg.addHistogram( TH2F('match_etVsEta', "Passed;E_{T};#eta;Count", len(self._etBins)-1, np.array(self._etBins), 
          len(self._etaBins)-1, np.array(self._etaBins)) )
        sg.addHistogram( TH2F('etVsEta' , "Total;E_{T};#eta;Count", len(self._etBins)-1,  np.array(self._etBins), 
          len(self._etaBins)-1, np.array(self._etaBins)) )
        sg.addHistogram( TProfile2D('eff_etVsEta' , "Total;E_{T};#eta;Count", len(self._etBins)-1,  np.array(self._etBins), 
          len(self._etaBins)-1, np.array(self._etaBins)) )


    self.init_lock()
    return StatusCode.SUCCESS 

    

  def execute(self, context):
  
    from prometheus.tools.atlas.common.constants import GeV
    # Retrieve Electron container
    elCont = context.getHandler( "ElectronContainer" )
    self._evt = context.getHandler("EventInfoContainer")
    
    
    for item in self._itemList:
      self._mode=item[2] ### switch to analysis mode 
      if self._mode is EfficiencyMode.Athena:
        info = self.getTrigInfo(item[1])
        for el in elCont:
          if el.et()/GeV < (info['etthr']- 5):  continue 
          dirname = self._basepath+'/'+item[0]+'/Efficiency'
          self.fillEfficiency(dirname+'/'+'L1Calo', el, info['etthr'], info['pidword'], self.isPassed(info['core']+'__L1Calo__'+info['trigger']))
          self.fillEfficiency(dirname+'/'+'L2Calo', el, info['etthr'], info['pidword'], self.isPassed(info['core']+'__L2Calo__'+info['trigger']))
          self.fillEfficiency(dirname+'/'+'L2'    , el, info['etthr'], info['pidword'], self.isPassed(info['core']+'__L2__'+info['trigger']    ))
          self.fillEfficiency(dirname+'/'+'EFCalo', el, info['etthr'], info['pidword'], self.isPassed(info['core']+'__EFCalo__'+info['trigger']))
          self.fillEfficiency(dirname+'/'+'HLT'   , el, info['etthr'], info['pidword'], self.isPassed(info['core']+'__HLT__'+info['trigger']   ))  
      elif self._mode is EfficiencyMode.Selector:
        # retrieve internal selection tool from the main framework
        dirname = self._basepath+'/'+item[0]+'/Efficiency'
        etthr = self.re().search_et(item[1])
        pidword = self.re().search_pid(item[1])
        # el_lhtight && Et>15GeV && HLT__isElectronRingerTight 
        for el in elCont:
          if abs(el.eta())>2.47: continue
          if el.et()/GeV < (etthr - 5):  continue 
          self.fillEfficiency(dirname+'/'+'Selector' , el, etthr, pidword, self.re().apply(item[1])  )

    return StatusCode.SUCCESS 


  def fillEfficiency( self, dirname, el, etthr, pidword, isPassed ):
    
    from prometheus.tools.atlas.common.constants import GeV
    pid = el.accept(pidword)
    eta = el.caloCluster().etaBE2()
    et = el.et()/GeV
    phi = el.phi()
    avgmu = self._evt.avgmu()
    nvtx = self._evt.nvtx()
 
    evt = self.getContext().getHandler("EventInfoContainer")
    pw = evt.MCPileupWeight()

    pid=True
    if pid: 
      sg.histogram( dirname+'/et' ).Fill(et, pw)
      if et > etthr+1.0:
        sg.histogram( dirname+'/eta' ).Fill(eta, pw)
        sg.histogram( dirname+'/phi' ).Fill(phi, pw)
        sg.histogram( dirname+'/mu' ).Fill(avgmu, pw)
        sg.histogram( dirname+'/nvtx' ).Fill(nvtx, pw)
        sg.histogram( dirname+'/etVsEta' ).Fill(et,eta, pw)

      if isPassed:
        sg.histogram( dirname+'/match_et' ).Fill(et, pw)
        sg.histogram( dirname+'/eff_et' ).Fill(et,1, pw)
        
        if et > etthr+1.0:
          sg.histogram( dirname+'/match_eta' ).Fill(eta, pw)
          sg.histogram( dirname+'/match_phi' ).Fill(phi, pw)
          sg.histogram( dirname+'/match_mu' ).Fill(avgmu, pw)
          sg.histogram( dirname+'/match_nvtx' ).Fill(nvtx, pw)
          sg.histogram( dirname+'/match_etVsEta' ).Fill(et,eta, pw)
          sg.histogram( dirname+'/eff_eta' ).Fill(eta,1, pw)
          sg.histogram( dirname+'/eff_phi' ).Fill(phi,1, pw)
          sg.histogram( dirname+'/eff_mu' ).Fill(avgmu,1, pw)
          sg.histogram( dirname+'/eff_nvtx' ).Fill(nvtx,1, pw)
          sg.histogram( dirname+'/eff_etVsEta' ).Fill(et,eta,1, pw)

      else:
        sg.histogram( dirname+'/eff_et' ).Fill(et,0)
        if et > etthr+1.0:
          sg.histogram( dirname+'/eff_eta' ).Fill(eta,0, pw)
          sg.histogram( dirname+'/eff_phi' ).Fill(phi,0, pw)
          sg.histogram( dirname+'/eff_mu' ).Fill(avgmu,0, pw)
          sg.histogram( dirname+'/eff_nvtx' ).Fill(nvtx,0, pw)
          sg.histogram( dirname+'/eff_etVsEta' ).Fill(et,eta,0, pw)



  def finalize(self):
    
    for item in self._itemList:
      self._logger.info('{:-^78}'.format((' %s ')%(item[0])))
      self._mode=item[2]
      if self._mode is EfficiencyMode.Athena:
        for trigLevel in self._triggerLevels:
          dirname = self._basepath+'/'+item[0]+'/Efficiency/'+trigLevel
          total  = sg.histogram( dirname+'/eta' ).GetEntries()
          passed = sg.histogram( dirname+'/match_eta' ).GetEntries()
          eff = passed/float(total) * 100. if total>0 else 0
          eff=('%1.2f')%(eff); passed=('%d')%(passed); total=('%d')%(total)
          stroutput = '| {0:<30} | {1:<5} ({2:<5}, {3:<5}) |'.format(trigLevel,eff,passed,total)
          self._logger.info(stroutput)

      elif self._mode is EfficiencyMode.Selector:
        dirname = self._basepath+'/'+item[0]+'/Efficiency/Selector'
        total  = sg.histogram( dirname+'/eta' ).GetEntries()
        passed = sg.histogram( dirname+'/match_eta' ).GetEntries()
        eff = passed/float(total) * 100. if total>0 else 0
        eff=('%1.2f')%(eff); passed=('%d')%(passed); total=('%d')%(total)
        stroutput = '| {0:<30} | {1:<5} ({2:<5}, {3:<5}) |'.format('Efficiency',eff,passed,total)
        self._logger.info(stroutput)

      self._logger.info('{:-^78}'.format((' %s ')%('-')))
    self.fina_lock()
    return StatusCode.SUCCESS 




