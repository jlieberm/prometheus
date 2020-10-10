
__all__ = ['MonteCarlo']

from Gaugi import EDM
from Gaugi  import StatusCode
from prometheus.enumerations  import Dataframe as DataframeEnum


class MonteCarlo(EDM):

  __eventBranches = {
                    'v1':[ # For electron and photon
                      'mc_hasMC',
                      'mc_isTruthElectronAny',
                      'mc_isTruthElectronFromZ',
                      'mc_isTruthElectronFromW',
                      'mc_isTruthElectronFromJpsi',
                      ],
                    }


  def __init__(self):
    EDM.__init__(self)
 


  def initialize(self):
    """
    Initialize all branches
    """
    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      self.link( self.__eventBranches["v1"] )
      return StatusCode.SUCCESS
    else:
      self._logger.warning( "Can not initialize the MonteCarlo object. Dataframe not available." )
      return StatusCode.FAILURE
    



  def isTruthElectronFromZ(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromZ'%self._elCand)
    elif self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromZ
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromW(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromW'%self._elCand)
    elif self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromW
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromJpsi(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromJpsiPromt'%self._elCand)
    elif self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromJpsi
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromAny(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromAny'%self._elCand)
    elif self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromAny
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isMC(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return True if getattr(self._event, ('elCand%d_type')%(self._elCand)) != -999 else False
    elif self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return bool(self._event.mc_hasMC)
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")



  
