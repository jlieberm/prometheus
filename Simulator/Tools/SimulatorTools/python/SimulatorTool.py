
__all__ = ['SimulatorTool']


from prometheus import Algorithm
from Gaugi.messenger.macros import *
from Gaugi import StatusCode
import numpy as np


def PlotShapes( h1, h2, name1, name2, varname, outname ,drawopt='hist'):
  from monet.PlotFunctions import *
  from monet.TAxisFunctions import *
  from monet.utilities import *
  from ROOT import TCanvas, kBlack, kAzure
  h1 = NormHist(h1, 1/h1.GetMaximum())
  h2 = NormHist(h2, 1/h2.GetMaximum())
  outcan = TCanvas( 'canvas', "", 700, 500 ) 
  h1.SetLineColor(kAzure-5)
  h1.SetFillColor(kAzure-4)
  h1.SetMarkerColor(kAzure-4)
  h2.SetLineColor(kBlack)
  AddHistogram(outcan,h1,drawopt=drawopt) 
  AddHistogram(outcan,h2,drawopt=drawopt) 
  h1.SetStats(False)
  h2.SetStats(False)
  MakeLegend(outcan,.5,.77,.89,.97,option='p',textsize=14, names=[name1,name2], ncolumns=1, 
             squarebox=False, doFixLength=False)
  AutoFixAxes(outcan,ignoreErrors=False)
  FormatCanvasAxes(outcan, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  SetAxisLabels(outcan,varname,'Count')
  FixYaxisRanges(outcan, ignoreErrors=True, yminc=-eps )
  outcan.SaveAs(outname+".pdf")
  return outname+'.pdf'


def reshape_to_square_array( array ):
  import numpy as np
  size = array.shape
  array_copy = np.zeros( (max(size),max(size)) )
  def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
      yield l[i:i + n]
  # duplicate the column
  if size[0] > size[1]:
    for x in range(size[0]):
      gy = chunks( range(size[0]), int(size[0]/float(size[1])))
      for y, gy_ in enumerate(gy):
        for y_ in gy_:
          array_copy[x][y_] = array[x][y]
  else:
    for y in range(size[1]):
      gx = chunks( range(size[1]), int(size[1]/float(size[0])))
      for x, gx_ in enumerate(gx):
        for x_ in gx_:
          array_copy[x_][y] = array[x][y]
  return array_copy


class SimulatorTool( Algorithm ):


  def __init__( self, name, **kw ):
    Algorithm.__init__( self, name )


  def initialize(self):

    Algorithm.initialize(self)
    sg = self.getStoreGateSvc()
    
    from ROOT import TH1F, TH2F
    sg.addHistogram( TH1F( "TotalEnergy", ";Energy;Count", 100, 0, 100 ) ) 
    sg.addHistogram( TH2F( "layer_0_2D", "First EM Layer; Energy (eta); Energy (phi)" , 96,0,96,96,0,96) )
    sg.addHistogram( TH2F( "layer_1_2D", "Second EM Layer; Energy (eta); Energy (phi)", 12,0,12,12,0,12) )
    sg.addHistogram( TH2F( "layer_2_2D", "Third EM Layer; Energy (eta); Energy (phi)" , 12,0,12,12,0,12) )

   
    sg.mkdir("Cells")
    hists_per_layer = [(3, 96), (12, 12), (12, 6)]
    for layer, hists in enumerate(hists_per_layer):
      for x in range( hists[0] ):
        for y in range( hists[1] ):
          sg.addHistogram( TH1F( ("layer_%d_x%d_y%d")%(layer,x,y), ";Energy;Count", 140, -5, 65 ) ) 

    
    sg.mkdir("rings")
    for ring in range(56):
      sg.addHistogram( TH1F( ("ring_%d")%(ring), ";Energy;Count", 500, 0, 1000 ) ) 
    sg.addHistogram( TH2F( ("rings"), ";Energy;Count", 56,0,56,500, 0, 1000 ) ) 
    sg.addHistogram( TH1F( "ring_profile", ";Energy;Count", 56, 0, 56 ) ) 


    sg.mkdir( "showers" )

    sg.addHistogram( TH1F("reta", ";;;", 100, 0, 1) )
    sg.addHistogram( TH1F("rphi", ";;;", 100, 0, 1) )
    sg.addHistogram( TH1F("eratio", ";;;", 100, 0, 1) )
    sg.addHistogram( TH1F("f1", ";;;", 100, 0, 1) )
    sg.addHistogram( TH1F("f3", ";;;", 100, 0, 1) )


    self.init_lock()
    return StatusCode.SUCCESS 
 
  def execute(self, context):
   
    from EventGeant import CaloGAN_Definitions
    sg = self.getStoreGateSvc()
    cells = self.getContext().getHandler("CaloCellsContainer")
    rings = self.getContext().getHandler("CaloRingsContainer").ringsE()
    showers = self.getContext().getHandler( "ShowerShapesContainer" )
    
    for layer, layer_enum in enumerate( [CaloGAN_Definitions.FIRST_LAYER, CaloGAN_Definitions.SECOND_LAYER, CaloGAN_Definitions.THIRD_LAYER]):
      collections = cells.getCollection( layer_enum )
      for c in collections:
        key = ('Cells/layer_%d_x%d_y%d') % ( layer, c.x(), c.y() )
        sg.histogram( key ).Fill( c.energy() )
    sg.histogram( "TotalEnergy" ).Fill( cells.totalEnergy() )



    for r, energy in enumerate(rings):
      sg.histogram('rings/ring_%d' % r).Fill(energy)
      sg.histogram('rings/rings' ).Fill(r,energy)


    sg.histogram( "showers/reta" ).Fill( showers.reta() )
    sg.histogram( "showers/rphi" ).Fill( showers.rphi() )
    sg.histogram( "showers/eratio" ).Fill( showers.eratio() )
    sg.histogram( "showers/f1" ).Fill( showers.f1() )
    sg.histogram( "showers/f3" ).Fill( showers.f3() )
  

    return StatusCode.SUCCESS 




  def finalize(self):

    sg = self.getStoreGateSvc()
    
    # Fill all 2D histograms 
    hists_per_layer = [(3, 96), (12, 12), (12, 6)]
    for layer, hists in enumerate(hists_per_layer):
      E_energy = np.zeros( hists )
      for x in range( hists[0] ):
        for y in range( hists[1] ):
          E_energy[x][y] = sg.histogram( "Cells/layer_%d_x%d_y%d" % (layer,x,y) ).GetMean()
      #prepare to reshape
      E_energy = reshape_to_square_array(E_energy)
      for (x,y), energy in np.ndenumerate(E_energy):
        sg.histogram( "layer_%d_2D"%layer ).SetBinContent( x+1, y+1, energy )  
  
    for r in range(56):
      mean_energy = sg.histogram('rings/ring_%d' % r).GetMean()
      sg.histogram('rings/ring_profile').SetBinContent( r+1, mean_energy )

    self.fina_lock()
    return StatusCode.SUCCESS 




  def plot( self, store1, store2, particle_1, particle_2 ):

    import ROOT
    ROOT.gErrorIgnoreLevel=ROOT.kWarning
    from monet.AtlasStyle import SetAtlasStyle
    SetAtlasStyle()

    plotnames = {}
    varnames_tex = ['E_{ratio}','R_{#eta}','R_{#phi}', 'f_{1}', 'f_{3}']
    varnames = ['eratio','reta','rphi','f1','f3']
    for idx, var in enumerate(varnames):
      h1 = store1.histogram('showers/'+var)
      h2 = store2.histogram('showers/'+var)
      plotnames[var] = PlotShapes( h1, h2, particle_1, particle_2, varnames_tex[idx], var )
    
    h1 = store1.histogram('rings/ring_profile')
    h2 = store2.histogram('rings/ring_profile')
    plotnames['rings'] = PlotShapes( h1, h2, particle_1, particle_2, 'rings', 'rings' )
 








