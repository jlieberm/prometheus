

from ROOT import kBlack,kBlue,kRed,kAzure,kGreen,kMagenta,kCyan,kOrange,kGray,kYellow,kWhite
from monet import *
from array import array
from copy import deepcopy
import time,os,math,sys,pprint,glob,warnings
import numpy as np
import ROOT, math

 

_g = []




def rebinY(th2, newbinning): 
  #print newbinning
  c = type(th2)
  f = lambda a: array('d',[a.GetBinLowEdge(x) for x in range(1,a.GetNbins()+1)] + [a.GetBinUpEdge(a.GetNbins())])
  th2_ret = c( th2.GetName(), th2.GetTitle(), th2.GetNbinsX(), f(th2.GetXaxis())
             , len(newbinning)-1, array('d',newbinning) )
  from itertools import product
  for x, y in product(xrange(th2.GetNbinsX()+2), xrange(th2.GetNbinsY()+2)):
    th2_ret_idx = th2_ret.FindBin(th2.GetXaxis().GetBinCenter(x),(th2.GetYaxis().GetBinLowEdge(y)+th2.GetYaxis().GetBinLowEdge(y+1))/2.)
    th2_ret_x_idx = ROOT.Long(0); th2_ret_y_idx = ROOT.Long(0); dummy = ROOT.Long(0);
    th2_ret.GetBinXYZ (th2_ret_idx, th2_ret_x_idx, th2_ret_y_idx, dummy)
    c = th2_ret.GetBinContent(th2_ret_x_idx, th2_ret_y_idx)
    cAdd = th2.GetBinContent(x,y)
    th2_ret.SetBinContent(th2_ret_x_idx, th2_ret_y_idx,c+cAdd)
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
  for bx in xrange(int(xlowidx),int(xhighidx)):
    y = 1
    for by in xrange(int(ylowidx),int(yhighidx)) :
      value = hist.GetBinContent(bx,by)
      tot+=value
      h.SetBinContent(x,y,value)
      if value>M:
        M=value;
        c=(x,y)
      passed+=h.GetBinContent(x,y)
      y+= 1
    x+=1

  return h.Clone()


def calcSP( pd, pj ):
  #  ret  = calcSP(x,y) - Calculates the normalized [0,1] SP value.
  #  effic is a vector containing the detection efficiency [0,1] of each
  #  discriminating pattern.  
  from numpy import sqrt
  return sqrt(geomean([pd,pj]) * mean([pd,pj]))


def CalculateMaxSP( hist_sgn, hist_bkg ):

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
    FirstBinVal = hist.GetYaxis().GetBinLowEdge(hist.GetYaxis().GetFirst())
    LastBinVal = hist.GetYaxis().GetBinLowEdge(hist.GetYaxis().GetLast()+1)
    f1 = ROOT.TF1('f1','pol1',FirstBinVal, LastBinVal)
    g.Fit(f1,"FRq")
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
  for by in xrange(int(ylow),int(yhigh)) :
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
    Denominator+=xproj.Integral(-1, xproj.GetNbinsX()+1)
    den = xproj.Integral(-1, xproj.GetNbinsX()+1)

  return h1, Numerator, Denominator




def CalculateEfficiency(h2D, effref, b, a, fix_fraction=1, doCorrection=True, limits=[15,30,60]):

  from copy import deepcopy
  hist2D=deepcopy(h2D)

  if doCorrection:
    a,b = PileUpDiscFit(hist2D,effref) # a + bx, b is slope
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
  eff=passed/float(total)
  if doCorrection:
    return histNum, histDen, histEff, (eff,passed,float(histDen.GetEntries())), b, a
  else:
    return histNum, histDen, histEff, (eff,passed,float(histDen.GetEntries()))



class TH2Holder(object):
  def __init__(self,xmin,xmax,xres,ymin,ymax,yres):
    self._xmin=xmin; self._xmax=xmax; self._xres=xres
    self._ymin=ymin; self._ymax=ymax; self._yres=yres
  def xmin(self): 
    return self._xmin
  def xmax(self): 
    return self._xmax
  def xresolution(self): 
    return self._xres
  def ymin(self): 
    return self._ymin
  def ymax(self): 
    return self._ymax
  def yresolution(self): 
    return self._yres
  def xbins(self):
    print self.xresolution
    return (len(self.xresolution())-1) if type(self.xresolution()) is list else ((self.xmax() - self.xmin()) / float(self.xresolution()))




def ApplyThresholdLinearCorrection( xmin, xmax, xres, mumin, mumax, mures,
  sgn_hist2D, bkg_hist2D, refvalue,  doLinearCorrection=True, false_alarm_limit=0.5, logger=None ):
  """
    This is the main function used to call the pileup correction and make the summary
  """
  xbins=int((xmax-xmin)/float(xres))
  sgn_hist2D = Copy2DRegion(sgn_hist2D.Clone(),xbins,xmin,xmax,np.int(np.round((mumax-mumin)/sgn_hist2D.GetYaxis().GetBinWidth(1))),mumin,mumax)
  bkg_hist2D = Copy2DRegion(bkg_hist2D.Clone(),xbins,xmin,xmax,np.int(np.round((mumax-mumin)/bkg_hist2D.GetYaxis().GetBinWidth(1))),mumin,mumax)
  

  if isinstance(mures,(float,int)):
    mubins=int((mumax-mumin)/float(mures))
    sgn_hist2D = sgn_hist2D.RebinY(np.int(math.floor(sgn_hist2D.GetNbinsY()/mubins)))
    bkg_hist2D = bkg_hist2D.RebinY(np.int(math.floor(bkg_hist2D.GetNbinsY()/mubins)))
  else:
    sgn_hist2D = rebinY(sgn_hist2D,mures)
    bkg_hist2D = rebinY(bkg_hist2D,mures)


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

  angular = a;  offset = b; offset0 = b0
  
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
           


















