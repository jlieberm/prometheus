
__all__ = ['ShowerShapes']

from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi  import StatusCode, EnumStringification
from Gaugi.types import NotSet
from EventCommon import EDM
import numpy as np



class ShowerShapes(EDM):

  __eventBranches = [ 
                    ]
                      
  def __init__(self):
    EDM.__init__(self)
    #from prometheus.tools.simulator.generic.reco import CaloRingsBuilder
    #self._reco_tool = CaloRingsBuilder()

  def initialize(self):
    # initialize the reconstruction tool that will be used to extract the rings from the cells
    #if self._reco_tool.initialize().isFailure():
    #  self._logger.error("Impossible to initialize the CaloRingsBuilder reco tool.")
    #  return StatusCode.FAILURE
    
    return StatusCode.SUCCESS



  def execute(self):
    # reconstruction step 
    # get the cell container
    #cells = self.retrieve("CaloTowersContainer")
    #self.reco_tool.executeTool( cells )
    # retrieve all rings
    #self.setDecor( 'ringsE', self._reco_tool.ringsE() )
    return StatusCode.SUCCESS



  def eratio1(self):    
    return self.getDecor('eratio1') 




