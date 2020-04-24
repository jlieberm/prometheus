
__all__ = ['Profiles']


from Gaugi import Algorithm
from Gaugi.messenger.macros import *
from Gaugi import StatusCode, retrieve_kw
import numpy as np

class Profiles( Algorithm ):

  def __init__( self, name, **kw ):
    Algorithm.__init__( self, name )
    self._basepath = retrieve_kw( kw, 'basepath', '')


  def initialize(self):

    Algorithm.initialize(self)
    sg = self.getStoreGateSvc()
    
    from ROOT import TH1F, TH2F

    sg.mkdir( self._basepath+"/Profiles" )
    sg.addHistogram( TH1F("res_et" 			,"#E_{TTruth}-#E_{T,Cluster};res_{E_{T}};Count",100,-40,40) )
    sg.addHistogram( TH1F("res_eta"			, "#eta_{Truth}-#eta_{Cluster};res_{#eta};Count",100,-2,2 ) )
    sg.addHistogram( TH1F("res_phi"			, "#phi_{Truth}-#phi_{Cluster};res_{#phi};Count",100,-2,2 ) )
    sg.addHistogram( TH1F("et"   	      , ";Count;E_{T};"       , 100, 0.0  , 100 ) )
    sg.addHistogram( TH1F("eta"  	      , ";Count;#eta;"        , 100, -1.5 , 1.5 ) )
    sg.addHistogram( TH1F("phi"  	      , ";Count;#phi;"        , 100, -3.2 , 3.2 ) )
    sg.addHistogram( TH1F("f1"   	      , ";Count;f_{1};"       , 100, -0.02, 0.7 ) )
    sg.addHistogram( TH1F("f3"   	      , ";Count;f_{3};"       , 200, -0.05, 0.15) )
    sg.addHistogram( TH1F("weta2"	      , ";Count;W_{#eta2};"   , 100, 0.005, 0.02) )
    sg.addHistogram( TH1F("reta" 	      ,  ";Count;R_{#eta};"   , 200, 0.8  , 1.10) )
    sg.addHistogram( TH1F("rphi" 	      , ";Count;R_{#phi};"    , 200, 0.45 , 1.05) )
    sg.addHistogram( TH1F("rhad" 	      , ";Count;R_{had};"     , 200, -0.05, 0.05) )
    sg.addHistogram( TH1F("eratio"      , ";Count;E_{ratio};"  	, 100, 0.0  , 1.05) )


    sg.mkdir( self._basepath+"/Profiles/rings" )
    sg.addHistogram( TH1F("rings_profile", "Ring Profile;#ring;E[Energy] [GeV]", 92, 0, 92 ) ) 
    for idx in range(92):
      sg.addHistogram( TH1F("ring_"+str(idx), "ring %d; ; E_{T} [GeV]; Count"%idx, 100, 0, 100) )

    
    
    
    self.init_lock()
    return StatusCode.SUCCESS 


 
  def execute(self, context):
    
    sg = self.getStoreGateSvc()
    
    cluster = self.getContext().getHandler( "Truth__CaloClusterContainer" )
    
    if cluster.isValid():
    	sg.histogram(self._basepath+"/Profiles/et").Fill( cluster.et()/1.e3 )
    	sg.histogram(self._basepath+"/Profiles/eta").Fill( cluster.eta() )
    	sg.histogram(self._basepath+"/Profiles/phi").Fill( cluster.phi() )
    	sg.histogram(self._basepath+"/Profiles/f1").Fill( cluster.f1() )
    	sg.histogram(self._basepath+"/Profiles/f3").Fill( cluster.f3() )
    	sg.histogram(self._basepath+"/Profiles/reta").Fill( cluster.reta() )
    	sg.histogram(self._basepath+"/Profiles/rphi").Fill( cluster.rphi() )
    	sg.histogram(self._basepath+"/Profiles/rhad").Fill( cluster.rhad() )
    	sg.histogram(self._basepath+"/Profiles/weta2").Fill( cluster.weta2() )
    	sg.histogram(self._basepath+"/Profiles/eratio").Fill( cluster.eratio() )
    

    ringer = self.getContext().getHandler( "Truth__CaloRingsContainer" )
    
    if ringer.isValid():
    	for idx in range(92):
    		sg.histogram(self._basepath+"/Profiles/rings/ring_"+str(idx)).Fill( ringer.ringsE().at(idx)/1.e3 )
    
    
    return StatusCode.SUCCESS 




  def finalize(self):
    
    sg = self.getStoreGateSvc()
    for idx in range(92):
      energy = sg.histogram(self._basepath+'/Profiles/rings/ring_'+str(idx)).GetMean()
      sg.histogram(self._basepath+'/Profiles/rings/rings_profile').SetBinContent( idx+1, energy )
 
    self.fina_lock()
    return StatusCode.SUCCESS 




