
__all__ = [ 'Dataframe' ]


from Gaugi import EnumStringification

class Dataframe(EnumStringification):
  
  # from the simulator.
  Delphes = -2
  Lorenzet = -1        # special dataframe used for the lab. first simulator (for future).
  # from athena ATLAS detector
  PhysVal = 0         # decrepted
  SkimmedNtuple  = 1  # decrepted
  MuonPhysVal = 2     # for future (muon studies)
  PhysVal_v2 = 3
  SkimmedNtuple_v2  = 4



