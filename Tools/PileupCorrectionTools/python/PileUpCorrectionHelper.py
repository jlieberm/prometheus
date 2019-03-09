

from RingerCore import Logger, LoggingLevel, retrieve_kw, checkForUnusedVars, \
                       expandFolders, csvStr2List, progressbar
from ROOT       import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite
from prometheus.core                          import StatusCode
from prometheus.core                          import Dataframe
from prometheus.drawers.functions             import *
from prometheus.tools.atlas.common            import ATLASBaseTool
from prometheus.tools.atlas.common.constants  import *
from prometheus.drawers.functions.AtlasStyle      import *
from prometheus.drawers.functions.PlotFunctions   import *
from prometheus.drawers.functions.TAxisFunctions  import *

from array                                    import array
import time,os,math,sys,pprint,glob
import warnings
import ROOT
import numpy as np
import array


_g = []

#def switchaxis(th2):
#  c = type(th2)
#  f = lambda a: array.array('d',[a.GetBinLowEdge(x) for x in range(a.GetNbins())] + [a.GetBinUpEdge(a.GetNbins())])
#  th2_ret = c( th2.GetName(), th2.GetTitle(), th2.GetNbinsY(), f(th2.GetYaxis())
#             , th2.GetNbinsX(), f(th2.GetXaxis()) )
#  from itertools import product
#  for x, y in product(xrange(th2_ret.GetNbinsX()+2), xrange(th2_ret.GetNbinsY()+2)):
#    th2_ret.SetBinContent(x,y,th2.GetBinContent(y,x))
#  _g.append(th2_ret)
#  return th2_ret



def rebinY(th2, newbinning):
  c = type(th2)
  #old = list(th2.ProjectionX())
  #oldY = list(th2.ProjectionY())
  #print len(old), len(oldY)
  #print list(th2.ProjectionY())
  f = lambda a: array.array('d',[a.GetBinLowEdge(x) for x in range(1,a.GetNbins()+1)] + [a.GetBinUpEdge(a.GetNbins())])
  #print len(newbinning)
  th2_ret = c( th2.GetName(), th2.GetTitle(), th2.GetNbinsX(), f(th2.GetXaxis())
             , len(newbinning)-1, array.array('d',newbinning) )
  from itertools import product
  for x, y in product(xrange(th2.GetNbinsX()+2), xrange(th2.GetNbinsY()+2)):
    #print th2.GetXaxis().GetBinCenter(x), (th2.GetYaxis().GetBinLowEdge(y)+th2.GetYaxis().GetBinLowEdge(y+1))/2.
    th2_ret_idx = th2_ret.FindBin(th2.GetXaxis().GetBinCenter(x),(th2.GetYaxis().GetBinLowEdge(y)+th2.GetYaxis().GetBinLowEdge(y+1))/2.)
    th2_ret_x_idx = ROOT.Long(0); th2_ret_y_idx = ROOT.Long(0); dummy = ROOT.Long(0);
    th2_ret.GetBinXYZ (th2_ret_idx, th2_ret_x_idx, th2_ret_y_idx, dummy)
    #print th2_ret.GetXaxis().GetBinCenter(th2_ret_x_idx), th2_ret.GetYaxis().GetBinCenter(th2_ret_y_idx)
    c = th2_ret.GetBinContent(th2_ret_x_idx, th2_ret_y_idx)
    cAdd = th2.GetBinContent(x,y)
    th2_ret.SetBinContent(th2_ret_x_idx, th2_ret_y_idx,c+cAdd)
  #new = list(th2_ret.ProjectionX())
  #newY = list(th2_ret.ProjectionY())
  #print np.array(new)-np.array(old)
  #print sum(np.array(new)-np.array(old))
  #print np.array(newY),np.array(oldY)
  #print len(new), len(newY)

  #print list(th2.ProjectionY())
  _g.append(th2_ret)
  return th2_ret


def Copy2DRegion(hist, xbins, xmin, xmax, ybins, ymin, ymax):


  from ROOT import TH2F
  #hist.Draw()
  h = TH2F(hist.GetName()+'_region',hist.GetTitle(),xbins,xmin,xmax,ybins,ymin,ymax)
  yhighidx = hist.GetYaxis().FindBin(ymax)
  ylowidx = hist.GetYaxis().FindBin(ymin) - 1
  yhighidx = min(hist.GetNbinsY(),yhighidx)
  
  xhighidx = hist.GetXaxis().FindBin(xmax)
  xlowidx = hist.GetXaxis().FindBin(xmin) - 1
  xhighidx = min(hist.GetNbinsX(),xhighidx)
 
  tot=0; passed=0; M=0; c=None
  # Keep track of outliers or not
  x = 0 if xlowidx == 0 else 1
  #for x, bx in enumerate(xrange(int(xlowidx),int(xhighidx))):
  for bx in xrange(int(xlowidx),int(xhighidx)):
    #x+=1
    y = 1
    for by in xrange(int(ylowidx),int(yhighidx)) :
      value = hist.GetBinContent(bx,by)
      #print '->',value, ' (',bx,',',by,')'
      tot+=value
      h.SetBinContent(x,y,value)
      if value>M:
        M=value;
        c=(x,y)
      passed+=h.GetBinContent(x,y)
      y+= 1
    x+=1

  return h.Clone()


def CalculateMaxSP( hist_sgn, hist_bkg ):

  from RingerCore import calcSP
  nbinsx = hist_sgn.GetNbinsX()
  maxSP=0.0; best_det=0.0; best_fa=0.0
  for bx in xrange(nbinsx):
    det = hist_sgn.Integral( bx, nbinsx+1 ) / float(hist_sgn.GetEntries())
    fa  = hist_bkg.Integral( bx, nbinsx+1 ) / float(hist_bkg.GetEntries())
    sp = calcSP(det,1-fa)
    if sp > maxSP:
      maxSP=sp; best_det=det; best_fa=fa
  return best_det,best_fa,maxSP



def FindThreshold(hist,effref):
  nbins = hist.GetNbinsX()
  fullArea = hist.Integral(0,nbins+1)
  if fullArea == 0:
    return 0,1
  notDetected = 0.0; i = 0
  while 1. - notDetected > effref:
    cutArea = hist.Integral(0,i)
    i+=1
    prevNotDetected = notDetected
    notDetected = cutArea/fullArea
  eff = 1. - notDetected
  prevEff = 1. -prevNotDetected
  deltaEff = (eff - prevEff)
  threshold = hist.GetBinCenter(i-1)+(effref-prevEff)/deltaEff*(hist.GetBinCenter(i)-hist.GetBinCenter(i-1))
  #threshold = hist.GetBinCenter(i)
  #error = math.sqrt(abs(threshold)*(1-abs(threshold))/fullArea)
  #error = eff/math.sqrt(fullArea)
  error = 1./math.sqrt(fullArea)
  return threshold, error


def CalculateDependentDiscrPoints( hist2D , effref):
  nbinsy = hist2D.GetNbinsY()
  x = list(); y = list(); errors = list()
  for by in xrange(nbinsy):
    xproj = hist2D.ProjectionX('xproj'+str(time.time()),by+1,by+1)
    discr, error = FindThreshold(xproj,effref)
    dbin = xproj.FindBin(discr)
    x.append(discr); y.append(hist2D.GetYaxis().GetBinCenter(by+1))
    errors.append( error )
  return x,y,errors





def PileUpDiscFit(hist,effref):
    NBINSY = hist.GetNbinsY()
    NBINSX = hist.GetNbinsX()
    discr_points, nvtx_points, error_points = CalculateDependentDiscrPoints(hist, effref )
    import array
    g = ROOT.TGraphErrors( len(discr_points)
                         , array.array('d',nvtx_points,)
                         , array.array('d',discr_points)
                         , array.array('d',[0.]*len(discr_points))
                         , array.array('d',error_points) )
    #counter = 0
    #for k in xrange(NBINSY) :
    #    n_sig = hist.Integral(0,-1,k,k)
    #    if n_sig == 0 : continue
    #    cut = -4.0
    #    pileupVal = 0
    #    for m in xrange(NBINSX) :
    #        #Below is where the efficiency is computed
    #        if (1 - hist.Integral(0,m,k,k)/n_sig) < effref :
    #            if abs((1 - hist.Integral(0,m-1,k,k)/n_sig) - effref) < abs((1 - hist.Integral(0,m,k,k)/n_sig) - effref) :
    #                cut = hist.GetXaxis().GetBinLowEdge(m)
    #            else:
    #                cut = hist.GetXaxis().GetBinLowEdge(m+1)
    #            pileupVal = hist.GetYaxis().GetBinLowEdge(k+1) + (-hist.GetYaxis().GetBinLowEdge(k+1)+hist.GetYaxis().GetBinLowEdge(k+2))/2.
    #            counter = counter + 1
    #            #print 'counter is: %3.15f' %counter
    #            #print 'pileupVal to be fitted: %3.15f' %pileupVal
    #            #print 'cut to be fitted is: %3.15f' %cut
    #            #print "effref is: %3.15f" % effref
    #            #print "calc eff is is: %3.15f" % (1 - hist.Integral(0,m,k,k)/n_sig)
    #            break
    #    if cut == -4.0 : continue
    #    #inverting plot to do fit
    #    ex = 0
    #    ey = 1/math.sqrt(hist.Integral(0,-1,k,k))
    #    g.SetPoint(counter - 1 ,pileupVal, cut)
    #    g.SetPointError(counter - 1 ,ex, ey)
    #    print "setting:", pileupVal, cut
    FirstBinVal = hist.GetYaxis().GetBinLowEdge(hist.GetYaxis().GetFirst())
    #LastBinVal = hist.GetYaxis().GetBinLowEdge(hist.GetYaxis().GetLast())
    LastBinVal = hist.GetYaxis().GetBinLowEdge(hist.GetYaxis().GetLast()+1)
    #print "First bin val is %3.15f" % FirstBinVal
    #print "Last bin val is %3.15f" % LastBinVal
    f1 = ROOT.TF1('f1','pol1',FirstBinVal, LastBinVal)
    g.Fit(f1,"FRq")
    #canvas = ROOT.TCanvas('Offline')
    #g.SetMarkerStyle(20)
    #g.Draw()
    #canvas.SaveAs('Tgraph'+hist.GetName()+'.pdf')
    a = f1.GetParameter(1)
    b = f1.GetParameter(0)
    return a,b


def GetEfficiencyRegion(hist,ylow,yhigh,a,b,err_on_higher_eff=False) : # yhigh is non-inclusive

  """
  Get the efficiency of a range of nvtx (ylow to yhigh) given discriminant parameters a and b
  (i.e. discr = a + bx where x is nvtx)
  """
  # inputs are nvtx (or TRT Track Occ)limits (i.e. ylow <= region < yhigh)
  yhigh = hist.GetYaxis().FindBin(yhigh) - 1
  ylow = hist.GetYaxis().FindBin(ylow) - 1
  yhigh = min(hist.GetNbinsY(),yhigh)
  den = float(hist.Integral(-99999,99999,int(ylow)+1,int(yhigh)))
  num = 0
  #for by in xrange(ylow,yhigh) :
  for by in xrange(int(ylow),int(yhigh)) :
    #print by, a, b
    discr = a + b*by
    dbin = hist.GetXaxis().FindBin(discr)
    num += hist.Integral(dbin+(0 if err_on_higher_eff else 1),99999,by+1,by+1)
  if den == 0 :
    return 1
  return num/den



def GetParameterizedDiscrNumeratorProfile(hist,a,b) :
  """
  Given a 2d hist, return the numerator of the efficiency vs nvtx (a 1d hist).
  """
  err_on_higher_eff = False
  nbinsy = hist.GetNbinsY()
  h1 = hist.ProjectionY(hist.GetName()+'_proj'+str(time.time()),1,1)
  h1.Reset("ICESM")
  Numerator=0; Denominator=0
  for by in xrange(nbinsy) :

    xproj = hist.ProjectionX('xproj'+str(time.time()),by+1,by+1)
    discr = a*hist.GetYaxis().GetBinCenter(by+1)+b

    dbin = xproj.FindBin(discr)

    num = xproj.Integral(dbin+(0 if err_on_higher_eff else 1),xproj.GetNbinsX()+1)
    h1.SetBinContent(by+1,num)
    Numerator+=num
    #Denominator+=xproj.GetEntries()
    Denominator+=xproj.Integral(-1, xproj.GetNbinsX()+1)
    den = xproj.Integral(-1, xproj.GetNbinsX()+1)

  return h1, Numerator, Denominator



def GetEquilibriumLine(hist,effref,a_1,limits) :
  #Takes a 2d hist (hist), the target efficiency (effref), the starting discr value (a_1),
  #and the three numbers corresponding to the boundary lines in nvtx (i.e. [0,12,23] for
  #nvtx = 0-11 and 12-22).

  err_on_higher_eff = True
  dslope = hist.GetXaxis().GetBinWidth(1)/15. # *10
  #binwidth = 10*hist.GetXaxis().GetBinWidth(1)
  binwidth = 5*hist.GetXaxis().GetBinWidth(1)
  if hist.Integral() != 0:
    error = math.sqrt(effref*(1-effref)/hist.Integral())
  else:
    error = 1
  if error == 0 :
    error = 1.

  nIters = 0; a = a_1; b = 0; tmp = 0
  islo,ishi,isgt,islt,reset = False,False,False,False,False
  flipcounter = 0
  while (True) :
    if a < hist.GetXaxis().GetBinLowEdge(1) :
      #print('GetEquilibriumLine: discriminant is at low egdge of histo. Breaking.')
      a = a_1
      b = 0
      break
    if a > hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()+1) :
      #print('GetEquilibriumLine: discriminant is at high egdge of histo. Breaking.')
      a = a_1
      b = 0
      break
    if flipcounter == 10 :
      #print('GetEquilibriumLine: flipcounter maxed out. breaking.')
      break
    if islo and ishi :
      #print('GetEquilibriumLine: oscillating...')
      binwidth = binwidth*0.5
      flipcounter += 1
    if isgt and islt :
      #print('GetEquilibriumLine: slope oscillating...')
      dslope = 0.5*dslope
      flipcounter += 1
    reset = not reset
    if reset :
        islo,ishi,isgt,islt = False,False,False,False
    tmp+=1
    lower = GetEfficiencyRegion(hist,limits[0],limits[1],a,b,err_on_higher_eff)
    upper = GetEfficiencyRegion(hist,limits[1],limits[2],a,b,err_on_higher_eff)
    #print('GetEquilibriumLine: a %f b %f lower %f upper %f effref %f'%(a,b,lower,upper,effref))
    if (lower - effref > error) and (upper - effref > error) :
      #print('GetEquilibriumLine: both effs are larger')
      islo = True
      a += binwidth
    elif (lower - effref < error) and (upper - effref < error) :
      #print('GetEquilibriumLine: both effs are smaller')
      ishi = True
      a -= binwidth
    elif lower - upper < error :
      #print('GetEquilibriumLine: both effs are within error %f'%error)
      break
    elif lower > upper :
      isgt = True
      #print('GetEquilibriumLine: Lower eff >>>>> Upper eff')
      a = a - limits[1]*dslope
      b -= dslope
    elif upper > lower :
      islt = True
      #print('GetEquilibriumLine: Lower eff <<<<< Upper eff')
      a = a + limits[1]*dslope
      b += dslope
    #print 'slope,intercept=', b, a


  lower = GetEfficiencyRegion(hist,limits[0],limits[1],a,b,err_on_higher_eff)
  upper = GetEfficiencyRegion(hist,limits[1],limits[2],a,b,err_on_higher_eff)
  if lower - upper > error :
    #print('GetEquilibriumLine Error! Results are not within error %f (%f,%f)'%(error,lower,upper))
    #print('GetEquilibriumLine a %f b %f'%(a,b))
    #print('GetEquilibriumLine end')
    pass
  #print "theSlope (GetEquilLine): %3.15f" % b
  return a,b



def CalculateEfficiency(h2D, effref, b, a, fix_fraction=1, doCorrection=True, limits=[15,30,60]):

  from copy import deepcopy
  hist2D=deepcopy(h2D)

  if doCorrection:
    # Get the intercept and slope in disc vs. pileup plane: y = ax+b
    #a,b = GetEquilibriumLine(hist2D,effref,b,limits)
    a,b = PileUpDiscFit(hist2D,effref) # a + bx, b is slope

    # Now do some correction to give the efficiency a small slope
    # (so backgrounds do not explode)
    pivotPoint = limits[1]
    b = b + pivotPoint*a*(1-fix_fraction)
    a = a*fix_fraction

  # Put into histograms
  histNum, passed, total = GetParameterizedDiscrNumeratorProfile(hist2D,a,b)
  histDen = hist2D.ProjectionY()
  histEff = histNum.Clone()
  histEff.Divide(histDen)
  for bin in xrange(histEff.GetNbinsX()):
    if histDen.GetBinContent(bin+1) != 0 :
      Eff = histEff.GetBinContent(bin+1)
      try:
        dEff = math.sqrt(Eff*(1-Eff)/histDen.GetBinContent(bin+1))
      except:
        dEff=0

      histEff.SetBinError(bin+1,dEff)
    else:
      histEff.SetBinError(bin+1,0)

  #eff=passed/float(histDen.GetEntries())
  eff=passed/float(total)
  if doCorrection:
    return histNum, histDen, histEff, (eff,passed,float(histDen.GetEntries())), b, a
  else:
    return histNum, histDen, histEff, (eff,passed,float(histDen.GetEntries()))




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




class Target( Logger ):

  def __init__( self, name, algname, reference, doSP=False, factor=None, relaxparameter=0.0 ):
    Logger.__init__(self)
    self._name =name
    self._algname = algname
    self._reference = reference
    self._relaxparameter = relaxparameter
    self._doSP = doSP


  def name(self):
    return self._name

  def algname(self):
    return self._algname

  def refname(self):
    return self._refname

  def reference( self, storegate=None, etbinidx=None, etabinidx=None, basepath=None, useFalseAlarm=False ):
    
    if not storegate:
      self._logger.fatal("Can not access the reference. You must pass the Storegate pointer as argument.")
    if not basepath:
      self._logger.fatal("Can not access the reference. You must pass the basepath as argument.")
    
    if type(self._reference) is list:
      if (etbinidx is not None) and (etabinidx is not None):
        eff = self._reference[etbinidx][etabinidx]        
        path = '{}/{}/{}/{}/{}'.format(self._basepath,'fakes' if useFalseAlarm else 'probes',self.name(),self._reference,binningname)
        total   = storegate.histogram(path+'/eta').GetEntries()
        passed = eff*float(total)
    elif type(self._reference) is float:
        path = '{}/{}/{}/{}/{}'.format(self._basepath,'fakes' if useFalseAlarm else 'probes',self.name(),self._reference,binningname)
        total   = storegate.histogram(path+'/eta').GetEntries()
        eff = self._reference
        passed = eff*float(total)
    elif type(self._reference) is str:
      if (etbinidx is None) and (etabinidx is None):
        self._logger.fatal("Can not access the reference. You must pass et/eta bin index as argument.")
        algname = pair[0]; 
        binningname = ('et%d_eta%d') % (etbinidx,etabinidx)
        if self._doSP:
          det, fa, sp = CalculateMaxSP(
          storegate.histogram('{}/{}/{}/{}/{}/discriminantVsMu'.format(basepath,'probes',self.name(),self.algname(),binningname)).ProjectionX(),
          storegate.histogram('{}/{}/{}/{}/{}/discriminantVsMu'.format(basepath,'fakes',self.name(),self.algname(),binningname)).ProjectionX())
          total = storegate.histogram('{}/{}/{}/{}/{}/eta'.format(basepath,'probes',target.name(), self._reference,binningname)).GetEntries()
