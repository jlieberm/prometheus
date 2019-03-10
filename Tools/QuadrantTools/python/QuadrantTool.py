__all__ = ['QuadrantTool']



from Gaugi import StatusCode
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.utilities import retrieve_kw, mkdir_p
from Gaugi.types import NotSet
from CommonTools import AlgorithmTool
from CommonTools.constants import *
from CommonTools.utilities import RetrieveBinningIdx
import ROOT
import numpy as np

class QuadrantTool( AlgorithmTool ):

  # quadrant names definition
  _quadrants = ['passed_passed',
                'rejected_rejected',
                'passed_rejected',
                'rejected_passed']

  def __init__(self, name, **kw):
    
    AlgorithmTool.__init__(self, name)
    self._basepath = 'Event/QuadrantTool'
    self._quadrantFeatures = list()
    self._etBins  = NotSet
    self._etaBins = NotSet
    

  def add_quadrant( self, name_a, expression_a, name_b, expression_b):
    from utilities import QuadrantConfig
    self._quadrantFeatures.append( QuadrantConfig(name_a,expression_a,name_b,expression_b) )


  def setEtBinningValues( self, etbins ):
    self._etBins = etbins
  
  def setEtaBinningValues( self, etabins ):
    self._etaBins = etabins


  def initialize(self):
    
    AlgorithmTool.initialize(self)
    sg = self.getStoreGateSvc()

    #if super(TrigBaseTool,self).initialize().isFailure():
    #  self._logger.fatal("Impossible to initialize the Trigger services.")
    from ROOT import TH1F
    etabins = default_etabins

    for feat in self._quadrantFeatures:
      # hold quadrant name
      quadrant_name = feat.name_a()+'_Vs_'+feat.name_b()

      ### loopover ets...
      for etBinIdx in range(len(self._etBins)-1):
        ### loop over etas...
        for etaBinIdx in range(len(self._etaBins)-1):
          ### loop over quadrants...
          for quadrant in self._quadrants:  
            # hold binning name
            binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)


            dirname = self._basepath+'/'+quadrant_name+'/'+binning_name+'/'+quadrant
            sg.mkdir( dirname )
            sg.addHistogram(TH1F('et',('%s;%s;Count')%(basicInfoQuantities['et'],basicInfoQuantities['et']),
             basicInfoNBins['et'],basicInfoLowerEdges['et'],basicInfoHighEdges['et']) )
            sg.addHistogram(TH1F('eta',('%s;%s;Count')%(basicInfoQuantities['eta'],basicInfoQuantities['eta']),
                            len(etabins)-1, np.array(etabins)) )
            sg.addHistogram(TH1F('phi',('%s;%s;Count')%(basicInfoQuantities['phi'],basicInfoQuantities['phi']),
                            20, -3.2, 3.2) )
            sg.addHistogram(TH1F('avgmu',('%s;%s;Count')%(basicInfoQuantities['avgmu'],basicInfoQuantities['avgmu']),
                            16,0,80) )
            sg.addHistogram(TH1F('nvtx',('%s;%s;Count')%(basicInfoQuantities['nvtx'],basicInfoQuantities['nvtx']),
                            len(nvtx_bins)-1,np.array(nvtx_bins)) )

            for key in standardQuantitiesNBins.keys():
              sg.addHistogram(TH1F(key, 
                ('%s;%s;Count')%(electronQuantities[key],electronQuantities[key]),
                standardQuantitiesNBins[key],
                standardQuantitiesLowerEdges[key],
                standardQuantitiesHighEdges[key]))

            # loop over quadrants

    # loop over pairs
    self.init_lock()
    return StatusCode.SUCCESS



  def execute(self, context):
    
    import math
    from Gaugi.constants import GeV
    # Retrieve Electron container
    el = context.getHandler( "ElectronContainer" )
    evt = context.getHandler( "EventInfoContainer" )
    eta = math.fabs(el.eta())
    et = el.et()/GeV
    track = el.trackParticle()
    
    evt = context.getHandler("EventInfoContainer")
    pw = evt.MCPileupWeight()
    sg = self.getStoreGateSvc()

    if et < self._etBins[0]:
      return StatusCode.SUCCESS
    if eta > 2.47:
      return StatusCode.SUCCESS

    etBinIdx, etaBinIdx = RetrieveBinningIdx(et,eta,self._etBins, self._etaBins, logger=self._logger )
    binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)

    for feat in self._quadrantFeatures:
      
      name     = feat.name_a()+'_Vs_'+feat.name_b()
      passed_x = self.accept( feat.expression_a() )
      passed_y = self.accept( feat.expression_b() )
      passed_x = 'passed' if passed_x else 'rejected'
      passed_y = 'passed' if passed_y else 'rejected'
      dirname  = self._basepath+'/'+name+'/'+binning_name+'/'+passed_x +'_'+ passed_y

      pw=1
      # Fill basic infos
      sg.histogram(dirname+'/et').Fill(et,pw)
      sg.histogram(dirname+'/eta').Fill(el.eta(),pw)
      sg.histogram(dirname+'/phi').Fill(el.phi(),pw)
      sg.histogram(dirname+'/avgmu').Fill(evt.avgmu(),pw)
      sg.histogram(dirname+'/nvtx').Fill(evt.nvtx(),pw)
      # Fill shower shapes
      sg.histogram(dirname+'/f1').Fill(el.f1(),pw)
      sg.histogram(dirname+'/f3').Fill(el.f3(),pw)
      sg.histogram(dirname+'/weta2').Fill(el.weta2(),pw)
      sg.histogram(dirname+'/wtots1').Fill(el.wtots1(),pw)
      sg.histogram(dirname+'/reta').Fill(el.reta(),pw)
      sg.histogram(dirname+'/rhad').Fill(el.rhad(),pw)
      sg.histogram(dirname+'/rphi').Fill(el.rphi(),pw)
      sg.histogram(dirname+'/eratio').Fill(el.eratio(),pw)
      sg.histogram(dirname+'/deltaEta1').Fill(el.deltaEta1(),pw)
      sg.histogram(dirname+'/deltaPhiRescaled2').Fill(el.deltaPhiRescaled2(),pw)
      # Fill track variables
      if track:
        sg.histogram(dirname+'/trackd0pvunbiased').Fill(track.d0(),pw)
        sg.histogram(dirname+'/d0significance').Fill(track.d0significance(),pw)
        sg.histogram(dirname+'/eProbabilityHT').Fill(track.eProbabilityHT(),pw)
        sg.histogram(dirname+'/TRT_PID').Fill(track.trans_TRT_PID(),pw)
        sg.histogram(dirname+'/DeltaPOverP').Fill(track.DeltaPOverP(),pw)
     

    return StatusCode.SUCCESS


  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS



  def plot(self, dirnames, pdfoutputs, pdftitles, runLabel='' ,doPDF=True):
    
    from itertools import product
    from Gaugi.utilities import progressbar

    import time
    import os, gc

    beamer_plots = {}
    global tobject_collector

    for idx, feat in enumerate(self._quadrantFeatures):
      
      dirname = os.getcwd()+'/'+dirnames[idx]
      mkdir_p(dirname)
      # hold quadrant name
      quadrant_name = feat.name_a()+'_Vs_'+feat.name_b()
      # For beamer... 
      if not quadrant_name in beamer_plots.keys():
        beamer_plots[quadrant_name]={}
        beamer_plots[quadrant_name]['integrated']={}

      ### Plot binning plots  
      if (len(self._etBins) * len(self._etaBins)) > 1:
        for etBinIdx, etaBinIdx in progressbar(product(range(len(self._etBins)-1),range(len(self._etaBins)-1)), 
                                               prefix = "Plotting... "):
          # hold binning name
          binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          # for beamer...
          if not binning_name in beamer_plots[quadrant_name].keys():
            beamer_plots[quadrant_name][binning_name]={}
          
          ### loop over standard quantities
          for key in standardQuantitiesNBins.keys(): 
            outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
            out = self._plotQuantities(self._basepath+'/'+quadrant_name+'/'+binning_name, key, 
                outname,etidx=etBinIdx,etaidx=etaBinIdx,xlabel=electronQuantities[key],divide='b',runLabel=runLabel)
            beamer_plots[quadrant_name][binning_name][key] = out
            #del tobject_collector[:]
        
          ### loop over info quantities
          for key in basicInfoQuantities.keys():
            outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
            out = self._plotQuantities(self._basepath+'/'+quadrant_name+'/'+binning_name, key, 
                outname, etidx=etBinIdx,etaidx=etaBinIdx,xlabel=basicInfoQuantities[key],divide='b', runLabel=runLabel)
            beamer_plots[quadrant_name][binning_name][key] = out
            #del tobject_collector[:]

          
          beamer_plots[quadrant_name][binning_name]['statistics'] = self._getStatistics(self._basepath+'/'+quadrant_name+'/'+binning_name, \
                                                                                        'avgmu',etidx=etBinIdx,etaidx=etaBinIdx)
      

      #### Plot integrated histograms
      ### loop over standard quantities
      for key in standardQuantitiesNBins.keys(): 
        outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key
        out = self._plotQuantities(self._basepath+'/'+quadrant_name, key, 
              outname,xlabel=electronQuantities[key],divide='b',runLabel=runLabel,
              addbinlines=True)
        beamer_plots[quadrant_name]['integrated'][key] = out
        tobject_collector = []
        gc.collect()
      ### loop over info quantities
      for key in basicInfoQuantities.keys():
        outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
        out = self._plotQuantities(self._basepath+'/'+quadrant_name, key, 
            outname,xlabel=basicInfoQuantities[key],divide='b', runLabel=runLabel,
            addbinlines=True)
        beamer_plots[quadrant_name]['integrated'][key] = out
        tobject_collector = []
        gc.collect()
      
      beamer_plots[quadrant_name]['integrated']['statistics'] = self._getStatistics(self._basepath+'/'+quadrant_name, 'avgmu')




    if doPDF:
      ### Make Latex str et/eta labels
      etbins_str = []; etabins_str=[]
      for etBinIdx in range( len(self._etBins)-1 ):
        etbin = (self._etBins[etBinIdx], self._etBins[etBinIdx+1])
        if etbin[1] > 100 :
          etbins_str.append( r'$E_{T}\text{[GeV]} > %d$' % etbin[0])
        else:
          etbins_str.append(  r'$%d < E_{T} \text{[Gev]}<%d$'%etbin )
 
      for etaBinIdx in range( len(self._etaBins)-1 ):
        etabin = (self._etaBins[etaBinIdx], self._etaBins[etaBinIdx+1])
        etabins_str.append( r'$%.2f<\eta<%.2f$'%etabin )



      from tex.TexAPI    import *
      from tex.BeamerAPI import *
      
      for slideIdx, feat in enumerate(self._quadrantFeatures):
        
        with BeamerTexReportTemplate1( theme = 'Berlin'
                                   , _toPDF = True
                                   , title = pdftitles[slideIdx]
                                   , outputFile = pdfoutputs[slideIdx]
                                   , font = 'structurebold' ):


          # hold quadrant name
          quadrant_name = feat.name_a()+'_Vs_'+feat.name_b() 
          section_name = feat.name_a()+' Vs '+feat.name_b()
          #with BeamerSection( name = 'x' ):
            
          with BeamerSection( name = 'Integrated Quantities' ):
            # prepare files for basic quantities
            figures = []
            for key in ['et','eta','phi','avgmu','nvtx']:
              figures.append( beamer_plots[quadrant_name]['integrated'][key])

            BeamerMultiFigureSlide( title = 'Basic Quantities'
                    , paths = figures
                    , nDivWidth = 3 # x
                    , nDivHeight = 2 # y
                    , texts=None
                    , fortran = False
                    , usedHeight = 0.6
                    , usedWidth = 0.9
                    )
            # prepare files for calo standard quantities
            figures = []
            for key in ['eratio','rhad','reta','rphi','f1','f3','wtots1','weta2']:
              figures.append( beamer_plots[quadrant_name]['integrated'][key])

            BeamerMultiFigureSlide( title = 'Standard Calo Quantities'
                    , paths = figures
                    , nDivWidth = 4 # x
                    , nDivHeight = 2 # y
                    , texts=None
                    , fortran = False
                    , usedHeight = 0.6
                    , usedWidth = 0.9
                    )
 
            # prepare files for calo standard quantities
            figures = []
            for key in ['d0significance','trackd0pvunbiased','deltaPhiRescaled2',
                'eProbabilityHT','TRT_PID','deltaEta1','DeltaPOverP']:
              figures.append( beamer_plots[quadrant_name]['integrated'][key])

            BeamerMultiFigureSlide( title = 'Standard Track Quantities'
                    , paths = figures
                    , nDivWidth = 4 # x
                    , nDivHeight = 2 # y
                    , texts=None
                    , fortran = False
                    , usedHeight = 0.6
                    , usedWidth = 0.9
                    )
  

          section = ['Basic Quantity']*2
          section.extend( ['Standard Calo Quantity']*8 )
          section.extend( ['Standard Track Quantity']*7 )
          section.extend( ['Likelihood Discriminant','Ringer Neural Discriminant'] )
          for idx, key in enumerate(['avgmu','nvtx','eratio','rhad','reta','rphi',
                      'f1','f3','wtots1','weta2','d0significance',
                      'trackd0pvunbiased','deltaPhiRescaled2',
                      'eProbabilityHT','TRT_PID','deltaEta1','DeltaPOverP',
                      #'lhOutput','nnOutput'
                      ]):
            with BeamerSection( name = key.replace('_','\_') ):

              from itertools import product
              figures = []; binning_name_list=[];
              for etBinIdx, etaBinIdx in product(range(len(self._etBins)-1),range(len(self._etaBins)-1)):
                binning_name_list.append( ('et%d_eta%d') % (etBinIdx,etaBinIdx) )
                
              while len(binning_name_list)>0:
                figures = []
                if len(binning_name_list)>9:
                  for _ in range(9):
                    binning_name = binning_name_list.pop(0)
                    figures.append( beamer_plots[quadrant_name][binning_name][key])
                else:
                  for _ in range(len(binning_name_list)):
                    binning_name = binning_name_list.pop(0)
                    figures.append( beamer_plots[quadrant_name][binning_name][key])
                BeamerMultiFigureSlide( title = section[idx]+' ('+key.replace('_','\_')+')' 
                      , paths = figures
                      , nDivWidth = 4 # x
                      , nDivHeight = 3 # y
                      , texts=None
                      , fortran = False
                      , usedHeight = 0.7
                      , usedWidth = 0.8
                      )

          with BeamerSection( name = 'Statistics' ):
               
            ### Prepare tables
            lines1 = []
            lines1 += [ HLine(_contextManaged = False) ]
            lines1 += [ HLine(_contextManaged = False) ]
            
            #lines1 += [ TableLine( columns = ['kinematic region'] + reduce(lambda x,y: x+y,[ [r'\multicol{4}{*}{'+s+'}','','',''] for s in etbins_str]), \
            lines1 += [ TableLine( columns = ['kinematic region'] + reduce(lambda x,y: x+y,[ [s,'','',''] for s in etbins_str]), \
                                                                            _contextManaged = False ) ]
            
            lines1 += [ HLine(_contextManaged = False) ]
            lines1 += [ TableLine( columns = ['Det. Region'] + reduce(lambda x,y: x+y,[[r'$Q_{ij}$',r'$\rho{ij}$',r'$\kappa_{P}$',r'$dis_{ij}$'] \
            #lines1 += [ TableLine( columns = ['Det. Region'] + reduce(lambda x,y: x+y,[['a','b','c','d'] \
                        for _ in etbins_str]), _contextManaged = False ) ]
            lines1 += [ HLine(_contextManaged = False) ]

            for etaBinIdx in range( len(self._etaBins)-1 ):
              str_values = []
              for etBinIdx in range( len(self._etBins)-1 ):
                binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
                stats = beamer_plots[quadrant_name][binning_name]['statistics']
                str_values += [ '%1.2f'%stats['Qij'],
                                '%1.2f'%stats['Pij'],
                                '%1.2f'%stats['Kp'],
                                '%1.2f'%stats['dis_ij']]
              lines1 += [ TableLine( columns = [ etabins_str[etaBinIdx] ] + str_values   , _contextManaged = False ) ]
              lines1 += [ HLine(_contextManaged = False) ]
            
            lines1 += [ HLine(_contextManaged = False) ]     

            with BeamerSlide( title = "The General Statistics"  ):          
              with Table( caption = 'The statistics pair wise values.') as table:
                with ResizeBox( size = 0.9 ) as rb:
                  with Tabular( columns = '|l|' + 'cccc|' * len(etbins_str) ) as tabular:
                    tabular = tabular
                    for line in lines1:
                      if isinstance(line, TableLine):
                        tabular += line
                      else:
                        TableLine(line, rounding = None)




  def _plotQuantities( self,basepath, key, outname, drawopt='hist', divide='B', 
      etidx=None, etaidx=None, xlabel='', runLabel='', addbinlines=False):



    from monet.utilities import sumHists
    from monet.PlotFunctions import *
    from monet.TAxisFunctions import *
    from utilities import AddTopLabels


    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gErrorIgnoreLevel=ROOT.kWarning
    ROOT.TH1.AddDirectory(ROOT.kFALSE)

    #if (not "_et2" in outname) or (not "_eta0" in outname): return outname + '.pdf'
    sg = self.getStoreGateSvc()
    # get all quadrant histograms

    if (etidx is not None) and (etaidx is not None):
      hists = [
                sg.histogram(basepath+'/passed_passed/'+key),
                sg.histogram(basepath+'/passed_rejected/'+key),
                sg.histogram(basepath+'/rejected_passed/'+key),
                sg.histogram(basepath+'/rejected_rejected/'+key)
              ]
    else:
      from itertools import product
      passed_passed = []; passed_rejected = []; rejected_passed = []; rejected_rejected = []
      for etBinIdx, etaBinIdx in product(range(len(self._etBins)-1),range(len(self._etaBins)-1)):
        binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx) 
        passed_passed.append( sg.histogram(basepath+'/'+binning_name+'/passed_passed/'+key) ) 
        passed_rejected.append( sg.histogram(basepath+'/'+binning_name+'/passed_rejected/'+key) )
        rejected_passed.append( sg.histogram(basepath+'/'+binning_name+'/rejected_passed/'+key) )
        rejected_rejected.append( sg.histogram(basepath+'/'+binning_name+'/rejected_rejected/'+key) )

      hists = [
                sumHists(passed_passed),
                sumHists(passed_rejected),
                sumHists(rejected_passed),
                sumHists(rejected_rejected),
              ]

    ref_hist = sumHists(hists)
    from ROOT import kBlack,kRed,kGreen,kGray,kMagenta,kBlue
    outcan = RatioCanvas( outname.split('/')[-1], outname.split('/')[-1], 500, 500)
    pad_top = outcan.GetPrimitive('pad_top')
    pad_bot = outcan.GetPrimitive('pad_bot')

    pad_top.SetLogy()
    collect=[]
    divs=[]
    #outcan.GetPrimitive('pad_bot').SetLogy()
    these_colors = [kBlack,kRed+1, kBlue+2,kGray+1]
    #these_colors = [kBlack,kGray+1]
    these_transcolors=[]
    for c in these_colors:
      these_transcolors.append(ROOT.TColor.GetColorTransparent(c, .5))
 
    #hists = [hists[0], hists[3]] 
    divs = []
    for idx, hist in enumerate(hists):
      #AddHistogram(outcan,hist,drawopt=drawopt) 
      #AddRatio(outcan, hist, ref_hist, drawopt = drawopt, divide=divide)
      div = hist.Clone(); div.Divide(div,ref_hist,1.,1.,'b'); div.Scale(100.); collect.append(div)
      hist.SetMarkerSize(0.35)
      div.SetMarkerSize(0.5)
      hist.SetLineColor(these_colors[idx])
      hist.SetMarkerColor(these_colors[idx])
      hist.SetFillColor(these_transcolors[idx])
      div.SetMarkerColor(these_colors[idx])
      AddHistogram( pad_top, hist, 'histE2 L same', False, None, None)
      divs.append( div )
      if idx == 0 or idx == 3: AddHistogram( pad_bot, div , 'p', False, None, None)
    #AddHistogram( pad_bot, divs[2] , 'p'   , False, None, None)

    #pad_bot.SetLogy() 
    #SetColors(pad_top,these_colors=these_colors)
    #SetColors(pad_bot,these_colors=these_colors)
    #pad_top.cd()
    #SetColors(pad_top,these_colors=these_transcolors, lineColor=False,markerColor=False,fillColor=True)
    #SetColors(pad_bot,these_colors=these_transcolors, lineColor=False,markerColor=False,fillColor=True)
  
    legend = [ 'Both Approved','Ringer Rejected', 'Ringer Approved', 'Both Rejected' ]
    AddTopLabels(outcan, legend, runLabel=runLabel, legOpt='p',
                 logger=self._logger,etlist=self._etBins,etalist=self._etaBins,etidx=etidx,etaidx=etaidx)
    FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
    SetAxisLabels(outcan,xlabel,'Count','Agreement [%]')
    AutoFixAxes(pad_top,ignoreErrors=False)
    FixYaxisRanges(pad_bot, ignoreErrors=True, yminc=-eps )
    if addbinlines:
      AddBinLines(pad_top,hists[0],useHistMax=True,horizotalLine=0.)
      #AddBinLines(pad_bot,hists[0],useHistMax=True,horizotalLine=0.)
    AddRightAxisObj(pad_bot, divs[1:3], drawopt="p,same", equate=[0., max([d.GetBinContent(h.GetMaximumBin()) for d,h in zip(divs[1:3], hists[1:3])])]
                   , drawAxis=True, axisColor=(ROOT.kGray+3), ignorezeros=False
                   , ignoreErrors=True, label = "Disagreement [%]")
    #AddOutOfBoundArrows(pad_bot, useFill=True, useMarkerColor=True, colors=None, lengthDiv=.01,arrowLenghtDiv=.003, textPerc=2, addNumbers=False)
    outcan.SaveAs( outname+'.C' ) 
    outname = outname+'.pdf'
    outcan.SaveAs( outname ) 
    return outname




  def _getStatistics( self,basepath, key, etidx=None, etaidx=None ):
    sg = self.getStoreGateSvc()
    # get all quadrant histograms

    if (etidx is not None) and (etaidx is not None):
      hists = [
                sg.histogram(basepath+'/passed_passed/'+key),
                sg.histogram(basepath+'/passed_rejected/'+key),
                sg.histogram(basepath+'/rejected_passed/'+key),
                sg.histogram(basepath+'/rejected_rejected/'+key)
              ]
    else:
      from itertools import product
      passed_passed = []; passed_rejected = []; rejected_passed = []; rejected_rejected = []
      for etBinIdx, etaBinIdx in product(range(len(self._etBins)-1),range(len(self._etaBins)-1)):
        binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx) 
        passed_passed.append( sg.histogram(basepath+'/'+binning_name+'/passed_passed/'+key) ) 
        passed_rejected.append( sg.histogram(basepath+'/'+binning_name+'/passed_rejected/'+key) )
        rejected_passed.append( sg.histogram(basepath+'/'+binning_name+'/rejected_passed/'+key) )
        rejected_rejected.append( sg.histogram(basepath+'/'+binning_name+'/rejected_rejected/'+key) )

      hists = [
                sumHists(passed_passed),
                sumHists(passed_rejected),
                sumHists(rejected_passed),
                sumHists(rejected_rejected),
              ]

    # NOTE: Follow the statistics definitions for each case.
    # passed is 1 and rejected is zero
    # expression A is i and expression B is j
    # Contigency table:
    #      | hi=0  hi=1
    # hj=0 |  a     c
    # hj=1 |  b     d
    a = hists[3].GetEntries()
    d = hists[0].GetEntries()
    b = hists[2].GetEntries()
    c = hists[1].GetEntries()
    m = a+b+c+d
    
    Qij=0;Pij=0;Kp=0;dis_ij=0

    try:
      # Q statistics
      Qij = (a*d-b*c) / float(a*d+b*c)
  
      # correlation coef
      Pij = (a*d-b*c)/np.sqrt(( (a+b)*(a+c)*(c+d)*(b+d) ))

      # kappa-statistics
      Q1 = (a+d)/float(m)
      Q2 = ( (a+b)*(a+c)+(c+d)*(b+d) ) / float(m*m)
      Kp = (Q1-Q2)/ float(1-Q2)
      
      dis_ij = (b+c)/float(m)
    except:
      pass
    return  {'Qij':Qij,'Pij':Pij,'Kp':Kp, 'dis_ij':dis_ij}





