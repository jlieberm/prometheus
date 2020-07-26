
__all__ = ['Chain']

from Gaugi import Algorithm 
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi.messenger.macros import *
from EventAtlas import Accept
from TrigEgammaEmulationTool.menu import TriggerInfo


#
# Chain definition
#
class Chain( Algorithm ):


  #
  # Constructor
  #
  def __init__(self, name, L1Item, chain):
    
    Algorithm.__init__(self, name)
    self.__trigInfo = TriggerInfo(chain)
    self.__l1item = L1Item
    self.__trigger = chain






  #
  # Initialize method
  #
  def initialize(self):
    
     
    # Configure the L2Calo hypo step
    from TrigEgammaEmulatorTool.TrigEgammaL1CaloHypoTool import configure
    self.__l1caloItem = configure( self.__l1item )


    # Configure L2Calo step
    if self.__trigInfo.ringer():
      version = self.__trigInfo.ringerVersion()

      if version < 0:
        MSG_FATAL( self, "The trigger %s is ringer chain but you don't specifie a correct tuning version.", self.__trigger)
     
      if version == 6:
        from RingerSelectorTools import installElectronL2CaloRingerSelector_v6
        names = installElectronL2CaloRingerSelector_v6()
      elif version == 8:
        from RingerSelectorTools import installElectronL2CaloRingerSelector_v8
        names = installElectronL2CaloRingerSelector_v8()
      elif version == 10:
        from RingerSelectorTools import installElectronL2CaloRingerSelector_v10
        names = installElectronL2CaloRingerSelector_v10()

        
      # define like tight, medium, loose and vloose
      self.__l2caloItem = names[self.__trigInfo.pidnameIdx()]


    else:
      # Configure the L2Calo hypo step
      from TrigEgammaEmulatorTool.TrigEgammaL2CaloHypoTool import configure
      self.__l2caloItem = configure( self.__trigger )
    
     
    # Configure the EFCalo hypo step
    from TrigEgammaEmulatorTool.TrigEgammaL2ElectronHypoTool import configure
    self.__l2Item = configure( self.__trigger )
    

    # Configure the HLT hypo step
    from TrigEgammaEmulatorTool.TrigEgammaEFElectronHypoTool import configure
    self.__hltItem = configure( self.__trigger )
    

    # configure et cuts
    self.__l2caloEtCuts = (self.__trigInfo.etthr() - 3 ) * GeV
    self.__efcaloEtCuts = (self.__trigInfo.etthr()) * GeV
    self.__hltEtCuts = (self.__trigInfo.etthr()) * GeV

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

    dec = context.getHandler( "MenuContainer" )

    accept = self.getAcceptInfo()

    passedL1 = bool(dec.accept( self.L1Item ))

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










