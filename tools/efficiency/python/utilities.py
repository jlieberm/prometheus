
__all__ = [ "GetHistogramFromMany","GetProfile",
            "GetMaxNonLinearityValue","is_high_et", "GetHistogramRootPaths"]

from Gaugi.messenger import Logger
from Gaugi.messenger.macros import *
from Gaugi.gtypes import NotSet




def GetHistogramFromMany( files, paths, keys , prefix='Loading...' , logger=None):
  
  from monet.utilities import sumHists as SumHists
  from Gaugi import progressbar
  from copy import deepcopy 
  # internal open function
  def Open( path ):
    from ROOT import TFile
    f = TFile(path, 'read')
    basedirs = []
    for key in f.GetListOfKeys():
      kname = key.GetName()
      basedirs.append(kname)
    return f, basedirs
  # internal close function
  def Close( f ):
    f.Close()
    del f

  if type(paths) is not list:
    paths=[paths]  
  objects={}
  for f in progressbar(files, len(files), prefix=prefix, logger=logger):
    _f, _basepaths = Open(f)
    for idx, path in enumerate(paths):
      h = GetHistogram(_f, _basepaths, path, logger=logger)
      if h is not None:
        if not keys[idx] in objects.keys():
          objects[keys[idx]]=[deepcopy(h.Clone())]
        else:
          objects[keys[idx]].append(deepcopy(h.Clone()))
    Close(_f)
  
  for key in objects.keys():
    objects[key]=SumHists(objects[key])
  return objects


def GetHistogram( f, basepaths, path ,logger=None):
  from ROOT import TH1F
  from monet.utilities import sumHists as SumHists
  hists=list()
  for p in basepaths:
    try:
      tobject=TH1F()
      f.GetObject(p+'/'+path, tobject)
      hists.append(tobject)
    except:
      if logger:
        logger.debug('Can not retrieve %s',p+'/'+path)
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
 

def GetMaxNonLinearityValue( hist, fit, errorThreshold=0.01 ):
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

def is_high_et( chain ):
  # HLT_(e/g)XX_...
  import re
  return True if int(re.search('HLT_e(.*?)_',chain).group(1)) >=100 else False





def GetHistogramRootPaths( triggerList, removeInnefBefore=False, is_emulation=False, logger=None ):
  plot_names = ['et','eta','mu']
  level_names = ['L1Calo','L2Calo','L2','EFCalo','HLT']
  levels_input = ['L1Calo','L1Calo','L1Calo','L2','EFCalo']
  from Gaugi import progressbar
  paths=[]; keys=[]
  entries=len(triggerList)
  step = int(entries/100) if int(entries/100) > 0 else 1
  for trigItem in progressbar(triggerList, entries, step=step,logger=logger, prefix='Making paths...'):
    isL1 = True if trigItem.startswith('L1_') else False
    these_level_names = ['L1Calo'] if isL1 else level_names
    ### Retrieve all paths
    for idx ,level in enumerate(these_level_names):
      for histname in plot_names:
        if not isL1 and 'et' == histname and is_high_et(trigItem):  histname='highet'
        if is_emulation:
          histpath = 'HLT/Egamma/Expert/{TRIGGER}/Emulation/{LEVEL}/{HIST}'
        else:
          histpath = 'HLT/Egamma/Expert/{TRIGGER}/Efficiency/{LEVEL}/{HIST}'
        paths.append(histpath.format(TRIGGER=trigItem,HIST='match_'+histname,LEVEL=level))
        if removeInnefBefore:
          paths.append(histpath.format(TRIGGER=trigItem,HIST= ('match_'+histname if idx!=0 else histname),LEVEL=levels_input[idx]))
        else:
          paths.append(histpath.format(TRIGGER=trigItem,HIST=histname,LEVEL='L1Calo'))
        if 'highet' == histname:  histname='et'
        keys.append(trigItem+'_'+level+'_match_'+histname)
        keys.append(trigItem+'_'+level+'_'+histname)
  # Loop over triggers
  return paths, keys







