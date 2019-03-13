

from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite
from monet import *
from array import array
from copy import deepcopy
import time,os,math,sys,pprint,glob,warnings
import numpy as np
import ROOT, math

 

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




# threshold pileup correction
def ApplyThresholdLinearCorrection( chist, sgn_hist2D, bkg_hist2D, refvalue,  doLinearCorrection=True, false_alarm_limit=0.5, logger=None ):
  """
    This is the main function used to call the pileup correction and make the summary
  """
 
  mumin = chist.ymin()
  mumax = chist.ymax()

  sgn_hist2D = Copy2DRegion(sgn_hist2D.Clone(),chist.xbins(),chist.xmin(),chist.xmax(),np.int(np.round((mumax-mumin)/sgn_hist2D.GetYaxis().GetBinWidth(1))),mumin,mumax)
  bkg_hist2D = Copy2DRegion(bkg_hist2D.Clone(),chist,xbins(),chist.xmin(),chist.xmax(),np.int(np.round((mumax-mumin)/bkg_hist2D.GetYaxis().GetBinWidth(1))),mumin,mumax)
  

  if isinstance(chist.yres(),(float,int)):
    sgn_hist2D = sgn_hist2D.RebinY(np.int(math.floor(sgn_hist2D.GetNbinsY()/chist.ybins())))
    bkg_hist2D = bkg_hist2D.RebinY(np.int(math.floor(bkg_hist2D.GetNbinsY()/chist.ybins())))
  else:
    sgn_hist2D = rebinY(sgn_hist2D,chist.yres())
    bkg_hist2D = rebinY(bkg_hist2D,chist.yres())


  false_alarm = 1.0
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
      sgn_histNum_corr, sgn_histDen_corr, sgn_histEff_corr, sgn_info_corr ,b, a = CalculateEfficiency( sgn_hist2D, refvalue, b0, 0, doCorrection=True)
      if a>0:
        if logger:  logger.warning("Retrieved positive angular factor of the linear correction, setting to 0!")
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
  
  if logger:
    logger.info( 'Signal with correction is: %1.2f%%', sgn_info_corr[0]*100 )
    logger.info( 'Background with correction is: %1.2f%%', bkg_info_corr[0]*100 )
  
  # create the summary with all counts
  summary = {
             'signal_corr_values'     : {'eff'  : sgn_info_corr[0], 'passed'  : sgn_info_corr[1]  , 'total'  : sgn_info_corr[2]},
             'background_corr_values' : {'eff'  : bkg_info_corr[0], 'passed'  : bkg_info_corr[1]  , 'total'  : bkg_info_corr[2]},
             'signal_values'          : {'eff'  : sgn_info[0]     , 'passed'  : sgn_info[1]       , 'total'  : sgn_info[2]},
             'background_values'      : {'eff'  : bkg_info[0]     , 'passed'  : bkg_info[1]       , 'total'  : bkg_info[2]},
             }
  # create the root object dict holder
  objects = {
             'signal_corr_hists'      : {'num'  : sgn_histNum_corr, 'den'     : sgn_histDen_corr , 'eff'     : sgn_histEff_corr , 'hist2D'    : sgn_hist2D},      
             'background_corr_hists'  : {'num'  : bkg_histNum_corr, 'den'     : bkg_histDen_corr , 'eff'     : bkg_histEff_corr , 'hist2D'    : bkg_hist2D},
             'signal_hists'           : {'num'  : sgn_histNum     , 'den'     : sgn_histDen      , 'eff'     : sgn_histEff      , 'hist2D'    : sgn_hist2D},
             'background_hists'       : {'num'  : bkg_histNum     , 'den'     : bkg_histDen      , 'eff'     : bkg_histEff      , 'hist2D'    : bkg_hist2D},
             'correction'             : {'discr_points'   : discr_points    , 'nvtx_points'      : nvtx_points      , 'error_points'      : error_points,
                                         'angular'        : angular         , 'offset'           : offset           , 'offset0'           : offset0 },
            }

  # return the summary and objects 
  return summary, objects
           


















