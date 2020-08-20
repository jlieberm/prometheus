
__all__ = [ 'Dataframe' ]


from Gaugi import EnumStringification

class Dataframe(EnumStringification):
  
  # from athena ATLAS detector
  PhysVal = 0         # decrepted
  SkimmedNtuple  = 1  # decrepted
  MuonPhysVal = 2     # for future (muon studies)
  PhysVal_v2 = 3
  SkimmedNtuple_v2  = 4
  Electron_v1 = 5
  Photon_v1 = 6