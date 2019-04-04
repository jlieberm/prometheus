
__all__ = ['CaloCells', 'CaloCell','CaloGAN_Definitions']

from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi  import StatusCode, EnumStringification
from Gaugi.types import NotSet
from EventCommon import EDM
import numpy as np

# Do not change this definitions.
# the from: https://github.com/hep-lbdl/CaloGAN/tree/master/generation
class CaloGAN_Definitions(EnumStringification):
  LAYER_SPECS = [(3, 96), (12, 12), (12, 6)]
  LAYER_DIV = np.cumsum(map(np.prod, LAYER_SPECS)).tolist()
  LAYER_DIV = zip([0] + LAYER_DIV, LAYER_DIV)
  FIRST_LAYER = 1
  SECOND_LAYER = 2
  THIRD_LAYER = 3



class CaloCell(object):
  def __init__(self):
    self._x= 0.0 # In MeV
    self._y= 0.0 # In MeV
    self._energy = 0.0 # In MeV
  
  def energy(self):
    return self._energy
  
  def x(self):
    return self._x
  
  def y(self):
    return self._y
  
  def setEnergy(self,v):
    self._energy=v
 
  def setX(self,v):
    self._x=v
 
  def setY(self,v):
    self._y=v

  def layer(self):
    return self._layer

  def setLayer(self,v):
    self._layer=v



class CaloCells(EDM):

  __eventBranches = [ 
                      #'EventNumber',
                      #'RunNumber',
                      'TotalEnergy',
                    ]
  __eventBranches.extend(['cell_%d'%(i) for i in range(507)])
                      
                  

  def __init__(self):
    EDM.__init__(self)
    # three layers calorimeter

    self._first_sampling  = NotSet
    self._second_sampling = NotSet
    self._third_sampling  = NotSet

  def initialize(self):
    try:
      # Link all branches 
      for branch in self.__eventBranches:
        self.setBranchAddress( self._tree, branch, self._event)
        self._branches.append(branch) # hold all branches from the body class
      return StatusCode.SUCCESS
    except TypeError, e:
      self._logger.error("Impossible to create the CaloTowers Container. Reason:\n%s", e)
      return StatusCode.FAILURE


  def execute(self):
    from CaloCells import CaloGAN_Definitions as Layer
    def convert2obj(c,layer):
      object_list=[]
      for (x,y), value in np.ndenumerate(c):
        obj=CaloCell(); obj.setX(x); obj.setY(y); obj.setEnergy(c[x][y]); obj.setLayer(layer)
        object_list.append(obj)
      return object_list
    self._first_sampling  = convert2obj(self._get_cells(Layer.FIRST_LAYER ) , Layer.FIRST_LAYER )
    self._second_sampling = convert2obj(self._get_cells(Layer.SECOND_LAYER) , Layer.SECOND_LAYER)
    self._third_sampling  = convert2obj(self._get_cells(Layer.THIRD_LAYER ) , Layer.THIRD_LAYER )
    return StatusCode.SUCCESS


  # private method 
  def _get_cells(self, layer):
    # See: https://github.com/hep-lbdl/CaloGAN/tree/master/generation
    # Get the calo GAN cells schemma
    # First layer definitions: 96 X 3
    if layer is CaloGAN_Definitions.FIRST_LAYER:
      cells = np.array([ getattr(self._event, 'cell_%d'%c) for c in range(CaloGAN_Definitions.LAYER_DIV[0][0],
        CaloGAN_Definitions.LAYER_DIV[0][1] )])
      return cells.reshape((96,3))
    # Second layer definicions: 12 X 12
    elif layer is CaloGAN_Definitions.SECOND_LAYER:
      cells = np.array([ getattr(self._event, 'cell_%d'%c) for c in range(CaloGAN_Definitions.LAYER_DIV[1][0],
        CaloGAN_Definitions.LAYER_DIV[1][1] )])
      return cells.reshape((12,12))
    # Third Layer definitions: 6 X 12
    elif layer is CaloGAN_Definitions.THIRD_LAYER:
      cells = np.array([ getattr(self._event, 'cell_%d'%c) for c in range(CaloGAN_Definitions.LAYER_DIV[2][0],
        CaloGAN_Definitions.LAYER_DIV[2][1] )])
      return cells.reshape((6,12))
    else:
      self._logger.warning('Invalid layer definition for CaloGAN')      
 
    
        
  def totalEnergy(self):
    return self._event.TotalEnergy

 
  def getCollection( self, layer ):
    if layer is CaloGAN_Definitions.FIRST_LAYER:
      return self._first_sampling
    elif layer is CaloGAN_Definitions.SECOND_LAYER:
      return self._second_sampling
    elif layer is CaloGAN_Definitions.THIRD_LAYER:
      return self._third_sampling
    else:
      self._logger.warning('Invalid layer definition for CaloGAN')      





