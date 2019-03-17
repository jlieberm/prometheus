
__all__ = ["TriggerInfo", "GetHistogramFromMany","GetProfile","GetMaxNonLinearityValue"]

from Gaugi.messenger import Logger
from Gaugi.messenger.macros import *
from Gaugi.types import NotSet


class TriggerInfo(object):
  
  def __init__(self, expression, mode, label):
    self._label = label
    self._expression = expression
    # can be Athena or Selector mode
    self._mode = mode
    self._core = NotSet
    self._pid = NotSet
    self._etthr = 0.0
    # extract some useful informations from the expression
    # if the mode is athena
    self.compile()

  def label(self):
    return self._label

  def etthr(self):
    return self._etthr

  def pid(self):
    return self._pid

  def core(self):
    return self._core

  def trigger(self):
    return self._trigger

  def expression(self):
    return self._expression

  def isAthena( self ):
    return True if self._mode is EfficicencyMode.Athena else False

  def compile(self):
    if self.isAthena():
      try:
        # (TDT/EMU)__(HLT/EFCalo/L2/L2Calo/L1Calo)__eXX_*
        trigParts = self.expression().split('__')
        # default offline pid   
        pidword = 'el_lhvloose'
        if 'lhtight' in trigParts[-1]:
          pidword = 'el_lhtight'
        elif 'lhmedium' in trigParts[-1]:
          pidword = 'el_lhmedium'
        elif 'lhloose' in trigParts[-1]:
          pidword = 'el_lhloose'
        elif 'lhvloose' in trigParts[-1]:
          pidword = 'el_lhvloose'
        else: 
          MSG_WARNING( self, "No Pid name was fount in the expression (%s) with path (%s)", self.expression(), trigParts[-1])
        # get the HLT threshold from the trigger name (eXX_*)
        self._etthr = float(trigParts[-1].split('_')[0][1::])
        self.trigger = trigParts[-1]
        # get the core (TDT or EMU)
        core = trigParts[0]
      except e:
        MSG_ERROR( "Can not extract the trigger info: %s", e)
 




def GetHistogramFromMany( files, paths, keys , prefix='Loading...' ):
  
  from Gaugi.utilities import sumHists as SumHists
  from Gaugi.utilities import progressbar
  from copy import deepcopy 
  # internal open function
  def _Open( path ):
    from ROOT import TFile
    f = TFile(path, 'read')
    basedirs = []
    for key in f.GetListOfKeys():
      kname = key.GetName()
      basedirs.append(kname)
    return f, basedirs
  # internal close function
  def _Close( f ):
    f.Close()
    del f

  if type(paths) is not list:
    paths=[paths]  
  objects={}
  for f in progressbar(files, prefix, 60):
    _f, _basepaths = Open(f)
    for idx, path in enumerate(paths):
      h = GetHistogram(_f, _basepaths, path)
      if h is not None:
        if not keys[idx] in objects.keys():
          objects[keys[idx]]=[deepcopy(h.Clone())]
        else:
          objects[keys[idx]].append(deepcopy(h.Clone()))
    Close(_f)
  
  for key in objects.keys():
    objects[key]=SumHists(objects[key])
  return objects


def GetHistogram( f, basepaths, path ):
  from ROOT import TH1F
  from Gaugi.utilities import sumHists as SumHists
  hists=list()
  for p in basepaths:
    try:
      tobject=TH1F()
      f.GetObject(p+'/'+path, tobject)
      hists.append(tobject)
    except:
      localLogger.debug('Can not retrieve %s',p+'/'+path)
  h = SumHists(hists);
  del hists[:]
  return h


def GetXAxisWorkAround( hist, nbins, xmin, xmax ):
  from ROOT import TH1F
  h=TH1F(hist.GetName()+'_resize', hist.GetTitle(), nbins,xmin,xmax)
  for bin in range(h.GetNbinsX()):
    x = h.GetBinCenter(bin+1)
    m_bin = hist.FindBin(x)
    y = hist.GetBinContent(m_bin)
    error = hist.GetBinError(m_bin)
    h.SetBinContent(bin+1,y)
    h.SetBinError(bin+1,error)
  return h


def GetProfile( passed, tot, resize=None):
  """
    Resize optin must be a list with [nbins, xmin, xmax]
  """
  if resize:
    tot=GetXAxisWorkAround(tot,resize[0],resize[1],resize[2])
    passed=GetXAxisWorkAround(passed,resize[0],resize[1],resize[2])
  passed.Sumw2(); tot.Sumw2()
  h = passed.Clone()
  h.Divide( passed, tot,1.,1.,'B' )
  return h
 

def GetMaxNonLineaarityValue( hist, fit, errorThreshold=0.01 ):
  NL=[]
  for bin in range(hist.GetNbinsX()):
    x1 = hist.GetBinCenter(bin+1)
    y1 = hist.GetBinContent(bin+1)
    e1 = hist.GetBinError(bin+1)
    # y = ax+b
    b = fit.GetParameter(0)
    a = fit.GetParameter(1)
    y2 = a*x1+b
    if y1>0 and e1 < errorThreshold and y1 < 1:
      NL.append(abs( (y1 - (a*x1+b))/y1 ) * 100)
  return max(NL)




