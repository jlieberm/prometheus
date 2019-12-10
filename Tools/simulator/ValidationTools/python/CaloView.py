
__all__ = ['CaloView']


from prometheus import Algorithm
from Gaugi.messenger.macros import *
from Gaugi import StatusCode, retrieve_kw
import numpy as np

class CaloView( Algorithm ):


  def __init__( self, name, **kw ):
    Algorithm.__init__( self, name )
    self._basepath = retrieve_kw( kw, 'basepath' , '')


  def initialize(self):

    Algorithm.initialize(self)
    sg = self.getStoreGateSvc()
    
    from ROOT import TH1F, TH2F
    sg.mkdir( self._basepath + '/CaloView' )
    sg.addHistogram( TH2F( "lateral_view", ";;;", 4000, -240, 240, 4000, -240, 240) )
    sg.addHistogram( TH2F( "layer_0", "First EM Layer; Energy (eta); Energy (phi)" , 3,0,3,96,0,96)   )
    sg.addHistogram( TH2F( "layer_1", "Second EM Layer; Energy (eta); Energy (phi)", 12,0,12,12,0,12) )
    sg.addHistogram( TH2F( "layer_2", "Third EM Layer; Energy (eta); Energy (phi)" , 12,0,12,6,0,6)   )

    hists_per_layer = [(3, 96), (12, 12), (12, 6)]
    for layer, hists in enumerate(hists_per_layer):
      for x in range( hists[0] ):
        for y in range( hists[1] ):
          sg.addHistogram( TH1F( ("layer_%d_x%d_y%d")%(layer,x,y), ";Energy;Count", 140, -5, 65 ) ) 

    self.init_lock()
    return StatusCode.SUCCESS 
 
  def execute(self, context):
   
    from EventLorenzet import CaloGAN_Definitions
    sg = self.getStoreGateSvc()
    cells = self.getContext().getHandler("CaloCellsContainer")
    
    for layer, layer_enum in enumerate( [CaloGAN_Definitions.FIRST_LAYER, CaloGAN_Definitions.SECOND_LAYER, CaloGAN_Definitions.THIRD_LAYER]):
      collections = cells.getCollection( layer_enum )
      for c in collections:
        key = ('%s/CaloView/layer_%d_x%d_y%d') % ( self._basepath, layer, c.x(), c.y() )
        sg.histogram( key ).Fill( c.energy() )
  
    for point in cells.getPoints():
      sg.histogram( self._basepath+"/CaloView/lateral_view" ).Fill( point.z(), point.x(), point.energy() )

    return StatusCode.SUCCESS 




  def finalize(self):

    sg = self.getStoreGateSvc()
    # Fill all 2D histograms 
    hists_per_layer = [(3, 96), (12, 12), (12, 6)]
    for layer, hists in enumerate(hists_per_layer):
      E_energy = np.zeros( hists )
      for x in range( hists[0] ):
        for y in range( hists[1] ):
          E_energy[x][y] = sg.histogram( self._basepath+"/CaloView/layer_%d_x%d_y%d" % (layer,x,y) ).GetMean()
      for (x,y), energy in np.ndenumerate(E_energy):
        sg.histogram( self._basepath+"/CaloView/layer_%d"%layer ).SetBinContent( x+1, y+1, energy )  
    self.fina_lock()
    return StatusCode.SUCCESS 




