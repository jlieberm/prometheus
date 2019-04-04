
__all__ = ['Photon']


from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi  import StatusCode
from EventCommon import EDM
from Gaugi.utilities import stdvector_to_list


class Photon(EDM):

  __eventBranches = { 
                      'PhysVal':
                    [
                    ]
                  }

  def __init__(self):
    EDM.__init__(self)
    self._is_hlt = False

  @property
  def is_hlt(self):
    return self._is_hlt


  @is_hlt.setter
  def is_hlt(self, v):
    self._is_hlt = v


  def initialize(self):
    try:
      if self._dataframe is DataframeEnum.PhysVal_v2:
        for branch in self.__eventBranches["PhysVal"]:
          try:
            self.setBranchAddress( self._tree, branch , self._event)
            self._branches.append(branch) # hold all branches from the body class
          except:
            self._logger.warning('Exception when try to setBranchAddress for %s...',branch)
      else:
        self._logger.warning( "Photon object can''t retrieved" )
        return StatusCode.FAILURE
      
      return StatusCode.SUCCESS
    except TypeError, e:
      self._logger.error("Impossible to create Photon Container. Reason:\n%s", e)

    return StatusCode.SUCCESS

  #def emClus(self):
  #  """
  #    Retrieve the L1 EmClus information from Physval or SkimmedNtuple
  #  """
  #  if self._dataframe is DataframeEnum.SkimmedNtuple:
  #    return 
  #  elif self._dataframe is DataframeEnum.PhysVal_v2:
  #    return self._event.trig_L1_emClus
  #  else:
  #    self._logger.warning("Impossible to retrieve the value of L1 EmClus. Unknow dataframe")


  
