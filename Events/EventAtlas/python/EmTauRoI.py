
__all__ = ['EmTauRoI']

from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi import StatusCode
from EventCommon import EDM
from Gaugi.utilities import stdvector_to_list

class EmTauRoI(EDM):

  __eventBranches = { 'SkimmedNtuple': 
                      [
                      'trig_L1_calo_match',
                      'trig_L1_calo_eta',
                      'trig_L1_calo_phi',
                      'trig_L1_calo_emClus',
                      'trig_L1_calo_tauClus',
                      'trig_L1_calo_emIsol',
                      'trig_L1_calo_hadIsol',
                      'trig_L1_calo_hadCore',
 
                      ],
                      'PhysVal':
                    [
                      'trig_L1_eta',
                      'trig_L1_phi',
                      'trig_L1_emClus',
                      'trig_L1_tauClus',
                      'trig_L1_emIsol',
                      'trig_L1_hadIsol',
                      #'trig_L1_thrNames',
                    ]
                  }


  def __init__(self):
    EDM.__init__(self)
    # this is use only for SkimmedNtuple
    self._elCand = 2 # Default is probe
 
  @property
  def candidate(self, v):
    return self._elCand

  # Use this only for skimmed ntuple dataframe
  # Default is 2 (probes)
  @candidate.setter
  def candidate(self, v):
    self._elCand = v

  def initialize(self):
    try:
      if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
        # Link all branches 
        for branch in self.__eventBranches["SkimmedNtuple"]:
          try:
      	    self.setBranchAddress( self._tree, ('elCand%d_%s')%(self._elCand,branch), self._event)
            self._branches.append(branch) # hold all branches from the body class
          except:
            self._logger.warning('Exception when try to setBranchAddress for %s...',branch)

      elif self._dataframe is DataframeEnum.PhysVal_v2:
        for branch in self.__eventBranches["PhysVal"]:
          try:
            self.setBranchAddress( self._tree, branch , self._event)
            self._branches.append(branch) # hold all branches from the body class
          except:
            self._logger.warning('Exception when try to setBranchAddress for %s...',branch)
      else:
        self._logger.warning( "EmTauRoI object can''t retrieved" )
        return StatusCode.FAILURE
      
      return StatusCode.SUCCESS
    except TypeError, e:
      self._logger.error("Impossible to create the EmTauRoI Container. Reason:\n%s", e)
      return StatusCode.SUCCESS


  def emClus(self):
    """
      Retrieve the L1 EmClus information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_trig_L1_calo_emClus'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.trig_L1_emClus
    else:
      self._logger.warning("Impossible to retrieve the value of L1 EmClus. Unknow dataframe")

  def tauClus(self):
    """
      Retrieve the L1 tauClus information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_trig_L1_calo_tauClus'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.trig_L1_tauClus
    else:
      self._logger.warning("Impossible to retrieve the value of L1 tauClus. Unknow dataframe")

  def emIsol(self):
    """
      Retrieve the L1 emIsol information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_trig_L1_calo_emIsol'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.trig_L1_emIsol
    else:
      self._logger.warning("Impossible to retrieve the value of L1 EmIsol. Unknow dataframe")


  def hadCore(self):
    """
      Retrieve the L1 hadIsol information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_trig_L1_calo_hadCore'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.trig_L1_hadIsol
    else:
      self._logger.warning("Impossible to retrieve the value of L1 hadIsol. Unknow dataframe")


  def eta(self):
    """
      Retrieve the eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_trig_L1_calo_eta'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.trig_L1_eta
    else:
      self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")

  def phi(self):
    """
      Retrieve the phi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
      return getattr(self._event, 'elCand%d_trig_L1_calo_phi'%self._elCand)
    elif self._dataframe is DataframeEnum.PhysVal_v2:
      return self._event.trig_L1_phi
    else:
      self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")




  
