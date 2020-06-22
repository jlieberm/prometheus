


from Gaugi.monet.PlotFunctions  import *
from Gaugi.monet.TAxisFunctions import *
from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,TCanvas
from ROOT import TCanvas, TH1F, TH2F
import numpy as np
import ROOT
from CommonTools import basicInfoNBins,basicInfoLowerEdges,basicInfoHighEdges,\
                        standardQuantitiesNBins,standardQuantitiesLowerEdges,\
                        standardQuantitiesHighEdges,electronQuantities,basicInfoQuantities
                                                                                   
from Gaugi.monet.AtlasStyle import SetAtlasStyle
SetAtlasStyle()



def histToUnitArea(hist, norm=""):
  integral = hist.Integral(norm) if norm is not None else 1
  if integral == 0 : integral = 1
  hist.Scale(1./integral);
  hist.SetMinimum(0)
  return hist


from collections import OrderedDict
layers = OrderedDict([ ('PS', 8),
                       ('EM1', 64),
                       ('EM2', 8),
                       ('EM3', 8),
                       ('HAD1', 4),
                       ('HAD2', 4),
                       ('HAD3', 4) ])

def ringParser(quantity):
  _, idx = quantity.split('_')
  idx = int(idx)
  cTotal = 0
  for key, nRings in layers.items():
    if idx < cTotal+nRings: break
    cTotal += nRings
  return 'Ring_{(%s,%d;%d)} [MeV]' % (key, idx-cTotal, idx)



def AddTopLabels(can,legend, legOpt = 'p', quantity_text = '', etlist = None
                     , etalist = None, etidx = None, etaidx = None, legTextSize=10
                     , runLabel = '', extraText1 = None, legendY1=.68, legendY2=.93
                     , maxLegLength = 19, logger=None):
    text_lines = []
    text_lines += [GetAtlasInternalText()]
    text_lines.append( GetSqrtsText(13) )
    if runLabel: text_lines.append( runLabel )
    if extraText1: text_lines.append( extraText1 )
    DrawText(can,text_lines,.40,.68,.70,.93,totalentries=4)
    from copy import copy
    _etlist = copy(etlist)
    _etalist = copy(etalist)
   
    if legend:
        MakeLegend( can,.73,legendY1,.89,legendY2,textsize=legTextSize
                  , names=legend, option = legOpt, squarebox=False
                  , totalentries=0, maxlength=maxLegLength )
    try:
        extraText = []
        if _etlist and etidx is not None:
            # add infinity in case of last et value too large
            if _etlist[-1]>9999:  _etlist[-1]='#infty'
            binEt = (str(_etlist[etidx]) + ' < E_{T} [GeV] < ' + str(_etlist[etidx+1]) if etidx+1 < len(_etlist) else
                                     'E_{T} > ' + str(_etlist[etidx]) + ' GeV')
            extraText.append(binEt)
        if quantity_text: 
            if not isinstance(quantity_text,(tuple,list)): quantity_text = [quantity_text]
            extraText += quantity_text
        if _etalist and etaidx is not None:
            binEta = (str(_etalist[etaidx]) + ' < #eta < ' + str(_etalist[etaidx+1]) if etaidx+1 < len(_etalist) else
                                        str(_etalist[etaidx]) + ' < #eta < 2.47')
            extraText.append(binEta)
        DrawText(can,extraText,.14,.68,.35,.93,totalentries=4)
    except NameError as e:
        if logger:
          logger.warning("Couldn't print test due to error: %s", e)
        pass





def PlotDistributions( histData, histMC, outname,  
    drawopt='hist', etidx=None, etaidx=None, etlist=None, etalist=None, normalize=True, 
    extra_legend=None, logger=None, xlabel=''):
  if normalize:
    histData = histToUnitArea(histData)
    histMC = histToUnitArea(histMC)


  outcan = TCanvas( 'canvas', "", 500, 500 ) 
  histData.SetMarkerColor(kBlack)
  #histData.SetMarkerSize(0.8)
  histData.SetLineColor(kBlack)
  histMC.SetLineColor(kAzure-4)
  histMC.SetMarkerColor(kAzure-4)
  #histMC.SetMarkerSize(0.8)
  histMC.SetFillColor(kAzure-4)
  
  AddHistogram(outcan,histMC,drawopt,False, None, None)
  AddHistogram(outcan,histData,'hist',False, None, None)

 

  legend = ['Simulation (mc15)', 'Collision (2016)']
  AddTopLabels(outcan, legend, runLabel=extra_legend, legOpt='pb',
                 logger=logger,etlist=etlist,etalist=etalist,etidx=etidx,etaidx=etaidx)

  FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  SetAxisLabels(outcan,xlabel,'counts/bin (norm by counts)')
  FixYaxisRanges(outcan, ignoreErrors=True, yminc=-eps )
  AutoFixAxes(outcan,ignoreErrors=True)
  #AddBinLines(outcan,histData,useCanvasHistsMax=False,useHistMax=False, maxvalue=1.0 if normalize else None)
  outcan.SaveAs( outname ) 
  del outcan






from ROOT import TFile

datafile = '../phd_data/mc15_data16_comparison/data16_13TeV.EGAM1.probes_lhmedium.correction.root'
mcfile = '../phd_data/mc15_data16_comparison/mc15_13TeV.Zee.probes_lhmedium.correction.root'
mc_f   = TFile( mcfile,'r')
data_f = TFile( datafile,'r')
etbins = [15,20, 30, 40, 50, 100000]
etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]
#etabins = [0, 0.8, 1.37, 1.54, 2.5]
basepath = 'Event/PileupCorrection/probes/L2_Tight/T0HLTElectronRingerTight_v6' 

for etbinIdx in range(5):
  for etabinIdx in range(4):
    binningname = 'et%d_eta%d' % (etbinIdx,etabinIdx)
    h2_mc = TH2F(); h2_data = TH2F()
    mc_f.GetObject( basepath+'/'+binningname+'/discriminantVsMu', h2_mc)
    data_f.GetObject( basepath+'/'+binningname+'/discriminantVsMu', h2_data)
    h_mc = h2_mc.ProjectionX().Clone()
    h_data = h2_data.ProjectionX().Clone()
    h_mc.Rebin(100)    
    h_data.Rebin(100)    
    outname = 'discriminant_'+binningname+'.pdf'
    PlotDistributions(h_data, h_mc, outname, etidx=etbinIdx,etaidx=etabinIdx,etlist=etbins,etalist=etabins,
                      xlabel='Neural Network Output (Discriminant)')

 

datafile = '../phd_data/mc15_data16_comparison/data16_13TeV.EGAM1.probes_lhmedium.profiles.root'
mcfile = '../phd_data/mc15_data16_comparison/mc15_13TeV.Zee_probes.lhmedium.profiles.root'

mc_f2   = TFile( mcfile,'r')
data_f2 = TFile( datafile,'r')

for etbinIdx in range(5):
  for etabinIdx in range(5):
    binningname = 'et%d_eta%d' % (etbinIdx,etabinIdx)
    for key in standardQuantitiesNBins.keys():
      basepath = 'Profiles/StandardQuantities' 
      xlabel = electronQuantities[key]
      h1_mc = TH1F(); h1_data = TH1F()
      data_f2.GetObject( basepath+'/'+binningname+'/'+key+'_'+binningname, h1_data)
      mc_f2.GetObject( basepath+'/'+binningname+'/'+key+'_'+binningname, h1_mc)
      outname = key+'_'+binningname+'.pdf'
      PlotDistributions(h1_data, h1_mc, outname, etidx=etbinIdx,etaidx=etabinIdx,etlist=etbins,etalist=etabins,xlabel=xlabel)

    
    for ringIdx in range(100):
      quantity = 'ring_%d_et%d_eta%d'%(ringIdx,etbinIdx,etabinIdx)
      basepath = 'Profiles/RingProfiles' 
      key = 'ring_%d'%ringIdx
      xlabel = ringParser(key)
      h1_mc = TH1F(); h1_data = TH1F()
      data_f2.GetObject( basepath+'/'+binningname+'/'+key+'_'+binningname, h1_data)
      mc_f2.GetObject( basepath+'/'+binningname+'/'+key+'_'+binningname, h1_mc)
      outname = key+'_'+binningname+'.pdf'
      PlotDistributions(h1_data, h1_mc, outname, etidx=etbinIdx,etaidx=etabinIdx,etlist=etbins,etalist=etabins,xlabel=xlabel)


