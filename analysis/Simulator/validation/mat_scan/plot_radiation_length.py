from monet.PlotFunctions import *
from monet.TAxisFunctions import *
from monet.utilities import *
from ROOT import TH1F, TLatex, gPad
from ROOT import kRed, kGray, kBlue
from monet.AtlasStyle import SetAtlasStyle
SetAtlasStyle()
import ROOT

def LZTALabel(x,y,text,color=1):
  p = TLatex(); 
  p.SetNDC();
  p.SetTextFont(72);
  p.SetTextColor(color);
  p.DrawLatex(x,y,"LZTA "+text);
  #p.DrawLatex(x,y,"#sqrt{s}=900GeV");



def fill( h, values ):
  for idx, v in enumerate(values):
    h.SetBinContent(idx,v)


# Simple parser to get the x0 and lambda values from the cmd output 
def get_values(path, varname):
  
  file = open(path,'r')
  lines = file.readlines()
  all_values = []
  for line in lines:
    values = []
    if 'Theta' in line:
      continue
    for s in line.split(' '):
      if s!='':
        s=s.replace('\n','')
        values.append(float(s))
    if 'x0' == varname:
      all_values.append(values[3])
    elif 'L' == varname:
      all_values.append(values[4])
    else:
      all_values.append(values)
  return all_values

import numpy as np
from ROOT import TCanvas, kBlack, kAzure

#eta=atanh(cos(theta))
theta = np.radians(np.array( list(range(90+1))))
eta=  -1*np.log(np.tan( theta/2. ) )
print(theta)


eta[0] = 5
eta=eta[::-1]
eta = eta[0:75].tolist()


deadMaterialBeforeECal = get_values('data/matScan_deadMaterialBeforeECal.txt','x0')[0:75]
em1= get_values('data/matScan_em1.txt','x0')[0:75]
em2= get_values('data/matScan_em2.txt','x0')[0:75]
em3= get_values('data/matScan_em3.txt','x0')[0:75]

 
drawopt = 'hist'
canvas = TCanvas( 'canvas', "", 500, 500 ) 

h_deadMaterialBeforeECal=TH1F("h1", "", len(eta)-1 , np.array(eta) )
h_em1= TH1F("h2", "", len(eta)-1 , np.array(eta) )
h_em2= TH1F("h3", "", len(eta)-1 , np.array(eta) )
h_em3= TH1F("h4", "", len(eta)-1 , np.array(eta) )

fill( h_deadMaterialBeforeECal, deadMaterialBeforeECal )
fill( h_em1, em1 )
fill( h_em2, em2 )
fill( h_em3, em3 )


h_deadMaterialBeforeECal.SetLineColor( kGray )
h_deadMaterialBeforeECal.SetMarkerColor( kGray )
h_em1.SetLineColor( kBlue )
h_em1.SetMarkerColor( kBlue )
h_em2.SetLineColor( kBlue+2 )
h_em2.SetMarkerColor( kBlue+2 )
h_em3.SetLineColor( kBlack )
h_em3.SetMarkerColor( kBlack )


AddHistogram(canvas,h_deadMaterialBeforeECal,drawopt=drawopt) 
AddHistogram(canvas,h_em1,drawopt=drawopt) 
AddHistogram(canvas,h_em2,drawopt=drawopt) 
AddHistogram(canvas,h_em3,drawopt=drawopt) 




#LZTALabel(0.2,0.88,"Simulation",color=1)

MakeLegend(canvas,.2,.70,.4,.90,option='p',textsize=14, names=['DeadMaterialBeforeECal','EM1','EM2','EM3'], ncolumns=1, 
           squarebox=True, doFixLength=False)
AutoFixAxes(canvas,ignoreErrors=False)
FormatCanvasAxes(canvas, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
SetAxisLabels(canvas,'#eta',"Radiation Length [X_{0}]")
FixYaxisRanges(canvas, ignoreErrors=True, yminc=-eps )
canvas.SaveAs('x0.pdf')




















