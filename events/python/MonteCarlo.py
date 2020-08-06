
__all__ = ['MonteCarlo']

from Gaugi import EDM
from Gaugi  import StatusCode
from prometheus.enumerations  import Dataframe as DataframeEnum


class MonteCarlo(EDM):

  __eventBranches = {
                    'SkimmedNtuple':[
                        'type',
                        'isTruthElectronFromZ',
                        'isTruthElectronFromW',
                        'isTruthElectronFromJpsiPrompt',
                        'isTruthElectronAny',
                       ],
                    'PhysVal':[
                      'mc_hasMC',
                      'mc_isTruthElectronAny',
                      'mc_isTruthElectronFromZ',
                      'mc_isTruthElectronFromW',
                      'mc_isTruthElectronFromJpsi',
                      ]
                    }


  def __init__(self):
    EDM.__init__(self)
 


  def initialize(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      # Link all branches 
      for branch in self.__eventBranches["SkimmedNtuple"]:
        self.setBranchAddress( self._tree, ('elCand%d_%s')%(self._elCand, branch)  , self._event)
        #self._branches.append(branch) # hold all branches from the body class
    
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      for branch in self.__eventBranches["PhysVal"]:
        self.setBranchAddress( self._tree, ('%s')%(branch)  , self._event)
        #self._branches.append(branch) # hold all branches from the body class
    else:
      self._logger.warning( "Electron object can''t retrieved" )
      return StatusCode.FAILURE
    
    return StatusCode.SUCCESS


  def isTruthElectronFromZ(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromZ'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.mc_isTruthElectronFromZ
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromW(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromW'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.mc_isTruthElectronFromW
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromJpsi(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromJpsiPromt'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.mc_isTruthElectronFromJpsi
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromAny(self):
    
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_isTruthElectronFromAny'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.mc_isTruthElectronFromAny
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isMC(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return True if getattr(self._event, ('elCand%d_type')%(self._elCand)) != -999 else False
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return bool(self._event.mc_hasMC)
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")



  
