
__all__ = [ "GetHistogramFromMany",
            "GetHistogramRootPaths",
            "GetProfile",
					  "PlotProfiles",
            ]


def PlotProfiles( hists, xlabel, these_colors, these_transcolors, these_markers,
                  drawopt='pE1', 
                  rlabel='Trigger/Ref.',
                  ylabel='Trigger Efficiency', 
                  doRatioCanvas=False,
                  y_axes_maximum=1.1, 
                  y_axes_minimum=0.0, 
                  pad_top_y_axes_maximum=1.1, 
                  pad_top_y_axes_minimum=0.0, 
                  pad_bot_y_axes_maximum=1.1,
                  pad_bot_y_axes_minimum=0.9):
    
    from ROOT import TCanvas
    from Gaugi.monet import RatioCanvas, AddHistogram, FormatCanvasAxes, SetAxisLabels
    doRatio = True if (doRatioCanvas and (len(hists)>1)) else False
    collect = []
    canvas = RatioCanvas( 'canvas', "", 700, 500) if doRatio else TCanvas( 'canvas', "", 700, 500 )
    if doRatio:
        pad_top = canvas.GetPrimitive('pad_top')
        pad_bot = canvas.GetPrimitive('pad_bot')
    
    refHist = hists[0]
    for idx, hist in enumerate(hists):
        if doRatio:
            if idx < 1:
                refHist.SetLineColor(these_colors[idx])
                refHist.SetMarkerColor(these_colors[idx])
                refHist.SetMaximum(pad_top_y_axes_maximum)
                refHist.SetMinimum(pad_top_y_axes_minimum)
                AddHistogram(pad_top, refHist, drawopt = drawopt, markerStyle=these_markers[idx])
            else:
                h_hist=hist.Clone()
                h_hist.Divide(h_hist,refHist,1.,1.,'B')
                h_hist.SetMinimum(pad_bot_y_axes_minimum)
                h_hist.SetMaximum(pad_bot_y_axes_maximum)
                collect.append(h_hist)
                hist.SetLineColor(these_colors[idx])
                hist.SetMarkerColor(these_colors[idx])
                hist.SetMaximum(pad_top_y_axes_maximum)
                AddHistogram( pad_top, hist, drawopt, markerStyle=these_markers[idx])
                AddHistogram( pad_bot, h_hist, 'P', markerStyle=these_markers[idx])
        else:
            hist.SetLineColor(these_colors[idx])
            hist.SetMarkerColor(these_colors[idx])
            hist.SetMaximum(y_axes_maximum)
            hist.SetMinimum(y_axes_minimum)
            AddHistogram(canvas, hist, drawopt = drawopt, markerStyle=these_markers[idx])
    
    FormatCanvasAxes(canvas, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
    SetAxisLabels(canvas,xlabel,ylabel,rlabel)
    return canvas
     



def GetHistogramFromMany( basepath, paths, keys , prefix='Loading...' , logger=None):
  
    from Gaugi.monet.utils import sumHists as SumHists
    from Gaugi import progressbar, expandFolders
    from copy import deepcopy     
    # internal open function
    def Open( path ):
        from ROOT import TFile
        f = TFile(path, 'read')
        if len(f.GetListOfKeys())>0:
            run_number = f.GetListOfKeys()[0].GetName()
            return f, run_number
        else:
            return f, None
    # internal close function
    def Close( f ):
        f.Close()
        del f
    # internal retrive histogram
    def GetHistogram( f, run_number, path ,logger=None):
        try:            
            hist = f.Get(run_number+'/'+path)
            hist.GetEntries()
            return hist
            
        except:
            return None

    files = expandFolders(basepath)
    hists = {}
    for f in progressbar(files, len(files), prefix=prefix, logger=logger):
        
        try:
            _f, _run_number = Open(f)
        except:
            continue
        if _run_number is None:
            continue
        for idx, _path in enumerate(paths):
            hist = GetHistogram(_f, _run_number, _path)
            
            if (hist is not None):
                if not keys[idx] in hists.keys():
                    hists[keys[idx]]=[deepcopy(hist.Clone())]
                else:
                    hists[keys[idx]].append(deepcopy(hist.Clone()))
       
        Close(_f)
  
    for key in hists.keys():
        hists[key]=SumHists(hists[key])
    return hists





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



def is_high_et( chain ):
  # HLT_(e/g)XX_...
  import re
  return True if int(re.search('HLT_e(.*?)_',chain).group(1)) >=100 else False





