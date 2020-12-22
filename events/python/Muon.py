
__all__ = ['Muon']

from Gaugi import EDM
from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi  import StatusCode
from Gaugi import stdvector_to_list

class Muon(EDM):

  __eventBranches = {
                      'MuonPhysVal':
                    [
                    ]
                  }

  def __init__(self):
    EDM.__init__(self)


  def initialize(self):
    return StatusCode.SUCCESS

