
__all__ = ['RingerSelectorTool']

from RingerCore      import EnumStringification
from RingerCore      import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars, \
                            expandFolders, csvStr2List, NotSet

from prometheus.core                            import StatusCode, Algorithm
from prometheus.dataframe.atlas                 import *
from prometheus.tools.atlas.common              import ATLASBaseTool
from prometheus.tools.atlas.common.constants    import *

import numpy as np




class RingerSelectorTool(Algorithm):

  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)
    from prometheus.tools.atlas.common.selector.ringer import ElectronRingerPid
    self._asg           = NotSet
    self._calibPath     = retrieve_kw( kw, 'CalibPath', None )
    self._workingPoint  = retrieve_kw( kw, 'WorkingPoint', ElectronRingerPid.VeryLoose)
    self._fromPickle    = retrieve_kw( kw, 'FromPickle' , False)
    self._useTileCal    = retrieve_kw( kw, 'UseTileCal' , True)
    self._nnOutput=-999
 
  def asg(self):
    return self._asg


  def initialize(self):
    import cppyy
    cppyy.loadDict("prometheus")
    from ROOT import prometheus
    #from ROOT import AsgElectronRingerSelector
    from prometheus.tools.atlas.common.selector.ringer import Norm1, RingerPidConfs, ElectronRingerPid
    from RingerCore import list_to_stdvector
    # TODO: Do this an external configuration for future.
    preproc = Norm1()
    # create the ringer conf helper
    theRingerPIDConf = RingerPidConfs()
    if self._calibPath: # point to other calib path
      theRingerPIDConf.setCalibPath(self._calibPath)
    # create the ASG selector tool
    self._asg = prometheus.AsgElectronRingerSelector(self.name)
    pidname = ElectronRingerPid.tostring(self._workingPoint).lower()
    # set other properties
    self._asg.setProperty('CalibPathConstants', theRingerPIDConf.get_constants_path('e', pidname) )
    self._asg.setProperty('CalibPathThresholds', theRingerPIDConf.get_cutDefs_path('e', pidname) )
    self._asg.setProperty('NRings', list_to_stdvector('unsigned int',preproc.NRings ))
    self._asg.setProperty('SectionRings', list_to_stdvector('unsigned int',preproc.SectionRings) )
    self._asg.setProperty('NormalisationRings', list_to_stdvector('unsigned int',preproc.NormalisationRings  ))
    self._asg.setProperty('UseTileCal', self._useTileCal  )
    # Initialize the ASG Tool
    if(self._asg.initialize().isFailure()):
      self._logger.fatal('Can not initialize the Ringer Selector ASG.')
      return StatusCode.FAILURE   
       
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS


  def accept( self, eg, mu ):
    if eg.isGoodRinger():
      self._nnOutput = self.calculate( eg, mu ) 
      return bool(self._asg.accept( self._nnOutput, eg.et(), eg.eta(), mu ))
    else:
      self._nnOutput=-999
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
 




  def getNNOutput(self):
    return self._nnOutput




