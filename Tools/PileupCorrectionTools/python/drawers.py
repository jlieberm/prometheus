

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
    if legend:
        MakeLegend( can,.73,legendY1,.89,legendY2,textsize=legTextSize
                  , names=legend, option = legOpt, squarebox=False
                  , totalentries=0, maxlength=maxLegLength )
    try:
        from copy import copy
        extraText = []
        if etlist and etidx is not None:
            # add infinity in case of last et value too large
            etlist=copy(etlist)
            if etlist[-1]>9999:  etlist[-1]='#infty'
            binEt = (str(etlist[etidx]) + ' < E_{T} [GeV] < ' + str(etlist[etidx+1]) if etidx+1 < len(etlist) else
                                     'E_{T} > ' + str(etlist[etidx]) + ' GeV')
            extraText.append(binEt)
        if quantity_text:
            if not isinstance(quantity_text,(tuple,list)): quantity_text = [quantity_text]
            extraText += quantity_text
        if etalist and etaidx is not None:
            binEta = (str(etalist[etaidx]) + ' < #eta < ' + str(etalist[etaidx+1]) if etaidx+1 < len(etalist) else
                                        str(etalist[etaidx]) + ' < #eta < 2.47')
            extraText.append(binEta)
        DrawText(can,extraText,.14,.68,.35,.93,totalentries=4)
    except NameError, e:
        if logger:
          logger.warning("Couldn't print test due to error: %s", e)
        pass




def Plot2DLinearFit( hist2D, title, xname
                    , limits, graph
                    , label, eff_uncorr, eff
                    , etBin = None, etaBin = None ):
  import array as ar
  from ROOT import TCanvas, gStyle, TLegend, kRed, kBlue, kBlack, TLine, kBird, kOrange
  from ROOT import TGraphErrors, TF1, TColor
  pileup_max = hist2D.GetYaxis().GetXmax()
  pileup_min = hist2D.GetYaxis().GetXmin()
  # Retrieve some usefull information
  gStyle.SetPalette(kBird)
  canvas = TCanvas(title,title, 500, 500)
  #canvas3.SetTopMargin(0.10)
  canvas.SetRightMargin(0.12)
  canvas.SetLeftMargin(0.10)
  #canvas3.SetBottomMargin(0.11)
  FormatCanvasAxes(canvas, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  #hist2D.SetTitle('Neural Network output as a function o nvtx, '+partition_name)
  #hist2D.GetXaxis().SetTitle('Neural Network output (Discriminant)')
  #hist2D.GetYaxis().SetTitle(xname)
  #hist2D.GetZaxis().SetTitle('Counts')
  #if not useNoActivationFunctionInTheLastLayer: hist2D.SetAxisRange(-1,1, 'X' )
  hist2D.Draw('colz')
  (miny,maxy) = GetYaxisRanges(canvas,check_all=True,ignorezeros=True,ignoreErrors=True)
  canvas3.SetLogz()
  # Invert graph
  nvtx_points        = ar.array( 'd', graph.GetX(), )
  nvtx_error_points  = ar.array( 'd', graph.GetEX(),)
  discr_points       = ar.array( 'd', graph.GetY(), )
  discr_error_points = ar.array( 'd', graph.GetEY(),)
  g1 = TGraphErrors(len(discr_points), discr_points, nvtx_points, discr_error_points, nvtx_error_points)
  g1.SetLineWidth(1)
  g1.SetLineColor(kBlack)
  g1.SetMarkerColor(kBlack)
  g1.SetMarkerSize(.6)
  g1.Draw("P same")
  _g.append(g1)
  l2 = TLine(eff_uncorr.thres,miny,eff_uncorr.thres,maxy)
  l2.SetLineColor(kRed)
  l2.SetLineWidth(2)
  l2.Draw("l,same")
  _g.append(l2)
  f1 = eff.f1
  l3 = TLine(f1.Eval(miny), miny, f1.Eval(maxy), maxy)
  l3.SetLineColor(kBlack)
  l3.SetLineWidth(2)
  l3.Draw("l,same")
  _g.append(l3)
  SetAxisLabels(canvas,'Neural Network output (Discriminant)',xname,'Entries')
  t = DrawText(canvas3,[GetAtlasInternalText(), '', FixLength(label,16), '', GetSqrtsText()],.05,.70,.45,.9)
  t.SetTextAlign(12)
  t2 = DrawText(canvas,[ '#color[2]{%s}' % eff_uncorr.thresstr( 'Fixed Threshold' )
                   , '#color[2]{#varepsilon=%s}' % eff_uncorr.asstr(addname = False, addthres = False )
                   , ''
                   , eff.threstr( prefix = 'Correction' )
                   , '#varepsilon=%s' % eff.asstr(addname = False, addthres = False )
                   ]
          ,.45,.70,.45,.9,totalentries=5, textsize = 14 )
  t2.SetTextAlign(12)
  AutoFixAxes( canvas, ignoreErrors = True, limitXaxisToFilledBins = True, changeAllXAxis = True )
  return canvas



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



