
__all__ = ["Collector"]

from prometheus import Algorithm
from prometheus import Dataframe as DataframeEnum
from Gaugi import StatusCode, NotSet, retrieve_kw, progressbar
from Gaugi import csvStr2List, expandFolders, save, load
from Gaugi.messenger.macros import *
from Gaugi.messenger  import Logger
from Gaugi.constants import GeV
from Gaugi.enumerations import StatusWatchDog
from Gaugi import EnumStringification
import numpy as np




from CommonTools import AlgorithmTool

class Collector( AlgorithmTool ):

  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    self._event = {}
    self._event_label = []
    self._save_these_bins = list()
    self._extra_features = list()
    self._outputname = retrieve_kw( kw, 'outputname', 'sample.pic'  )
    self._doTrack    = retrieve_kw( kw, 'doTrack'   , False         )


  def setEtBinningValues( self, etbins ):
    self._etbins = etbins


  def setEtaBinningValues( self, etabins ):
    self._etabins = etabins


  def SaveThisBin( self, key ):
    self._save_these_bins.append( key )

  def AddFeature( self, key ):
    self._extra_features.append( key )


  def initialize(self):
    AlgorithmTool.initialize(self) 
    for etBinIdx in range(len(self._etbins)-1):
      for etaBinIdx in range(len(self._etabins)-1):
        self._event[ 'et%d_eta%d' % (etBinIdx,etaBinIdx) ] = None
        #self._event[ 'et%d_eta%d' % (etBinIdx,etaBinIdx) ] = []

    self._event_label.append( 'avgmu' )

    # Add fast calo ringsE
    self._event_label.extend( [ 'L2Calo_ring_%d'%r for r in range(100) ] )
    
    self._event_label.extend( [ 'L2Calo_et',
                                'L2Calo_eta',
                                'L2Calo_phi',
                                'L2Calo_reta',
                                #'L2Calo_rphi',
                                'L2Calo_eratio',
                                'L2Calo_f1',
                                ] )


    if self._doTrack:
      self._event_label.extend( ['L2_pt',
                                 'L2_eta',
                                 'L2_phi',
                                 'L2_trkClusDeta',
                                 'L2_trkClusDphi',
                                 'L2_etOverPt'] )


    self._event_label.extend( [
                                # Offline variables
                                'el_lhtight',
                                'el_lhmedium',
                                'el_lhloose',
                                'el_lhvloose',
                                'et',
                                'eta',
                                'phi',
                                'et',
                                'eratio',
                                'reta',
                                'rphi',
                                'f1',
                                'f3',
                                'rhad',
                                'rhad1',
                                'wtots1',
                                'weta1',
                                'weta2',
                                'e277',
                                'deltaE',
                                ] )


    self._event_label.extend( self._extra_features )

    return StatusCode.SUCCESS

  def fill( self, key , event ):

    if self._event[key]:
      self._event[key].append( event )
    else:
      self._event[key] = [event]

  def execute(self, context):
    
    elCont    = context.getHandler( "ElectronContainer" )
    eventInfo = context.getHandler( "EventInfoContainer" )
    fc        = context.getHandler( "HLT__FastCaloContainer" )
    trk       = context.getHandler( "HLT__FastElectronContainer" )

    if self._doTrack and not (trk.size()>0):
      # skip if the event does not fast electron feature in the 
      # trigger element.
      return StatusCode.SUCCESS


    from CommonTools.utilities import RetrieveBinningIdx
    etBinIdx, etaBinIdx = RetrieveBinningIdx( fc.et()/1000., abs(fc.eta()), self._etbins, self._etabins, logger=self._logger )
    if etBinIdx < 0 or etaBinIdx < 0:
      #MSG_WARNING( self,'Skipping event since et/eta idx does not match with the current GEO/Energy position.')
      return StatusCode.SUCCESS

    key = ('et%d_eta%d') % (etBinIdx, etaBinIdx)
    if (len(self._save_these_bins) > 0) and (not key in self._save_these_bins):
        return StatusCode.SUCCESS
    

    event_row = list()
    # event info
    event_row.append( eventInfo.avgmu() )

    # fast calo features
    event_row.extend( fc.ringsE()   )
    event_row.append( fc.et()       )
    event_row.append( fc.eta()      )
    event_row.append( fc.phi()      )
    event_row.append( fc.reta()     )
    #event_row.append( fc.rphi()     )
    event_row.append( fc.eratio()   )
    event_row.append( fc.f1()   )

    # fast electron features
    if self._doTrack:
      event_row.append( trk.pt() )
      event_row.append( trk.eta() )
      event_row.append( trk.phi() )
      event_row.append( trk.trkClusDeta() )
      event_row.append( trk.trkClusDphi() )
      event_row.append( trk.etOverPt() )


    from EventAtlas import EgammaParameters
    # Offline Shower shapes
    event_row.append( elCont.accept( "el_lhtight"  ) )
    event_row.append( elCont.accept( "el_lhmedium" ) )
    event_row.append( elCont.accept( "el_lhloose"  ) )
    event_row.append( elCont.accept( "el_lhvloose" ) )
    
    event_row.append( elCont.et() )
    event_row.append( elCont.eta() )
    event_row.append( elCont.phi() )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Eratio ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Reta ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rphi ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.f1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.f3 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rhad ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rhad1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.wtots1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.weta1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.weta2 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.e277 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.DeltaE ) )
  

    for feature in self._extra_features:
      if self.doTrigger:
        # Get the decoration from HLT electron or fast calo (only for skimmed)
        passed = self.accept(feature)
      else:
        # Get de decision from Offline electron
        passed = elCont.accept(feature)
      event_row.append( passed )

    self.fill(key , event_row)


    return StatusCode.SUCCESS
  

  def finalize( self ):
    
    from Gaugi import save, mkdir_p
    for etBinIdx in range(len(self._etbins)-1):
      for etaBinIdx in range(len(self._etabins)-1):
       
        key =  'et%d_eta%d' % (etBinIdx,etaBinIdx)         
        mkdir_p( self._outputname ) 
        if self._event[key] is None: 
          continue

        d = { 
            "features"  : self._event_label,
            "etBins"    : self._etbins,
            "etaBins"   : self._etabins,
            "etBinIdx"  : etBinIdx,
            "etaBinIdx" : etaBinIdx
            }

        d[ 'pattern_'+key ] = np.array( self._event[key] )
        MSG_INFO( self, 'Saving %s with : (%d, %d)', key, d['pattern_'+key].shape[0], d['pattern_'+key].shape[1] )
        save( d, self._outputname+'/'+self._outputname+"_"+key , protocol = 'savez_compressed')
    return StatusCode.SUCCESS





