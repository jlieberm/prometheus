
__all__ = ['FastCaloCutBasedSelectorTool']


from RingerCore import  (checkForUnusedVars,
                         retrieve_kw, NotSet
                        )

from prometheus.core import Algorithm, StatusCode
import numpy as np
import math

class FastCaloCutBasedSelectorTool( Algorithm ):


  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    self._IDinfo = retrieve_kw( kw, 'IDinfo', 'lhvloose')
    checkForUnusedVars(kw)
    self._tools = []


  @property
  def IDinfo(self):
    return self._IDinfo

  @IDinfo.setter
  def IDinfo(self,v):
    self._IDinfo=v


  def initialize(self):

    # take from hypo config
    from configs.TrigL2CaloHypoCutDefs            import L2CaloCutMaps
    from prometheus.tools.atlas.emulation         import TrigEgammaL2CaloSelectorTool
    from prometheus.tools.atlas.common.constants  import GeV
    thrs = [0.0, 15.0, 28] # dummy thrsholds to select the energy range inside of L2CaloCutMaps

    for idx, threshold in enumerate(thrs):
      cuts = L2CaloCutMaps(threshold)
      selector  = TrigEgammaL2CaloSelectorTool(self._name+"_"+str(idx),
                                              dETACLUSTERthr = 0.1,
                                              dPHICLUSTERthr = 0.1,
                                              EtaBins        = [0.0, 0.6, 0.8, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47],
                                              F1thr          = [0.005]*9,
                                              ETthr          = [0]*9,
                                              ET2thr         = [90.0*GeV, 90.0*GeV, 90.0*GeV, 90.0*GeV, 90.0*GeV, 90.0*GeV, 90.0*GeV, 90.0*GeV, 90.0*GeV],
                                              HADET2thr      = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0, 999.0, 999.0, 999.0],
                                              #HADETthr       = [0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058],
                                              WETA2thr       = [99999.,99999.,99999.,99999.,99999.,99999.,99999.,99999.,99999.],
                                              WSTOTthr       = [99999.,99999.,99999.,99999.,99999.,99999.,99999.,99999.,99999.],
                                              F3thr          = [99999.,99999.,99999.,99999.,99999.,99999.,99999.,99999.,99999.],
                                              HADETthr       = cuts.MapsHADETthr[self._IDinfo],
                                              CARCOREthr     = cuts.MapsCARCOREthr[self._IDinfo],
                                              CAERATIOthr    = cuts.MapsCAERATIOthr[self._IDinfo],
                                              )
      self._tools.append(selector)

    return StatusCode.SUCCESS


  def accept(self, fc, mu=0.0):
    from prometheus.tools.atlas.common.constants  import GeV
    et = fc.et()
    if et < 12*GeV:
      return self._tools[0].emulation(fc, None)
    elif et>=12*GeV and et < 22*GeV:
      return self._tools[1].emulation(fc, None)
    else:
      return self._tools[2].emulation(fc, None)



  def finalize(self):
    for tool in self._tools:
      tool.finalize()
    return StatusCode.SUCCESS




