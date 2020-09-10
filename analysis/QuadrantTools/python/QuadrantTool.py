__all__ = ['QuadrantTool']


# core includes
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi import mkdir_p
from Gaugi import GeV
from Gaugi import progressbar
from Gaugi.tex.TexAPI       import *
from Gaugi.tex.BeamerAPI    import *
from Gaugi.monet.AtlasStyle import SetAtlasStyle

# tool includes
from PileupCorrectionTools.utilities import RetrieveBinningIdx
from ProfileTools.constants import *
from QuadrantTools.drawers import *
from ROOT import TH1F
from functools import reduce
from itertools import product
import os, gc, time, math
import numpy as np
from prometheus import Dataframe as DataframeEnum



#
# Analysis tool
#
class QuadrantTool( Algorithm ):

  # quadrant names definition
  __quadrants = [
                  'passed_passed',
                  'rejected_rejected',
                  'passed_rejected',
                  'rejected_passed',
                  ]

  #
  # Constructor
  #
  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name)

    # declare all properties with default values  
    self.declareProperty( "Basepath", "Event/QuadrantTool", "Quadrant base path histogram." )
    self.declareProperty( "EtBinningValues" , [], "Et bin selection for data selection." )
    self.declareProperty( "EtaBinningValues", [], "Et bin selection for data selection." )


    # Set all properties values from the contructor args
    for key, value in kw.items():
      self.setProperty( key, value )


    self.__quadrantFeatures = list()
   

  #
  # Add quadrant configuration
  #
  def add_quadrant( self, name_a, expression_a, name_b, expression_b):
    from . import QuadrantConfig
    self.__quadrantFeatures.append( QuadrantConfig(name_a,expression_a,name_b,expression_b) )


  #
  # Set et binning values 
  #
  def setEtBinningValues( self, etbins ):
    self.setProperty( "EtBinningValues", etbins )
 
  #
  # Set eta binning values
  #
  def setEtaBinningValues( self, etabins ):
    self.setProperty( "EtaBinningValues", etabins )


  #
  # Initialize method
  #
  def initialize(self):
    
    Algorithm.initialize(self)
    sg = self.getStoreGateSvc()

    basepath = self.getProperty("Basepath")
    etBins = self.getProperty( "EtBinningValues" )
    etaBins = self.getProperty( "EtaBinningValues" )

    etabins = default_etabins

    for feat in self.__quadrantFeatures:
      # hold quadrant name
      quadrant_name = feat.name_a()+'_Vs_'+feat.name_b()

      ### loopover ets...
      for etBinIdx in range(len(etBins)-1):
        ### loop over etas...
        for etaBinIdx in range(len(etaBins)-1):
          ### loop over quadrants...
          for quadrant in self.__quadrants:  
            # hold binning name
            binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)


            dirname = basepath+'/'+quadrant_name+'/'+binning_name+'/'+quadrant
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



  #
  # Execute method
  #
  def execute(self, context):
    

    basepath = self.getProperty("Basepath")
    etBins = self.getProperty( "EtBinningValues" )
    etaBins = self.getProperty( "EtaBinningValues" )


    # Retrieve container
    if self._dataframe is DataframeEnum.Electron_v1:
      eg    = context.getHandler( "ElectronContainer" )
    elif self._dataframe is DataframeEnum.Photon_v1:
      eg    = context.getHandler( "PhotonContainer" )
    else:
      eg    = context.getHandler( "ElectronContainer" )
    
    evt = context.getHandler( "EventInfoContainer" )
    eta = math.fabs(eg.eta())
    et = eg.et()/GeV
    if self._dataframe is DataframeEnum.Electron_v1:
      track = eg.trackParticle()
    elif self._dataframe is DataframeEnum.Photon_v1:
      track = False
    
    dec = context.getHandler( "MenuContainer" )

    evt = context.getHandler("EventInfoContainer")
    pw = evt.MCPileupWeight()
    sg = self.getStoreGateSvc()

    if et < etBins[0]:
      return StatusCode.SUCCESS
    if eta > 2.47:
      return StatusCode.SUCCESS

    etBinIdx, etaBinIdx = RetrieveBinningIdx(et,eta,etBins, etaBins, logger=self._logger )
    
    if etBinIdx==-1 and etaBinIdx==-1:
      return StatusCode.SUCCESS
    
    binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)

    for feat in self.__quadrantFeatures:
      
      name     = feat.name_a()+'_Vs_'+feat.name_b()
      passed_x = bool(dec.accept( feat.expression_a() ))
      passed_y = bool(dec.accept( feat.expression_b() ))
      passed_x = 'passed' if passed_x else 'rejected'
      passed_y = 'passed' if passed_y else 'rejected'
      dirname  = basepath+'/'+name+'/'+binning_name+'/'+passed_x +'_'+ passed_y

      pw=1
      # Fill basic infos
      sg.histogram(dirname+'/et').Fill(et,pw)
      sg.histogram(dirname+'/eta').Fill(eg.eta(),pw)
      sg.histogram(dirname+'/phi').Fill(eg.phi(),pw)
      sg.histogram(dirname+'/avgmu').Fill(evt.avgmu(),pw)
      sg.histogram(dirname+'/nvtx').Fill(evt.nvtx(),pw)
      # Fill shower shapes
      sg.histogram(dirname+'/f1').Fill(eg.f1(),pw)
      sg.histogram(dirname+'/f3').Fill(eg.f3(),pw)
      sg.histogram(dirname+'/weta2').Fill(eg.weta2(),pw)
      sg.histogram(dirname+'/wtots1').Fill(eg.wtots1(),pw)
      sg.histogram(dirname+'/reta').Fill(eg.reta(),pw)
      sg.histogram(dirname+'/rhad').Fill(eg.rhad(),pw)
      sg.histogram(dirname+'/rphi').Fill(eg.rphi(),pw)
      sg.histogram(dirname+'/eratio').Fill(eg.eratio(),pw)
      if self._dataframe is DataframeEnum.Electron_v1:
        sg.histogram(dirname+'/deltaEta1').Fill(eg.deltaEta1(),pw)
        sg.histogram(dirname+'/deltaPhiRescaled2').Fill(eg.deltaPhiRescaled2(),pw)
      # Fill track variables
      if track:
        sg.histogram(dirname+'/trackd0pvunbiased').Fill(track.d0(),pw)
        sg.histogram(dirname+'/d0significance').Fill(track.d0significance(),pw)
        sg.histogram(dirname+'/eProbabilityHT').Fill(track.eProbabilityHT(),pw)
        sg.histogram(dirname+'/TRT_PID').Fill(track.trans_TRT_PID(),pw)
        sg.histogram(dirname+'/DeltaPOverP').Fill(track.DeltaPOverP(),pw)
     

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
  def plot(self, dirnames, pdfoutputs, pdftitles, runLabel='' ,doPDF=True, legends=None):
    
    legends = [ 'Both Approved','Ringer Rejected', 'Ringer Approved', 'Both Rejected' ] if legends is None else legends

    SetAtlasStyle()
    beamer_plots = {}
    global tobject_collector

    basepath = self.getProperty("Basepath")
    etBins = self.getProperty( "EtBinningValues" )
    etaBins = self.getProperty( "EtaBinningValues" )


    sg = self.getStoreGateSvc()

    for idx, feat in enumerate(self.__quadrantFeatures):
      
      dirname = os.getcwd()+'/'+dirnames[idx]
      mkdir_p(dirname)
      # hold quadrant name
      quadrant_name = feat.name_a()+'_Vs_'+feat.name_b()
      # For beamer... 
      if not quadrant_name in beamer_plots.keys():
        beamer_plots[quadrant_name]={}
        beamer_plots[quadrant_name]['integrated']={}

      ### Plot binning plots  
      if (len(etBins) * len(etaBins)) > 1:
        for etBinIdx, etaBinIdx in progressbar(product(range(len(etBins)-1),range(len(etaBins)-1)),
                                               (len(etBins)-1)*(len(etaBins)-1),
                                               prefix = "Plotting... ", logger=self._logger):
          # hold binning name
          binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          # for beamer...
          if not binning_name in beamer_plots[quadrant_name].keys():
            beamer_plots[quadrant_name][binning_name]={}
          
          ### loop over standard quantities
          for key in standardQuantitiesNBins.keys(): 
            outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
            out = PlotQuantities(sg, basepath+'/'+quadrant_name+'/'+binning_name, key, outname, legends, etBins=etBins, etaBins=etaBins,
                etidx=etBinIdx,etaidx=etaBinIdx,xlabel=electronQuantities[key],divide='b',runLabel=runLabel)
            beamer_plots[quadrant_name][binning_name][key] = out
            #del tobject_collector[:]
        
          ### loop over info quantities
          for key in basicInfoQuantities.keys():
            outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
            out = PlotQuantities(sg, basepath+'/'+quadrant_name+'/'+binning_name, key, outname, legends, etBins=etBins, etaBins=etaBins,
                etidx=etBinIdx,etaidx=etaBinIdx,xlabel=basicInfoQuantities[key],divide='b', runLabel=runLabel)
            beamer_plots[quadrant_name][binning_name][key] = out
            #del tobject_collector[:]

          
          beamer_plots[quadrant_name][binning_name]['statistics'] = GetStatistics(sg, basepath+'/'+quadrant_name+'/'+binning_name, \
                                                                                        'avgmu',etidx=etBinIdx,etaidx=etaBinIdx,
                                                                                        etBins=etBins, etaBins=etaBins)
      

      #### Plot integrated histograms
      ### loop over standard quantities
      for key in standardQuantitiesNBins.keys(): 
        outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key
        out = PlotQuantities(sg, basepath+'/'+quadrant_name, key, outname, legends, xlabel=electronQuantities[key],divide='b',runLabel=runLabel,
              addbinlines=True, etBins=etBins, etaBins=etaBins)
        beamer_plots[quadrant_name]['integrated'][key] = out
        tobject_collector = []
        gc.collect()
      ### loop over info quantities
      for key in basicInfoQuantities.keys():
        outname = dirname+'/'+quadrant_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
        out = PlotQuantities(sg, basepath+'/'+quadrant_name, key, outname, legends, xlabel=basicInfoQuantities[key],divide='b', runLabel=runLabel,
            addbinlines=True, etBins=etBins , etaBins=etaBins)
        beamer_plots[quadrant_name]['integrated'][key] = out
        tobject_collector = []
        gc.collect()
      
      beamer_plots[quadrant_name]['integrated']['statistics'] = GetStatistics(sg, basepath+'/'+quadrant_name, 'avgmu', etBins=etBins, etaBins=etaBins)




    if doPDF:
      ### Make Latex str et/eta labels
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


     
      for slideIdx, feat in enumerate(self.__quadrantFeatures):
        
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


              figures = []; binning_name_list=[];
              for etBinIdx, etaBinIdx in product(range(len(etBins)-1),range(len(etaBins)-1)):
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

            for etaBinIdx in range( len(etaBins)-1 ):
              str_values = []
              for etBinIdx in range( len(etBins)-1 ):
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






