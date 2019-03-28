

from prometheus.drawers.functions.TAxisFunctions          import *
from prometheus.drawers.functions.PlotFunctions           import *
from prometheus.drawers.functions.PlotHelper              import *
from prometheus.tools.atlas.common.constants  import *
from ROOT                                     import TH1,TH1F, TH2F, TProfile,TCanvas, TFile, TPad
from ROOT                                     import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow
import numpy as np
import math, ROOT
import os

from ROOT import gStyle
#gStyle.SetOptStat(1)

drawopt='hist'
divide=''

def SetBoxes(pad, hists):
  pad.Modified();
  x_begin = 1.
  x_size = .18
  x_dist = .03;
  histStatsList=[]
  from ROOT import TPaveStats
  for hist in hists:
    histStats = hist.GetListOfFunctions().FindObject("stats")
    histStats.__class__=TPaveStats
    histStats.SetX1NDC(x_begin-x_dist); histStats.SetX2NDC(x_begin-x_size-x_dist);
    histStats.SetTextColor(hist.GetLineColor())
    histStatsList.append(histStats)
    x_begin-=x_dist+x_size;
  return histStatsList
 


from ROOT import TLatex, gPad

def ATLASLabel(x,y,text,color=1):
  l = TLatex()
  l.SetNDC();
  l.SetTextFont(72);
  l.SetTextColor(color);
  delx = 0.115*696*gPad.GetWh()/(472*gPad.GetWw());
  l.DrawLatex(x,y,"ATLAS");
  if True:
    p = TLatex(); 
    p.SetNDC();
    p.SetTextFont(42);
    p.SetTextColor(color);
    p.DrawLatex(x+delx,y,text);
    #p.DrawLatex(x,y,"#sqrt{s}=900GeV");

def ATLASLumiLabel(x,y,lumi=None,color=1):   
    l = TLatex()
    l.SetNDC();
    l.SetTextFont(42);
    l.SetTextSize(0.045);
    l.SetTextColor(color);
    dely = 0.115*472*gPad.GetWh()/(506*gPad.GetWw());
    label="#sqrt{s}=13 TeV"
    if lumi is not None: label += ", #intL dt = " + lumi + " fb^{-1}"
    l.DrawLatex(x,y-dely,label);


def setLegend1(leg):
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.032)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.Draw()


def AtlasTemplate( canvas, **kw ):
  #ATLASLabel(0.2,0.85,'Preliminary')
  ATLASLabel(0.2,0.85,'Internal')
  #ATLASLumiLabel(0.2,0.845)
  canvas.Modified()
  canvas.Update()


def AddTopLabels(can, legend, extra=None,textsize=10):

  from prometheus.drawers.functions.PlotFunctions import GetAtlasInternalText, GetSqrtsText, DrawText, MakeLegend
  text_lines = []
  text_lines += [GetAtlasInternalText()]
  text_lines.append( GetSqrtsText(13) )
  if extra:
    text_lines.append(extra)
  MakeLegend(can,.73,.68,.89,.93,option='p',textsize=textsize, names=legend, ncolumns=1, squarebox=False, doFixLength=False)
  DrawText(can,text_lines,.40,.68,.70,.93,totalentries=4)


f_ringer    = TFile("expert-monitoring-ringer.root",'r')
f_noringer  = TFile("expert-monitoring-noringer.root",'r')


def plot_fex_totaltime():

  h1 = TH1F(); h2 = TH1F(); h3 = TH1F()
  outcan = TCanvas( 'canvas', "", 700, 500 ) 
  f_noringer.GetObject("T2CaloEgamma_eGamma/Execute_Time", h1)
  f_ringer.GetObject("T2CaloEgamma_Ringer/Execute_Time", h2)
  f_ringer.GetObject("T2CaloEgamma_Ringer/RingerFex_Execute_Time", h3)
  outcan.cd()
  h1.SetLineColor(kAzure-5)
  h1.SetFillColor(kAzure-4)
  h1.SetMarkerColor(kAzure-4)
  h2.SetLineColor(kBlack)
  AddHistogram(outcan,h1,drawopt=drawopt) 
  AddHistogram(outcan,h2,drawopt=drawopt) 
  h1.SetStats(False)
  h2.SetStats(False)
  AtlasTemplate(outcan)
  
  bot = TPad("pad_bot", "This is the bottom pad",0.5,0.2,0.93,0.7)
  bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
  bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
  bot.SetRightMargin (0.05)
  bot.SetLeftMargin  (0.16)
  bot.SetFillColor(0)
  bot.Draw(drawopt)
  bot.cd()
  h3.SetAxisRange(0., 2.5,"X")
  h3.SetLineColor(kBlack)
  h3.SetLineWidth(1)
  h3.SetFillColor(16)
  h3.Draw()
  
  #DrawText(bot,['Ringer Extraction', 'Mean = %1.4f'%h3.GetMean(), 'Std  = %1.4f'%h3.GetStdDev()],.40,.68,.70,.93,totalentries=4)
  DrawText(bot,['Ringer Extraction Only', 'Time: %1.2f#pm%1.2f ms'%(h3.GetMean(),h3.GetStdDev())],.40,.68,.70,.93,totalentries=4)
  #bot.Update()
  #outcan.Update()
  AddHistogram(bot,h3,drawopt=drawopt) 
  #stat = SetBoxes(bot,[h3])
  AutoFixAxes(bot,ignoreErrors=False)
  FormatCanvasAxes(bot, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  FixYaxisRanges(bot, ignoreErrors=True, yminc=-eps )
  
  
  MakeLegend(outcan,.5,.77,.89,.97,option='p',textsize=14, names=['Without Ringer (FastCalo extraction)','With Ringer (FastCalo extraction)'], ncolumns=1, 
             squarebox=False, doFixLength=False)
  
  AutoFixAxes(outcan,ignoreErrors=False)
  FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  SetAxisLabels(outcan,"[ms]",'Count')
  FixYaxisRanges(outcan, ignoreErrors=True, yminc=-eps )
  #AddBinLines(outcan,h1,useCanvasHistsMax=False,useHistMax=False)
  outcan.SaveAs("EgammaFex_TotalTime.pdf")




def plot_fex_samp2time():

  h1 = TH1F(); h2 = TH1F(); h3 = TH1F()
  outcan = TCanvas( 'canvas', "", 700, 500 ) 
  f_noringer.GetObject("T2CaloEgamma_eGamma/Execute_Time", h1)
  f_noringer.GetObject("T2CaloEgamma_eGamma/ESamp2Total_Time", h2)
  outcan.cd()
  h1.SetLineColor(kAzure-5)
  h1.SetFillColor(kAzure-4)
  h1.SetMarkerColor(kAzure-4)
  #h2.SetLineColor(kBlack)
  AddHistogram(outcan,h1,drawopt=drawopt) 
  #AddHistogram(outcan,h2,drawopt=drawopt) 
  h1.SetStats(False)
  #h2.SetStats(False)
  AtlasTemplate(outcan)
  
  bot = TPad("pad_bot", "This is the bottom pad",0.5,0.2,0.93,0.7)
  bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
  bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
  bot.SetRightMargin (0.05)
  bot.SetLeftMargin  (0.16)
  bot.SetFillColor(0)
  bot.Draw(drawopt)
  bot.cd()
  #h2.SetAxisRange(0., 2.5,"X")
  h2.SetLineColor(kBlack)
  h2.SetLineWidth(1)
  h2.SetFillColor(16)
  h2.Draw()
  
  #DrawText(bot,['Ringer Extraction', 'Mean = %1.4f'%h3.GetMean(), 'Std  = %1.4f'%h3.GetStdDev()],.40,.68,.70,.93,totalentries=4)
  DrawText(bot,['EgammaSampl2 Only'],.20,.70,.60,.95,totalentries=4)
  #bot.Update()
  #outcan.Update()
  AddHistogram(bot,h2,drawopt=drawopt) 
  #stat = SetBoxes(bot,[h3])
  AutoFixAxes(bot,ignoreErrors=False)
  FormatCanvasAxes(bot, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  FixYaxisRanges(bot, ignoreErrors=True, yminc=-eps )
 
  FormatCanvasAxes(bot, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  FixYaxisRanges(bot, ignoreErrors=True, yminc=-eps )
  
  MakeLegend(outcan,.50,.77,.89,.97,option='p',textsize=14, names=['Without Ringer (FastCalo extraction)'], ncolumns=1, 
             squarebox=False, doFixLength=False)
 
  
  AutoFixAxes(outcan,ignoreErrors=False)
  FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  SetAxisLabels(outcan,"[ms]",'Count')
  FixYaxisRanges(outcan, ignoreErrors=True, yminc=-eps )
  #AddBinLines(outcan,h1,useCanvasHistsMax=False,useHistMax=False)
  outcan.SaveAs("EgammaFex_Samp2Time.pdf")




def plot_hypo_totaltime():

  h1 = TH1F(); h2 = TH1F(); h_noringer = TH1F()
  outcan = TCanvas( 'canvas', "", 700, 500 ) 

  f_ringer.GetObject("TrigL2CaloRingerHypo_e17_lhloose/Execute_Time", h1)
  #f_ringer.GetObject("TrigL2CaloRingerHypo_e17_lhloose/Execute_Time", h2)
  f_ringer.GetObject("TrigL2CaloRingerFex_e17_lhloose/Execute_Time", h2)
  #f_ringer.GetObject("TrigL2CaloRingerFex_e17_lhloose/Execute_Time", h3)
  
  # make shift
  offset = h1.FindBin( h1.GetMean() )
  offset = h2.FindBin(offset*h1.GetXaxis().GetXmax()/float(h1.GetNbinsX()))
  h_shift = TH1F('','', h2.GetNbinsX(), 0, h2.GetXaxis().GetXmax())
  for bin in xrange(h2.GetNbinsX()):
    h_shift.SetBinContent( bin+offset, h2.GetBinContent(bin) )
  h_ringer = h_shift

  f_noringer.GetObject("TrigL2CaloHypo_e17_lhloose/Execute_Time", h_noringer)
  

  #h_noringer.RebinX(5)
  #h2.RebinX(2)
  outcan.cd()
  h_noringer.SetLineColor(kAzure-5)
  h_noringer.SetFillColor(kAzure-4)
  h_noringer.SetMarkerColor(kAzure-4)
  h_ringer.SetLineColor(kBlack)

  h_ringer.SetAxisRange(0,0.15,'X')
  h_noringer.SetAxisRange(0,0.15,'X')
  h_noringer.Rebin(2)
  AddHistogram(outcan,h_ringer,drawopt=drawopt) 
  AddHistogram(outcan,h_noringer,drawopt=drawopt) 

  AtlasTemplate(outcan)
  MakeLegend(outcan,.50,.77,.89,.97,option='p',textsize=14, names=['With Ringer (FastCalo Decision)',
    'Without Ringer (FastCalo Decision)'], ncolumns=1, 
             squarebox=False, doFixLength=False)
 
  
  AutoFixAxes(outcan,ignoreErrors=False)
  FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  SetAxisLabels(outcan,"[ms]",'Count')
  FixYaxisRanges(outcan, ignoreErrors=True, yminc=-eps )
  
  
  
  
  #bot = TPad("pad_bot", "This is the bottom pad",0.5,0.2,0.93,0.7)
  #bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
  #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
  #bot.SetRightMargin (0.05)
  #bot.SetLeftMargin  (0.16)
  #bot.SetFillColor(0)
  #bot.Draw(drawopt)
  #bot.cd()

  ##h3.SetLineColor(15)
  ##h3.SetLineWidth(1)
  ##h3.SetFillColor(16)
  ##h3.Draw()
  #
  #h4 = TH1F(); h5 = TH1F(); h6 = TH1F()
  #f_ringer.GetObject("TrigL2CaloRingerFex_e17_lhloose/Normalization_Time", h4)
  #f_ringer.GetObject("TrigL2CaloRingerFex_e17_lhloose/Propagation_Time", h5)
  #f_ringer.GetObject("TrigL2CaloRingerFex_e17_lhloose/StoreOutput_Time", h6)
  ##DrawText(bot,['Ringer Extraction', 'Mean = %1.4f'%h3.GetMean(), 'Std  = %1.4f'%h3.GetStdDev()],.40,.68,.70,.93,totalentries=4)



  #h4.RebinX(2)
  #h5.RebinX(2)
  #h4.SetAxisRange(0., 0.01,"X")
  #h5.SetAxisRange(0., 0.01,"X")
  ##AddHistogram(bot,h6,drawopt=drawopt) 
  #h6.SetLineColor(16)
  #h6.SetFillColor(15)
  #h6.SetMarkerColor(16)
  #h5.SetLineColor(kBlack)
  #h5.SetMarkerColor(kBlack)
  #h4.SetMarkerColor(kRed)
  #AddHistogram(bot,h4,drawopt=drawopt) 
  #AddHistogram(bot,h5,drawopt=drawopt) 
  ##AddHistogram(bot,h6,drawopt=drawopt) 
  #DrawText(bot,['Ringer Hypothesis Steps', 
  #              'Norm. Time: %1.3f#pm%1.3f ms'%(h4.GetMean(),h4.GetStdDev()),
  #              'Prop. Time: %1.3f#pm%1.3f ms'%(h5.GetMean(),h5.GetStdDev()),
  #              #'Store Time: See distribution',
  #              #'Decision Time: %1.4f#pm%1.4f ms'%(h1.GetMean(),h1.GetStdDev()),
  #              ],.30,.68,.70,.93,totalentries=4)


  ##stat = SetBoxes(bot,[h3])
  #AutoFixAxes(bot,ignoreErrors=False)
  #FormatCanvasAxes(bot, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  #FixYaxisRanges(bot, ignoreErrors=True, yminc=-eps )
 
  
  
  
  
  
  
  #AddBinLines(outcan,h1,useCanvasHistsMax=False,useHistMax=False)
  outcan.SaveAs("EgammaHypo_TotalTime.pdf")























plot_hypo_totaltime()
plot_fex_totaltime()
plot_fex_samp2time()





















