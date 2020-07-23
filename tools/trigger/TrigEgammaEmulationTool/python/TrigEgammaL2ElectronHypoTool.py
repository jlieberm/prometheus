
__all__ = ['TrigEgammaL2ElectronHypoTool']


from Gaugi.messenger.macros import *
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import GeV
from EventAtlas import Accept



class TrigEgammaL2ElectronHypoTool( Algorithm ):

  __property = [
                "EtCut",
                "TrackPt",
                "CaloTrackdETA",
                "CaloTrackdPHI",
                "CaloTrackdEoverPLow",
                "CaloTrackdEoverPHigh",
                "TRTRatio",
                ]

  #
  # Constructor
  #
  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name, self.__property)

    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )

  #
  # Initialize method
  #
  def initialize(self):
    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept( self, context ):

    elCont = context.getHandler( "HLT__FastElectronContainer" )
    current = elCont.getPos()
  
    bitAccept = [False for _ in range(elCont.size())]
    
    etThr                   =  self.getProperty( 'EtCut'                 )
    trackPtthr              =  self.getProperty( 'TrackPt'               )
    calotrackdeta           =  self.getProperty( 'CaloTrackdETA'         )
    calotrackdphi           =  self.getProperty( 'CaloTrackdPHI'         )
    calotrackdeoverp_low    =  self.getProperty( 'CaloTrackdEoverPLow'   )
    calotrackdeoverp_high   =  self.getProperty( 'CaloTrackdEoverPHigh'  )
    trtratio                =  self.getProperty( 'TRTRatio'              )

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

      if (pTcalo > trackPtthr):
        if (dEtaCalo < calotrackdeta):
          if (dPhiCalo < calotrackdphi):
            if(eTOverPt >  calotrackdeoverp_low ):
              if ( eTOverPt < calotrackdeoverp_high ):
                if (TRTHitRatio > trtratio):
                  # TrigElectron passed all cuts: set flags
                  bitAccept[el.getPos()] = True 
                  MSG_DEBUG( self,  "Event accepted !" )         
                #TRTHitRatio
              #etOverPt
            #dphi
          #deta
        #pt
      #apply cuts
    # Loop over electrons
    
    elCont.setPos( current )
    # got this far => passed!
    passed = any( bitAccept )
    return Accept( self.name(), [("Pass", passed)] )

     





