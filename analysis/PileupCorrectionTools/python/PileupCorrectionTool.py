

__all__ = ["PileupCorrectionTool"]

from Gaugi import GeV
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import progressbar
from Gaugi.messenger.macros import *
from Gaugi.tex.TexAPI       import Table, ResizeBox, Tabular, HLine, TableLine
from Gaugi.tex.BeamerAPI    import BeamerTexReportTemplate1, BeamerSection, BeamerSubSection, BeamerMultiFigureSlide, BeamerSlide
from Gaugi.monet.AtlasStyle import SetAtlasStyle
from PileupCorrectionTools.utilities  import RetrieveBinningIdx
from ProfileTools.constants import zee_etbins, default_etabins, nvtx_bins
from prometheus import Dataframe as DataframeEnum


from ROOT import TH2F, TH1F, TProfile
from itertools import product

import numpy as np
import collections, math, os, ROOT

# local includes
from .functions import TH2Holder


#
# Pileup tool
#
class PileupCorrectionTool( Algorithm ):

  #
  # Constructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)

    # Declate all properties
    self.declareProperty( "Basepath"        , "Event/PileupCorrection"  )
    self.declareProperty( "IsBackground"    , False                     )
    self.declareProperty( "EtBinningValues" , []                        )
    self.declareProperty( "EtaBinningValues", []                        )


    # Set property values using the constructor args
    for key, value in kw.items():
      self.setProperty(key, value)

    # Target objetc
    self.__targets = collections.OrderedDict()


  #
  # Add target object
  #
  def addTarget( self, target ):
    if target.name() in self.__targets.keys():
      MSG_ERROR( self, "Can not include %s as target. This target already exist into the target list", target.name())
    else:
      self.__targets[ target.name() ] = target


  def setEtBinningValues( self, etbins ):
    self.setProperty( "EtBinningValues", etbins )


  def setEtaBinningValues( self, etabins ):
    self.setProperty( "EtaBinningValues", etabins )


  def setHistogram2DRegion( self, xmin, xmax, ymin, ymax, xres=0.02, yres=0.5 ):
    self.__histConfig = TH2Holder(xmin,xmax,xres,ymin,ymax,yres)



  #
  # Initialize method
  #
  def initialize(self):

    # initialize the base tool
    Algorithm.initialize(self)

    basepath = self.getProperty( "Basepath" )
    etBins = self.getProperty( "EtBinningValues")
    etaBins = self.getProperty( "EtaBinningValues")


    keyWanted = ['probes','fakes']

    # get the storegate
    sg = self.getStoreGateSvc()

    for dx, dirname in enumerate(keyWanted):
      for name, target in self.__targets.items():
        for etBinIdx, etaBinIdx in product(range(len(etBins)-1),range(len(etaBins)-1)):

          binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          etbins  = zee_etbins
          etabins = default_etabins
          xmin = self.__histConfig.xmin()
          xmax = self.__histConfig.xmax()
          mumin = self.__histConfig.ymin()
          mumax = self.__histConfig.ymax()
          xbins = int( (xmax-xmin) / float(0.02) )
          nmubins = int((mumax-mumin)/ float(0.5))

          # create neural network histograms
          sg.mkdir( basepath+'/'+dirname+'/'+name+'/'+target.algname()+'/'+binningname )
          sg.addHistogram(TH2F('discriminantVsEt'  , 'Et Vs discriminant' , xbins, xmin, xmax, len(etbins)-1 , np.array(etbins) ) )
          sg.addHistogram(TH2F('discriminantVsEta' , 'Eta Vs discriminant', xbins, xmin, xmax, len(etabins)-1, np.array(etabins) ) )
          sg.addHistogram(TH2F('discriminantVsNvtx', 'Offline Pileup as function of the discriminant;discriminant;nvtx;Count', \
                                       xbins, xmin,xmax,len(nvtx_bins)-1,np.array(nvtx_bins)) )
          sg.addHistogram(TH2F('discriminantVsMu'  , 'Online Pileup as function of the discriminant;discriminant;nvtx;Count' , \
                                       xbins, xmin,xmax,nmubins,mumin,mumax) )

          # create efficiency target histograms
          sg.mkdir( basepath+'/'+dirname+'/'+name+'/'+target.refname()+'/'+binningname )
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


  #
  # Execute method
  #
  def execute(self, context):


    basepath = self.getProperty( "Basepath" )
    etBins = self.getProperty( "EtBinningValues")
    etaBins = self.getProperty( "EtaBinningValues")

    isBackground = self.getProperty("IsBackground")

    # offline container
    if self._dataframe is DataframeEnum.Electron_v1:
      elCont    = context.getHandler( "ElectronContainer" )
    elif self._dataframe is DataframeEnum.Photon_v1:
      elCont    = context.getHandler( "PhotonContainer" )
    else:
      elCont    = context.getHandler( "ElectronContainer" )
    
    dec = context.getHandler( "MenuContainer" )
    sg = self.getStoreGateSvc()

    # retrive the correct et/eta information
    #  phi = el.phi()
    #  eta = el.caloCluster().etaBE2()
    #  if el.trackParticle().eta() != 0:
    #    et = (el.caloCluster().energy()/math.cosh(el.trackParticle().eta()))/GeV
    #  else:
    #    et = (el.caloCluster().energy()/math.cosh(eta))/GeV
    
    fc = context.getHandler( "HLT__FastCaloContainer" ); et = fc.et()/GeV; eta = fc.eta(); phi = fc.phi()

    # TODO: This should be a property for future?
    # Remove events after 2.47 in eta. This region its not good for calo cells. (Fat cells)
    if abs(eta)>2.47:
      MSG_WARNING(self, "Skippint. event eta > 2.47")
      return StatusCode.SUCCESS

    # retrieve the pileup event information
    eventInfo = context.getHandler( "EventInfoContainer" )
    nvtx = eventInfo.nvtx()
    avgmu = eventInfo.avgmu()

    # check if the current event looper contains the list
    # if id to fill all histograms.
    #dirname = 'probes' if eventInfo.id() in self._probesId else 'fakes'
    dirname = 'fakes' if isBackground  else 'probes'

    # Get the correct binning to fill the histogram later...

    etBinIdx, etaBinIdx = RetrieveBinningIdx( et, abs(eta), etBins, etaBins, logger=self._logger )
    if etBinIdx < 0 or etaBinIdx < 0:
      MSG_WARNING( self,'Skipping event since et/eta idx does not match with the current GEO/Energy position.')
      return StatusCode.SUCCESS

    # get bin name to point to the correct directory
    binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)

    # Loop over pid names
    for name , target in self.__targets.items():

      algname = target.algname(); refname = target.refname()

      # Get the decision from the menu assitent
      passed = bool(dec.accept(refname))
      accept = dec.accept( algname )
      discriminant = accept.getDecor( "discriminant" )

      path = basepath+'/'+dirname+'/'+name+'/'+refname+'/'+binningname
      MSG_DEBUG( self, 'Et = %1.2f, Eta = %1.2f, phi = %1.2f, nvtx = %1.2f, mu = %1.2f, passed = %d',
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
      path = basepath+'/'+dirname+'/'+name+'/'+target.algname()+'/'+binningname
      sg.histogram(path+'/discriminantVsEt').Fill(discriminant, et)
      sg.histogram(path+'/discriminantVsEta').Fill(discriminant, eta)
      sg.histogram(path+'/discriminantVsMu').Fill(discriminant, avgmu)
      sg.histogram(path+'/discriminantVsNvtx').Fill(discriminant, nvtx)

    return StatusCode.SUCCESS


  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  #
  # Standalone plot method
  #
  def plot(self, dirname, pdftitle, pdfoutput,  export=True ):

    from ROOT import gROOT, kTRUE
    gROOT.SetBatch(kTRUE)
    SetAtlasStyle()
    # generate all plots and the summary
    summary = self.generate_plots(dirname)

    etBins = self.getProperty( "EtBinningValues")
    etaBins = self.getProperty( "EtaBinningValues")



    if export:
      from ROOT import TEnv
      for _, target in self.__targets.items():

        etmin_list = []; etmax_list = []; etamin_list = []; etamax_list = []; slopes = []; offsets = []

        for threshold in summary[target.name()]['thresholds']:
          etmin_list.append( threshold['etBin'][0] )
          etmax_list.append( threshold['etBin'][1] )
          etamin_list.append( threshold['etaBin'][0] )
          etamax_list.append( threshold['etaBin'][1] )
          slopes.append( threshold['threshold'][0] )
          offsets.append( threshold['threshold'][1] )
        # helper function
        def list_to_str( l ):
          s = str()
          for ll in l:
            s+=str(ll)+'; '
          #s[-1]='' # remove last ;
          return s[:-2]

        env = TEnv('correction')
        env.SetValue("Threshold__etmin" , list_to_str( etmin_list ) )
        env.SetValue("Threshold__etmax" , list_to_str( etmax_list ) )
        env.SetValue("Threshold__etamin", list_to_str( etamin_list ) )
        env.SetValue("Threshold__etamax", list_to_str( etamax_list ) )
        env.SetValue("Threshold__slope" , list_to_str( slopes ) )
        env.SetValue("Threshold__offset", list_to_str( offsets ) )
        MSG_INFO( self, "Export %s...", target.name() )
        env.WriteFile( target.name() +'.conf' )

    MSG_INFO( self, 'Do pdf maker...')
    # Slide maker
    with BeamerTexReportTemplate1( theme = 'Berlin'
                                 , _toPDF = True
                                 , title = pdftitle
                                 , outputFile = pdfoutput
                                 , font = 'structurebold' ):

      # Generate all str latex et/eta bins
      etbins_str = []; etabins_str=[]
      for etBinIdx in range( len(etBins)-1 ):
        etbin = (etBins[etBinIdx], etBins[etBinIdx+1])
        if etbin[1] > 100 :
          etbins_str.append( r'$E_{T}\text{[GeV]} > %d$' % etbin[0])
        else:
          etbins_str.append(  r'$%d < E_{T} \text{[Gev]}<%d$'%etbin )

      for etaBinIdx in range( len(etaBins)-1 ):
        etabin = (etaBins[etaBinIdx], etaBins[etaBinIdx+1])
        etabins_str.append( r'$%.2f<\eta<%.2f$'%etabin )


      for _, target in self.__targets.items():

        with BeamerSection( name = target.name().replace('_','\_') ):

          with BeamerSubSection( name = 'Correction plots for each phase space'):

            algname = target.algname()
            tgtname = target.refname()

            for etBinIdx in range( len(etBins)-1 ):
              for etaBinIdx in range( len(etaBins)-1 ):
                plots = summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]
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

            for etBinIdx in range( len(etBins)-1 ):
              values_det = []; values_fa = []
              for etaBinIdx in range( len(etaBins)-1 ):
                det = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_corr_values']['eff']*100.0
                fa  = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_corr_values']['eff']*100.0
                ref = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_reference']['eff']*100.0


                if (det-ref) > 0.0:
                  values_det.append( ('\\cellcolor[HTML]{9AFF99}%1.2f ($\\uparrow$%1.2f[$\\Delta_{ref}$])')%(det,det-ref) )
                elif (det-ref) < 0.0:
                  values_det.append( ('\\cellcolor[HTML]{F28871}%1.2f ($\\downarrow$%1.2f[$\\Delta_{ref}$])')%(det,det-ref) )
                else:
                  values_det.append( ('\\cellcolor[HTML]{9AFF99}%1.2f')%(det) )

                ref = summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_reference']['eff']*100.0
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


            fa = summary[target.name()]['background_corr_values']['eff']*100
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

            if target.expertAndExperimentalMethods().scaleParameter!=0.0:
              extra_legend = 'The relax param is $R_{%s} = %1.2f\%%$ more for each reference bin.' % \
                            (target.name(),target.expertAndExperimentalMethods().scaleParameter*100)
            else:
              extra_legend = ''


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


    from .functions import ApplyThresholdLinearCorrection
    from .drawers import PlotEff, Plot2DHist

    basepath = self.getProperty( "Basepath" )
    etBins = self.getProperty( "EtBinningValues")
    etaBins = self.getProperty( "EtaBinningValues")


    ROOT.gErrorIgnoreLevel=ROOT.kFatal

    # get the basepath to generate the plots
    localpath = os.getcwd()+'/'+dirname
    try:
      if not os.path.exists(localpath): os.makedirs(localpath)
    except:
      MSG_WARNING( self,'The director %s exist.', localpath)

    # the summary
    summary = {}
    sg = self.getStoreGateSvc()

    for _, target in self.__targets.items():

      # build the efficiency table
      summary[target.name()] = {
                        'summary_values'          : [[dict() for _ in range(len(etaBins)-1)] for __ in range(len(etBins)-1)],
                        'plotnames'               : [[dict() for _ in range(len(etaBins)-1)] for __ in range(len(etBins)-1)],
                        'signal_values'           : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'background_values'       : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'signal_corr_values'      : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'background_corr_values'  : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'signal_reference'        : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'background_reference'    : {'total':0.0, 'passed':0.0, 'eff':0.0},
                        'thresholds'              : [],
                        }


      for etBinIdx, etaBinIdx in progressbar(product(range(len(etBins)-1),range(len(etaBins)-1)),
                                                 (len(etBins)-1)*(len(etaBins)-1),
                                                 logger = self._logger, prefix = "Plotting (%s)... " % target.name()):


        binningname = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
        #doLinearCorrection= False if (etBinIdx, etaBinIdx) in excludedEt_EtaBinIdx else True
        doLinearCorrection=True
        MSG_INFO( self, 'Applying correction in <et=%d, eta=%d> ? %s', etBinIdx,etaBinIdx, doLinearCorrection)

        sgn_hist2D = sg.histogram(basepath+'/probes/'+target.name()+'/'+target.algname()+'/'+binningname+'/'+ 'discriminantVsMu' )
        bkg_hist2D = sg.histogram(basepath+'/fakes/'+target.name()+'/'+target.algname()+'/'+binningname+'/'+ 'discriminantVsMu' )


        # apply the threshold linear correction follow the last strategy using the root linear fitting
        # This functions was implemented taken some functions from the tag and probe offline framework.
        # If the false alarm is higher than an threshold (default is 0.5) than we will reduce the
        # detection probability until the false alarm is lower than the stabilish limit.
        # The summary hold all counts and object hold all root python objects.
        h=self.__histConfig
        xres = h.xresolution()[etBinIdx][etaBinIdx] if type(h.xresolution()) is list else h.xresolution()
        yres = h.yresolution()[etBinIdx][etaBinIdx] if type(h.yresolution()) is list else h.yresolution()


        # Retreive the reference for the pileup selected region
        sgn_eff, sgn_passed, sgn_total  = target.reference( self.getStoreGateSvc(), basepath, etBinIdx, etaBinIdx, h.ymin(), h.ymax() )
        bkg_eff, bkg_passed, bkg_total  = target.reference( self.getStoreGateSvc(), basepath, etBinIdx, etaBinIdx, h.ymin(), h.ymax(), True )
        #sgn_counters   = {'eff':sgn_eff,'passed':sgn_passed,'total':sgn_total}
        #bkg_counters   = {'eff':bkg_eff,'passed':bkg_passed,'total':bkg_total}




        csummary, objects = ApplyThresholdLinearCorrection( h.xmin(),h.xmax(),xres,h.ymin(),h.ymax(),yres,
                                                            sgn_hist2D, bkg_hist2D, sgn_eff,
                                                            doLinearCorrection=doLinearCorrection, logger=self._logger)


        sgn_counters   = {'eff':sgn_eff,'passed':int( sgn_eff *csummary['signal_values']['total']),'total': csummary['signal_values']['total']}
        bkg_counters   = {'eff':bkg_eff,'passed':int( bkg_eff *csummary['background_values']['total']),'total': csummary['background_values']['total']}

        # helper function to increase the counter
        def UpdateCounters(obj1,obj2):
          for key in ['total','passed']: obj1[key]+=obj2[key]
          obj1['eff']=obj1['passed']/float(obj1['total'])

        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_corr_values']     = csummary['signal_corr_values']
        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_corr_values'] = csummary['background_corr_values']
        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['signal_reference']       = sgn_counters
        summary[target.name()]['summary_values'][etBinIdx][etaBinIdx]['background_reference']   = bkg_counters
        UpdateCounters( summary[target.name()]['signal_values']         , csummary['signal_values']    )
        UpdateCounters( summary[target.name()]['signal_corr_values']    , csummary['signal_corr_values']    )
        UpdateCounters( summary[target.name()]['background_values']     , csummary['background_values'])
        UpdateCounters( summary[target.name()]['background_corr_values'], csummary['background_corr_values'])
        UpdateCounters( summary[target.name()]['signal_reference']      , sgn_counters                      )
        UpdateCounters( summary[target.name()]['background_reference']  , bkg_counters                      )


        # Plot signal efficicency w.r.t the pileup
        outname = localpath+'/eff_signal_corr_'+target.name()+'_'+binningname
        plotname = PlotEff( self.__histConfig, objects['signal_hists']['eff'], objects['signal_corr_hists']['eff'],
                           sgn_eff, outname, runLabel=None,  etBinIdx=etBinIdx, etaBinIdx=etaBinIdx, etBins=etBins,
                           etaBins=etaBins, xlabel='<#mu>' )
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['signal_corr_eff'] = plotname

        # Plot background efficicency w.r.t the pileup
        outname = localpath+'/eff_background_corr_'+target.name()+'_'+binningname
        plotname = PlotEff( self.__histConfig, objects['background_hists']['eff'], objects['background_corr_hists']['eff'],
                           sgn_eff, outname, runLabel=None,  etBinIdx=etBinIdx, etaBinIdx=etaBinIdx, etBins=etBins,
                           etaBins=etaBins, xlabel='<#mu>' )
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['background_corr_eff'] = plotname


        outname = localpath+'/hist2D_signal_corr_'+target.name()+'_'+binningname
        plotname = Plot2DHist( self.__histConfig, objects['signal_corr_hists']['hist2D'], objects['correction']['angular'], objects['correction']['offset'],
                               objects['correction']['discr_points'], objects['correction']['nvtx_points'], objects['correction']['error_points'], outname,
                               xlabel='<#mu>' ,
                               etBinIdx=etBinIdx, etaBinIdx=etaBinIdx, etBins=etBins, etaBins=etaBins)
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['hist2D_signal_corr'] = plotname


        outname = localpath+'/hist2D_background_corr_'+target.name()+'_'+binningname
        plotname = Plot2DHist( self.__histConfig, objects['background_corr_hists']['hist2D'], objects['correction']['angular'], objects['correction']['offset'],
                               objects['correction']['discr_points'], objects['correction']['nvtx_points'], objects['correction']['error_points'], outname,
                               xlabel= '<#mu>',
                               etBinIdx=etBinIdx, etaBinIdx=etaBinIdx, etBins=etBins, etaBins=etaBins)
        summary[target.name()]['plotnames'][etBinIdx][etaBinIdx]['hist2D_background_corr'] = plotname


        etbin   = (etBins[etBinIdx]   , etBins[etBinIdx+1]  )
        etabin  = (etaBins[etaBinIdx] , etaBins[etaBinIdx+1])
        muBin   = (0,200) # this should be used in config for future
        obj=objects['correction']
        summary[target.name()]['thresholds'].append( {
                                                        'etBin'     : np.array(etbin),
                                                        'etaBin'    : np.array(etabin),
                                                        'muBin'     : np.array(muBin),
                                                        'etBinIdx'  : etBinIdx,
                                                        'etaBinIdx' : etaBinIdx,
                                                        'threshold' : (obj['angular'],obj['offset'], obj['offset0'])
                                                     } ) # angular, offset, threshold_no_correction


    return summary





