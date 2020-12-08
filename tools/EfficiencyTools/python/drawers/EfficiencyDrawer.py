
__all__ = ["PlotProfiles"]

from Gaugi.monet.PlotFunctions import *
from Gaugi.monet.TAxisFunctions import *
from Gaugi.monet.AtlasStyle import SetAtlasStyle
from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite,TColor,gStyle

SetAtlasStyle()


local_these_colors = [kBlack,kBlue-4,kGray+2, kRed-2,kAzure+2,kGreen-2,kMagenta+1,kCyan+1,kOrange+1
                ,kBlack+2,kRed+3,kBlue+3,kGreen+3,kMagenta+3,kCyan+3,kOrange+3
                ,kGray,kRed-7,kBlue-7,kGreen-7,kMagenta-7,kCyan-7,kOrange-7
                ,kYellow+2,kRed-5,kBlue-5,kGreen-5,kMagenta-5,kCyan-5,kOrange-5
                ,21,22,23,24,25,26,27,28,29,30
                ,21,22,23,24,25,26,27,28,29,30
                ,21,22,23,24,25,26,27,28,29,30
                ]

local_these_transcolors=[TColor.GetColorTransparent(c,.5) for c in local_these_colors]
local_these_marker = (23, 24, 22, 26, 32 ,23, 20,25)




def AddTopLabels(can,legend, legOpt = 'p', quantity_text = '', legTextSize=15
                     , runLabel = '', extraText1 = None, legendY1=.68, legendY2=.93
                     , maxLegLength = 25, legendX1=0.75):
    text_lines = []
    text_lines += [GetAtlasInternalText(status='Internal')]
    #text_lines += [GetAtlasInternalText()]
    #text_lines.append( GetSqrtsText(13) )
    if runLabel: text_lines.append( runLabel )
    if extraText1:
      if type(extraText1) is str:
        extraText1=[extraText1]
      text_lines.extend( extraText1 )

    DrawText(can,text_lines,.15,.68,.47,.93,totalentries=4)
    if legend:
        MakeLegend( can,legendX1,legendY1,.98,legendY2,textsize=legTextSize
                  , names=legend, option = legOpt, squarebox=False
                  , totalentries=0, maxlength=maxLegLength )



def PlotProfiles( hists, legends=None, title=None, divide='B',drawopt='pE1', runLabel=None, outname=None,
                  doShadedProfile=None, theseColors=None,theseTransColors=None,theseMarker=None,
                  doRatioCanvas=True, extraText1=None, doFitting=False, formula='pol1',drawFitting=False,
                  legendX1=.65, xlabel=None, rlabel='Trigger/Ref.',ylabel='Trigger Efficiency',
                  SaveAsC=False):

  doRatio = True if (doRatioCanvas and (len(hists)>1)) else False
  these_colors = theseColors if theseColors else local_these_colors
  these_transcolors = theseTransColors if theseTransColors else local_these_transcolors
  these_marker = theseMarker if theseMarker else local_these_marker
  from ROOT import TCanvas
  outcan = RatioCanvas( 'canvas', "", 500, 500) if doRatio else TCanvas( 'canvas', "", 500, 500 )


  collect=[]
  res = {'fitting':[]}

  if doRatio:
    pad_top = outcan.GetPrimitive('pad_top')
    pad_bot = outcan.GetPrimitive('pad_bot')

  if doFitting:

    def Fitting(canvas,hist,drawopt,formula,color):
      canvas.cd()
      hist.Fit(formula,'q')
      #hist.Fit(formula)
      fitting = hist.GetFunction(formula)
      fitting.SetName('ShadedProfile') # Skip this object in setcolor
      c=ROOT.TColor.GetColorTransparent(color,.2)
      fitting.SetLineColor( c )
      fitting.Draw(drawopt)
      canvas.Modified()
      canvas.Update()
      return fitting

    for idx, hist in enumerate(hists):
      try:
        if doRatio: f=Fitting(pad_top,hist,'',formula,these_colors[idx])
        else:  f=Fitting(outcan,hist,'',formula,these_colors[idx])
      except:
        print ('Can not fit the linear test')
        f=None
      collect.append(f)
      res['fitting'].append(f)

  refHist = hists[0]
  for idx, hist in enumerate(hists):
    if doRatio:
      if idx < 1:
        AddHistogram(pad_top, refHist, drawopt = drawopt)
      else:
        h_hist=hist.Clone()
        h_hist.Divide(h_hist,refHist,1.,1.,'B')
        collect.append(h_hist)
        AddHistogram( pad_top, hist, drawopt, False, None, None)
        AddHistogram( pad_bot, h_hist, 'P', False, None, None)
    else:
      AddHistogram(outcan, hist, drawopt = drawopt)


  if doRatio:
    SetColors(pad_top,these_colors=these_colors)
    SetColors(pad_top,these_colors=these_transcolors, lineColor=False,markerColor=False,fillColor=True)
    SetColors(pad_bot,these_colors=these_transcolors[1::], lineColor=True,markerColor=False,fillColor=True)
    SetColors(pad_bot,these_colors=these_colors)
    SetMarkerStyles(pad_top, these_styles=these_marker)
    SetMarkerStyles(pad_bot, these_styles=these_marker[1::])
  else:
    SetColors(outcan,these_colors=these_colors)
    SetMarkerStyles(outcan, these_styles=these_marker)


  #pad_top.cd()
  if doRatio:
    SetColors(pad_top,these_colors=these_transcolors, lineColor=False,markerColor=False,fillColor=True)
    SetColors(pad_bot,these_colors=these_colors[1::], lineColor=True,markerColor=True,fillColor=False)
    #SetColors(pad_bot,these_colors=[kOrange-3], lineColor=False,markerColor=False,fillColor=True)
  else:
    SetColors(outcan,these_colors=these_transcolors, lineColor=False,markerColor=False,fillColor=True)



  AddTopLabels(outcan, legends, runLabel=runLabel, legOpt='p',extraText1=extraText1, legendX1=legendX1)
  FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  if not xlabel:  xlabel=refHist.GetXaxis().GetTitle()
  SetAxisLabels(outcan,xlabel,ylabel,rlabel)

  if doRatio:
    AddHorizontalLine(pad_bot,color=kBlack)
    FixYaxisRanges(pad_bot, ignoreErrors=False, yminc=-eps )
    AutoFixAxes(pad_top,ignoreErrors=False)
    #AddBinLines(pad_top,hists[0],useHistMax=True,horizotalLine=0.)
    #AddBinLines(pad_bot,hists[0],useHistMax=True,horizotalLine=0.)

  else:
    AutoFixAxes(outcan,ignoreErrors=False)
    #FixYaxisRanges(outcan, ignoreErrors=True, yminc=-eps )
    #AddBinLines(outcan,hists[0],useHistMax=True,horizotalLine=0.)
    #AddBinLines(outcan,hists[0],useHistMax=True,horizotalLine=0.)

  if outname:
    outcan.SaveAs( outname )
    if SaveAsC:
      outcan.SaveAs(outname.replace('.pdf','.C'))

  return res




