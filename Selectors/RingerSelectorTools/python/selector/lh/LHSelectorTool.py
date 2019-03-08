
__all__ = ['LHSelectorTool']

# move to local __init__
#import ROOT,cppyy
#ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
 
from RingerCore import  (checkForUnusedVars,retrieve_kw, NotSet)
from prometheus.dataframe.atlas import EgammaParameters,SummaryType,TrackCaloMatchType
from prometheus.core import Algorithm, StatusCode
import numpy as np
import math

class LHSelectorTool( Algorithm ):

  _asg = NotSet
  _rootTool = NotSet
  _accept = NotSet

  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    self._configFile = retrieve_kw( kw, 'ConfigFile', str())
    self._caloOnly   = retrieve_kw( kw, 'caloOnly', False  )
    checkForUnusedVars(kw)
    

  def initialize(self):

    import cppyy
    cppyy.loadDict("prometheus")
    from ROOT import prometheus
    #from ROOT import AsgElectronLikelihoodTool
    self._asg = prometheus.AsgElectronLikelihoodTool(self.name)
    self._asg.setProperty('ConfigFile', self._configFile )
    self._asg.setProperty('caloOnly'  , self._caloOnly   )
    #asg.setProperty('OutputLevel', 1)
    if self._asg.initialize().isFailure():
      self._logger.error('Can not initialize the AsgElectronLikelihoodTool.')
      return StatusCode.FAILURE    
    # get the TElectron root tool from the asg tool
    try:
      self._rootTool = self._asg.getRootTool()
    except:
      self._loggar.fatal("The ElectronPhotonSelectorTools used do not allow the getRootTool methos to retrieve de root tool.")
    
    return StatusCode.SUCCESS


  @property
  def likelihood(self):
    return self._likelihood

  @likelihood.setter
  def likelihood(self,v):
    self._likelihood=v

  def getLikelihood(self):
    return self._likelihood

  def accept(self, el, mu):
    
    self._likelihood = -999
    # get the calo cluster
    cluster = el.caloCluster()

    if not cluster:
      self._logger.warning('There is no caloCluster.')
      return False

    energy = cluster.energy()
    eta = cluster.etaBE2()

    if math.fabs(eta) > 2.5:
      self._logger.warning('Failed, cluster->etaBE(2) range.')
      return False


    if (el.trackParticle() and not self._caloOnly):
      et = energy/(math.cosh(el.trackParticle().eta())) if (math.cosh(el.trackParticle().eta()) != 0.0) else 0.0
    else:
      et = energy/(math.cosh(eta)) if (math.cosh(eta) != 0.0) else 0.0

    wtots1 = el.showerShapeValue(EgammaParameters.wtots1)
    # number of track hits
    nSiHitsPlusDeadSensors=0.0; nPixHitsPlusDeadSensors=0.0; passBLayerRequirement=False 
    d0=0.0; deltaEta=0.0; deltaPhiRescaled2=0.0; EoverP=0.0

    if not self._caloOnly:
      track = el.trackParticle()
      if track:
        nSiHitsPlusDeadSensors  = self.numberOfSiliconHitsAndDeadSensors(track)
        nPixHitsPlusDeadSensors = self.numberOfPixelHitsAndDeadSensors(track)
        passBLayerRequirement   = self.passBLayerRequirement(track)
        d0 = track.d0()
        EOverP = math.fabs(track.qOverP()) * energy
      else:
        self._logger.warning('Failed, no track particle')

      deltaEta=  el.trackCaloMatchValue(TrackCaloMatchType.deltaEta1)
      deltaPhiRescaled2 = el.trackCaloMatchValue(TrackCaloMatchType.deltaPhiRescaled2)



    wstot = el.showerShapeValue(EgammaParameters.wtots1)
    ip=float(mu); convBit=0;
    # calculate the disciminant LH value
    self._likelihood = float(self.calculate(el,mu))
    # Get the answer from the underlying ROOT tool
    self._accept = self._rootTool.accept( self._likelihood,
                             eta,
                             et,
                             int(nSiHitsPlusDeadSensors),
                             int(nPixHitsPlusDeadSensors),
                             passBLayerRequirement,
                             convBit,
                             d0,
                             deltaEta,
                             deltaPhiRescaled2,
                             wstot,
                             EoverP,
                             ip
                           )

    return bool(self._accept)

  def finalize(self):
    self._asg.finalize()
    return StatusCode.SUCCESS


  def calculate(self, el, mu):

    cluster = el.caloCluster()
    if ( not cluster ):
      self._logger.warning("Failed, no cluster.")
      return False
    
    energy =  cluster.energy()
    eta = cluster.etaBE2() 
    if ( math.fabs(eta) > 300.0 ):
      self._logger.warning("Failed, eta range.")
      return False
      
    # transverse energy of the electron (using the track eta) 
    # const double et = eg->pt() 
    if (el.trackParticle() and not self._caloOnly):
      et = energy/math.cosh(el.trackParticle().eta()) if (math.cosh(el.trackParticle().eta()) != 0.0) else 0.0
    else:
      et = energy/math.cosh(eta) if (math.cosh(eta) != 0.0) else 0.0

    # number of track hits and other track quantities
    trackqoverp=0.0
    d0=0.0
    d0sigma=0.0
    dpOverp=0.0
    TRT_PID=0.0
    trans_TRT_PID=0.0
    deltaEta=0.0
    deltaPhiRescaled2=0.0

    if (not self._caloOnly):
      # retrieve associated TrackParticle
      track = el.trackParticle()    
      if track:
        trackqoverp = track.qOverP()
        d0 = track.d0()
        d0sigma=track.sigd0()
        trans_TRT_PID = track.trans_TRT_PID()
        dpOverp = track.DeltaPOverP()
      else:
        self._logger.warning ( "Failed, no track particle: et= "+ et + "eta= " + eta )

    Reta=0.0; Rphi=0.0;  Rhad1=0.0; Rhad=0.0; ws3=0.0; w2=0.0; f1=0.0; Eratio=0.0; f3=0.0;

    # reta = e237/e277
    Reta = el.showerShapeValue(EgammaParameters.Reta)
    # rphi e233/e237
    Rphi = el.showerShapeValue(EgammaParameters.Rphi)
    # rhad1 = ethad1/et
    Rhad1 = el.showerShapeValue(EgammaParameters.Rhad1)
    # rhad = ethad/et
    Rhad = el.showerShapeValue(EgammaParameters.Rhad)
    # shower width in 3 strips in 1st sampling
    #ws3 = el.showerShapeValue(EgammaParameters.weta1)
    # shower width in 2nd sampling
    w2 = el.showerShapeValue(EgammaParameters.weta2)
    # fraction of energy reconstructed in the 1st sampling
    f1 = el.showerShapeValue(EgammaParameters.f1)
    # E of 2nd max between max and min in strips
    Eratio = el.showerShapeValue(EgammaParameters.Eratio)
    # fraction of energy reconstructed in the 3rd sampling
    f3 = el.showerShapeValue(EgammaParameters.f3)

    if not self._caloOnly:
      deltaEta = el.trackCaloMatchValue(TrackCaloMatchType.deltaEta1)
      # difference between the cluster phi (sampling 2) and the eta of the track extrapolated from the last measurement point.
      deltaPhiRescaled2 = el.trackCaloMatchValue(TrackCaloMatchType.deltaPhiRescaled2)

    ip = float(mu)
    
    # Get the answer from the underlying ROOT tool
    return self._rootTool.calculate(  eta,
                                  et,
                                  f3,
                                  Rhad,
                                  Rhad1,
                                  Reta,
                                  w2,
                                  f1,
                                  Eratio,
                                  deltaEta,
                                  d0,
                                  d0sigma,
                                  Rphi,
                                  dpOverp,
                                  deltaPhiRescaled2,
                                  trans_TRT_PID,
                                  ip
                                  )
  
  def getAccept(self):
    return self._accept

  def passBLayerRequirement(self, track):

    expectInnermostLayer         = track.summaryValue(SummaryType.expectBLayerHit)
    nInnermostLayerHits          = track.summaryValue(SummaryType.numberOfBLayerHits)
    nInnermostLayerOutliers      = track.summaryValue(SummaryType.numberOfBLayerOutliers)
    expectNextToInnermostLayer   = track.summaryValue(SummaryType.expectNextToInnermostPixelLayerHit)
    nNextToInnermostLayerHits    = track.summaryValue(SummaryType.numberOfNextToInnermostPixelLayerHits)
    nNextToInnermostLayerOutliers= track.summaryValue(SummaryType.numberOfNextToInnermostPixelLayerOutliers)
    if bool(expectInnermostLayer):
      passBLReq = True if (nInnermostLayerHits + nInnermostLayerOutliers > 0) else False
    elif bool(expectNextToInnermostLayer):
      passBLReq = True if ( nNextToInnermostLayerHits + nNextToInnermostLayerOutliers > 0 ) else False
    else:
      passBLReq=False

    return passBLReq

  def numberOfPixelHitsAndDeadSensors(self,track):
    return int(track.summaryValue(SummaryType.numberOfPixelHits)+track.summaryValue(SummaryType.numberOfPixelDeadSensors))

  def numberOfSCTHitsAndDeadSensors(self,track):
    return int(track.summaryValue(SummaryType.numberOfSCTHits)+track.summaryValue(SummaryType.numberOfSCTDeadSensors))

  def numberOfSiliconHitsAndDeadSensors(self,track):
    return int(self.numberOfPixelHitsAndDeadSensors(track) + self.numberOfSCTHitsAndDeadSensors(track))


