
__all__ = [ 'Dataframe', 'StatusTool','StatusWatchDog' ]


from Gaugi import EnumStringification

class Dataframe(EnumStringification):
  
  # from the simulator.
  Delphes = -2
  Geant = -1        # special dataframe used for the lab. first simulator (for future).
  # from athena ATLAS detector
  PhysVal = 0         # decrepted
  SkimmedNtuple  = 1  # decrepted
  MuonPhysVal = 2     # for future (muon studies)
  PhysVal_v2 = 3
  SkimmedNtuple_v2  = 4


class StatusTool(EnumStringification):
  """
    The status of the tool
  """
  IS_FINALIZED   = 3
  IS_INITIALIZED = 2 
  ENABLE  = 1
  DISABLE = -1
  NOT_INITIALIZED = -2
  NOT_FINALIZED = -3
 

class StatusWatchDog(EnumStringification):
  """
    Use this to enable or disable the tool in execute call
  """
  ENABLE  = 1
  DISABLE = 0



