
__all__ = ['TrigEgammaL1CaloSelectorTool']

from Gaugi import Algorithm, StatusCode
from Gaugi.messenger.macros import *
from EventAtlas import Accept
import numpy as np
import math
import re


class TrigEgammaL1CaloSelectorTool( Algorithm ):

  __property = [
                'L1Item',
                ]

  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name)
   
    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
  

  #
  # Initialize method
  #
  def initialize(self):
    
    l1item = self.getProperty("L1Item")

    # L1 configuration parameters
    self.__hypo = TrigEgammaL1CaloHypoTool( l1item
                                            WPNames        =  ['Tight','Medium','Loose'], # must be: ["T","M","L"] (Tight,Medium and Loose)
                                            HadCoreCutMin  =  [ 1.0   ,  1.0  ,  1.0  ,  1.0  ], # must be a list with for values: (default,tight,medium and loose)
                                            HadCoreCutOff  =  [-0.2   , -0,2  , -0.2  , -0.2  ],
                                            HadCoreSlope 	 = [ 1/23. ,  1/23.,  1/23.,  1/23.],
                                            EmIsolCutMin   = [ 2.0   ,  1.0  ,  1.0  ,  1.5  ],
                                            EmIsolCutOff   = [-1.8   , -2.6  , -2.0  , -1.8  ],
                                            EmIsolSlope    = [ 1/8.  ,  1/8. ,  1/8. ,  1/8. ],
                                            IsolCutMax     = 50,
                                            L1Item         = l1item )

    if self.__hypo.initialize().isFailure():
      MSG_ERROR( self, "It's not possible to inialize the L1Calo hypo with item %s.", l1item)
      return StatusCode.FAILURE


    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Finalize method
  #
  def finalize(self):

    self.__hypo.finalize()
    self.fina_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept( self, context ):

    passed = self.__hypo.accept( context )
    return Accept( self.name(), [ ("Pass", passed] )



