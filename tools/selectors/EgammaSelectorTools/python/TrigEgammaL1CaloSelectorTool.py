
__all__ = ['TrigEgammaL1CaloSelectorTool']

from Gaugi import Algorithm, StatusCode
from Gaugi import checkForUnusedVars, retrieve_kw
from Gaugi.messenger.macros import *
from EventAtlas import Accept
import numpy as np
import math
import re


class TrigEgammaL1CaloSelectorTool( Algorithm ):

  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name)
    # L1 configuration parameters
    
    self._wpNames        = retrieve_kw( kw, 'WPNames' 			,        ['Tight','Medium','Loose']) # must be: ["T","M","L"] (Tight,Medium and Loose)
    self._hadCoreCutMin  = retrieve_kw( kw, 'HadCoreCutMin'	, [ 1.0   ,  1.0  ,  1.0  ,  1.0  ]) # must be a list with for values: (default,tight,medium and loose)
    self._hadCoreCutOff  = retrieve_kw( kw, 'HadCoreCutOff'	, [-0.2   , -0,2  , -0.2  , -0.2  ])
    self._hadCoreSlope   = retrieve_kw( kw, 'HadCoreSlope'	, [ 1/23. ,  1/23.,  1/23.,  1/23.])
    self._emIsolCutMin   = retrieve_kw( kw, 'EmIsolCutMin'	, [ 2.0   ,  1.0  ,  1.0  ,  1.5  ])
    self._emIsolCutOff   = retrieve_kw( kw, 'EmIsolCutOff'	, [-1.8   , -2.6  , -2.0  , -1.8  ])
    self._emIsolCutSlope = retrieve_kw( kw, 'EmIsolSlope'		, [ 1/8.  ,  1/8. ,  1/8. ,  1/8. ])
    self._isolMaxCut     = retrieve_kw( kw, 'IsolCutMax'		, 50 )
    self._l1item         = retrieve_kw( kw, 'L1Item'        , 'L1_EM3' ) # default
    checkForUnusedVars(kw)


  def initialize(self):
    
    self._l1type      = self._l1item.replace('L1_','')
    self._l1threshold = float(re.findall('\d+', self._l1type)[0])
    self.init_lock()
    return StatusCode.SUCCESS



  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  def accept( self, context ):

    l1 = context.getHandler( "HLT__EmTauRoIContainer" )
    accept = Accept( self.name() )
    passed = self.emulation( l1, self._l1type, self._l1item, self._l1threshold )
    accept.setCutResult( "Pass" , passed )
    return accept


  def emulation(self, l1, l1type, L1Item, l1threshold):
    
    c=0
    if(self._wpNames[0] in l1type):  c=1 # Tight
    if(self._wpNames[1] in l1type):  c=2 # Medium
    if(self._wpNames[2] in l1type):  c=3 # Loose
    hadCoreCutMin  = self._hadCoreCutMin[c]
    hadCoreCutOff  = self._hadCoreCutOff[c]
    hadCoreSlope   = self._hadCoreSlope[c]
    emIsolCutMin   = self._emIsolCutMin[c] 
    emIsolCutOff   = self._emIsolCutOff[c]
    emIsolCutSlope = self._emIsolCutSlope[c]
    
    # hadCoreCutMin = 1.0; // This could be defined somewhere else
    # hadCoreCutOff = -0.2;
    # hadCoreSlope = 1/23.0;
    # emIsolCutMin = 2.0; // This could be defined somewhere else
    # emIsolCutOff = -1.8;
    # emIsolCutSlope = 1/8.0;
    
    emE = 0.0
    emIsol = 0.0
    hadCore = 0.0
    eta = 0.0
    
    emE     = l1.emClus()/1.e3   # Cluster energy
    eta     = l1.eta()           # eta
    hadCore = l1.hadCore()/1.e3  # Hadronic core energy
    emIsol  = l1.emIsol()/1.e3   # EM Isolation energy
    
    if ('H' in l1type):
      self._logger.debug("L1 (H) CUT")
      if not self.isolationL1(hadCoreCutMin,hadCoreCutOff,hadCoreSlope,hadCore,emE):
        self._logger.debug("rejected")
        return False
      self._logger.debug("accepted")
    
    if ('I' in l1type):
      self._logger.debug("L1 (I) CUT")
      if not self.isolationL1(emIsolCutMin,emIsolCutOff,emIsolCutSlope,emIsol,emE):
        self._logger.debug("rejected")
        return False
      self._logger.debug("accepted")
    
    
    if ('V' in l1type):
      self._logger.debug("L1 (V) CUT")
      if not self.variableEtL1(L1Item,emE,eta):
        self._logger.debug("rejected")
        return False
      self._logger.debug("accepted")
    
    # add new method for this also
    elif  (emE <= l1threshold): # // this cut is confirmed to be <=
      return False

    return True

     

  #//!==========================================================================
  #// (H) and (I) Hadronic core and electromagnetic isolation
  def isolationL1(self, min_, offset, slope, energy, emE):
  	
    if (emE > self._isolMaxCut):
      self._logger.debug("L1 Isolation skipped, ET > Maximum isolation")
      return True
    
    isolation = offset + emE*slope
    if (isolation < min_): isolation = min_;
    
    value = False if (energy > isolation) else True
    #self._logger.debug( ("L1 Isolation ET = %1.3f ISOLATION CUT %1.3f")%(energy,isolation) )
    return value
  
  #//!==========================================================================
  #// (V) Variable Et cut
  def variableEtL1(self, L1item, l1energy, l1eta):
  	cut = self.emulationL1V(L1item,l1eta)
  	energy = l1energy
  	# if (energy <= cut) return false;
  	value = False if (energy <= cut) else True
  	return value
  
  
  #//!==========================================================================
  #// Eta dependant cuts for (V)
  def emulationL1V(self, L1item, l1eta):
    # Values updated from TriggerMenu-00-13-26
    # Now they all look symmetric in negative and positive eta
    # look that in general que can remove the first region since it is the defaul value
    cut=0.0
    # float eta = fabs((int)l1eta*10);
    eta = math.fabs(l1eta)


    if (L1item=="50V"):
      if (eta >= 0.8 and eta < 1.2): cut = 51.0
      elif (eta >= 1.2 and eta < 1.6): cut = 50.0
      elif (eta >= 1.6 and eta < 2.0): cut = 51.0
      else: cut = 52;
    
    elif (L1item=="8VH"):
      if   (eta > 0.8 and eta <= 1.1): cut = 7.0
      elif (eta > 1.1 and eta <= 1.4): cut = 6.0
      elif (eta > 1.4 and eta <= 1.5): cut = 5.0
      elif (eta > 1.5 and eta <= 1.8): cut = 7.0
      elif (eta > 1.8 and eta <= 2.5): cut = 8.0
      else: cut = 9.0
    
    elif (L1item=="10VH"):
      if   (eta > 0.8 and eta <= 1.1): cut = 9.0
      elif (eta > 1.1 and eta <= 1.4): cut = 8.0
      elif (eta > 1.4 and eta <= 1.5): cut = 7.0
      elif (eta > 1.5 and eta <= 1.8): cut = 9.0
      elif (eta > 1.8 and eta <= 2.5): cut = 10.0
      else: cut = 11.0
    
    elif (L1item=="13VH"):
      if   (eta > 0.7 and eta <= 0.9): cut = 14.0
      elif (eta > 0.9 and eta <= 1.2): cut = 13.0
      elif (eta > 1.2 and eta <= 1.4): cut = 12.0
      elif (eta > 1.4 and eta <= 1.5): cut = 11.0
      elif (eta > 1.5 and eta <= 1.7): cut = 13.0
      elif (eta > 1.7 and eta <= 2.5): cut = 14.0
      else: cut = 15.0
    
    elif (L1item=="15VH"):
      if   (eta > 0.7 and eta <= 0.9): cut = 16.0
      elif (eta > 0.9 and eta <= 1.2): cut = 15.0
      elif (eta > 1.2 and eta <= 1.4): cut = 14.0
      elif (eta > 1.4 and eta <= 1.5): cut = 13.0
      elif (eta > 1.5 and eta <= 1.7): cut = 15.0
      elif (eta > 1.7 and eta <= 2.5): cut = 16.0
      else: cut = 17.0
    
    elif (L1item == "18VH"):
      if   (eta > 0.7 and eta <= 0.8): cut = 19.0
      elif (eta > 0.8 and eta <= 1.1): cut = 18.0
      elif (eta > 1.1 and eta <= 1.3): cut = 17.0
      elif (eta > 1.3 and eta <= 1.4): cut = 16.0
      elif (eta > 1.4 and eta <= 1.5): cut = 15.0
      elif (eta > 1.5 and eta <= 1.7): cut = 17.0
      elif (eta > 1.7 and eta <= 2.5): cut = 19.0
      else: cut = 20.0
    
    elif (L1item == "20VH"):
      if   (eta > 0.7 and eta <= 0.8): cut = 21.0
      elif (eta > 0.8 and eta <= 1.1): cut = 20.0
      elif (eta > 1.1 and eta <= 1.3): cut = 19.0
      elif (eta > 1.3 and eta <= 1.4): cut = 18.0
      elif (eta > 1.4 and eta <= 1.5): cut = 17.0
      elif (eta > 1.5 and eta <= 1.7): cut = 19.0
      elif (eta > 1.7 and eta <= 2.5): cut = 21.0
      else: cut = 22.0
    
    elif (L1item == "20VHI"): # Same as 20VH
      if   (eta > 0.7 and eta <= 0.8): cut = 21.0
      elif (eta > 0.8 and eta <= 1.1): cut = 20.0
      elif (eta > 1.1 and eta <= 1.3): cut = 19.0
      elif (eta > 1.3 and eta <= 1.4): cut = 18.0
      elif (eta > 1.4 and eta <= 1.5): cut = 17.0
      elif (eta > 1.5 and eta <= 1.7): cut = 19.0
      elif (eta > 1.7 and eta <= 2.5): cut = 21.0
      else: cut = 22.0
    
    elif (L1item == "22VHI"):
      if   (eta > 0.7 and eta <= 0.8): cut = 23.0
      elif (eta > 0.8 and eta <= 1.1): cut = 22.0
      elif (eta > 1.1 and eta <= 1.3): cut = 21.0
      elif (eta > 1.3 and eta <= 1.4): cut = 20.0
      elif (eta > 1.4 and eta <= 1.5): cut = 19.0
      elif (eta > 1.5 and eta <= 1.7): cut = 21.0
      elif (eta > 1.7 and eta <= 2.5): cut = 23.0
      else: cut = 24.0


    return cut




