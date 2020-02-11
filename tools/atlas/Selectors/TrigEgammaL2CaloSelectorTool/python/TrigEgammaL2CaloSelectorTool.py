
__all__ = ['TrigEgammaL2CaloSelectorTool']

from Gaugi.messenger.macros import *
from Gaugi.messenger import Logger
from Gaugi.gtypes import NotSet
from Gaugi import StatusCode
from prometheus import Algorithm
import numpy as np
import math

# Private tool used only here
class _TrigEgammaL2CaloSelectorTool( Logger ):

  def __init__(self, name, **kw):

    Logger.__init__(self)
    from Gaugi import retrieve_kw
    self._hadeTthr        = retrieve_kw( kw, 'HADETthr'				, NotSet	)
    self._carcorethr      = retrieve_kw( kw, 'CARCOREthr'			, NotSet	)
    self._caeratiothr     = retrieve_kw( kw, 'CAERATIOthr'		, NotSet	)
    self._etabin          = retrieve_kw( kw, 'EtaBins'				, NotSet	)
    self._detacluster		  = retrieve_kw( kw, 'dETACLUSTERthr'	, 0.1			)
    self._dphicluster		  = retrieve_kw( kw, 'dPHICLUSTERthr'	, 0.1			)
    self._eTthr			      = retrieve_kw( kw, 'ETthr'					, 999.0		)
    self._eT2thr		      = retrieve_kw( kw, 'ET2thr'					, 999.0		)
    self._hadeT2thr			  = retrieve_kw( kw, 'HADET2thr'			, 999.0		)
    self._F1thr			      = retrieve_kw( kw, 'F1thr'					, 0.005		)
    self._WETA2thr			  = retrieve_kw( kw, 'WETA2thr'				, 99999.	)
    self._WSTOTthr			  = retrieve_kw( kw, 'WSTOTthr' 			, 99999.	)
    self._F3thr				    = retrieve_kw( kw, 'F3thr'					, 99999.	)

  def initialize(self):
    return StatusCode.SUCCESS

  def emulation(self, pClus, info):

    # get the equivalent L1 EmTauRoi object in athena
    emTauRoi = pClus.emTauRoI()
    PassedCuts=0
    # initialise monitoring variables for each event
    dPhi          = -1.0
    eT_T2Calo     = -1.0
    hadET_T2Calo  = -1.0
    rCore         = -1.0
    energyRatio   = -1.0
    Weta2         = -1.0
    Wstot         = -1.0
    F3            = -1.0
    F1            = -1.0

    # fill local variables for RoI reference position
    phiRef = emTauRoi.phi()
    etaRef = emTauRoi.eta()

    if etaRef > 2.6:
      self._logger.debug('The cluster had eta coordinates beyond the EM fiducial volume.')
      return False


    # correct phi the to right range (probably not needed anymore)
    if  math.fabs(phiRef) > np.pi: phiRef -= 2*np.pi; # correct phi if outside range

    absEta = math.fabs( pClus.eta() )
    etaBin = -1
    if absEta > self._etabin[-1]:
      absEta=self._etabin[-1]
    # get the corrct eta bin range
    for idx, value in enumerate(self._etabin):
      if ( absEta > self._etabin[idx] and absEta < self._etabin[idx+1] ):
      	etaBin = idx;

    # Is in crack region?
    inCrack = True if (absEta > 2.37 or (absEta > 1.37 and absEta < 1.52)) else False

    # Deal with angle diferences greater than Pi
    dPhi =  math.fabs(pClus.phi() - phiRef);
    dPhi = dPhi if (dPhi < np.pi) else  (2*np.pi - dPhi)


    # calculate cluster quantities // definition taken from TrigElectron constructor
    if ( pClus.emaxs1() + pClus.e2tsts1() ) > 0 :
    	energyRatio = ( pClus.emaxs1() - pClus.e2tsts1() ) / float( pClus.emaxs1() + pClus.e2tsts1() )

    # (VD) here the definition is a bit different to account for the cut of e277 @ EF
    if ( pClus.e277()!= 0.):
    	rCore = pClus.e237() / float(pClus.e277())

    # fraction of energy deposited in 1st sampling
    #if ( math.fabs(pClus.energy()) > 0.00001) :
    #	F1 = (pClus.energy(CaloSampling.EMB1)+pClus.energy(CaloSampling.EME1))/float(pClus.energy())
    F1 = pClus.f1()

    eT_T2Calo  = float(pClus.et());

    if ( eT_T2Calo!=0 and pClus.eta()!=0 ):
    	 hadET_T2Calo = pClus.ehad1()/math.cosh(math.fabs(pClus.eta()))/eT_T2Calo

    # extract Weta2 varable
    Weta2 = pClus.weta2()
    # extract Wstot varable
    Wstot = pClus.wstot()

    # extract F3 (backenergy i EM calorimeter
    #e0 = pClus.energy(CaloSampling.PreSamplerB) + pClus.energy(CaloSampling.PreSamplerE)
    #e1 = pClus.energy(CaloSampling.EMB1) 				+ pClus.energy(CaloSampling.EME1)
    #e2 = pClus.energy(CaloSampling.EMB2) 				+ pClus.energy(CaloSampling.EME2)
    #e3 = pClus.energy(CaloSampling.EMB3) 				+ pClus.energy(CaloSampling.EME3)
    #eallsamples = float(e0+e1+e2+e3)
    #F3= e3/eallsamples if math.fabs(eallsamples)>0. else 0.
    F3 = pClus.f3()

    # apply cuts: DeltaEta(clus-ROI)
    if ( math.fabs(pClus.eta() - etaRef) > self._detacluster ):
      return False

    PassedCuts+=1  #Deta

    # DeltaPhi(clus-ROI)
    if ( dPhi > self._dphicluster ):
    	self._logger.debug('dphi > dphicluster')
    	return False

    PassedCuts+=1 #DPhi

    # eta range
    if ( etaBin==-1 ):  # VD
      self._logger.debug("Cluster eta: %1.3f  outside eta range ",absEta )
      return False
    else:
      self._logger.debug("eta bin used for cuts ")

    PassedCuts+=1 # passed eta cut

    # Rcore
    if ( rCore < self._carcorethr[etaBin] ):  return False
    PassedCuts+=1 # Rcore

    # Eratio
    if ( inCrack or F1<self._F1thr[etaBin] ):
      self._logger.debug("TrigEMCluster: InCrack= %d F1=%1.3f",inCrack,F1 )
    else:
      if ( energyRatio < self._caeratiothr[etaBin] ): return False

    PassedCuts+=1 # Eratio
    if(inCrack): energyRatio = -1; # Set default value in crack for monitoring.

    # ET_em
    if ( eT_T2Calo*1e-3 < self._eTthr[etaBin]): return False
    PassedCuts+=1 # ET_em

    hadET_cut = 0.0;
    # find which ET_had to apply : this depends on the ET_em and the eta bin
    if ( eT_T2Calo >  self._eT2thr[etaBin] ):
      hadET_cut = self._hadeT2thr[etaBin]
    else:
      hadET_cut = self._hadeTthr[etaBin]

    # ET_had
    if ( hadET_T2Calo > hadET_cut ): return False
    PassedCuts+=1 #ET_had
    # F1
    # if ( F1 < m_F1thr[0]) return true;  //(VD) not cutting on this variable, only used to select whether to cut or not on eRatio
    PassedCuts+=1 # F1
    # Weta2
    if ( Weta2 > self._WETA2thr[etaBin]): return False
    PassedCuts+=1 # Weta2
    # Wstot
    if ( Wstot >= self._WSTOTthr[etaBin]): return False
    PassedCuts+=1 # Wstot
    # F3
    if ( F3 > self._F3thr[etaBin]): return False
    PassedCuts+=1 # F3
    # got this far => passed!
    self._logger.debug('T2Calo emulation approved...')
    return True


  def finalize(self):
    return StatusCode.SUCCESS






class TrigEgammaL2CaloSelectorTool( Algorithm ):


  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    from Gaugi import retrieve_kw
    self._IDinfo = retrieve_kw( kw, 'IDinfo', 'lhvloose')
    self._tools = []

  @property
  def IDinfo(self):
    return self._IDinfo

  @IDinfo.setter
  def IDinfo(self,v):
    self._IDinfo=v


  def initialize(self):

    # take from hypo config
    from .TrigEgammaL2CaloSelectorCuts import L2CaloCutMaps
    from Gaugi.constants  import GeV
    thrs = [0.0, 15.0, 28] # dummy thrsholds to select the energy range inside of L2CaloCutMaps

    for idx, threshold in enumerate(thrs):
      cuts = L2CaloCutMaps(threshold)
      selector  = _TrigEgammaL2CaloSelectorTool(self._name+"_"+str(idx),
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
    from Gaugi.constants  import GeV
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






