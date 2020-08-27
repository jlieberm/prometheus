#!/usr/bin/env python



from Gaugi import progressbar, expandFolders
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi.gtypes import NotSet
from ROOT import gROOT
import argparse
import os



mainLogger = Logger.getModuleLogger("PlotTools", LoggingLevel.INFO)
# Mute ROOT logger
gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;")

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-d','--dirs', action='store',
    dest='dirs', required = True, default = None, nargs='+',
    help = "The reference file location for each bundle: e.g. path_1, path_2, ..., path_n")

parser.add_argument('-e','--emulation_list', action='store',
    dest='emulation_list', required = False, default = None, nargs='+', type=int,
    help = "Choose the dir index to use as emulation.")

parser.add_argument('-o','--outputDir', action='store',
    dest='outputDir', required = False, default = 'plots',
    help = "The output directory name.")

parser.add_argument('--debug', action='store_true', default=False,
    dest='debug', help = "debug mode.", required = False)

parser.add_argument('-l','--legends', action='store',
    dest='legends', required = False, nargs='+', default=None,
    help = "The legends to be add in the TLegend display")

parser.add_argument('-r','--runLabel', action='store',
    dest='runLabel', required = False, default = None,
    help = "The run label")

parser.add_argument('--pdf_title', action='store',
    dest='pdf_title', required = False, default = "Efficiency plots",
    help = "The slide title")

parser.add_argument('--pdf_output', action='store',
    dest='pdf_output', required = False, default = "efficiencies",
    help = "The output PDF file")

parser.add_argument('--removeInnefBefore', action='store_true', default=False,
    dest='removeInnefBefore', help = "Remove innef before.", required = False)

parser.add_argument('--triggers', action='store',
    dest='triggers', required = True, default='[()]',
    help = "Use like: ['HLT_et_etcut','HLT_e24_lhtight','HLT_e28_lhtight_nod0_ivarloose','HLT_e5_lhtight' ]")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

######################################################################################################

# definitions
level_names   = ['L1Calo','L2Calo','L2','EFCalo','HLT']
plot_names    = ['et','eta','mu']
xlabel_names  = ['Offline isolated electron E_{T} [GeV]','#eta','<#mu>']
triggerList = eval(args.triggers)

### Get all files if needed!
files=[]; is_emulated_trigger = []; legends = []
for idx, basepath in enumerate(args.dirs):
  mainLogger.info( basepath )
  f = expandFolders( basepath )
  if len(f)>10 and args.debug: f=f[0:10]
  files.append(f)
  is_emulated_trigger.append(False)
  legends.append(args.legends[idx] if args.legends else str())




if args.emulation_list:
  for idx in args.emulation_list:
    is_emulated_trigger[idx]=True


localpath=os.getcwd()
dirpath=args.outputDir
import os
try:
  os.mkdir(dirpath)
except:
  mainLogger.warning("The output directory %s exist into the local path", args.outputDir)

mainLogger.info("Start...")
### Retrieve all histograms from each path
from EfficiencyTools.utilities import GetHistogramRootPaths, GetHistogramFromMany, is_high_et, GetProfile
mainLogger.info('Get histograms from files....')
objects = []; summary = []
for idx, files_ref in enumerate(files):
  paths_ref, keys =  GetHistogramRootPaths( triggerList, removeInnefBefore=args.removeInnefBefore, is_emulation=is_emulated_trigger[idx], logger=mainLogger )
  objects.append( GetHistogramFromMany(files_ref, paths_ref, keys, prefix='Getting reference...', logger=mainLogger) )
  s={}
  for trigger in triggerList:
    s[trigger]={'L1Calo':0.0, 'L2Calo':0.0, 'L2':0.0, 'EFCalo':0.0, 'HLT':0.0}
  summary.append( s )

### Plotting
entries=len(triggerList)
step = int(entries/100) if int(entries/100) > 0 else 1

from EfficiencyTools.drawers import PlotProfiles
for trigItem in progressbar(triggerList, entries, step=step,logger=mainLogger, prefix='Plotting...'):

  isL1 = True if trigItem.startswith('L1_') else False
  these_level_names = ['L1Calo'] if isL1 else level_names
  ### Plot all profiles here!
  for idx, histname in enumerate(plot_names):
    # resize <mu> range
    resize = [12,20,80] if 'mu' in histname else None
    #doFitting = True if 'mu' in histname and args.doNonLinearityTest else False
    for level in these_level_names:
      #try:
      outname = localpath+'/'+dirpath+'/'+level+'_'+trigItem.replace('HLT_','')+'_'+histname+'.pdf'
      legends = []; curves  = []
      # loop over each turn-on inside of the plot
      for jdx, objects_ref in enumerate(objects):
        summary[jdx][trigItem][level]=(objects_ref[trigItem+'_'+level+'_match_'+histname].GetEntries()/
                                      float(objects_ref[trigItem+'_'+level+'_'+histname].GetEntries()))*100
        curves.append( GetProfile(objects_ref[trigItem+'_'+level+'_match_'+histname],objects_ref[trigItem+'_'+level+'_'+histname],resize=resize) )
        #legends.append( trigItem.replace('HLT_','')) #+args.legends[jdx])
        legends.append( args.legends[jdx] ) #+args.legends[jdx])

      # make plots!
      res = PlotProfiles( curves,
                          legends = legends,
                          runLabel=args.runLabel,
                          outname=outname,
                          extraText1='%s%s'%(level, trigItem.replace('HLT','')),
                          doFitting=False,
                          xlabel=xlabel_names[idx],
                          doRatioCanvas=False,
                          legendX1=0.58,
                          SaveAsC=True)

    #Loop over histograms
  #Loop over levels
# Loop over triggers

from pprint import pprint
pprint(summary)




from copy import copy
from pprint import pprint
from Gaugi.tex.TexAPI import *
from Gaugi.tex.BeamerAPI import *

# apply beamer
with BeamerTexReportTemplate2( theme = 'Berlin'
                             , _toPDF = True
                             , title = args.pdf_title
                             , outputFile = args.pdf_output
                             , font = 'structurebold' ):
  for trigItem in triggerList:
    section = (trigItem).replace('_','\_')
    paths=[]
    isL1 = True if trigItem.startswith('L1_') else False
    these_level_names = ['L1Calo'] if isL1 else level_names

    for histname in plot_names:
      if not isL1 and 'et' is histname and is_high_et(trigItem):  histname='highet'
      for level in these_level_names:
        abspath = localpath+'/'+dirpath+'/'+level+'_'+trigItem.replace('HLT_','')+'_'+histname+'.pdf'
        paths.append( abspath )

    with BeamerSection( name = section ):
      BeamerMultiFigureSlide( title = 'L1Calo Efficiency Plots' if isL1 else 'Efficiency plots'
                    , paths = paths
                    , nDivWidth = 3 if isL1 else 5  # x
                    , nDivHeight = 1 if isL1 else 3 # y
                    , texts=None
                    , fortran = False
                    , usedHeight = 0.4 if isL1 else 0.7
                    , usedWidth = 1.0 if isL1 else 0.95
                    )

      ### Prepare tables
      lines1 = []
      lines1 += [ HLine(_contextManaged = False) ]
      lines1 += [ HLine(_contextManaged = False) ]
      lines2 = copy(lines1)
      lines1 += [ TableLine( columns = ['Trigger Efficiency'] + [level+'[\%]' for level in these_level_names], _contextManaged = False ) ]
      lines1 += [ HLine(_contextManaged = False) ]

      for idx, s in enumerate(summary):
        leg = args.legends[idx]
        lines1 += [ TableLine( columns = [leg] + [('%1.2f')%(s[trigItem][level]) for level in these_level_names] , _contextManaged = False ) ]
      #lines1 += [ TableLine( columns = ['Test'] + [('%1.2f')%(values[trigItem][level]['test_eff']) for level in these_level_names] , _contextManaged = False ) ]
      lines1 += [ HLine(_contextManaged = False) ]
      lines1 += [ HLine(_contextManaged = False) ]

      with BeamerSlide( title = "Trigger Monitoring"  ):

        with Table( caption = 'Trigger Efficiency for each step.') as table:
          with ResizeBox( size = 0.4 if isL1 else 1.) as rb:
            with Tabular( columns = 'l' + 'c' * len(these_level_names)) as tabular:
              tabular = tabular
              for line in lines1:
                if isinstance(line, TableLine):
                  tabular += line
                else:
                  TableLine(line, rounding = None)


        #if args.doNonLinearityTest:
        #  lines2 += [ TableLine( columns = ['Nonlinearity Test'] + [level+'[\%]' for level in these_level_names], _contextManaged = False ) ]
        #  lines2 += [ HLine(_contextManaged = False) ]
        #  lines2 += [ TableLine( columns = ['Reference (gray)'] + [('%1.2f')%(values[trigItem][level]['fref_ref_NL_mu']) \
        #      for level in these_level_names] , _contextManaged = False ) ]
        #  #lines2 += [ TableLine( columns = ['Test (gray)'] + [('%1.2f')%(values[trigItem][level]['fref_test_NL_mu']) \
        #  #    for level in these_level_names] , _contextManaged = False ) ]

        #  #lines2 += [ HLine(_contextManaged = False) ]
        #  #lines2 += [ TableLine( columns = ['Reference (blue)'] + [('%1.2f')%(values[trigItem][level]['ftest_ref_NL_mu']) \
        #  #    for level in these_level_names] , _contextManaged = False ) ]
        #  lines2 += [ TableLine( columns = ['Test (blue)'] + [('%1.2f')%(values[trigItem][level]['ftest_test_NL_mu']) \
        #      for level in these_level_names] , _contextManaged = False ) ]


        #  lines2 += [ HLine(_contextManaged = False) ]
        #  lines2 += [ HLine(_contextManaged = False) ]

        #  with Table( caption = "Nonlinearity test for the $\mu$ depedence.") as table:
        #    with ResizeBox( size = 0.4 if isL1 else 1.) as rb:
        #      with Tabular( columns = 'l' + 'c' * len(these_level_names)) as tabular:
        #        for line in lines2:
        #          if isinstance(line, TableLine):
        #            tabular += line
        #          else:
        #            TableLine(line, rounding = None)



