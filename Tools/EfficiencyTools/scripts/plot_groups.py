#!/usr/bin/env python

from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite,TColor
from Gaugi.messenger import LoggingLevel, Logger
from Gaugi.utilities import expandFolders, progressbar
from EfficiencyTools.utilities import GetHistogramFromMany, is_high_et
from EfficiencyTools.drawers import PlotProfiles
from EfficiencyTools.utilities import *
import argparse
import os

# Mute ROOT logger
from ROOT import gROOT
gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;");


# kGray_2
local_these_colors = [kBlack,kBlue-4,kRed-2,kAzure+2,kGreen+1,kMagenta+1,kCyan+1,kOrange+1
                ,kBlack+2,kRed+3,kBlue+3,kGreen+3,kMagenta+3,kCyan+3,kOrange+3
                ,kGray,kRed-7,kBlue-7,kGreen-7,kMagenta-7,kCyan-7,kOrange-7
                ,kYellow+2,kRed-5,kBlue-5,kGreen-5,kMagenta-5,kCyan-5,kOrange-5
                ,21,22,23,24,25,26,27,28,29,30
                ,21,22,23,24,25,26,27,28,29,30
                ,21,22,23,24,25,26,27,28,29,30
                ]

local_these_transcolors=[TColor.GetColorTransparent(c,.5) for c in local_these_colors]
local_these_marker = (23, 24, 22, 26, 32 ,23, 20,25)
local_these_marker_full = (20,21,22,23,33,34)
local_these_marker_open = (24,25,26,32,27,28)



mainLogger = Logger.getModuleLogger("PlotTools", LoggingLevel.INFO)

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-l','--legends', action='store', 
    dest='legends', required = False, nargs='+', default=None,
    help = "The legends to be add in the TLegend display")

parser.add_argument('--extraText1', action='store', 
    dest='extraText1', required = False, default='[]',
    help = "This used in (extraText1)")


parser.add_argument('-o','--outputDir', action='store', 
    dest='outputDir', required = False, default = 'plots',
    help = "The output directory name.")

parser.add_argument('-r','--reference', action='store', nargs='+', 
    dest='reference', required = False, default = None,
    help = "The reference file location")

parser.add_argument('-t','--test', action='store',  nargs='+',
    dest='test', required = True,
    help = "The test file location")

parser.add_argument('--pdf_title', action='store', 
    dest='pdf_title', required = False, default = "Efficiency plots",
    help = "The slide title")

parser.add_argument('--pdf_output', action='store', 
    dest='pdf_output', required = False, default = "efficiencies",
    help = "The output PDF file")

parser.add_argument('--doNonLinearityTest', action='store_true', default=False,
    help = "Draw the fitting curve and apply the non linearity test.", required = False) 

parser.add_argument('--doRatio', action='store_true', default=False,
    help = "Apply Ratio Canvas", required = False) 

parser.add_argument('--runLabel', action='store', 
    dest='runLabel', required = False, default = "Data 2017",
    help = "Set the run label text.")

parser.add_argument('--debug', action='store_true', default=False,
    help = "Debug mode", required = False) 

parser.add_argument('--ref_is_emulation', action='store_true', default=False,
    help = "Use emulation plots in reference curves", required = False) 

parser.add_argument('--test_is_emulation', action='store_true', default=False,
    help = "Use emulation plots in test curves", required = False) 

parser.add_argument('--groups', action='store', 
    dest='groups', required = True, default='[()]',
    help = "Use like: [('HLT_et_etcut','HLT_e24_lhtight'),('HLT_e28_lhtight_nod0_ivarloose'), ('HLT_e5_lhtight') ]")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
# definitions
level_names   = ['L1Calo','L2Calo','L2','EFCalo','HLT']
plot_names    = ['et','eta','mu']
xlabel_names  = ['Offline isolated electron E_{T} [GeV]','#eta','<#mu>']


######################################################################################################

mainLogger.info("Reference file: %s", args.reference)
mainLogger.info("Test file: %s", args.test)
triggerList_group = eval(args.groups)

######################################################################################################
localpath=os.getcwd()
dirpath=args.outputDir
try:
  os.mkdir(dirpath)
except:
  mainLogger.warning("The output directory %s exist into the local path", args.outputDir)

if not args.legends:
  args.legends=['(Ref)','(Test)']


### Get all files if needed!
files_ref=[]; files_test=[]

if args.reference:
  for paths in args.reference:
    files_ref.extend( expandFolders( paths )  )

for paths in args.test:
  files_test.extend( expandFolders( paths ) )

if args.debug:
  if len(files_ref)>10: files_ref=files_ref[0:10]
  if len(files_test)>10: files_test=files_test[0:10]


from pprint import pprint

### Get all trigger for each group
triggerList= []
for group in triggerList_group:
  if type(group) is tuple:
    for t in group:  triggerList.append(t)
  else:
    triggerList.append(group)

### Making all paths
entries=len(triggerList)
step = int(entries/100) if int(entries/100) > 0 else 1
paths_test=[]; paths_ref=[]; keys=[]

for trigItem in progressbar(triggerList, entries, step=step, prefix='Making paths...', logger=mainLogger):
  #mainLogger.info(trigItem)
  isL1 = True if trigItem.startswith('L1_') else False
  these_level_names = ['L1Calo'] if isL1 else level_names  
  ### Retrieve all paths
  for level in these_level_names:
    for histname in plot_names:

      if not isL1 and 'et' == histname and is_high_et(trigItem):  histname='highet'
      histpath = 'HLT/Egamma/Expert/{TRIGGER}/{CORE}/{LEVEL}/{HIST}'
      
      # Ref
      if args.reference:
        paths_ref.append(histpath.format(TRIGGER=trigItem,HIST='match_'+histname,LEVEL=level, CORE='Emulation' if args.ref_is_emulation else 'Efficiency')) 
        paths_ref.append(histpath.format(TRIGGER=trigItem,HIST=histname,LEVEL='L1Calo', CORE='Emulation' if args.ref_is_emulation else 'Efficiency'))
      
      # Test
      paths_test.append(histpath.format(TRIGGER=trigItem,HIST='match_'+histname,LEVEL=level, CORE='Emulation' if args.test_is_emulation else 'Efficiency')) 
      paths_test.append(histpath.format(TRIGGER=trigItem,HIST=histname,LEVEL='L1Calo', CORE='Emulation' if args.test_is_emulation else 'Efficiency'))
      
      if 'highet' == histname:  histname='et' 
      keys.append(trigItem+'_'+level+'_match_'+histname)
      keys.append(trigItem+'_'+level+'_'+histname)
# Loop over triggers


### Retrieve all histograms
mainLogger.info('Get histograms from files....')
if args.reference:
  objects_ref = GetHistogramFromMany(files_ref, paths_ref, keys, prefix='Getting reference...', logger=mainLogger)
objects_test = GetHistogramFromMany(files_test, paths_test, keys, prefix='Getting test...', logger=mainLogger)

 


idx=0
values = []
entries=len(triggerList_group)
step = int(entries/100) if int(entries/100) > 0 else 1

### Plotting
for group in progressbar(triggerList_group, entries, step=step, prefix="Plotting...", logger=mainLogger):

  # FIXME: Fix this in the case of a single string trigger
  if type(group) is str:
    group = [group]

  isL1=False
  ### Check if there is a L1 seed in this group
  for trigItem in group:
    if trigItem.startswith('L1_'):
      isL1=True
  these_level_names = ['L1Calo'] if isL1 else level_names
  values.append({})

  for jdx, histname in enumerate(plot_names):
    resize = [12,20,80] if 'mu' in histname else None
    #resize=None
    for level in these_level_names:
      legends=[]; h_ref=[]; h_test=[];
      pname=str()
      for trigItem in group:  
        pname+='_'+trigItem
        legends.append(trigItem)
        if not trigItem in values[idx].keys():
          values[idx][trigItem] = {'L1Calo':{},'L2Calo':{},'L2':{},'EFCalo':{},'HLT':{}}
        ### Plot all profiles here!
        if args.reference:
          if 'eta' in histname:
            values[idx][trigItem][level]['ref_eff']=(objects_ref[trigItem+'_'+level+'_match_'+histname].GetEntries()/
                                               float(objects_ref[trigItem+'_'+level+'_'+histname].GetEntries()))*100
          h_ref.append(GetProfile(objects_ref[trigItem+'_'+level+'_match_'+histname],
                                  objects_ref[trigItem+'_'+level+'_'+histname],resize=resize))
 
        if 'eta' in histname:
          values[idx][trigItem][level]['test_eff']=(objects_test[trigItem+'_'+level+'_match_'+histname].GetEntries()/
                                             float(objects_test[trigItem+'_'+level+'_'+histname].GetEntries()))*100
        h_test.append(GetProfile(objects_test[trigItem+'_'+level+'_match_'+histname],
                                objects_test[trigItem+'_'+level+'_'+histname],resize=resize))
      # Loop over triggers
      if args.reference:
        these_colors =[local_these_transcolors[c] for c in range(len(h_ref))]
        these_colors+=[local_these_colors[c] for c in range(len(h_ref))]
        these_transcolors =2*[local_these_transcolors[c] for c in range(len(h_ref))]
        these_marker = [local_these_marker_full[c] for c in range(len(h_ref))]
        these_marker+= [local_these_marker_open[c] for c in range(len(h_ref))]
      else:
        these_colors=local_these_colors; these_transcolors=local_these_transcolors; these_marker=local_these_marker

      ### NOTE: hack legend for werner's article. 
      #if len(legends)==2:
      #  legends = ['Ringer chain','Baseline chain']
      #extraText1='Full: without ringer, Open: with ringer'
      extraText1=eval(args.extraText1)
      #extraText1=group[0]
      if args.legends:
        legends = args.legends
      outname = localpath+'/'+dirpath+'/'+level+pname+'_'+histname+'.pdf'
      res = PlotProfiles( h_ref+h_test, legends = legends, outname=outname, runLabel=args.runLabel, extraText1=extraText1, 
                          doFitting=False, doRatioCanvas=args.doRatio,xlabel=xlabel_names[jdx],theseColors=these_colors,theseMarker=these_marker,
                          theseTransColors=these_transcolors, legendX1=0.50,
                          SaveAsC=True)  

    #Loop over histograms
  #Loop over levels
  idx+=1
#Loop over groups



from copy import copy
from pprint import pprint
#pprint( values )
#Loop over triggers

from pytex.TexAPI import *
from pytex.BeamerAPI import *

# apply beamer
with BeamerTexReportTemplate2( theme = 'Berlin'
                             , _toPDF = True
                             , title = args.pdf_title
                             , outputFile = args.pdf_output
                             , font = 'structurebold' ):
  
  
  for idx, group in enumerate(triggerList_group):
    #section = (trigItem).replace('_','\_')
    section = ''
    paths=[]
    isL1=False
    ### Check if there is a L1 seed in this group
    pname=str()
    for trigItem in group:
      pname+='_'+trigItem
      if trigItem.startswith('L1_'):
        isL1=True

    these_level_names = ['L1Calo'] if isL1 else level_names
 
    for histname in plot_names:
      for level in these_level_names:
        abspath = localpath+'/'+dirpath+'/'+level+pname+'_'+histname+'.pdf'
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

      #### Prepare tables
      lines1 = []
      lines1 += [ HLine(_contextManaged = False) ]
      lines1 += [ HLine(_contextManaged = False) ]
      lines1 += [ TableLine( columns = ['Trigger Efficiency'] + [level+'[\%]' for level in these_level_names], _contextManaged = False ) ]
      lines1 += [ HLine(_contextManaged = False) ]
      
      for trigItem in group:
        lines1 += [ TableLine( columns = [trigItem.replace('_','\_')] + [('%1.2f')%(values[idx][trigItem][level]['test_eff']) for level in these_level_names] , 
            _contextManaged = False ) ]   
        if args.reference:
          lines1 += [ TableLine( columns = [trigItem.replace('_','\_')+' (Ref.)'] + [('%1.2f')%(values[idx][trigItem][level]['ref_eff']) for level in these_level_names] , 
                      _contextManaged = False ) ]   
          lines1 += [ HLine(_contextManaged = False) ]
          
      if not args.reference:
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
       
