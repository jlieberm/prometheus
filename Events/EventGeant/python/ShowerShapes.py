
__all__ = ['ShowerShapes']

from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi  import StatusCode, EnumStringification
from EventCommon import EDM
import numpy as np
import sys
from copy import copy

class ShowerShapes(EDM):

  __eventBranches = [ 
                    ]
                      
  def __init__(self):
    EDM.__init__(self)
    self._eratio = 0.0
    self._rphi = 0.0
    self._reta = 0.0
    self._f1 = 0.0
    self._f3 = 0.0


  def initialize(self):
    
    return StatusCode.SUCCESS



  def execute(self):

    from copy import deepcopy
    from EventGeant import CaloGAN_Definitions as Layer
    # reconstruction step, get the cell container
    roi = self.getContext().getHandler("CaloCellsContainer")
    layers = [ 
                roi.getCollection( Layer.FIRST_LAYER  ),
                roi.getCollection( Layer.SECOND_LAYER ),
                roi.getCollection( Layer.THIRD_LAYER  ),
             ] 

    # Shower shape: Eratio
    # Eratio = (E1max - E2max)/(E1max + E2max) where E1max and E2max is the first and second cell in
    # the first EM (strips) layer with most energy
    energies = deepcopy(layers[0])
    E1max, index = self._maxCell( energies ); energies.pop(index)
    E2max, _  = self._maxCell( energies )
    self._eratio = (E1max.energy()-E2max.energy()) / float(E1max.energy()+E2max.energy()) if (E1max.energy()+E1max.energy())>0.0 else 0.0

    # Shower shape: Reta
    # The second EM layers is 12 X 12 cells. To calculate the Reta we must do:
    # Reta = E_3X7 / E_7X7 where E_aXb is the sum energy in this region
    E_max, _ = self._maxCell( layers[1] );
    E_3X7 = self._sumCells( layers[1], E_max.eta() - 1, E_max.eta() + 1, E_max.phi() - 3, E_max.phi() + 3) 
    E_7X7 = self._sumCells( layers[1], E_max.eta() - 3, E_max.eta() + 3, E_max.phi() - 3, E_max.phi() + 3) 
    self._reta = E_3X7 / float(E_7X7) if E_7X7>0.0 else 0.0

    # Shower shape: Rphi
    E_3X3 = self._sumCells( layers[1], E_max.eta() - 1, E_max.eta() + 1, E_max.phi() - 1, E_max.phi() + 1) 
    self._rphi = E_3X3 / float(E_3X7) if E_3X7>0.0 else 0.0


    # Shower shapes: f1 and f3
    E_back = self._sumCells( layers[2] )
    E_middle = self._sumCells( layers[1] )
    E_front = self._sumCells( layers[0] )
    self._f1 = E_front/float(E_middle) if E_middle>0.0 else 0.0
    self._f3 = E_back/float(E_middle) if E_middle>0.0 else 0.0



    return StatusCode.SUCCESS


  def eratio(self):
    return self._eratio

  def f1(self):
    return self._f1

  def f3(self):
    return self._f3

  def reta(self):
    return self._reta

  def rphi(self):
    return self._rphi


  def _maxCell( self, containers ):
    energy=-999; max_cell_object=None; index=None
    for idx, c in enumerate(containers):
      if c.energy() > energy:
        max_cell_object=copy(c); energy=c.energy(); index=idx
    return max_cell_object, index

 
  def _sumCells( self, containers, etamin=-999, etamax=999, 
                                   phimin=-999, phimax=999):
    energy=0.0
    for c in containers:
      if c.eta() >= etamin and c.eta() <= etamax:
        if c.phi() >= phimin and c.phi() <= phimax:
          energy += c.energy()
    return energy

 




