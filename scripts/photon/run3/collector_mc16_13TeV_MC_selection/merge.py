

from CollectorTool  import CreateData

cdata  = CreateData(10)

#cdata( 'cern_data/test/EGAM1/', 'cern_data/test/EGAM7/', 'data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.VProbes_EGAM7.GRL_v97' )
cdata( '~/prometheus/scripts/photon/run3/collector_mc16_13TeV_MC_selection/mc16_13TeV_photons_mcProbes/', '~/prometheus/scripts/photon/run3/collector_mc16_13TeV_MC_selection/mc16_13TeV_photons_mcFakes/', '~/datasets/trigger/photons/npz/mc16_13TeV.sgn.probes_MC_DP.bkg.noMC.JF17' )
#cdata( 'EGAM2_17/', 'EGAM7_17/', 'data17_13TeV.sgn.probes_lhmedium_Jpsi.bkg.EGAM7' )
#cdata( 'EGAM2_18/', 'EGAM7_18/', 'data18_13TeV.sgn.probes_lhmedium_Jpsi.bkg.EGAM7' )



