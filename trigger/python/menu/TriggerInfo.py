
__all__ = ["TriggerInfo"]


from Gaugi.messenger import Logger
from Gaugi.messenger.macros import *

import re 

#
# Trigger info
#
class TriggerInfo(Logger):
  
  #
  # Constructor
  #
  def __init__(self, trigger):

    Logger.__init__(self)
    # Compile all internal variables
    self.compile(trigger)


  #
  # Compile the trigger flags from the chain name
  #
  def compile(self, trigger):

    self.__trigger = trigger

    if trigger.startswith('HLT_'):
      trigger = trigger.replace( 'HLT_','')
      
    trigParts = trigger.split('_')

    part = trigParts[0]
    if part[0]=='e':
      self.__signature = 'electron'
      from TrigEgammaEmulationTool import electron_chainDict as chainDict
    elif part[0]=='g':
      self.__signature = 'photon'
      from TrigEgammaEmulationTool import photon_chainDict as chainDict
    else:
      MSG_FATAL( self, "Signature not found" )

    # Get the energy threshold
    self.__etthr = float( part[1::] )
    
    self.__pidname = 'etcut'
    for pidname in chainDict['idInfo']:
      if pidname == trigParts[1]:
        self.__pidname = pidname; break
    
 
    # check the ringer flag
    if 'noringer' in trigger:
      self.__ringer = False
    elif 'ringerss' in trigger:
      self.__ringerss = True
      self.__ringer = False
    elif 'ringer' in trigger and 'ringerss' not in trigger:
      self.__ringer = True
    else:
      self.__ringer = True

    self.__ringerVersion = None

    if self.__ringer:
      for version in chainDict['ringerVersion']:
        if version in trigger:
          self.__ringerVersion = version

      for extraInfo in chainDict['ringerExtraInfo']:
        if extraInfo in trigger:
          self.__ringerVersion += '_' + extraInfo

   
    self.__isolationType=None
    self.__isolated = False

    for isoInfo in chainDict['isoInfo']:
      if isoInfo in trigger:
        self.__isolationType = isoInfo
        self.__isolated = True
        break

  
  #
  # Get the signature
  #
  def signature(self):
    return self.__signature

  #
  # Get the eT threshold
  #
  def etthr(self):
    return self.__etthr

  #
  # Is a ringer chain?
  #
  def ringer(self):
    return self.__ringer

  def ringerss(self):
    return self.__ringerss


  #
  # Get the ringer tuning version
  #
  def ringerVersion(self):
    return self.__ringerVersion

  #
  # Get the chain name
  #
  def trigger(self):
    return self.__trigger

  #
  # Get the  operation point
  #
  def pidname(self):
    return self.__pidname


  #
  # This trigger is isolated
  #
  def isolated(self):
    return self.__isolated


  #
  # Get the isolation pid name
  #
  def isolationType( self ):
    return self.__isolationType
      

  #
  # Get the pid index 
  #
  def pidnameIdx(self):

    if 'tight' in self.__pidname:
      return 0
    elif 'medium' in self.__pidname:
      return 1
    elif 'loose' in self.__pidname:
      return 2
    elif 'vloose' in self.__pidname:
      return 3
    else:
      return 0



 







