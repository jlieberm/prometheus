
__all__ = ['EventInfo']

from Gaugi import EDM
from prometheus.enumerations  import Dataframe as DataframeEnum
from Gaugi  import StatusCode


class EventInfo(EDM):

    __eventBranches = {
            'SkimmedNtuple':
            [ 'EventNumber',
                'RunNumber',
                'Nvtx',
                'RandomRunNumber',
                'MCChannelNumber',
                'RandomLumiBlockNumber',
                'MCPileupWeight',
                'averageIntPerXing'],

            'PhysVal':
            [ 'RunNumber',
                'avgmu',
                'LumiBlock',
                'el_nPileupPrimaryVtx'],
            }

    def __init__(self):
        EDM.__init__(self)

    def initialize(self):
        try:
            if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
                # Link all branches
                for branch in self.__eventBranches["SkimmedNtuple"]:
                    self.setBranchAddress( self._tree, branch, self._event)
                    self._branches.append(branch) # hold all branches from the body class
            elif self._dataframe is DataframeEnum.PhysVal_v2:
                for branch in self.__eventBranches["PhysVal"]:
                    self.setBranchAddress( self._tree, branch , self._event)
                    self._branches.append(branch) # hold all branches from the body class
            else:
                self._warning( "Electron object can''t retrieved" )
                return StatusCode.FAILURE
            # Success
            return StatusCode.SUCCESS
        except TypeError as e:
            self._logger.error("Impossible to create the EventInfo Container. Reason:\n%s", e)
            return StatusCode.FAILURE

    def nvtx(self):
        """
          Retrieve the Nvtx information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
            return self._event.Nvtx
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.el_nPileupPrimaryVtx
        else:
            self._logger.warning("Impossible to retrieve the value of nvtx. Unknow dataframe.")

    def avgmu(self):
        """
          Retrieve the avgmu information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
            return self._event.averageIntPerXing
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.avgmu
        else:
            self._logger.warning("Impossible to retrieve the value of avgmu. Unknow dataframe.")

    def RunNumber(self):
        """
          Retrieve the avgmu information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
            return self._event.RunNumber
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.RunNumber
        else:
            self._logger.warning("Impossible to retrieve the value of avgmu. Unknow dataframe.")

    def LumiBlock(self):
        """
          Retrieve the avgmu information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
            return -999
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return self._event.LumiBlock
        else:
            self._logger.warning("Impossible to retrieve the value of LB. Unknow dataframe.")


    def MCPileupWeight(self):
        """
          Retrieve the Pileup Weight information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.SkimmedNtuple_v2:
            return self._event.MCPileupWeight
        elif self._dataframe is DataframeEnum.PhysVal_v2:
            return 1
        else:
            self._logger.warning("Impossible to retrieve the value of MC Pileup Weight")


    def id(self):
        return self._id

    def setId(self, v):
        self._id = v





