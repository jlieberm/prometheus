
__all__ = ['FastPhoton']

from Gaugi import EDM
from Gaugi  import StatusCode
from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi import stdvector_to_list

class FastPhoton(EDM):

    __eventBranches = { 'SkimmedNtuple':
                    [
                      ],
                      'PhysVal':
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
        try:
            if self._dataframe is DataframeEnum.SkimmedNtuple:
                # Link all branches
                for branch in self.__eventBranches["SkimmedNtuple"]:
                    try:
                        self.setBranchAddress( self._tree, ('fcCand%d_%s')%(self._fcCand,branch), self._event)
                        self._branches.append(branch) # hold all branches from the body class
                    except:
                        self._logger.warning('Exception when try to setBranchAddress for %s...',branch)
            elif self._dataframe is DataframeEnum.PhysVal_v2:
                for branch in self.__eventBranches["PhysVal"]:
                    try:
                        self.setBranchAddress( self._tree, branch , self._event)
                        self._branches.append(branch) # hold all branches from the body class
                    except:
                        self._logger.warning('Exception when try to setBranchAddress for %s...',branch)
            else:
                self._logger.warning( "FastCalo object can''t retrieved" )
                return StatusCode.FAILURE
            return StatusCode.SUCCESS
        except TypeError as e:
            self._logger.error("Impossible to create the FastCalo Container. Reason:\n%s", e)
            return StatusCode.SUCCESS

    def pt(self):
        """
        Retrieve the pt information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_pt[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of pt. Unknow dataframe")


    def eta(self):
        """
        Retrieve the eta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_eta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_phi[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")

    def caloEta(self):
        """
        Retrieve the caloEta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_caloEta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of caloEta. Unknow dataframe")

    def numberOfTRTHits(self):
        """
        Retrieve the number of TRT hits information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_nTRTHits[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of nTRTHits. Unknow dataframe")

    def numberOfTRTHiThresholdHits(self):
        """
        Retrieve the number of TRT high thresholdhits information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_nTRTHiThresholdHits[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of nTRTHiThrehsoldHits. Unknow dataframe")


    def etOverPt(self):
        """
        Retrieve the et/pt information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple:
            return
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.trig_L2_ph_etOverPt[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of et/pt. Unknow dataframe")

    def size(self):
        return self._event.trig_L2_el_pt.size()