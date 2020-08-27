__all__ = ['StandardQuantityProfiles']

from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from ProfileTools  import ProfileToolBase
from ProfileTools.constants import ( standardQuantitiesEtaEdge, standardQuantitiesHighEdges, standardQuantitiesLowerEdges
                                   , standardQuantitiesSpecialBins, standardQuantitiesNBins, standardQuantitiesPDFsHighEdges
                                   , standardQuantitiesPDFsLowerEdges, standardQuantitiesPDFsNBins )
from prometheus import Dataframe as DataframeEnum






class StandardQuantityProfiles( ProfileToolBase ):

  def __init__(self, name, dataframe, **kw):
    ProfileToolBase.__init__(self, name, **kw)
    self.doSpecialBins  = False
    self.standardQuantities = standardQuantitiesNBins.keys()

  def setAndCheckStandardQuantities(self, values):
    self.standardQuantities = []
    from CommonTools.constants import electronLatexStr
    if not isinstance(values, (list,tuple)):
      values = [values]
    for value in values:
      try:
        standardQuantitiesHighEdges[value]
        standardQuantitiesLowerEdges[value]
        standardQuantitiesNBins[value]
        electronLatexStr(value)
        self.standardQuantities.append(value)
      except KeyError as e:
        MSG_WARNING( self,"Ignoring quantity '%s' due to error: %s", e)

  def initialize(self):
    ProfileToolBase.initialize()
    sg = selg.getStoreGateSvc()
    from ROOT import TH1F, TH1I
    # Fill all histograms needed
    from ProfileTools.constants import electronLatexStr
    def createHist(var, binLabel):
      latexvar = electronLatexStr( var )
      nBins = standardQuantitiesNBins[var]
      lb = standardQuantitiesLowerEdges[var]
      ub = standardQuantitiesHighEdges[var]
      sg.addHistogram(TH1F(var + "_" + binLabel, latexvar + ' profile;' + latexvar + ';Counts/bin', nBins, lb, ub ))
      sg.addHistogram(TH1I(var + "_" + binLabel + "_specialBins", latexvar + ' special bins;Special bins;Counts/bin', 3, 0, 3 ))
    for etBinIdx in range(len(self._etBins)-1):
      for etaBinIdx in range(len(self._etaBins)-1):
        path = self.getPath(etBinIdx, etaBinIdx)
        sg.mkdir( path )
        MSG_DEBUG( self,'Initializing path: %s', path)
        for var in self.standardQuantities: createHist(var, self.binStr(etBinIdx,etaBinIdx))
    path_integrated = self.getPath()
    sg.mkdir( path_integrated )
    MSG_DEBUG( self,'Initializing path: %s', path_integrated)
    for var in self.standardQuantities: createHist(var, self.binStr())
    return StatusCode.SUCCESS

  def execute(self, context):
    sg = selg.getStoreGateSvc()
    if self._doTrigger:
      obj = context.getHandler('HLT__FastCaloContainer')
    elif self._dataframe is DataframeEnum.Electron_v1:
      obj   = context.getHandler( "ElectronContainer" )
    elif self._dataframe is DataframeEnum.Photon_v1:
      obj    = context.getHandler( "PhotonContainer" )
    else:
      obj    = context.getHandler( "ElectronContainer" )

    # If is trigger, the position must use the trigger et/eta positions.
    from Gaugi.constants import GeV 
    from ProfileTools.constants import specialElectronBins
    etBinIdx, etaBinIdx = self._retrieveBinIdx( obj.et()/GeV, abs(obj.eta()) )
    if etBinIdx is None or etaBinIdx is None:
      MSG_WARNING( self,"Ignoring event with none index. Its et[GeV]/eta is: %f/%f", obj.et()/GeV, obj.eta())
      return StatusCode.SUCCESS

    # Force this to be the offline object
    el = context.getHandler('ElectronContainer')
    
    path = self.getPath(etBinIdx, etaBinIdx)
    path_integrated = self.getPath()

    def getQuantities(obj):
      return {'weta2':obj.weta2(),'f1':obj.f1(),'reta':obj.reta(),'eratio':obj.eratio(), 'reta':obj.reta(),'rphi':obj.rphi(),
            'rhad':obj.rhad(),'deltaEta1':obj.deltaEta1(),'wtots1':obj.wtots1(), 'd0significance':obj.trackParticle().d0significance(),
            'eProbabilityHT':obj.trackParticle().eProbabilityHT(),'trackd0pvunbiased':obj.trackParticle().d0(),
            'DeltaPOverP':obj.trackParticle().DeltaPOverP(),'TRT_PID':obj.trackParticle().trans_TRT_PID(),'f3':obj.f3(),
            'deltaPhiRescaled2':obj.deltaPhiRescaled2()}
    quantitiesDict=getQuantities(el)

    for var in self.standardQuantities:
      quantityVal = quantitiesDict[var]
      # TODO if doSpecialBins
      try:
        try: 
          index = specialElectronBins[var].index(quantityVal)
          sg.histogram(path+'/'+var+"_"+self.binStr(etBinIdx,etaBinIdx)+"_specialBins").Fill(index)
          sg.histogram(path_integrated+'/'+var+"_"+self.binStr()+"_specialBins").Fill(index)
          continue
        except (KeyError, ValueError):
          pass
        sg.histogram(path+'/'+var+"_"+self.binStr(etBinIdx,etaBinIdx)).Fill(quantityVal)
        sg.histogram(path_integrated+'/'+var+"_"+self.binStr()).Fill(quantityVal)
      except AttributeError as e:
        MSG_FATAL( self,"Couldn't fill histogram at path: %s", e)

    return StatusCode.SUCCESS

  def finalize(self):
    ProfileToolBase.finalize()
    self.fina_lock()
    return StatusCode.SUCCESS
