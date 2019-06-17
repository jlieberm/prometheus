
__all__ = ['RingerSelectorTool']


from prometheus import Algorithm
from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from Gaugi.gtypes import NotSet
import numpy as np

from EventAtlas import *


class RingerSelectorTool(Algorithm):

  def __init__(self, name, constants, thresholds, useOutputBeforeTheActivationFunction=True, **kw):
    Algorithm.__init__(self, name, **kw)
    self._asg           = NotSet
    self._nnOutput=-999
    self._constantsCalibPath = constants
    self._thresholdsCalibPath = thresholds
    self._useOutputBeforeTheActivationFunction = useOutputBeforeTheActivationFunction

  def asg(self):
    return self._asg


  def initialize(self):
    import cppyy
    cppyy.loadDict("libprometheus")
    from ROOT import prometheus
    # create the ASG selector tool
    self._asg = prometheus.ElectronRingerSelector(self._name)
    # set other properties
    self._asg.setConstantsCalibPath( self._constantsCalibPath )
    self._asg.setThresholdsCalibPath( self._thresholdsCalibPath )
    # Initialize the ASG Tool
    if( not self._asg.initialize()):
      MSG_FATAL( self, 'Can not initialize the Ringer Selector ASG.')
    
    MSG_INFO( self, "RingerSelectorTool was initialized." )
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS


  def accept( self, eg, mu ):
    if eg.isGoodRinger():
      nnOutput = self.calculate( eg, mu ) 
      return bool(self._asg.accept( nnOutput, eg.et(), eg.eta(), mu ))
    else:
      return True


  def calculate(self, eg, mu):

    if type(eg) is FastElectron:
      return self._asg.calculate( eg.emCluster().ringsE(), eg.et(), eg.eta(), mu,
                                  # fast track variables
                                  eg.etOverPt(), 
                                  eg.trkClusDeta(), 
                                  eg.trkClusDphi()) 
    elif type(eg) is FastCalo:
      return self._asg.calculate( eg.ringsE(), eg.et(), eg.eta(), mu ) 
    
    elif type(eg) is Electron:

      if self._asg.useCaloRings() and self._asg.useShowerShape() and self._asg.useTrack():
        return self._asg.calculate( eg.ringsE(), eg.et(), eg.eta(), mu,
                                    # standard shower shapes
                                    eg.showerShapeValue(EgammaParameters.Eratio),
                                    eg.showerShapeValue(EgammaParameters.Reta),
                                    eg.showerShapeValue(EgammaParameters.Rphi),
                                    eg.showerShapeValue(EgammaParameters.Rhad),
                                    eg.showerShapeValue(EgammaParameters.weta2),
                                    eg.showerShapeValue(EgammaParameters.f1),
                                    eg.showerShapeValue(EgammaParameters.f3),
                                    # standard track variables
                                    eg.trackCaloMatchValue(TrackCaloMatchType.deltaEta1),
                                    eg.trackParticle().DeltaPOverP(),
                                    eg.deltaPhiRescaled2(),
                                    eg.trackParticle().d0significance(),
                                    eg.trackParticle().d0(),
                                    eg.trackParticle().trans_TRT_PID() ) 
      elif self._asg.useCaloRings() and self._asg.useShowerShape():
        return self._asg.calculate( eg.ringsE(), eg.et(), eg.eta(), mu,
                                    # standard shower shapes
                                    eg.showerShapeValue(EgammaParameters.Eratio),
                                    eg.showerShapeValue(EgammaParameters.Reta),
                                    eg.showerShapeValue(EgammaParameters.Rphi),
                                    eg.showerShapeValue(EgammaParameters.Rhad),
                                    eg.showerShapeValue(EgammaParameters.weta2),
                                    eg.showerShapeValue(EgammaParameters.f1),
                                    eg.showerShapeValue(EgammaParameters.f3))
      elif self._asg.useCaloRings()  and self._asg.useTrack():
        
        return self._asg.calculate( eg.ringsE(), eg.et(), eg.eta(), mu,
                                    # standard track variables
                                    eg.trackCaloMatchValue(TrackCaloMatchType.deltaEta1),
                                    eg.trackParticle().DeltaPOverP(),
                                    eg.deltaPhiRescaled2(),
                                    eg.trackParticle().d0significance(),
                                    eg.trackParticle().d0(),
                                    eg.trackParticle().trans_TRT_PID() ) 
      elif self._asg.useTrack():
        return self._asg.calculate( eg.et(), eg.eta(), mu,
                                    # standard track variables
                                    eg.trackCaloMatchValue(TrackCaloMatchType.deltaEta1),
                                    eg.trackParticle().DeltaPOverP(),
                                    eg.deltaPhiRescaled2(),
                                    eg.trackParticle().d0significance(),
                                    eg.trackParticle().d0(),
                                    eg.trackParticle().trans_TRT_PID() ) 
 
      else:
        return self._asg.calculate( eg.ringsE(), eg.et(), eg.eta(), mu)



  def getDiscriminant(self):
    if self._useOutputBeforeTheActivationFunction:
      return self._asg.outputBeforeTheActivationFunction()
    else:
      return self._asg.output()





