
__all__ = ["PileupLinearCorrectionTool"]

from RingerCore                                   import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars,expandFolders, csvStr2List, progressbar
from prometheus.core                              import StatusCode
from prometheus.core                              import Dataframe
from prometheus.drawers.functions                 import *
from prometheus.tools.atlas.common                import ATLASBaseTool
from prometheus.tools.atlas.common.constants      import *
from prometheus.drawers.functions.AtlasStyle      import *
from prometheus.drawers.functions.PlotFunctions   import *
from prometheus.drawers.functions.TAxisFunctions  import *





def PlotEff( chist, hist_eff, hist_eff_corr, refvalue, outname, xlabel=None, runLabel=None,  etBinIdx=None, etaBinIdx=None, etBins=None,etaBins=None):

  from ROOT import TCanvas, gStyle, TLegend, kRed, kBlue, kBlack,TLine,kBird, kOrange
  from ROOT import TGraphErrors,TF1,TColor
  gStyle.SetPalette(kBird)
  ymax = chist.ymax(); ymin = chist.ymin()
  xmin = ymin; xmax = ymax
  drawopt='lpE2'
  
  canvas = TCanvas('canvas','canvas',500, 500)
  hist_eff.SetTitle('Signal Efficiency in: '+partition_name)
  hist_eff.SetLineColor(kGray+2)
  hist_eff.SetMarkerColor(kGray+2)
  hist_eff.SetFillColor(TColor.GetColorTransparent(kGray, .5))
  hist_eff_corr.SetLineColor(kBlue+1)
  hist_eff_corr.SetMarkerColor(kBlue+1)
  hist_eff_corr.SetFillColor(TColor.GetColorTransparent(kBlue+1, .5))
  AddHistogram(canvas,hist_eff,drawopt)
  AddHistogram(canvas,hist_eff_corr,drawopt)
  l0 = TLine(xmin,refvalue,xmax,refvalue)
  l0.SetLineColor(kBlack)
  l0.Draw()
  l1 = TLine(x_min,refvalue,x_max,refvalue)
  l1.SetLineColor(kGray+2)
  l1.SetLineStyle(9)
  l1.Draw()
  AddTopLabels( canvas, ['Without correction','With correction'], runLabel=runLabel, legOpt='p',
                etlist=etBins,
                etalist=EtaBins,
                etidx=etBinIdx,etaidx=etaBinIdx)
  
  FormatCanvasAxes(canvas, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  SetAxisLabels(canvas,xlabel,'#epsilon('+xlabel+')')
  FixYaxisRanges(canvas, ignoreErrors=False,yminc=-eps)
  AutoFixAxes(canvas,ignoreErrors=False)
  AddBinLines(canvas,sgn_hist_eff)
  canvas.SaveAs(outname+'.pdf')
  canvas.SaveAs(outname+'.C')





def Plot2DHist( chist, hist2D, a, b, discr_points, nvtx_points, error_points, outname, xlabel):
    
  from ROOT import TCanvas, gStyle, TLegend, kRed, kBlue, kBlack,TLine,kBird, kOrange
  from ROOT import TGraphErrors,TF1,TColor
  gStyle.SetPalette(kBird)
  ymax = chist.ymax(); ymin = chist.ymin()
  xmin = ymin; xmax = ymax
  drawopt='lpE2'

  canvas = TCanvas('canvas','canvas',500, 500)
  canvas.SetRightMargin(0.15)
  hist2D.SetTitle('Neural Network output as a function of nvtx, '+partition_name)
  hist2D.GetXaxis().SetTitle('Neural Network output (Discriminant)')
  hist2D.GetYaxis().SetTitle(xlabel)
  hist2D.GetZaxis().SetTitle('Count')
  #if not removeOutputTansigTF:  hist2D.SetAxisRange(-1,1, 'X' )
  sgn_hist2D.Draw('colz')
  canvas.SetLogz()
  g1 = TGraphErrors(len(discr_points), array.array('d',discr_points), array.array('d',nvtx_points), array.array('d',error_points)
                   , array.array('d',[0]*len(discr_points)))
  g1.SetLineWidth(1)
  g1.SetLineColor(kBlue)
  g1.SetMarkerColor(kBlue)
  g1.Draw("P same")
  l3 = TLine(b+a*xmin,ymin, a*xmax+b, ymax)
  l3.SetLineColor(kBlack)
  l3.SetLineWidth(2)
  l3.Draw()
  FormatCanvasAxes(canvas, XLabelSize=16, YLabelSize=16, XTitleOffset=0.87, ZLabelSize=14,ZTitleSize=14, YTitleOffset=0.87, ZTitleOffset=1.1)
  SetAxisLabels(canvas,'Neural Network output (Discriminant)',xname)
  AtlasTemplate1(canvas,atlaslabel=atlaslabel)
  canvas.SaveAs(outname+'.pdf')
  canvas.SaveAs(outname+'.C')







class PileupLinearCorrectionTool( ATLASBaseTool ):

  def __init__(self, name):

    ATLASBaseTool.__init__(self, name)
    self._basepath = 'Event/PileupCorrection'
    self._thresholdEtBins   = ringer_tuning_etbins
    self._thresholdEtaBins  = ringer_tuning_etabins
    import collection
    self._targets = collection.OrderedDict()
    self._probesId = []

  def setProbesId(self, id):
    self._probesId.append(id)
    self.setId(id)

  def setBackgroundId( self, id ):
    self.setId(id)


  def addTarget( self, target ):
    if target.name() in self._targets.keys():
      self._logger.error("Can not include %s as target. This target already exist into the target list", target.name())
    else:
      self._targets[ target.name() ] = target



  def setEtBinningValues( self, etbins ):
    self._thresholdEtBins = etbins

  def setEtaBinningValues( self, etabins ):
    self._thresholdEtaBins = etabins


  def setHistogram2DRegion( self, xmin, xmax, ymin, ymax, xres=0.02, yres=0.5 ):
    self._histparams = TH2FParameters(xmin,xmax,xres,ymin,ymax,yres)



  def initialize(self):

    ATLASBaseTool.initialize(self)
    from ROOT import TH2F, TH1F, TProfile
    keyWanted = ['probes','fakes']
    from itertools import product

    sg = self.getStoreGateSvc()

    for dx, dirname in enumerate(keyWanted):
      for target in self._targets:
        for etBinIdx, etaBinIdx in product(range(len(self._threshold_etbins)-1),range(len(self._threshold_etabins)-1)):
 
          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          etbins  = zee_etbins
          etabins = default_etabins
          xbins = int( (self._histparams.xmax()-self._histparams.xmin()) / float(0.001) )
          nmubins = int((self._histparams.ymax()-self._histparams.ymin())/ float(0.5)) 

          # create neural network histograms
          sg.mkdir( self._basepath+'/'+dirname+'/'+target.name()+'/'+target.algname()+'/'+binningname )
          sg.addHistogram(TH2F('discriminantVsEt'  , 'Et Vs discriminant' , xbins, xmin, xmax, len(etbins)-1 , np.array(etbins) ) )
          sg.addHistogram(TH2F('discriminantVsEta' , 'Eta Vs discriminant', xbins, xmin, xmax, len(etabins)-1, np.array(etabins) ) )
          sg.addHistogram(TH2F('discriminantVsNvtx', 'Offline Pileup as function of the discriminant;discriminant;nvtx;Count', \
                                       xbins, xmin,xmax,len(nvtx_bins)-1,np.array(nvtx_bins)) )
          sg.addHistogram(TH2F('discriminantVsMu'  , 'Online Pileup as function of the discriminant;discriminant;nvtx;Count' , \
                                       xbins, xmin,xmax,nmubins,mumin,mumax) )

          # create efficiency target histograms
          sg.mkdir( self._basepath+'/'+dirname+'/'+target.name()+'/'+target.refname()+'/'+binningname )
          sg.addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', len(etbins)-1, np.array(etbins)))
          sg.addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(etabins)-1, np.array(etabins)))
          sg.addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", 20, -3.2, 3.2));
          sg.addHistogram(TH1F('nvtx' ,'N_{vtx} distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
          sg.addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', 16, 0, 80))
          sg.addHistogram(TH1F('match_et','E_{T} matched distribution;E_{T};Count', len(etbins)-1, np.array(etbins)))
          sg.addHistogram(TH1F('match_eta','#eta matched distribution;#eta;Count', len(etabins)-1, np.array(etabins)))
          sg.addHistogram(TH1F("match_phi", "#phi matched distribution; #phi ; Count", 20, -3.2, 3.2));
          sg.addHistogram(TH1F('match_nvtx' ,'N_{vtx} matched distribution;N_{vtx};Count', len(nvtx_bins)-1, np.array(nvtx_bins)))
          sg.addHistogram(TH1F('match_mu' ,'<#mu> matched distribution;<#mu>;Count', 16, 0, 80))
          sg.addHistogram(TProfile("eff_et", "#epsilon(E_{T}); E_{T} ; Efficiency" , len(etbins)-1, np.array(etbins)))
          sg.addHistogram(TProfile("eff_eta", "#epsilon(#eta); #eta ; Efficiency"  , len(etabins)-1,np.array(etabins)))
          sg.addHistogram(TProfile("eff_phi", "#epsilon(#phi); #phi ; Efficiency", 20, -3.2, 3.2));
          sg.addHistogram(TProfile("eff_nvtx", "#epsilon(N_{vtx}); N_{vtx} ; Efficiency", len(nvtx_bins)-1, np.array(nvtx_bins)));
          sg.addHistogram(TProfile("eff_mu", "#epsilon(<#mu>); <#mu> ; Efficiency", 16, 0, 80));


    self.init_lock()
    return StatusCode.SUCCESS


  def execute(self, context):

    # offline electron
    el = context.getHandler( "ElectronContainer" )
    sg = self.getStoreGateSvc()
    
    from prometheus.tools.atlas.common.constants import GeV
    import math
    # retrive the correct et/eta information
    if self._doTrigger: # Online
      fc = context.getHandler( "HLT__FastCaloContainer" ); et = fc.et()/GeV; eta = fc.eta(); phi = fc.phi()
    else: # Offline
      phi = el.phi()
      eta = el.caloCluster().etaBE2()
      if el.trackParticle().eta() != 0:
        et = (el.caloCluster().energy()/math.cosh(el.trackParticle().eta()))/GeV
      else:
        et = (el.caloCluster().energy()/math.cosh(eta))/GeV

    # TODO: This should be a property for future?
    # Remove events after 2.47 in eta. This region its not good for calo cells. (Fat cells)
    if abs(eta)>2.47:
      return StatusCode.SUCCESS

    # retrieve the pileup event information
    eventInfo = context.getHandler( "EventInfoContainer" )
    nvtx = eventInfo.nvtx()
    avgmu = eventInfo.avgmu()

    # check if the current event looper contains the list
    # if id to fill all histograms.
    dirname = 'probes' if eventInfo.id() in self._probesId else 'fakes'

    # Get the correct binning to fill the histogram later...
    etBinIdx, etaBinIdx = RetrieveBinningIdx( et, abs(eta), self._threshold_etbins, self._threshold_etabins, logger=self._logger )
    if etBinIdx < 0 or etaBinIdx < 0:
      self._logger.warning('Skipping event since et/eta idx does not match with the current GEO/Energy position.')
      return StatusCode.SUCCESS

    # get bin name to point to the correct directory
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)

    # Loop over pid names
    for target in self._targets:

      algname = target.algname(); refname = target.refname()
      # get the target answer
      if self._doTrigger:
        # Get the decoration from HLT electron or fast calo (only for skimmed)
        passed = self.accept(tgtname)
        if self.dataframe is Dataframe.PhysVal_v2:
          obj = context.getHandler( "HLT__ElectronContainer" )
        elif self.dataframe is Dataframe.SkimmedNtuple_v2:
          obj = context.getHandler( "HLT__FastCaloContainer" )
        # get the ringer RNN discriminant
        discriminant = obj.getDecor(algname+'_discriminant')

      else:
        # Get de decision from Offline electron
        passed = el.accept(refname)
        # get the ringer RNN discriminant
        discriminant = el.getDecor(algname+'_discriminant')

      path = self._basepath+'/'+dirname+'/'+target.name()+'/'+refname+'/'+binningname
      self._logger.debug('Et = %1.2f, Eta = %1.2f, phi = %1.2f, nvtx = %1.2f, mu = %1.2f, passed = %d',
          et,eta,phi,nvtx,avgmu,int(passed))

      # Fill all target histograms
      sg.histogram(path+'/et').Fill(et)
      sg.histogram(path+'/eta').Fill(eta)
      sg.histogram(path+'/phi').Fill(phi)
      sg.histogram(path+'/nvtx').Fill(nvtx)
      sg.histogram(path+'/mu').Fill(avgmu)

      if passed: # If approved by the selector
        sg.histogram(path+'/match_et').Fill(et)
        sg.histogram(path+'/match_eta').Fill(eta)
        sg.histogram(path+'/match_phi').Fill(phi)
        sg.histogram(path+'/match_nvtx').Fill(nvtx)
        sg.histogram(path+'/match_mu').Fill(avgmu)

      sg.histogram(path+'/eff_et').Fill(et,passed)
      sg.histogram(path+'/eff_eta').Fill(eta,passed)
      sg.histogram(path+'/eff_phi').Fill(phi,passed)
      sg.histogram(path+'/eff_nvtx').Fill(nvtx,passed)
      sg.histogram(path+'/eff_mu').Fill(avgmu,passed)

      # Fill discriminant distributions
      path = self._basepath+'/'+dirname+'/'+target.name()+'/'+targer.algname()+'/'+binningname
      sg.histogram(path+'/discriminantVsEt').Fill(discriminant, et)
      sg.histogram(path+'/discriminantVsEta').Fill(discriminant, eta)
      sg.histogram(path+'/discriminantVsMu').Fill(discriminant, avgmu)
      sg.histogram(path+'/discriminantVsNvtx').Fill(discriminant, nvtx)


    return StatusCode.SUCCESS


  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  
  def plot(self, dirname, filenames, exportTool=None ):


    if not exportTool:
      from TuningTools.export import TrigMultiVarHypo_v2
      exportTool = TrigMultiVarHypo_v2( removeOutputTansigTF=True )

    summary = self.generate_plots(dirname)
    #generate thresholds config file
    for target in self._targets:
      exportTool.create_thresholds( summary[target.name()]['thresholds'], target.outputname() )

  


    etbins_str = []; etabins_str=[]
    for etBinIdx in range( len(self._threshold_etbins)-1 ):
      etbin = (self._threshold_etbins[etBinIdx], self._threshold_etbins[etBinIdx+1])
      if etbin[1] > 100 :
        etbins_str.append( r'$E_{T}\text{[GeV]} > %d$' % etbin[0])
      else:
        etbins_str.append(  r'$%d < E_{T} \text{[Gev]}<%d$'%etbin )

    for etaBinIdx in range( len(self._threshold_etbins)-1 ):
      etabin = (self._threshold_etabins[etaBinIdx], self._threshold_etabins[etaBinIdx+1])
      etabins_str.append( r'$%.2f<\eta<%.2f$'%etabin )



    from RingerCore.tex.TexAPI import Table, ResizeBox, Tabular, HLine, TableLine
    from RingerCore.tex.BeamerAPI import BeamerTexReportTemplate1, BeamerSection, BeamerSubSection, BeamerMultiFigureSlide, BeamerSlide

    self._logger.info('Do pdf maker...')
    # Slide maker
    with BeamerTexReportTemplate1( theme = 'Berlin'
                                 , _toPDF = True
                                 , title = pdftitle
                                 , outputFile = pdfoutput
                                 , font = 'structurebold' ):

      for target in self._targets:

        with BeamerSection( name = target.name().replace('_','\_') ):

          with BeamerSubSection( name = 'Correction plots for each phase space'):
            
            algname = target.algname()
            tgtname = target.refname()

            for etBinIdx in range( len(self._threshold_etbins)-1 ):
              for etaBinIdx in range( len(self._threshold_etabins)-1 ):
                plots = summary['plotnames'][etBinIdx][etaBinIdx]
                binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
                plotnames = [ plots['signal_corr_eff'], plots['background_corr_eff'], plots['hist2D_signal_corr'], plots['hist2D_background_corr'] ]
                title = 'Energy between %s in %s (et%d\_eta%d)'%(etbins_str[etBinIdx],etabins_str[etaBinIdx],etBinIdx,etaBinIdx)
                BeamerMultiFigureSlide( title = title
                              , paths = plotnames
                              , nDivWidth = 2 # x
                              , nDivHeight = 2 # y
                              , texts=None
                              , fortran = False
                              , usedHeight = 0.8
                              , usedWidth = 1.
                              )

          with BeamerSubSection( name = 'Efficiency Values' ):

            ### Prepare tables
            lines1 = []
            lines1 += [ HLine(_contextManaged = False) ]
            lines1 += [ HLine(_contextManaged = False) ]
            lines1 += [ TableLine( columns = [''] + [s for s in etabins_str], _contextManaged = False ) ]
            lines1 += [ HLine(_contextManaged = False) ]

            for etBinIdx in range( len(self._thresholdEtBins)-1 ):
              values_det = []; values_fa = []
              for etaBinIdx in range( len(self._thresholdEtaBins)-1 ):
                det = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_corr_eff']*100.0
                fa  = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_corr_eff']*100.0
                ref = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_reference']*100.0

                if (det-ref) > 0.0:
                  values_det.append( ('\\cellcolor[HTML]{9AFF99}%1.2f ($\\uparrow$%1.2f[$\\Delta_{ref}$])')%(det,det-ref) )
                elif (det-ref) < 0.0:
                  values_det.append( ('\\cellcolor[HTML]{F28871}%1.2f ($\\downarrow$%1.2f[$\\Delta_{ref}$])')%(det,det-ref) )
                else:
                  values_det.append( ('\\cellcolor[HTML]{9AFF99}%1.2f')%(det) )

                ref = summary[target.name()]['summaryValues'][etBinIdx][etaBinIdx]['background_reference']*100.0
                factor = fa/ref if ref else 0.
                if (fa-ref) > 0.0:
                  values_fa.append( ('\\cellcolor[HTML]{F28871}%1.2f ($\\rightarrow$%1.2f$\\times\\text{FR}_{ref}$)')%(fa,factor) )
                elif (fa-ref) < 0.0:
                  values_fa.append( ('\\cellcolor[HTML]{9AFF99}%1.2f ($\\rightarrow$%1.2f$\\times\\text{FR}_{ref}$)')%(fa,factor) )
                else:
                  values_fa.append( ('\\cellcolor[HTML]{9AFF99}%1.2f')%(fa) )

              lines1 += [ TableLine( columns = [etbins_str[etBinIdx]] + values_det   , _contextManaged = False ) ]
              lines1 += [ TableLine( columns = [''] + values_fa , _contextManaged = False ) ]
              lines1 += [ HLine(_contextManaged = False) ]
            lines1 += [ HLine(_contextManaged = False) ]

            
            # prepare table 2 (integrated values)

            fa          = summary[target.name()]['background_reference']['eff']*100
            passed_fa   = summary[target.name()]['background_reference']['passed']
            total_fa    = summary[target.name()]['background_reference']['total']
            det         = summary[target.name()]['signal_reference']['eff']*100
            passed_det  = summary[target.name()]['signal_reference']['passed']
            total_det   = summary[target.name()]['signal_reference']['total']


            lines2 = []
            lines2 += [ HLine(_contextManaged = False) ]
            lines2 += [ HLine(_contextManaged = False) ]
            lines2 += [ TableLine( columns = ['',r'$P_{D}[\%]$',r'$F_{a}[\%]$'], _contextManaged = False ) ]
            lines2 += [ HLine(_contextManaged = False) ]
            lines2 += [ TableLine( columns = ['Reference','%1.2f (%d/%d)'%(det,passed_det,total_det),
                                              '%1.2f (%d/%d)'%(fa,passed_fa,total_fa)]  , _contextManaged = False ) ]


            fa = summary[target.name()]['background__corr_values']['eff']*100
            passed_fa = summary[target.name()]['background_corr_values']['passed']
            total_fa = summary[target.name()]['background_corr_values']['total']
            det = summary[target.name()]['signal_corr_values']['eff']*100
            passed_det = summary[target.name()]['signal_corr_values']['passed']
            total_det = summary[target.name()]['signal_corr_values']['total']

            lines2 += [ TableLine( columns = [target.name().replace('_','\_'),'%1.2f (%d/%d)'%(det,passed_det,total_det),
                                              '%1.2f (%d/%d)'%(fa,passed_fa,total_fa)]  , _contextManaged = False ) ]

            det = summary[target.name()]['signal_values']['eff']*100
            passed_det = summary[target.name()]['signal_values']['passed']
            total_det = summary[target.name()]['signal_values']['total']
            fa = summary[target.name()]['background_values']['eff']*100
            passed_fa = summary[target.name()]['background_values']['passed']
            total_fa = summary[target.name()]['background_values']['total']
            lines2 += [ TableLine( columns = [target.name().replace('_','\_')+' (not corrected)','%1.2f (%d/%d)'%(det,passed_det,total_det),
              '%1.2f (%d/%d)'%(fa,passed_fa,total_fa)]  , _contextManaged = False ) ]

            lines2 += [ HLine(_contextManaged = False) ]
            lines2 += [ HLine(_contextManaged = False) ]

            if target.relaxParameter()!=0.0:
              extra_legend = 'The relax param is $R_{%s} = %1.2f\%%$ more for each reference bin.'%(target.name(),target.relaxParameter()*100)
            else:
              extra_legend = ''

            ### make sheet file
            try:
              xls = {}
              for etBinIdx in range( len(self._thresholdEtBins)-1 ):
                for etaBinIdx in range( len(self._thresholdEtaBins)-1 ):
                  if not etabins_str[etaBinIdx] in xls.keys(): xls[etabins_str[etaBinIdx]] = []
                  mu_limit = summary[target.name()]['summaryValues'][etBinIdx][etaBinIdx]['muLimits']
                  l = [ '%1.2f (%1.1f)'%(v,fa_limits[idx_]) for idx_, v in enumerate(mu_limit)]
                  xls[etabins_str[etaBinIdx]].extend(l)
              from pandas import DataFrame
              df = DataFrame(xls)
              df.to_excel('%s.xlsx'%target.name(), sheet_name='sheet1', index=False)
            except:
              self._logger.warning("Can not create sheets")



            with BeamerSlide( title = "Efficiency Values After Correction"  ):
              with Table( caption = '$P_{d}$ and $F_{a}$ for all phase space regions.'+extra_legend) as table:
                with ResizeBox( size = 1 ) as rb:
                  with Tabular( columns = 'l' + 'c' * len(etabins_str) ) as tabular:
                    tabular = tabular
                    for line in lines1:
                      if isinstance(line, TableLine):
                        tabular += line
                      else:
                        TableLine(line, rounding = None)
              with Table( caption = 'Integrated efficiency comparison.') as table:
                with ResizeBox( size = 0.6 ) as rb:
                  with Tabular( columns = 'l' + 'c' * 3 ) as tabular:
                    tabular = tabular
                    for line in lines2:
                      if isinstance(line, TableLine):
                        tabular += line
                      else:
                        TableLine(line, rounding = None)



    return StatusCode.SUCCESS




  def generate_plots(self, dirname):
    
    import ROOT
    ROOT.gErrorIgnoreLevel=ROOT.kFatal
    
    import os
    localpath = os.getcwd()+'/'+dirname
    try:
      if not os.path.exists(localpath): os.makedirs(localpath)
    except:
      self._logger.warning('The director %s exist.', localpath)

    summary = {}
    from itertools import product
    from RingerCore import progressbar

    for target in self._targets:
      
      # build the efficiency table
      summary[target.name()] = {
                        'summary_values'          : [[dict() for _ in range(len(self._threshold_etabins)-1)] for __ in range(len(self._threshold_etbins)-1)],
                        'plotnames'               : [[dict() for _ in range(len(self._threshold_etabins)-1)] for __ in range(len(self._threshold_etbins)-1)],
                        'signal_corr_values'      : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'background_corr_values'  : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'signal_reference'        : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'background_reference'    : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'thresholds'              : [],
                        }


      for etBinIdx, etaBinIdx in progressbar(product(range(len(self._threshold_etbins)-1),range(len(self._threshold_etabins)-1)),
                                                 (len(self._threshold_etbins)-1)*(len(self._threshold_etabins)-1),
                                                 logger = self._logger, prefix = "Plotting (%s)... " % target.name()):


        binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
        doLinearCorrection= False if (etBinIdx, etaBinIdx) in excludedEt_EtaBinIdx else True

        self._logger.info('Applying correction in <et=%d, eta=%d> ? %s', etBinIdx,etaBinIdx, doLinearCorrection)

        sgn_hist2D = sg.histogram(self._basepath+'/probes/'+target.name()+'/'+target.algname()+'/'+('discriminantVsMu' if self._doTrigger else 'discriminantVsNvtx') )
        bkg_hist2D = sg.histogram(self._basepath+'/fakes/'+target.name()+'/'+target.algname()+'/'+('discriminantVsMu' if self._doTrigger else 'discriminantVsNvtx') )

        sgn_eff, sgn_passed, sgn_total  = target.reference( self.getStoreGateSvc(), etBinIdx, etaBinIdx, self._basepath )
        bkg_eff, bkg_passed, bkg_total  = target.reference( self.getStoreGateSvc(), etBinIdx, etaBinIdx, self._basepath, True )
        sgn_counters   = {'eff':sgn_eff,'passed':sgn_passed,'total':sgn_total}
        bkg_counters   = {'eff':bkg_eff,'passed':bkg_passed,'total':bkg_total}
 
        csummary, objects = self._apply_threshold_correction( self._histparams, sgn_hist2D, bkg_hist2D, sgn_eff, doLinearCorrection=doLinearCorrection)
        

        def UpdateCounters(obj1,obj2):
          for key in ['total','passed']: obj1[key]+=obj2[key]
          obj1['eff']=obj1['passed']+float(obj1['total'])

        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_corr_values']     = csummary
        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_corr_values'] = csummary
        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_reference']       = sgn_counters
        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_reference']   = bkg_counters
        UpdateCounters( summary[target.name()]['signal_corr_values']    , csummary['signal_corr_values']    )
        UpdateCounters( summary[target.name()]['background_corr_values'], csummary['background_corr_values'])
        UpdateCounters( summary[target.name()]['signal_reference']      , sgn_counters                      )
        UpdateCounters( summary[target.name()]['background_reference']  , bkg_counters                      )


        # Plot signal efficicency w.r.t the pileup
        outname = localpath+'/eff_signal_corr_'+target.name()+'_'+binningname
        plotname = PlotEff( self._histparams, objects['signal_hists']['eff'], objects['signal_corr_hists']['eff'], 
                           sgn_eff, outname, xlabel='', runLabel=None,  etBinIdx=etBinIdx, etaBinIdx=etaBinIdx, etBins=self._threshold_etbins,
                           etaBins=self._threshold_etaBins)
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['signal_corr_eff'] = plotname

        # Plot background efficicency w.r.t the pileup
        outname = localpath+'/eff_background_corr_'+target.name()+'_'+binningname
        plotname = PlotEff( self._histparams, objects['background_hists']['eff'], objects['background_corr_hists']['eff'], 
                           sgn_eff, outname, xlabel='', runLabel=None,  etBinIdx=etBinIdx, etaBinIdx=etaBinIdx, etBins=self._threshold_etbins,
                           etaBins=self._threshold_etaBins)
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['background_corr_eff'] = plotname


        outname = localpath+'/hist2D_signal_corr_'+target.name()+'_'+binningname
        plotname = Plot2DHist( self._histparams, objects['signal_corr_hists']['hist2D'], objects['correction']['angular'], objects['correction']['offset'],
                               objects['correction']['discr_points'], objects['correction']['nvtx_points'], objects['correction']['error_points'], outname, 
                               '<#mu>' if self._doTrigger else 'N_{vtx}' )
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['hist2D_signal_corr'] = plotname
        

        outname = localpath+'/hist2D_background_corr_'+target.name()+'_'+binningname
        plotname = Plot2DHist( self._histparams, objects['background_corr_hists']['hist2D'], objects['correction']['angular'], objects['correction']['offset'],
                               objects['correction']['discr_points'], objects['correction']['nvtx_points'], objects['correction']['error_points'], outname, 
                               '<#mu>' if self._doTrigger else 'N_{vtx}' )
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['hist2D_background_corr'] = plotname


        etbin   = (self._threshold_etbins[etBinIdx]   , self._threshold_etbins[etBinIdx+1]  )
        etabin  = (self._threshold_etabins[etaBinIdx] , self._threshold_etabins[etaBinIdx+1])
        obj=objects['correction']
        summary[target.name()]['thresholds'].append( {
                                                        'etBin'     : np.array(etbin),
                                                        'etaBin'    : np.array(etabin),
                                                        'muBin'     : np.array(muBin),
                                                        'etBinIdx'  : etBinIdx,
                                                        'etaBinIdx' : etaBinIdx,
                                                        'threshold' : (obj['angular'],obj['offset'], obj['offset_0'])
                                                     } ) # angular, offset, threshold_no_correction



    return summary




  def _apply_threshold_correction( self, chist, sgn_hist2D, bkg_hist2D, refvalue, limits = None, doLinearCorrection=True ):


    mumin = chist.ymin()
    mumax = chist.ymax()

    sgn_hist2D = Copy2DRegion(sgn_hist2D.Clone(),chist.xbins(),chist.xmin(),chist.xmax(),np.int(np.round((mumax-mumin)/sgn_hist2D.GetYaxis().GetBinWidth(1))),mumin,mumax)
    bkg_hist2D = Copy2DRegion(bkg_hist2D.Clone(),chist,xbins(),chist.xmin(),chist.xmax(),np.int(np.round((mumax-mumin)/bkg_hist2D.GetYaxis().GetBinWidth(1))),mumin,mumax)
    
    import math
    if isinstance(chist.yres(),(float,int)):
      sgn_hist2D = sgn_hist2D.RebinY(np.int(math.floor(sgn_hist2D.GetNbinsY()/chist.ybins())))
      bkg_hist2D = bkg_hist2D.RebinY(np.int(math.floor(bkg_hist2D.GetNbinsY()/chist.ybins())))
    else:
      sgn_hist2D = rebinY(sgn_hist2D,chist.yres())
      bkg_hist2D = rebinY(bkg_hist2D,chist.yres())


    from copy import deepcopy
    false_alarm = 1.0
    false_alarm_limit = 0.5
    
    while false_alarm > false_alarm_limit:
      # Calculate the original threshold
      b0, error = FindThreshold(sgn_hist2D.ProjectionX(), refvalue )
      # Take eff points using uncorrection threshold
      discr_points, nvtx_points, error_points = CalculateDependentDiscrPoints(sgn_hist2D , refvalue )
      nvtx = np.array(nvtx_points)
      local_a = ( discr_points[0] - discr_points[1] ) / ( nvtx[0] - nvtx[1] )
      local_b = discr_points[0] - local_a*nvtx[0]
      # Calculate eff without correction
      sgn_histNum, sgn_histDen, sgn_histEff, sgn_info   = CalculateEfficiency(sgn_hist2D, refvalue, b0, 0,  doCorrection=False)

      if doLinearCorrection:
        sgn_histNum_corr, sgn_histDen_corr, sgn_histEff_corr, sgn_info_corr ,b, a = CalculateEfficiency( sgn_hist2D, refvalue, b0, 0, doCorrection=True, limits=limits)
        if a>0:
          self._warning("Retrieved positive angular factor of the linear correction, setting to 0!")
          a = 0; b = b0;
      else:
        sgn_histNum_corr=sgn_histNum.Clone()
        sgn_histDen_corr=sgn_histDen.Clone()
        sgn_histEff_corr=sgn_histEff.Clone()
        sgn_info_corr=deepcopy(sgn_info)
        b=b0; a=0.0


      # Calculate eff without correction
      bkg_histNum, bkg_histDen, bkg_histEff, bkg_info  = CalculateEfficiency(bkg_hist2D, refvalue, b0, 0,  doCorrection=False)
      
      # Calculate eff using the correction from signal
      #if addToBeta:  b = b + addToBeta
      bkg_histNum_corr, bkg_histDen_corr, bkg_histEff_corr, bkg_info_corr = CalculateEfficiency(bkg_hist2D, refvalue, b, a,  doCorrection=False)
      false_alarm = bkg_info_corr[0] # get the passed/total
      if false_alarm > false_alarm_limit:
        refvalue-=0.0025

    angular = a;  offset = b; offset_0 = b0
    self._logger.debug('Signal with correction is: %1.2f%%', sgn_info_corr[0]*100 )
    self._logger.debug('Background with correction is: %1.2f%%', bkg_info_corr[0]*100 )
    

    summary = {
               'signal_corr_values'     : {'eff'  : sgn_info_corr[0], 'passed'  : sgn_info_corr[1]  , 'total'  : sgn_info_corr[2]},
               'background_corr_values' : {'eff'  : bkg_info_corr[0], 'passed'  : bkg_info_corr[1]  , 'total'  : bkg_info_corr[2]},
               'signal_values'          : {'eff'  : sgn_info[0]     , 'passed'  : sgn_info[1]       , 'total'  : sgn_info[2]},
               'background_values'      : {'eff'  : bkg_info[0]     , 'passed'  : bkg_info[1]       , 'total'  : bkg_info[2]},
               }
    objects = {
               'signal_corr_hists'      : {'num'  : sgn_histNum_corr, 'den'     : sgn_histDen_corr , 'eff'     : sgn_histEff_corr , 'hist2D'    : sgn_hist2D},      
               'background_corr_hists'  : {'num'  : bkg_histNum_corr, 'den'     : bkg_histDen_corr , 'eff'     : bkg_histEff_corr , 'hist2D'    : bkg_hist2D},
               'signal_hists'           : {'num'  : sgn_histNum     , 'den'     : sgn_histDen      , 'eff'     : sgn_histEff      , 'hist2D'    : sgn_hist2D},
               'background_hists'       : {'num'  : bkg_histNum     , 'den'     : bkg_histDen      , 'eff'     : bkg_histEff      , 'hist2D'    : bkg_hist2D},
               'correction'             : {'discr_points'   : discr_points    , 'nvtx_points'      : nvtx_points      , 'error_points'      : error_points,
                                           'angular'        : angular         , 'offset'           : offset           , 'offset0'           : offset0 },
              }

    return summary, objects
           










