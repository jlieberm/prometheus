
__all__ = ['CaloTowers']

from prometheus.core.EnumCollection import Dataframe as DataframeEnum
from prometheus.core.StatusCode     import StatusCode
from prometheus.dataframe.EDM       import EDM
from RingerCore                     import EnumStringification
import numpy as np




##############
##   ECAL
##############
#pi=np.pi
#PhiBins_barrel  = []
#PhiBins_endcap  = []
#PhiBins_forward = []
#EtaBins_barrel  = []
#EtaBins_endcap  = []
#EtaBins_forward = []
#
## lists of the edges of each tower in eta and phi
## each list starts with the lower edge of the first tower
## the list ends with the higher edged of the last tower
#
## assume 0.02 x 0.02 resolution in eta,phi in the barrel |eta| < 1.5
#for i in range(-180, 180+1):
#  PhiBins_barrel.append(i * pi/180.0)
#
#
## 0.02 unit in eta up to eta = 1.5 (barrel)
#for i in range(-85,86+1):
#  EtaBins_barrel.append(i * 0.0174)
#
#
## assume 0.02 x 0.02 resolution in eta,phi in the endcaps 1.5 < |eta| < 3.0
#PhiBins_endcap = PhiBins_barrel
### 0.02 unit in eta up to eta = 3
#for i in range(1,84+1):
#  EtaBins_endcap.append( -2.958 + i * 0.0174 )
#for i in range(1,84+1):
#  EtaBins_endcap.append(  1.4964 + i * 0.0174)
#
# 
### take present CMS granularity for HF
### 0.175 x (0.175 - 0.35) resolution in eta,phi in the HF 3.0 < |eta| < 5.0
#PhiBins_forward=[]
#for i  in range(-18,18+1):
#  PhiBins_forward.append( i * pi/18.0 )
#EtaBins_forward = [-5.0, -4.7, -4.525, -4.35, -4.175, -4.0, -3.825, -3.65, -3.475, -3.3, -3.125, -2.958, 3.125, 3.3, 3.475, 3.65, 3.825, 4.0, 4.175, 4.35, 4.525, 4.7, 5.0]
#
# 
#EtaBins_barrel.sort()
#EtaBins_endcap.sort()
#PhiBins_endcap.sort()
#EtaBins_forward.sort()

class CaloTowers(EDM):

  __eventBranches = [ 
                    ]

  def __init__(self):
    EDM.__init__(self)

  def initialize(self):
    self._event = self._tree.UseBranch("Tower")
    return StatusCode.SUCCESS
    
  #def sizet(self):
  #  n = self._event.GetEntries()
  #  from ROOT import TH2F, TCanvas
  #  barrel = TH2F( 'barrel', 'barrel;#eta;#phi', len(EtaBins_barrel)+1, np.array(EtaBins_barrel), len(PhiBins_barrel)+1, np.array(PhiBins_barrel))
  #  for i in range(n):
  #    tower = self._event.At(i)
  #    barrel.Fill( tower.Eta, tower.Phi, tower.Eem )

  #  c1 = TCanvas('c1','c1',500,500)
  #  barrel.Draw('colz')
  #  c1.SaveAs('barrel_test.pdf')

