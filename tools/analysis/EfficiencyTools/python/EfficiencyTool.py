
__all__ = ['EfficiencyTool']

from EmulationTools import Chain, Group
from Gaugi.messenger.macros import *
from Gaugi import Algorithm, StatusCode
from EfficiencyTools import EfficiencyMode
from CommonTools import AlgBase

class EfficiencyTool( AlgBase ):
  
  _triggerLevels = ['L1Calo','L2Calo','L2','EFCalo','HLT']

  def __init__(self, name, **kw):
    AlgBase.__init__(self, name)
    self._groups = []
    self._basepath = 'Event/EfficiencyTool'



  def addGroup( self, group ): 
    from Gaugi import ToolSvc
    emulator = ToolSvc.retrieve( "Emulator" )
    emulator+=group.chain()
    self._groups.append( group )  


  def initialize(self):
    
    import numpy as np
    sg = self.getStoreGateSvc()
    from CommonTools.constants import zee_etbins, jpsiee_etbins, default_etabins, nvtx_bins, high_nvtx_bins
    #et_bins  = zee_etbins
    eta_bins = default_etabins
    nvtx_bins.extend(high_nvtx_bins)
    #eta_bins = [0,0.6,0.8,1.15,1.37,1.52,1.81,2.01,2.37,2.47]
    et_bins = jpsiee_etbins if self.doJpsiee() else [4.,7.,10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,80.,150.] 

    from ROOT import TH1F, TH2F, TProfile, TProfile2D
    for group in self._groups:
      # Get the chain object
      chain = group.chain()
      for dirname in ( self._triggerLevels if type(chain) is Chain else ['Selector'] ):

        sg.mkdir( self._basepath+'/'+chain.name()+'/Efficiency/'+dirname )
        
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
        sg.addHistogram( TH2F('match_etVsEta', "Passed;E_{T};#eta;Count", len(et_bins)-1, np.array(et_bins), len(eta_bins)-1, np.array(eta_bins)) )
        sg.addHistogram( TH2F('etVsEta' , "Total;E_{T};#eta;Count", len(et_bins)-1,  np.array(et_bins), len(eta_bins)-1, np.array(eta_bins)) )
        sg.addHistogram( TProfile2D('eff_etVsEta' , "Total;E_{T};#eta;Count", len(et_bins)-1,  np.array(et_bins), len(eta_bins)-1, np.array(eta_bins)) )

    self.init_lock()
    return StatusCode.SUCCESS 

    

  def execute(self, context):
  
    from Gaugi.constants import GeV
    # Retrieve Electron container
    elCont = context.getHandler( "ElectronContainer" )

    for group in self._groups:
      chain = group.chain()
      if type(chain) is Chain:

        for el in elCont:
          if el.et()  < (group.etthr()- 5)*GeV:  continue 
          if abs(el.eta())>2.47: continue
          dirname = self._basepath+'/'+chain.name()+'/Efficiency'
          accept = self.accept( chain.name() )
          self.fillEfficiency(dirname+'/'+'L1Calo', el, group.etthr(), group.pidname(), accept.getCutResult("L1Calo") )
          self.fillEfficiency(dirname+'/'+'L2Calo', el, group.etthr(), group.pidname(), accept.getCutResult("L2Calo") )
          self.fillEfficiency(dirname+'/'+'L2'    , el, group.etthr(), group.pidname(), accept.getCutResult("L2")     )
          self.fillEfficiency(dirname+'/'+'EFCalo', el, group.etthr(), group.pidname(), accept.getCutResult("EFCalo") )
          self.fillEfficiency(dirname+'/'+'HLT'   , el, group.etthr(), group.pidname(), accept.getCutResult("HLT")    )  

      else:
        MSG_FATAL( self, "Chain type not reconized." )

    return StatusCode.SUCCESS 



  def fillEfficiency( self, dirname, el, etthr, pidword, isPassed ):
  

    sg = self.getStoreGateSvc()
    from Gaugi.constants import GeV
    
    pid = el.accept(pidword) if pidword else True

    eta = el.caloCluster().etaBE2()
    et = el.et()/GeV
    phi = el.phi()
    evt = self.getContext().getHandler("EventInfoContainer")
    avgmu = evt.avgmu()
    nvtx = evt.nvtx()
    pw = evt.MCPileupWeight()

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
    
    sg = self.getStoreGateSvc()
    for group in self._groups:
      chain = group.chain()
      MSG_INFO( self, '{:-^78}'.format((' %s ')%(chain.name())))
      if type(chain) is Chain:
        for trigLevel in self._triggerLevels:
          dirname = self._basepath+'/'+chain.name()+'/Efficiency/'+trigLevel
          total  = sg.histogram( dirname+'/eta' ).GetEntries()
          passed = sg.histogram( dirname+'/match_eta' ).GetEntries()
          eff = passed/float(total) * 100. if total>0 else 0
          eff=('%1.2f')%(eff); passed=('%d')%(passed); total=('%d')%(total)
          stroutput = '| {0:<30} | {1:<5} ({2:<5}, {3:<5}) |'.format(trigLevel,eff,passed,total)
          MSG_INFO( self, stroutput)
      else:
        pass
        
      MSG_INFO(self, '{:-^78}'.format((' %s ')%('-')))
    self.fina_lock()
    return StatusCode.SUCCESS 




