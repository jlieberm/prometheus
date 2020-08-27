
from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite,TColor
from Gaugi.messenger import LoggingLevel, Logger
from EfficiencyTools import PlotProfiles
from Gaugi.storage import  restoreStoreGate
from ROOT import gROOT
gROOT.SetBatch(True)

theseColors = [kBlack, kGray+2, kBlue-4, kBlue-2]


mainLogger = Logger.getModuleLogger("job")
mainLogger.level = LoggingLevel.INFO


def plot_table( sg, logger, trigger, basepath ):
  triggerLevels = ['L1Calo','L2Calo','L2','EFCalo','HLT']
  logger.info( '{:-^78}'.format((' %s ')%(trigger)) ) 
  
  for trigLevel in triggerLevels:
    dirname = basepath+'/'+trigger+'/Efficiency/'+trigLevel
    total  = sg.histogram( dirname+'/eta' ).GetEntries()
    passed = sg.histogram( dirname+'/match_eta' ).GetEntries()
    eff = passed/float(total) * 100. if total>0 else 0
    eff=('%1.2f')%(eff); passed=('%d')%(passed); total=('%d')%(total)
    stroutput = '| {0:<30} | {1:<5} ({2:<5}, {3:<5}) |'.format(trigLevel,eff,passed,total)
    logger.info(stroutput)
  logger.info( '{:-^78}'.format((' %s ')%('-')))







inputFile = 'teste.root'
basepath = 'Event/EfficiencyTool'



sg =  restoreStoreGate( inputFile )



triggers = [ 'HLT_g10_etcut',
             ]


eff_et  = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_et' ) for trigger in triggers ]
eff_eta = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_eta' ) for trigger in triggers ]
eff_phi = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_phi' ) for trigger in triggers ]
eff_mu  = [ sg.histogram( basepath+'/'+trigger+'/Efficiency/HLT/eff_mu' ) for trigger in triggers ]
          

legends = ['tight','medium','loose']

PlotProfiles( eff_et, legends=legends,runLabel='mc16 13TeV', outname='efficiency_mc16_13TeV_DP_probes_medium_eff_et.pdf', theseColors=theseColors,
              extraText1=triggers,doRatioCanvas=False, legendX1=.65, xlabel='E_{T} [GeV]', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_eta, legends=legends,runLabel='mc16 13TeV', outname='efficiency_mc16_13TeV_DP_probes_medium_eff_eta.pdf',theseColors=theseColors,
              extraText1=triggers,doRatioCanvas=False, legendX1=.65, xlabel='#eta', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_phi, legends=legends,runLabel='mc16 13TeV', outname='efficiency_mc16_13TeV_DP_probes_medium_eff_phi.pdf',theseColors=theseColors,
              extraText1=triggers,doRatioCanvas=False, legendX1=.65, xlabel='#phi', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

PlotProfiles( eff_mu, legends=legends,runLabel='mc16 13TeV', outname='efficiency_mc16_13TeV_DP_probes_medium_eff_mu.pdf',theseColors=theseColors,
              extraText1=triggers,doRatioCanvas=False, legendX1=.65, xlabel='<#mu>', rlabel='Trigger/Ref.',ylabel='Trigger Efficiency')

for trigger in triggers:
  plot_table( sg, mainLogger, trigger, basepath )


for trigger in triggers:
  plot_table( sg, mainLogger, trigger, basepath )



