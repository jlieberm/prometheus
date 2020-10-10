
__all__ = ['FastPhoton']

from Gaugi import EDM
from Gaugi  import StatusCode
from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi import stdvector_to_list

class FastPhoton(EDM):

    __eventBranches = {
                      'Photon_v1':
                    [
                      'trig_L2_ph_pt',
                      'trig_L2_ph_caloEta',
                      'trig_L2_ph_eta',
                      'trig_L2_ph_phi',
                      'trig_L2_ph_nTRTHits',
                      'trig_L2_ph_nTRTHiThresholdHits',
                      'trig_L2_ph_etOverPt',
                    ]
                }

    def __init__(self):
        EDM.__init__(self)


    def initialize(self):
        """
          Initialize all branches
        """
        if self._dataframe is DataframeEnum.Photon_v1:
            self.link( self.__eventBranches["Photon_v1"] )
            return StatusCode.SUCCESS
        else:
            self._logger.warning( "Can not initialize the FastPhoton object. Dataframe not available." )
            return StatusCode.FAILURE
        


    def pt(self):
        """
          Retrieve the pt information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_pt[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of pt. Unknow dataframe")


    def eta(self):
        """
        Retrieve the eta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_eta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_phi[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")

    def caloEta(self):
        """
        Retrieve the caloEta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_caloEta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of caloEta. Unknow dataframe")

    def numberOfTRTHits(self):
        """
        Retrieve the number of TRT hits information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_nTRTHits[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of nTRTHits. Unknow dataframe")

    def numberOfTRTHiThresholdHits(self):
        """
        Retrieve the number of TRT high thresholdhits information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_nTRTHiThresholdHits[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of nTRTHiThrehsoldHits. Unknow dataframe")


    def etOverPt(self):
        """
        Retrieve the et/pt information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_ph_etOverPt[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of et/pt. Unknow dataframe")

    def size(self):
        return self._event.trig_L2_el_pt.size()
