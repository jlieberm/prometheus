
from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite,TColor
from EfficiencyTools import PlotProfiles
from Gaugi.storage import  restoreStoreGate
from ROOT import gROOT
gROOT.SetBatch(True)

theseColors = [kBlack, kGray+2, kBlue-2, kBlue-4]






inputFile = '../phd_data/efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium/efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium.root'
basepath = 'Event/EfficiencyTool'



sg =  restoreStoreGate( inputFile )



triggers = [ 
             "EMU_e17_lhvloose_nod0_noringer_L1EM15VHI",
             "EMU_e17_lhvloose_nod0_ringer_v6_L1EM15VHI",
             "EMU_e17_lhvloose_nod0_ringer_v8_L1EM15VHI",
             "EMU_e17_lhvloose_nod0_ringer_v10_L1EM15VHI",
             ]


eff_et  = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_et' ) for trigger in triggers ]
eff_eta = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_eta' ) for trigger in triggers ]
eff_phi = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_phi' ) for trigger in triggers ]
eff_mu  = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_mu' ) for trigger in triggers ]
          

legends = ['noringer', 'ringer v6', 'ringer v8', 'ringer v10']

PlotProfiles( eff_et, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e17_lhvloose_eff_et.pdf', theseColors=theseColors,
              extraText1='e17_lhvloose_nod0_L1EM15VHI',doRatioCanvas=False, legendX1=.65, xlabel='E_{T}', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_eta, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e17_lhvloose_eff_eta.pdf',theseColors=theseColors,
              extraText1='e17_lhvloose_nod0_L1EM15VHI',doRatioCanvas=False, legendX1=.65, xlabel='#eta', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_phi, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e17_lhvloose_eff_phi.pdf',theseColors=theseColors,
              extraText1='e17_lhvloose_nod0_L1EM15VHI',doRatioCanvas=False, legendX1=.65, xlabel='#phi', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_mu, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e17_lhvloose_eff_mu.pdf',theseColors=theseColors,
              extraText1='e17_lhvloose_nod0_L1EM15VHI',doRatioCanvas=False, legendX1=.65, xlabel='<#mu>', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')


triggers = [ 
             "EMU_e28_lhtight_nod0_noringer_ivarloose",
             "EMU_e28_lhtight_nod0_ringer_v6_ivarloose",
             "EMU_e28_lhtight_nod0_ringer_v8_ivarloose",
             "EMU_e28_lhtight_nod0_ringer_v10_ivarloose",
             ]


eff_et  = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_et' ) for trigger in triggers ]
eff_eta = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_eta' ) for trigger in triggers ]
eff_phi = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_phi' ) for trigger in triggers ]
eff_mu  = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_mu' ) for trigger in triggers ]
          

legends = ['noringer', 'ringer v6', 'ringer v8', 'ringer v10']

PlotProfiles( eff_et, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e28_lhtight_eff_et.pdf',theseColors=theseColors,
              extraText1='e28_lhtight_nod0_ivarloose',doRatioCanvas=False, legendX1=.65, xlabel='E_{T}', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_eta, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e28_lhtight_eff_eta.pdf',theseColors=theseColors,
              extraText1='e28_lhtight_nod0_ivarloose',doRatioCanvas=False, legendX1=.65, xlabel='#eta', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_phi, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e28_lhtight_eff_phi.pdf',theseColors=theseColors,
              extraText1='e28_lhtight_nod0_ivarloose',doRatioCanvas=False, legendX1=.65, xlabel='#phi', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_mu, legends=legends,runLabel='data18 13TeV', outname='efficiency_v10_data18_13TeV_EGAM1_probes_lhmedium_e28_lhtight_eff_mu.pdf',theseColors=theseColors,
              extraText1='e28_lhtight_nod0_ivarloose',doRatioCanvas=False, legendX1=.65, xlabel='<#mu>', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')



