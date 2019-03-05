
__all__ = ['Muon']

from Gaugi  import Dataframe as DataframeEnum
from Gaugi  import StatusCode
from Events import EDM
from Gaugi.utilities import stdvector_to_list

class Muon(EDM):

  __eventBranches = { 
                      'MuonPhysVal':
                    [
                    ]
                  }

  def __init__(self):
    EDM.__init__(self)
 

  def initialize(self):
    try:
      if self._dataframe is DataframeEnum.MuonPhysVal:
        for branch in self.__eventBranches["MuonPhysVal"]:
          try:
            self.setBranchAddress( self._tree, branch , self._event)
            self._branches.append(branch) # hold all branches from the body class
          except:
            self._logger.warning('Exception when try to setBranchAddress for %s...',branch)
      else:
        self._logger.warning( "Muon object can''t retrieved" )
        return StatusCode.FAILURE
      
      return StatusCode.SUCCESS
    except TypeError, e:
      self._logger.error("Impossible to create Muon Container. Reason:\n%s", e)

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


  
