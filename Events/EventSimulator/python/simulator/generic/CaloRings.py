
__all__ = ['CaloRings']

from prometheus.core.EnumCollection import Dataframe as DataframeEnum
from prometheus.core.StatusCode     import StatusCode
from prometheus.dataframe.EDM       import EDM
from RingerCore                     import EnumStringification
from copy import copy
import numpy as np
import sys

class RingSet(object):

  def __init__(self, nrings):
    self._nrings = nrings
    # set all rings as zeros
    self._ringsE = [0.0 for _ in range(nrings)]

  def push_back(self, max_x, max_y, objects):
    for c in objects:
      dif_x = abs(max_x-c.x()); dif_y = abs(max_y-c.y())
      r = max(dif_x,dif_y)
      if r <= self._nrings-1:
        self._ringsE[r]+=c.energy()

  def ringsE(self):
    return self._ringsE



class CaloRings(EDM):

  __eventBranches = [ ]
                      
  def __init__(self):
    EDM.__init__(self)
    #from prometheus.tools.simulator.generic.reco import CaloRingsBuilder
    #self._reco_tool = CaloRingsBuilder()
    self._nrings = [46, 5, 5]
    self._ringsE = [0.0 for _ in range(sum(self._nrings))]

  def initialize(self):
    # initialize the reconstruction tool that will be used to extract the rings from the cells
    #if self._reco_tool.initialize().isFailure():
    #  self._logger.error("Impossible to initialize the CaloRingsBuilder reco tool.")
    #  return StatusCode.FAILURE
    return StatusCode.SUCCESS


  def execute(self):

    from prometheus.dataframe.simulator.generic import CaloGAN_Definitions as Layer
    # reconstruction step, get the cell container
    roi = self.getContext().getHandler("CaloCellsContainer")
    layers = [ 
                roi.getCollection( Layer.FIRST_LAYER  ),
                roi.getCollection( Layer.SECOND_LAYER ),
                roi.getCollection( Layer.THIRD_LAYER  ),
             ] 

    ringsets = [ 
                RingSet( self._nrings[0] ),
                RingSet( self._nrings[1] ),
                RingSet( self._nrings[2] ),
               ]

    self._ringsE=[]
    # build rings
    for rset, cells in enumerate(layers):
      max_cell = self._maxCell(cells)
      if max_cell:
        ringsets[rset].push_back( max_cell.x(), max_cell.y(), cells )  
      else: # there is no center, all cells are zero in the current layer
        self._logger.debug("All cells in the %d layer are zero. Fill with zeros this ringer set.",rset+1)

      self._ringsE+=ringsets[rset].ringsE()
    

    return StatusCode.SUCCESS


  def _maxCell( self, containers ):
    energy=sys.float_info.min; max_cell_object=None
    for c in containers:
      if c.energy() > energy:
        max_cell_object=copy(c); energy=c.energy()
    return max_cell_object



  def ringsE(self):    
    return self._ringsE 




