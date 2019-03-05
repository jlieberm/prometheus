
__all__ = ["TDT", "DecisionCore", "AcceptType"]




from Gaugi  import Dataframe as DataframeEnum
from Gaugi  import StatusCode, EnumStringification
from Events import EDM
from Gaugi.utilities import stdvector_to_list



class AcceptType(EnumStringification):

  L1Calo = 0
  L2Calo = 1
  L2     = 2
  EFCalo = 3
  HLT    = 4


class DecisionCore(EnumStringification):
  # Athena navigation core
  TriggerDecisionTool = 0
  # Athena e/g emulation tool
  TrigEgammaEmulationTool = 1



class TDT(EDM):
  # define all skimmed branches here.
  __eventBranches = {
      "SkimmedNtuple" : [ # default skimmed ntuple branches
                        ],
      "PhysVal"       : [
                          'trig_tdt_L1_calo_accept',
                          'trig_tdt_L2_calo_accept',
                          'trig_tdt_L2_el_accept',
                          'trig_tdt_EF_calo_accept',
                          'trig_tdt_EF_el_accept',
                          'trig_tdt_emu_L1_calo_accept',
                          'trig_tdt_emu_L2_calo_accept',
                          'trig_tdt_emu_L2_el_accept',
                          'trig_tdt_emu_EF_calo_accept',
                          'trig_tdt_emu_EF_el_accept',
                        ],
                }


  def __init__(self):
    EDM.__init__(self)
    # force this class to hold some extra params to read the external information
    # into a root file. This is call by metadata information. Usually, this metadata
    # is stored into the same basepath as the main ttree (event).
    self._useMetadataParams = True
    # the name of the ttree metadata where is stored the information
    # do not change is name.
    self._metadataName = 'tdt'
    # decision core (default)
    self._core = DecisionCore.TriggerDecisionTool


  def core(self, core):
    if core is (DecisionCore.TriggerDecisionTool) or (DecisionCore.TrigEgammaEmulationTool):
      self._core = core
    else:
      self._logger.error('DecisionCore type unknow')


  def initialize(self):

    import ROOT
    from RingerCore import stdvector_to_list
    if not (self._dataframe is DataframeEnum.PhysVal_v2):
      self._logger.warning('Not possible to initialize this metadata using this dataframe. skip!')
      return StatusCode.SUCCESS
    
    inputFile = self._metadataParams['file']
    
    # Check if file exists
    f  = ROOT.TFile.Open(inputFile, 'read')
    if not f or f.IsZombie():
      self._warning('Couldn''t open file: %s', inputFile)
      return StatusCode.FAILURE
    
    # Inform user whether TTree exists, and which options are available:
    self._debug("Adding file: %s", inputFile)
    treePath = self._metadataParams['basepath'] + '/' + self._metadataName
    obj = f.Get(treePath)
    if not obj:
      self._logger.warning("Couldn't retrieve TTree (%s)!", treePath)
      self._logger.info("File available info:")
      f.ReadAll()
      f.ReadKeys()
      f.ls()
      return StatusCode.FAILURE
    elif not isinstance(obj, ROOT.TTree):
      self._logger.fatal("%s is not an instance of TTree!", treePath, ValueError)
  
    try:
      obj.GetEntry(0)
      self._triggerList = stdvector_to_list(obj.trig_tdt_triggerList)
    except:
      self._logger.error("Can not extract the trigger list from the metadata file.")
      return StatusCode.FAILURE

    for trigItem in self._triggerList:
      self._logger.info("Metadata trigger: %s", trigItem)

    # try to get all triggers into the TDT metadata information
    try:
      for branch in self.__eventBranches["PhysVal"]:
      	self.setBranchAddress( self._tree, branch  , self._event)
        self._branches.append(branch) # hold all branches from the body class
      # Success
      return StatusCode.SUCCESS
    except:
      self._logger.warning("Impossible to create the TDTMetaData Container")
      return StatusCode.FAILURE


  def isPassed(self, trigItem):
    return self.ancestorPassed(trigitem,AcceptType.HLT, ignoreDeactivateRois=True)

  
  def isActive(self, trigItem):
    if trigItem in self._triggerList:
      #for idx , t in enumerate(self._triggerList):
      #  print idx,' = ',t,' = ',self._event.trig_tdt_EF_calo_accept[idx], '---> bool? ', bool(self._event.trig_tdt_EF_calo_accept[idx])
      idx = self._triggerList.index(trigItem)
      isGood = (self._event.trig_tdt_L1_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L1_calo_accept[idx])
      return False if isGood<0 else True
    else:
      return False


  def ancestorPassed( self, trigItem, acceptType ):
    """
      Method to retireve the bool accept for a trigger. To use this:
        l2caloPassed = tdt.ancestorPassed("HLT_e28_lhtight_nod0_ivarloose", AcceptType.L2Calo)
    """
    if trigItem in self._triggerList:
      # Has TE match with the offline electron/photon object
      idx = self._triggerList.index(trigItem)
      isGood = (self._event.trig_tdt_L1_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L1_calo_accept[idx])
      if isGood<0:
        return False

      if   acceptType is AcceptType.L1Calo:
        return bool(self._event.trig_tdt_L1_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L1_calo_accept[idx])
      elif acceptType is AcceptType.L2Calo:
        return bool(self._event.trig_tdt_L2_calo_accept[idx]if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L2_calo_accept[idx])
      elif acceptType is AcceptType.L2:
        return bool(self._event.trig_tdt_L2_el_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L2_el_accept[idx])
      elif acceptType is AcceptType.EFCalo:
        ef = bool(self._event.trig_tdt_EF_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_calo_accept[idx])
        return bool(self._event.trig_tdt_EF_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_calo_accept[idx])
      elif acceptType is AcceptType.HLT:
        return bool(self._event.trig_tdt_EF_el_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_el_accept[idx])
      else:
        self._logger.error('Trigger type not suppported.')
    else:
      self._logger.warning('Trigger %s not storage in TDT metadata.',trigItem)






