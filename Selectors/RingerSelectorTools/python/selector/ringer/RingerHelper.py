
__all__ = ['RingerPidConfs', 'ElectronRingerPid']

from RingerCore import Logger, EnumStringification
#from rDev.tools.emulation.selector import PreprocessorDefs


# @brief: the electron working point 
class ElectronRingerPid(EnumStringification):
  
  OfflineTight = -4
  OfflineMedium = -3
  OfflineLoose = -2
  OfflineVeryLoose = -1
  Tight = 0
  Medium = 1
  Loose = 2
  VeryLoose = 3


class RingerPidConfs(Logger):

  """
    This class will be responsible to build all calib
    paths and point the hypo to the ATLAS calib area files.
    This will be implemented here for now. To switch between
    tuning, you just need add this in your job option
    e.g:
    from TriggerMenu.egamma.EgammaSliceFlags import EgammaSliceFlags
    EgammaSliceFlags.ringerVersion = 'RingerSelectorTools/file_of_your_ringer_confs'
  """

  _signatureDict = {
      'signature' : ['e','g'],
  }

  _pidMap = {
      'tight'    : 'tight'  , 
      'medium'   : 'medium' , 
      'loose'    : 'loose'  , 
      'veryloose': 'vloose' ,
      ### Offline
      'offlinetight'     : 'egtight',
      'offlinemedium'    : 'egmedium',
      'offlineloose'     : 'egloose',
      'offlineveryloose' : 'egvloose',

      }

  # The default path for ringer selectors. The standard cuts will be the ringer v6 tuning for now.
  # Last modification in: 2017/02/21
  # MC15c tuning if pileup corrention using data 2016 (periods A to K) to fix all thresholds values
  _default_basepath = 'RingerSelectorTools/TrigL2_20170221_v6'

  def __init__(self):
    
    Logger.__init__(self)

    #TODO: Use this to configurate the calib path from triggerMenu flags
    #from TriggerMenu.egamma.EgammaSliceFlags import EgammaSliceFlags
    #if EgammaSliceFlags.ringerVersion():
    #  self._basePath = EgammaSliceFlags.ringerVersion()
    #  self._logger.info('TrigMultiVarHypo version: %s',self._basePath)
    #else:
    #  self._basePath = self._default_basepath
    #  self._logger.info('TrigMultiVarHypo version: %s (default)',self._basePath)
    self._basePath = self._default_basepath

    # Electron files
    self._electronConstants = {
        # trigger config files
        'vloose'   : 'TrigL2CaloRingerElectronVeryLooseConstants.root',
        'loose'    : 'TrigL2CaloRingerElectronLooseConstants.root',
        'medium'   : 'TrigL2CaloRingerElectronMediumConstants.root',
        'tight'    : 'TrigL2CaloRingerElectronTightConstants.root',
        # Offline config files
        'egvloose' : 'ElectronRingerVeryLooseConstants.root',
        'egloose'  : 'ElectronRingerLooseConstants.root',
        'egmedium' : 'ElectronRingerMediumConstants.root',
        'egtight'  : 'ElectronRingerTightConstants.root',


        }
    self._electronCutDefs = {
        # trigger config files
        'vloose' : 'TrigL2CaloRingerElectronVeryLooseThresholds.root',
        'loose'  : 'TrigL2CaloRingerElectronLooseThresholds.root',
        'medium' : 'TrigL2CaloRingerElectronMediumThresholds.root',
        'tight'  : 'TrigL2CaloRingerElectronTightThresholds.root',
        # Offline config files
        'egvloose' : 'ElectronRingerVeryLooseThresholds.root',
        'egloose'  : 'ElectronRingerLooseThresholds.root',
        'egmedium' : 'ElectronRingerMediumThresholds.root',
        'egtight'  : 'ElectronRingerTightThresholds.root',
        
        }

    #TODO: photon paths for future
    self._photonConstants = {
        'vloose' : 'TrigL2CaloRingerPhotonVeryLooseConstants.root',
        'loose'  : 'TrigL2CaloRingerPhotonLooseConstants.root',
        'medium' : 'TrigL2CaloRingerPhotonMediumConstants.root',
        'tight'  : 'TrigL2CaloRingerPhotonTightConstants.root',
        }
    self._photonCutDefs = {
        'vloose' : 'TrigL2CaloRingerPhotonVeryLooseThresholds.root',
        'loose'  : 'TrigL2CaloRingerPhotonLooseThresholds.root',
        'medium' : 'TrigL2CaloRingerPhotonMediumThresholds.root',
        'tight'  : 'TrigL2CaloRingerPhotonTightThresholds.root',
        }

    
  def get_constants_path(self, trigType, IDinfo):
    if not (trigType[0] in self._signatureDict['signature']):
      raise RuntimeError('Bad signature')
    # is Electron
    if self._signatureDict['signature'][0] in trigType:
      return self._basePath + '/' +self._electronConstants[self._pidMap[IDinfo]]
    else: #is Photon
      #TODO: this will be uncoment when we have photon tuning 
      #return self._basePath + '/' +self._photonConstants[self._pidMap[IDinfo]]
      return str()

  def get_cutDefs_path(self, trigType, IDinfo):
    if not (trigType[0] in self._signatureDict['signature']):
      raise RuntimeError('Bad signature')
    # is Electron
    if self._signatureDict['signature'][0] in trigType:
      return self._basePath + '/' +self._electronCutDefs[self._pidMap[IDinfo]]
    else: #is Photon
      #TODO: this will be uncoment when we have photon tuning 
      #return self._basePath + '/' +self._photonCutDefs[self._pidMap[IDinfo]]
      return str() 


  def setCalibPath(self, basepath):
    self._basePath = basepath




