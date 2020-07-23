
__all__ = ['Chain', 'Group']

from Gaugi import Algorithm, StatusCode, NotSet, GeV
from Gaugi import checkForUnusedVars, retrieve_kw
from Gaugi.messenger.macros import *
from EventAtlas import Accept



class Group( object ):

  def __init__( self, chain, pidname, etthr ):
    self._chain = chain
    self._pidname = pidname
    self._etthr = etthr

  def chain(self):
    return self._chain

  def pidname(self):
    return self._pidname
  
  def etthr(self):
    return self._etthr





class Chain( Algorithm ):

  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name)
    # L1 configuration parameters
    
    self._signature    = retrieve_kw( kw, 'Signature' , '' )
    self._l1Item       = retrieve_kw( kw, 'L1Item'    , '' )
    self._l2caloItem   = retrieve_kw( kw, 'L2CaloItem', '' )
    self._l2Item       = retrieve_kw( kw, 'L2Item'    , '' )
    self._hltItem      = retrieve_kw( kw, 'HLTItem'   , '' )
    self._l2caloEtCut  = retrieve_kw( kw, 'L2CaloEtCut', 0 )
    self._efcaloEtCut  = retrieve_kw( kw, 'EFCaloEtCut', 0 )
    self._hltEtCut     = retrieve_kw( kw, 'HLTEtCut'   , 0 )
    
    checkForUnusedVars(kw)


  def initialize(self):
    self.init_lock()
    return StatusCode.SUCCESS



  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  def accept( self, context ):

    dec = context.getHandler( "MenuContainer" )

    accept = self.getAcceptInfo()

    passedL1 = bool(dec.accept( self._l1Item ))

    # Is passed by L1?
    if not passedL1:
      return accept

    accept.setCutResult( 'L1Calo' , True )

    # Is passed by L2Calo et cut? AND hypo cut
    em = context.getHandler("HLT__FastCaloContainer")
    if  not ( ( em.et() > self._l2caloEtCut*GeV ) and bool(dec.accept( self._l2caloItem )) ):
      return accept

    accept.setCutResult( 'L2Calo' , True )
  
    
    # Is passed by L2 electron/photon
    passedL2 = bool(dec.accept( self._l2Item ))

    if not passedL2:
      return accept


    accept.setCutResult( 'L2' , True )

    # Is passed by EF calo et cut
    clCont = context.getHandler( "HLT__CaloClusterContainer" )
    current = clCont.getPos()
    passedEFCalo = False
    for cl in clCont:
      if cl.et() > self._efcaloEtCut * GeV:
        passedEFCalo=True
        break

    if not passedEFCalo:
      return accept


    accept.setCutResult( 'EFCalo' , True )

    

    # Is passed by HLT electron/photon et cut
    passedHLT_etcut = False

    if self._signature == 'electron':
      cont = context.getHandler("HLT__ElectronContainer")
      for el in cont:
        if el.et() > self._hltEtCut*GeV:
          passedHLT_etcut = True; break

    elif self._signature == 'photon':
      cont = context.getHandler("HLT__PhotonContainer")
      for ph in cont:
        if ph.et() > self._hltEtCut*GeV:
          passedHLT_etcut = True; break

    else:
      MSG_FATAL( self, "signature not reconized to emulate the HLT et cut step" )

    
    if not passedHLT_etcut:
      return accept


    # check the HLT decision
    passedHLT = bool( dec.accept( self._hltItem ) )

    accept.setCutResult( 'HLT', passedHLT )
    accept.setCutResult( 'Pass', passedHLT )

    return accept



  def getAcceptInfo(self):

    accept = Accept( self.name() )
    accept.setCutResult( 'L1Calo' , False )
    accept.setCutResult( 'L2Calo' , False )
    accept.setCutResult( 'L2'     , False )
    accept.setCutResult( 'EFCalo' , False )
    accept.setCutResult( 'HLT'    , False )
    accept.setCutResult( 'Pass'   , False )
    return accept



