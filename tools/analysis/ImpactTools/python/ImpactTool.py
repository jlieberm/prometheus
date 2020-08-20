__all__ = ['ImpactTool']


# core includes
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi import mkdir_p
from Gaugi import GeV
from Gaugi import progressbar
from Gaugi.tex.TexAPI       import *
from Gaugi.tex.BeamerAPI    import *
from Gaugi.monet.AtlasStyle import SetAtlasStyle
from prometheus import Dataframe as DataframeEnum


# tool includes
from PileupCorrectionTools.utilities import RetrieveBinningIdx
from ProfileTools.constants import *
from ROOT import TH1F
from functools import reduce
from itertools import product
import os, gc, time, math
import numpy as np

from ImpactTools.drawers import *

#
# Analysis tool
#
class ImpactTool( Algorithm ):

  #
  # Constructor
  #
  def __init__(self, name, dataframe, **kw):
    
    Algorithm.__init__(self, name, selection_list_labels=None)

    # declare all properties with default values  
    self.declareProperty( "Basepath", "Event/ImpactTool", "Impact base path histogram." )
    self.declareProperty( "EtBinningValues" , [], "Et bin selection for data selection." )
    self.declareProperty( "EtaBinningValues", [], "Et bin selection for data selection." )


    # Set all properties values from the contructor args
    for key, value in kw.items():
      self.setProperty( key, value )

    if selection_list_labels is None:
      # default selection names definition
      __selections = [
                      'ringer',
                      'no_ringer',
                    ]
    else:
      __selections = selection_list_labels

    self.__selectionFeatures = list()
   

  #
  # Add selection configuration
  #
  def add_selection( self, name_a, expression_a, name_b, expression_b):

    self.__selectionFeatures.append( SelectionConfig(name_a, expression_a, name_b, expression_b) )


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

    for feat in self.__selectionFeatures:
      # hold selection name
      selection_name = feat.name_a()+'_VS_'+feat.name_b()

      ### loopover ets...
      for etBinIdx in range(len(etBins)-1):
        ### loop over etas...
        for etaBinIdx in range(len(etaBins)-1):
          ### loop over selections...
          for selection in self.__selections:  
            # hold binning name
            binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)


            dirname = basepath+'/'+selection_name+'/'+binning_name+'/'+selection
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

            # loop over selections

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
      elCont    = context.getHandler( "ElectronContainer" )
    elif self._dataframe is DataframeEnum.Photon_v1:
      elCont    = context.getHandler( "PhotonContainer" )
    else:
      elCont    = context.getHandler( "ElectronContainer" )
    
    evt = context.getHandler( "EventInfoContainer" )
    eta = math.fabs(el.eta())
    et = el.et()/GeV
    track = el.trackParticle()
    
    dec = context.getHandler( "MenuContainer" )

    evt = context.getHandler("EventInfoContainer")
    pw = evt.MCPileupWeight()
    sg = self.getStoreGateSvc()

    if et < etBins[0]:
      return StatusCode.SUCCESS
    if eta > 2.47:
      return StatusCode.SUCCESS

    etBinIdx, etaBinIdx = RetrieveBinningIdx(et,eta,etBins, etaBins, logger=self._logger )
    binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)

    for feat in self.__selectionFeatures:
      # create a list of histogram paths
      dir_list       = []
      selection_name = feat.name_a()+'_VS_'+feat.name_b()
      # check the decision for this expression
      passed_a       = bool(dec.accept( feat.expression_a() ))
      if passed_a: # check if passed for expression_a
        # if passed then append the path in dir_list
        dir_list.append(basepath+'/'+selection_name+'/'+binning_name+'/ringer')
      # now do the same for expression_b
      passed_b       = bool(dec.accept( feat.expression_b() ))
      if passed_b:
        dir_list.append(basepath+'/'+selection_name+'/'+binning_name+'/no_ringer')
      
      # now loop over the dir_list to fill all histograms
      for ipath in dir_list:
        # getting the path to fill.
        dirname  = ipath

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

  
  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  #
  # Standalone plot method
  #
  def plot(self, dirnames, pdfoutputs, pdftitles, runLabel='' ,doPDF=True):
    


    SetAtlasStyle()
    beamer_plots = {}
    global tobject_collector

    basepath = self.getProperty("Basepath")
    etBins = self.getProperty( "EtBinningValues" )
    etaBins = self.getProperty( "EtaBinningValues" )




    for idx, feat in enumerate(self.__selectionFeatures):
      
      dirname = os.getcwd()+'/'+dirnames[idx]
      mkdir_p(dirname)
      # hold selection name
      selection_name = feat.name_a()+'_Vs_'+feat.name_b()
      # For beamer... 
      if not selection_name in beamer_plots.keys():
        beamer_plots[selection_name]={}
        beamer_plots[selection_name]['integrated']={}

      ### Plot binning plots  
      if (len(etBins) * len(etaBins)) > 1:
        for etBinIdx, etaBinIdx in progressbar(product(range(len(etBins)-1),range(len(etaBins)-1)),
                                               (len(etBins)-1)*(len(etaBins)-1),
                                               prefix = "Plotting... ", logger=self._logger):
          # hold binning name
          binning_name = ('et%d_eta%d') % (etBinIdx,etaBinIdx)
          # for beamer...
          if not binning_name in beamer_plots[selection_name].keys():
            beamer_plots[selection_name][binning_name]={}
          
          ### loop over standard quantities
          for key in standardQuantitiesNBins.keys(): 
            outname = dirname+'/'+selection_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
            out = PlotQuantities(basepath+'/'+selection_name+'/'+binning_name, key, 
                outname,etidx=etBinIdx,etaidx=etaBinIdx,xlabel=electronQuantities[key],divide='b',runLabel=runLabel)
            beamer_plots[selection_name][binning_name][key] = out
            #del tobject_collector[:]
        
          ### loop over info quantities
          for key in basicInfoQuantities.keys():
            outname = dirname+'/'+selection_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
            out = PlotQuantities(basepath+'/'+selection_name+'/'+binning_name, key, 
                outname, etidx=etBinIdx,etaidx=etaBinIdx,xlabel=basicInfoQuantities[key],divide='b', runLabel=runLabel)
            beamer_plots[selection_name][binning_name][key] = out
            #del tobject_collector[:]

          
          beamer_plots[selection_name][binning_name]['statistics'] = GetStatistics(basepath+'/'+selection_name+'/'+binning_name, \
                                                                                        'avgmu',etidx=etBinIdx,etaidx=etaBinIdx)
      

      #### Plot integrated histograms
      ### loop over standard quantities
      for key in standardQuantitiesNBins.keys(): 
        outname = dirname+'/'+selection_name.replace('_Vs_','_')+'_'+ key
        out = PlotQuantities(basepath+'/'+selection_name, key, 
              outname,xlabel=electronQuantities[key],divide='b',runLabel=runLabel,
              addbinlines=True)
        beamer_plots[selection_name]['integrated'][key] = out
        tobject_collector = []
        gc.collect()
      ### loop over info quantities
      for key in basicInfoQuantities.keys():
        outname = dirname+'/'+selection_name.replace('_Vs_','_')+'_'+ key + '_' + binning_name
        out = PlotQuantities(basepath+'/'+selection_name, key, 
            outname,xlabel=basicInfoQuantities[key],divide='b', runLabel=runLabel,
            addbinlines=True)
        beamer_plots[selection_name]['integrated'][key] = out
        tobject_collector = []
        gc.collect()
      
      beamer_plots[selection_name]['integrated']['statistics'] = GetStatistics(basepath+'/'+selection_name, 'avgmu')




