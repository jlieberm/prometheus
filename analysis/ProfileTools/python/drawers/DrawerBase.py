__all__ = ['DrawerBase', 'histToUnitArea', 'sumHists', 'getBounderies', 'colorGradient'
          , 'fadeToBlack', 'fadeToWhite', 'getBinText', 'formatQuantity', 'addTopLabels'
          , 'rearrange', 'formatBinsLegend', 'retrieveSpecialBinsLegend', 'returnArgument']

from Gaugi import retrieve_kw, ensureExtension, progressbar
from Gaugi.messenger import Logger
import os

def histToUnitArea(hist, norm):
  integral = hist.Integral(norm) if norm is not None else 1
  if integral == 0 : integral = 1
  hist.Scale(1./integral);
  hist.SetMinimum(0)
  return hist

def sumHists(histList, newNameSuffix = '_Sum', norm = None):
  totalHist = histList[0].Clone(histList[0].GetName() + newNameSuffix)
  for hist in histList[1:]: 
    if not totalHist.Add( hist ):
      return None
  if norm is not None: totalHist = histToUnitArea( totalHist, norm )
  return totalHist

def getBounderies( array, idx=None): 
  if idx is not None: return array[idx:idx+2]
  else: return None

def getColors(outColors):
  from ROOT import TColor
  return [TColor.GetColor(r, g, b) for r, g, b in zip(*outColors)]

def colorGradient(color1, color2, nSteps, smoothThres=None):
  import numpy as np
  color1 = np.array(color1)
  color2 = np.array(color2)
  deltas = color2 - color1
  deltaSum = sum(abs(deltas))
  if smoothThres is not None and deltaSum/nSteps>smoothThres:
    color2 = color1 + deltas*smoothThres*nSteps/deltaSum
  outColors = [np.linspace(pcolor1,pcolor2,nSteps) for pcolor1, pcolor2 in zip(color1,color2)]
  outColors = getColors(outColors)
  return outColors

def fadeToBlack(color1, nSteps=None, smoothThres=None):
  if nSteps is None: 
    smoothThres = 0.4; nSteps = 1
  return colorGradient(color1,[0,0,0], nSteps, smoothThres)

def fadeToWhite(color1, nSteps=None, smoothThres=None):
  if nSteps is None: 
    smoothThres = 0.4; nSteps = 1
  return colorGradient(color1,[1,1,1], nSteps, smoothThres)

def getBinText(binBounderies, binStr, binUnit):
  if not isinstance(binBounderies, (tuple, list)): 
    binBounderies = [binBounderies]
  binBounderies = [b for b in binBounderies if b is not None]
  binText = ('%s < %s < %s' % (str(binBounderies[0])
                           , binStr + (' ' + binUnit if binUnit else '')
                           ,str(binBounderies[1]))
              if len(binBounderies) is 2 else
              '%s %s > %s' % (binStr, binUnit if binUnit else '', str(binBounderies[0])) )
  return binText

def retrieveEtHists(hists, binIdx):
  return hists[binIdx]

def retrieveEtaHists(hists, binIdx):
  return [hist[binIdx] for hist in hists]

def formatQuantity(can, outputPath
                  , xLabel, divLabel, legend
                  , colorarr = None, stylearr = None, markersizes = []
                  , dataLegend = '', quantity_text = ''
                  , binBounderies = None, binStr = None, binUnit = None
                  , ignoreErrorsTop=True, ignoreErrorsBot=True
                  , specialBinsLegend=None
                  , useBlackLine=None
                  , norm=None
                  ):
  from Gaugi.monet.PlotFunctions import FormatCanvasAxes, SetAxisLabels, AutoFixAxes, FixYaxisRanges, SetColors, SetMarkerStyles
  # First change hist colors:
  if colorarr: SetColors(can,colorarr,fillColor=True)
  if useBlackLine: 
    from ROOT import kBlack
    SetColors(can,[kBlack]*len(colorarr),markerColor=False,fillColor=False)
  if stylearr: SetMarkerStyles(can,stylearr, markersizes)
  addTopLabels(can, legend = legend
              , dataLegend = dataLegend, quantity_text = quantity_text
              , binBounderies = binBounderies, binStr = binStr, binUnit = binUnit
              , specialBinsLegend = specialBinsLegend
              )
  FormatCanvasAxes(can,XLabelSize=18,YLabelSize=18,XTitleOffset=0.87, YTitleOffset=1.5)
  normLabel=""
  if norm == "":
    normLabel="(norm by counts)"
  elif norm == "width":
    normLabel="(norm by area)"
  SetAxisLabels(can, xLabel, "counts/bin %s" % normLabel, divLabel)
  AutoFixAxes(can, ignoreErrors=ignoreErrorsTop)
  # FIXME: Needed for the first versions, but can be buggy afterwards
  if can.GetPrimitive('pad_bot'):
    FixYaxisRanges(can.GetPrimitive('pad_bot'), ignoreErrors=ignoreErrorsBot )
    if colorarr: SetColors(can.GetPrimitive('pad_bot'),colorarr[1:])
    if stylearr: SetMarkerStyles(can.GetPrimitive('pad_bot'),stylearr[1:], markersizes[1:])
    can.GetPrimitive('pad_bot').SetTitle("")
  else:
    can.SetBottomMargin(0.105)
  fullFigPath = os.path.join( outputPath, ensureExtension(can.GetName(), 'pdf') )
  fullFigPathC = os.path.join( outputPath, ensureExtension(can.GetName(), 'C') )
  can.SaveAs( fullFigPath )
  can.SaveAs( fullFigPathC )
  return fullFigPath

def rearrange( binsLegend, refIdx, useRefFirst ): 
  from copy import copy
  binsLegend = copy(binsLegend)
  return [binsLegend.pop(refIdx)] + binsLegend if useRefFirst else binsLegend

def addTopLabels(can, legend
                , dataLegend = '', quantity_text = ''
                , binBounderies = None, binStr = None, binUnit = None
                , specialBinsLegend = None):
  from Gaugi.monet.PlotFunctions import GetAtlasInternalText, GetSqrtsText, DrawText, MakeLegend
  text_lines = []
  text_lines += [GetAtlasInternalText()]
  text_lines.append( GetSqrtsText(13) )
  if dataLegend: text_lines.append( dataLegend )
  if legend:
      MakeLegend(can,.73,.68,.89,.93,option='p',textsize=10, names=legend, ncolumns=1, squarebox=False, doFixLength=False)
  moreText = []
  if binBounderies:
    moreText.append( getBinText(binBounderies, binStr, binUnit ) if not isinstance(binBounderies,str) else binBounderies )
  elif binStr is not None:
    moreText.append( "Full %s range" % binStr)
  if quantity_text: moreText.append( quantity_text )
  if specialBinsLegend is not None and any(specialBinsLegend):
    MakeLegend(can,.19,.68,.35,.93,option='p',textsize=10, names=specialBinsLegend, ncolumns=1, totalentries=len(legend) if legend else 0, squarebox=False, doFixLength=False
              , title = "Not included occurrences:")
    if moreText: text_lines += moreText
  else:
    if moreText: DrawText(can, moreText, .15,.68,.35,.93,totalentries=4)
  DrawText(can,text_lines,.40,.68,.70,.93,totalentries=4)

def formatBinsLegend( label, binsLegend, notNormBaseHists, specialBinHists, entriesMap ):
  import itertools
  from copy import copy
  binsLegend = copy(binsLegend)
  for idx, legend, notNormHist, specialBinHist in zip( itertools.count(), binsLegend, notNormBaseHists, specialBinHists ):
    if specialBinHist and specialBinHist.GetEntries():
      entries = [specialBinHist.GetBinContent(x) for x in range(1,specialBinHist.GetNbinsX()+1) ]
      if any(entries):
        total = float(sum(entries) + notNormHist.GetEntries())
        percentage = [entry/total*100 for entry in entries]
        #legend = '#splitline{' + legend + '}{' + "#splitline{Occurrences not included:}{"
        legend = '#splitline{' + legend + '}{'
        alreadyFilled = False
        for specialBinIdx, perc in zip( itertools.count(), percentage):
          if perc:
            if alreadyFilled: legend += " | "
            legend += str(entriesMap[label][specialBinIdx]) if entriesMap is not None and label in entriesMap else str(specialBinIdx)
            legend += " : %.1f%%" % perc 
            alreadyFilled = True
        #legend += '}}'
        legend += '}'
        binsLegend[idx] = legend
  return binsLegend

def retrieveSpecialBinsLegend( label, notNormBaseHists, specialBinHists, entriesMap ):
  import itertools
  from copy import copy
  binsLegend = []
  for notNormHist, specialBinHist in zip( notNormBaseHists, specialBinHists ):
    legend = ''
    if specialBinHist and specialBinHist.GetEntries():
      entries = [specialBinHist.GetBinContent(x) for x in range(1,specialBinHist.GetNbinsX()+1) ]
      if any(entries):
        total = float(sum(entries) + notNormHist.GetEntries())
        percentage = [entry/total*100 for entry in entries]
        alreadyFilled = False
        for specialBinIdx, perc in zip( itertools.count(), percentage):
          if perc:
            if alreadyFilled: legend += " | "
            legend += "occ. " + str(entriesMap[label][specialBinIdx]) if entriesMap is not None and label in entriesMap else str(specialBinIdx)
            legend += " : %.1f%%" % perc 
            alreadyFilled = True
    binsLegend.append( legend if legend else None )
  return binsLegend

def returnArgument(arg):
  return arg

class DrawerBase(Logger):

  def __init__(self, d = {}, **kw):
    from Gaugi.storage import restoreStoreGate
    from Gaugi import retrieve_kw
    import numpy as np
    from ROOT import gROOT, kTRUE, kAzure
    gROOT.SetBatch(kTRUE)
    d.update( kw )
    Logger.__init__(self, d)
    self._sg                      = restoreStoreGate( retrieve_kw(d, 'filePath','') )
    #self._sg = None
    from CommonTools.constants import ringer_tuning_etbins, ringer_tuning_etabins
    self._etBins                  = retrieve_kw( d, 'etBins', ringer_tuning_etbins )
    self._etaBins                 = retrieve_kw( d, 'etaBins', ringer_tuning_etabins )
    self._EDM                     = retrieve_kw( d, 'EDM',        ''              )
    self._plotRatio               = retrieve_kw( d, 'plotRatio',   False          )
    self._outputPath              = retrieve_kw( d, 'outputPath', ''              )
    self._addEDMToOutputPath      = retrieve_kw( d, 'addEDMToOutputPath', True )
    self._etRefBin                = retrieve_kw( d, 'etRefBin',    2              )
    self._etaRefBin               = retrieve_kw( d, 'etaRefBin',   0              )
    self._dataLegend              = retrieve_kw( d, 'dataLegend',  None           )
    self._rebin                   = retrieve_kw( d, 'rebin',       None           )
    self._baseEtaColor            = retrieve_kw( d, 'baseEtaColor', np.array([255,124,124],dtype=np.float_)/255 )
    self._baseEtColor             = retrieve_kw( d, 'baseEtColor', np.array([124,124,255],dtype=np.float_)/255 )
    self._fullPhaseSpaceColor     = retrieve_kw( d, 'fullPhaseSpaceColor', kAzure-4 )
    self._useRefFirst             = retrieve_kw( d, 'useRefFirst', False )
    self.figures                  = {}
    self.paths                    = {}

  @property
  def sg(self):
    return self._sg

  @property
  def outputPath(self):
    outputPath = self._outputPath
    if not outputPath: outputPath = os.curdir
    return outputPath if not self._addEDMToOutputPath or os.path.basename(outputPath) == self._EDM else os.path.join(outputPath, self._EDM)

  def plot(self, **kw):
    pass

  @property
  def _etaBinsLegend(self):
    def etaBinStr(l): 
      for _ in range(l): yield '#eta'
    def etaBinUnit(l): 
      for _ in range(l): yield None
    l = len(self._etaBins)-1
    return list( map(getBinText, list(map(lambda x,y:(x,y),self._etaBins[:-1],self._etaBins[1:]) ), etaBinStr(l), etaBinUnit(l) ) ) 

  @property
  def _etaRefLabel(self):
    binRef = self._etaRefBin
    return getBinText(self._etaBins[binRef:binRef+2], '#eta', None)

  @property
  def _etBinsSpecial(self):
    from copy import copy
    bins = copy(self._etBins)
    bins[-1] = None
    return bins

  @property
  def _etBinsLegend(self):
    def etBinStr(l): 
      for _ in range(l): yield 'E_{T}'
    def etBinUnit(l): 
      for _ in range(l): yield '[GeV]'
    l = len(self._etBins)-1
    bins = self._etBinsSpecial
    return list( map(getBinText, list(map(lambda x,y:(x,y),bins[:-1],bins[1:])), etBinStr(l), etBinUnit(l) ) )

  @property
  def _etRefLabel(self):
    binRef = self._etRefBin
    return getBinText( self._etBins[binRef:binRef+2], 'E_{T}', '[GeV]')

  def retrieveQuantitiesInfo(self, dirName):
    import ROOT
    path = "Profiles/" + dirName + "/" + self._EDM
    ldir = self._sg.getDir( path )
    #if not ldir:
    #  return [None], [None], None, None
    #  raise ValueError("Couldn't access \"%s\" on file" % path)
    keys = ldir.GetListOfKeys() 
    _names = [key.GetName() for key in keys]
    names = []
    for n in _names:
      if n=="integrated":
        continue
      else:
        names.append(n)
    print(names)
    import re, numpy as np
    filt = re.compile('^et(?P<et_idx>\d+)_eta(?P<eta_idx>\d+)$')
    def transform(s):
      if s == "integrated": return (None,None)
      m = filt.match(s)
      if not m:
        self._fatal("Cannot parse folder '%s' bins", s)
      return (int(m.group('et_idx')), int(m.group('eta_idx')))
    bins = list(map(transform, names))

    from operator import itemgetter
    print(bins)
    highestEtIdx, highestEtaIdx = max([bin[0] for bin in bins]), max([bin[1] for bin in bins])
    if len(self._etBins) != highestEtIdx + 2:
      self._fatal("Number of et bins in the file do not match with the et bins provided")
    if len(self._etaBins) != highestEtaIdx + 2:
      self._fatal("Number of eta bins in the file do not match with the eta bins provided")
    quantities = self.getQuantitiesStr(keys)
    return ldir, quantities, highestEtIdx, highestEtaIdx

  def getQuantitiesStr(self,keys):
    # Retrieve all quantities available:
    checkDir = keys[0].ReadObj()
    import re
    # we remove each key bin string
    quantities = [re.sub("_et\d+_eta\d+|_integrated","",key.GetName()) for key in checkDir.GetListOfKeys() if not "_specialBins" in key.GetName()]
    return quantities

  def defaultPlotProfiles(self, dirName, quantityParser=returnArgument, logPrefix="Drawing profiles", entriesMap=None, norm=""):
    ldir, quantities, highestEtIdx, highestEtaIdx = self.retrieveQuantitiesInfo(dirName)
    def check(hists): return all([all(hlist) for hlist in hists])
    def update(s, kw, d): kw.update(d); return s.format(**kw);
    def getHists(key, **kwargs): return [[ldir.Get(update(key, kwargs,{'et' : et, 'eta':eta}))
                                          for eta in range(highestEtaIdx+1)] for et in range(highestEtIdx+1)]

    # Loop over all quantities
    total = 0
    for quantity in progressbar(quantities, len(quantities), prefix=logPrefix, 
                                logger = self._logger, measureTime = True):
      total += 1
      #if total == 1: break
      # Get all histograms:
      hists = getHists("et{et}_eta{eta}/{quantity}_et{et}_eta{eta}", quantity = quantity)
      specialBins = getHists("et{et}_eta{eta}/{quantity}_et{et}_eta{eta}_specialBins", quantity = quantity)
      if not check(hists): # compatibility with old files
        hists = getHists("et{et}_eta{eta}/{quantity}", quantity = quantity)
        specialBins = getHists("et{et}_eta{eta}/{quantity}_specialBins", quantity = quantity)
        if not check(hists):
          try:
            base, ringIdx = quantity.split("_")
            hists = getHists("et{et}_eta{eta}/{base}_et{et}_eta{eta}_{ringIdx}", base = base, ringIdx = ringIdx)
            specialBins = getHists("et{et}_eta{eta}/{base}_et{et}_eta{eta}_{ringIdx}_specialBins", base = base, ringIdx = ringIdx)
          except: pass
          if not check(hists):
            self._fatal("Could not read histograms at file for quantity %s. Hists retrieved are: %r", quantity, hists)
      if self._rebin:
        hists = [[h.Rebin(self._rebin) for h in histList] for histList in hists]
      normHists = [[histToUnitArea(h,norm) if norm is not None else h for h in histList] for histList in hists]
      integratedHist = ldir.Get("integrated/%s_integrated" % quantity)
      integratedSpecialBins = ldir.Get("integrated/%s_integrated_specialBins" % quantity)
      if not integratedHist:
        integratedHist = ldir.Get("integrated/%s" % quantity)
        integratedSpecialBins = ldir.Get("integrated/%s_specialBins" % quantity)
        if not integratedHist:
          integratedHist = ldir.Get("integrated/%s_integrated_%s" % (base, ringIdx))
          integratedSpecialBins = ldir.Get("integrated/%s_integrated_%s_specialBins" % (base, ringIdx))
          if not integratedHist:
            ldir.ls()
            self._fatal("Couldn't retrieve integrated hist for quantity: %s", quantity)
      normIntegratedHist = histToUnitArea(integratedHist, norm) if norm is not None else integratedHist
  
      etaCompCanvas, fullEtaCompCanvas, etaCompPaths, fullEtaCompPaths = \
        self.plotHists(hists = normHists, label=quantity, binLabel="et", xLabel = quantityParser(quantity),
                       compLabel="etaComp", refIdx=self._etaRefBin, maxIdx=highestEtaIdx,
                       maxOtherIdx=highestEtIdx, retrieveHists=retrieveEtaHists, 
                       refLabel = self._etaRefLabel, baseColor = self._baseEtaColor,
                       bins = self._etaBins, binsLegend = self._etaBinsLegend,
                       binBounderies = self._etBinsSpecial, binStr = 'E_{T}', binUnit = '[GeV]',
                       useRefFirst=self._useRefFirst, norm=norm,
                       notNormBaseHists = hists, specialBinHists = specialBins, entriesMap = entriesMap)
      etCompCanvas, fullEtCompCanvas, etCompPaths, fullEtCompPaths = \
        self.plotHists(hists = normHists, label=quantity, binLabel="eta", xLabel = quantityParser(quantity),  
                       compLabel="etComp", refIdx=self._etRefBin, maxIdx=highestEtIdx,
                       maxOtherIdx=highestEtaIdx, retrieveHists=retrieveEtHists, 
                       refLabel = self._etRefLabel, baseColor = self._baseEtColor,
                       bins = self._etBins, binsLegend = self._etBinsLegend,
                       binBounderies = self._etaBins, binStr = '#eta', 
                       useRefFirst=self._useRefFirst, norm=norm,
                       notNormBaseHists = hists, specialBinHists = specialBins, entriesMap = entriesMap)
      fullPhaseSpaceCanvas, fullPhaseSpacePath = \
        self.plotHists(hists = normIntegratedHist, label=quantity, xLabel = quantityParser(quantity),  
                       baseColor = self._fullPhaseSpaceColor,
                       notNormBaseHists = integratedHist, specialBinHists = integratedSpecialBins, entriesMap = entriesMap, drawopt='hist', 
                       useBlackLine=True, norm=norm)
      self.figures[quantity] = { 'etaComp' : etaCompCanvas
                               , 'fullEtaComp' : fullEtaCompCanvas
                               , 'etComp' : etCompCanvas
                               , 'fullEtComp' : fullEtCompCanvas
                               , 'fullPhaseSpace' : fullPhaseSpaceCanvas
                               }
      self.paths[quantity] = { 'etaComp' : etaCompPaths
                              , 'fullEtaComp' : fullEtaCompPaths
                              , 'etComp' : etCompPaths
                              , 'fullEtaComp' : fullEtCompPaths
                              , 'fullPhaseSpace' : fullPhaseSpacePath
                              }
      
  def plotHists(self, hists, label, xLabel, binLabel=None, compLabel=None, refIdx=None, maxIdx=None, maxOtherIdx=None, retrieveHists=None
               , refLabel=None, baseColor=[1.,.8039,0.], bins=None, binsLegend=None, binBounderies=None, binStr=None, binUnit=None
               , useRefFirst=False, notNormBaseHists=None, specialBinHists=None, entriesMap=None, drawopt='p', useBlackLine=None, norm=None):
    """
    Plot histograms looping over its row/columns
    """
    if label == "eta": 
      #from ROOT import gROOT, kFALSE
      #gROOT.SetBatch(kFALSE)
      #from RingerCore import keyboard
      #keyboard()
      pass
    if not isinstance(hists, (list,tuple)):
      maxIdx = 0; maxOtherIdx = -1
    import ROOT, numpy as np
    from operator import itemgetter
    from Gaugi.monet.PlotFunctions import RatioCanvas, AddHistogram, AddRatio, tobject_collector
    MCanvas = RatioCanvas if self._plotRatio and maxIdx != 0 else ROOT.TCanvas
    def addXAxisWorkaround(canvas, hists):
      axesLimits = [(hist.GetXaxis().GetBinLowEdge(1),hist.GetXaxis().GetBinUpEdge(hist.GetXaxis().GetNbins())) for hist in hists if hist]
      if not all(map(lambda x,y: x == y, axesLimits[1:], axesLimits[:-1])):
        limits = (min(axesLimits, key=itemgetter(0))[0], max(axesLimits, key=itemgetter(1))[1])
        hist = ROOT.TH1F("__xaxis","",1,limits[0], limits[1])
        AddHistogram(canvas, hist, drawopt="e1")
    def lAddHistogram( canvas, hist, *l ): AddHistogram(canvas, hist, drawopt=drawopt)
    def lAddRatio( canvas, hist, refHist ): AddRatio(canvas, hist, refHist, divide="", drawopt=drawopt, ratiodrawopt=drawopt, drawSpecialCases=False)
    compCanvas = [MCanvas("%s_%s%d_%s" % (label, binLabel, binIdx,compLabel), "", 500, 500) for binIdx in range(maxOtherIdx+1)]
    fullCompCanvas = MCanvas( "%s_%sAllRegions_%s" % (label, binLabel,compLabel) if binLabel is not None else "%s_FullPhaseSpace" % label, "", 500, 500)
    retrieveOtherHists = None
    if retrieveHists is not None:
      refHists = retrieveHists( hists, refIdx )
      totalRefHists = sumHists( refHists, '_total_%s%d' % (compLabel, refIdx), norm=norm )
      retrieveOtherHists = retrieveEtaHists if retrieveHists is retrieveEtHists else retrieveEtHists
      rearrangedHists = [retrieveOtherHists(hists, otherBinIdx) for otherBinIdx in range(maxOtherIdx+1) ] 
      map(addXAxisWorkaround, compCanvas, rearrangedHists)
      addXAxisWorkaround( fullCompCanvas, [sumHists(retrieveHists(hists, binIdx), '_dummyTotal%d' % binIdx) for binIdx in range(maxIdx+1)])
    else:
      refHists = []
      totalRefHists = hists
    if useRefFirst and maxIdx != 0: 
      map(lAddHistogram, compCanvas, refHists)
      if totalRefHists: lAddHistogram(fullCompCanvas, totalRefHists) 
    for binIdx in range(maxIdx+1):
      binHists = retrieveHists( hists, binIdx ) if retrieveHists else []
      if binIdx == refIdx and useRefFirst: continue
      map(lAddRatio if self._plotRatio and maxIdx != 0 else lAddHistogram, compCanvas, binHists, refHists)
      l = (fullCompCanvas, sumHists(binHists, '_total_%s%d' % (compLabel, binIdx), norm=norm) if binHists else hists, totalRefHists) 
      if l[1]: 
        lAddRatio(*l) if self._plotRatio and maxIdx != 0 else lAddHistogram(*l)
    paths = []
    for otherBinIdx in range(maxOtherIdx+2):
      can = compCanvas[otherBinIdx] if otherBinIdx < maxOtherIdx+1 else fullCompCanvas
      if otherBinIdx > maxOtherIdx: otherBinIdx = None
      specialBinsLegend = None
      if otherBinIdx is not None and maxIdx != 0:
        specialBinsLegend = retrieveSpecialBinsLegend( label, retrieveOtherHists(notNormBaseHists, otherBinIdx)
                                                     , retrieveOtherHists(specialBinHists, otherBinIdx), entriesMap )
      path = formatQuantity(can = can, outputPath = self.outputPath
                           , xLabel = xLabel, divLabel="ratio"
                           , quantity_text = ("#splitline{Reference used in ratio:}{" + self._etaRefLabel + "}" if self._plotRatio and maxIdx != 0 else '')
                           , colorarr = fadeToBlack(baseColor, len(bins)) if bins else [ROOT.TColor.GetColor(*baseColor) if isinstance(baseColor, (list, tuple, np.ndarray,)) else baseColor]
                           , useBlackLine = useBlackLine
                           #, stylearr = [20] + [24]*(len(self._etaBins)-1)
                           , stylearr = range(20,20+len(bins)) if bins else [20]
                           , markersizes = [0.5] * len(bins) if bins else [0.5]
                           , legend = rearrange( binsLegend, refIdx, useRefFirst ) if binsLegend else None
                           , dataLegend = self._dataLegend
                           , binBounderies = getBounderies(binBounderies, otherBinIdx) if binBounderies else "Full phase space"
                           , binStr = binStr, binUnit = binUnit
                           , specialBinsLegend = specialBinsLegend
                           , norm = norm
                           ) if can.GetListOfPrimitives().GetEntries() else None
      if otherBinIdx is None: 
        fullCompPaths = path
      else:
        paths.append(path)
    tobject_collector = []
    if maxIdx != 0:
      return compCanvas, fullCompCanvas, paths, fullCompPaths
    else:
      return compCanvas, fullCompCanvas


