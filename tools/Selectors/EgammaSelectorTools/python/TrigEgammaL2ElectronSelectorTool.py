
__all__ = ['TrigEgammaL2ElectronSelectorTool']

from Gaugi import Algorithm, StatusCode, GeV
from Gaugi import checkForUnusedVars, retrieve_kw
from Gaugi.messenger.macros import *
import numpy as np
import math
import re


class TrigEgammaL2ElectronSelectorTool( Algorithm ):

  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name)
    self._etThr                   =  retrieve_kw( kw, 'EtCut'                ,   0     )
    self._trackPtthr              =  retrieve_kw( kw, 'TrackPt'              ,   5*GeV )
    self._calotrackdeta           =  retrieve_kw( kw, 'CaloTrackdETA'        ,   0     )
    self._calotrackdphi           =  retrieve_kw( kw, 'CaloTrackdPHI'        ,   0     )
    self._calotrackdeoverp_low    =  retrieve_kw( kw, 'CaloTrackdEoverPLow'  ,   0     )
    self._calotrackdeoverp_high   =  retrieve_kw( kw, 'CaloTrackdEoverPHigh' ,   0     )
    self._trtratio                =  retrieve_kw( kw, 'TRTRatio'             ,   0     )
    checkForUnusedVars(kw)


  def initialize(self):
    self.init_lock()
    return StatusCode.SUCCESS


  def accept( self, context )

    elCont = context.getHandler( "HLT__FastElectronContainer" )
    current = elCont.getPos()
    passed = self.emulation( elCont )
    accept = Accept( self.name() )
    elCont.setPos( current )
    accept.setCutResult( "Pass", passed )
    return accept


  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  def emulation(self, elCont):
  
    passed = False
    bitAccept = [False for i in range(elCont.size())]
    
    for el in elCont:
      # Retrieve all quantities
      dPhiCalo    = el.trkClusDphi();
      dEtaCalo    = el.trkClusDeta();
      pTcalo      = el.pt();       
      eTOverPt    = el.etOverPt();         
      NTRHits     = el.numberOfTRTHits();
      NStrawHits  = el.numberOfTRTHiThresholdHits()
      TRTHitRatio = 1e10 if NStrawHits==0 else NTRHits/float(NStrawHits)
      # apply cuts
      if (pTcalo > self._trackPtthr):
        if (dEtaCalo < self._calotrackdeta):
          if (dPhiCalo < self._calotrackdphi):
            if(eTOverPt >  self._calotrackdeoverp_low ):
              if ( eTOverPt < self._calotrackdeoverp_high ):
                if (TRTHitRatio > self._trtratio):
                  # TrigElectron passed all cuts: set flags
                  bitAccept[el.getPos()] = True 
                  self._logger.debug( "Event accepted !" )         
                #TRTHitRatio
              #etOverPt
            #dphi
          #deta
        #pt
      #apply cuts
    # Loop over electrons
    
    # got this far => passed!
    return any( bitAccept )

     





