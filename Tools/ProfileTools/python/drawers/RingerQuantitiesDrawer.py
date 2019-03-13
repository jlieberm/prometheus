__all__ = ['RingerQuantitiesDrawer']

from DrawerBase import *
from Gaugi.utilites import retrieve_kw, ensureExtension

from collections import OrderedDict
layers = OrderedDict([ ('PS', 8),
                       ('EM1', 64),
                       ('EM2', 8),
                       ('EM3', 8),
                       ('HAD1', 4),
                       ('HAD2', 4),
                       ('HAD3', 4) ])

def ringParser(quantity):
  _, idx = quantity.split('_')
  idx = int(idx)
  cTotal = 0
  for key, nRings in layers.iteritems():
    if idx < cTotal+nRings: break
    cTotal += nRings
  return 'Ring_{(%s,%d;%d)} [MeV]' % (key, idx-cTotal, idx)


class RingerQuantitiesDrawer(DrawerBase):

  def __init__(self, **kw):
    DrawerBase.__init__(self, kw)

  def plot(self, **kw):
    from Gaugi.utilities import mkdir_p
    mkdir_p( self.outputPath )
    self.plotRingProfiles(**kw)

  def plotRingProfiles(self, **kw):
    self.defaultPlotProfiles("RingProfiles", logPrefix="Drawing ring profiles", quantityParser=ringParser)
  #def plotRingProfiles

  def _plot_mean_rings(self):
    # Plot ringer mean shapes
    h_mean_data = TH1F('h_mean_data','',100, 0, 100)

    for bin in range(100):
      self.setDir('MonteCarlo')
      h_mc = sumAllRegions('rings/ring_'+str(bin))
      self.setDir('Data')
      h_data = sumAllRegions('rings/ring_'+str(bin))
      h_mean_data.SetBinContent(bin+1, h_data.GetMean())
    canvas3 = TCanvas('canvas3','canvas3',2500,1600)
    
    drawopt='pE1' 
    canvas3.cd()  
    top = TPad("pad_top", "This is the top pad",0.0,ratio_size_as_fraction,1.0,1.0)
    top.SetBottomMargin(0.0)
    top.SetBottomMargin(0.06/float(top.GetHNDC()))
    #top.SetTopMargin   (0.04/float(top.GetHNDC()))
    top.SetRightMargin (0.05 )
    top.SetLeftMargin  (0.16 )
    top.SetFillColor(0)
    top.Draw(drawopt)
    
    canvas3.cd()
    bot = TPad("pad_bot", "This is the bottom pad",0.0,0.0,1.0,ratio_size_as_fraction)
    bot.SetBottomMargin(0.10/float(bot.GetHNDC()))
    #bot.SetTopMargin   (0.02/float(bot.GetHNDC()))
    bot.SetTopMargin   (0.0)
    bot.SetRightMargin (0.05)
    bot.SetLeftMargin  (0.16)
    bot.SetFillColor(0)
    bot.Draw(drawopt)


    gStyle.SetOptStat(000000)
    from ROOT import TH1,kGray
    divide=""
    drawopt='pE1'
    bot.cd()
    ref= h_mean_mc.Clone()
    h  = h_mean_data.Clone()
    ref.Sumw2()
    h.Sumw2()
    ratioplot = h.Clone()
    ratioplot.Sumw2()
    ratioplot.SetName(h.GetName()+'_ratio')
    ratioplot.Divide(h,ref,1.,1.,'')
    ratioplot.SetFillColor(0)
    ratioplot.SetFillStyle(0)
    ratioplot.SetMarkerColor(1)
    ratioplot.SetLineColor(kGray)
    ratioplot.SetMarkerStyle(24)
    ratioplot.SetMarkerSize(1.2)
    ratioplot.GetYaxis().SetTitleSize(0.10)
    ratioplot.GetXaxis().SetTitleSize(0.10)
    ratioplot.GetXaxis().SetLabelSize(0.10)
    ratioplot.GetYaxis().SetLabelSize(0.10)
    ratioplot.GetYaxis().SetRangeUser(-1.6,3.7)
    ratioplot.GetYaxis().SetTitleOffset(0.7)
    ratioplot.GetYaxis().SetTitle('Data/MC')
    ratioplot.GetXaxis().SetTitle('Rings')
    ratioplot.Draw(drawopt)
    from ROOT import TLine
    
    nbins = h_mean_data.GetNbinsX()
    xmin = h_mean_data.GetXaxis().GetBinLowEdge(1)
    xmax = h_mean_data.GetXaxis().GetBinLowEdge(nbins+1)
    l1 = TLine(xmin,1,xmax,1)
    l1.SetLineColor(kRed)
    l1.SetLineStyle(2)
    l1.Draw()
    bot.Update()
    
    top.cd()
    h_mean_mc.SetFillColor(basecolor)
    h_mean_mc.SetLineWidth(1)
    h_mean_mc.SetLineColor(basecolor)
    h_mean_data.SetLineColor(kBlack)
    h_mean_data.SetLineWidth(1)
    #h_mean_mc.Scale( 1./h_mean_mc.GetEntries() )
    #h_mean_data.Scale( 1./h_mean_data.GetEntries() )

    if h_mean_mc.GetMaximum()>h_mean_data.GetMaximum():
      ymin=h_mean_mc.GetMinimum()
      ymax=h_mean_mc.GetMaximum()
      h_mean_mc.Draw()
      h_mean_mc.GetYaxis().SetTitle('E[Ring] MeV')
      h_mean_data.Draw('same')
    else:
      ymin=h_mean_data.GetMinimum()
      ymax=h_mean_data.GetMaximum()
      h_mean_data.GetYaxis().SetTitle('E[Ring] MeV')
      h_mean_data.Draw()
      h_mean_mc.Draw('same')

    h_mean_data.Draw('same')
    # prepare ringer lines
    def gen_line_90(x , ymin,ymax,text):
      from ROOT import TLine,TLatex
      ymax=1.05*ymax
      l=TLine(x,ymin,x,ymax)
      l.SetLineStyle(2)
      l.Draw()
      txt = TLatex()
      txt.SetTextFont(12)
      txt.SetTextAngle( 90 )
      txt.SetTextSize(0.04)
      txt.DrawLatex(x-1, (ymax-ymin)/2., text)
      return l,txt

    l_ps,t_ps=gen_line_90(8, ymin,ymax, 'presampler')
    l_em1,t_em1=gen_line_90(72, ymin,ymax, 'EM1')
    l_em2,t_em2=gen_line_90(80, ymin,ymax, 'EM2')
    l_em3,t_em3=gen_line_90(88, ymin,ymax, 'EM3')
    l_had1,t_had1=gen_line_90(92,  ymin,ymax, 'HAD1')
    l_had2,t_had2=gen_line_90(96,  ymin,ymax, 'HAD2')
    l_had3,t_had3=gen_line_90(100, ymin,ymax, 'HAD3')

    leg1 = TLegend(0.8,0.70,0.95,0.95)
    setLegend1(leg1)
    leg1.AddEntry(h_mean_mc,'MC')
    leg1.AddEntry(h_mean_data,'Data')
    leg1.Draw()
    atlas_template(top)
    top.Update()

    canvas3.SaveAs(localpath+'/ringer_profile.pdf') 
    canvas3.SaveAs(localpath+'/ringer_profile.C') 
    figures['ringer_profile'] = localpath+'/ringer_profile.pdf'

  #def __scale_histograms(self, h_mc, h_data, nbins, percentage_left, percentage_right):

  #  # Internal method
  #  def getXrange(h,percentage_left, percentage_right):
  #    mean_bin = h.FindBin( h.GetMean() )
  #    firstValue=None; lastValue=None
  #    for bx in range(h.GetNbinsX()):
  #      if h.Integral(-1,bx+1)/float(h.GetEntries()) >= percentage_left :
  #        firstValue = h.GetBinCenter(bx) - 0.5
  #        xbin_min = bx
  #        break
  #    for bx in range(h.GetNbinsX(),-1,-1):
  #      if h.Integral(bx+1,h.GetNbinsX()+1)/float(h.GetEntries()) >= percentage_right :
  #        lastValue = h.GetBinCenter(bx) + 0.5
  #        xbin_max = bx
  #        break
  #    return firstValue, lastValue, xbin_min, xbin_max

  #  f1,l1,bx1_min, bx1_max = getXrange( h_mc , percentage_left, percentage_right)
  #  f2,l2,bx2_min, bx2_max = getXrange(h_data, percentage_left, percentage_right)
  #  f = min(f1,f2)
  #  l = max(l1,l2)
  #  bx_min = min(bx1_min,bx2_min)
  #  bx_max = max(bx1_max,bx2_max)
  #  bins = int(l-f)
  #  from ROOT import TH1F
  #  h_mc_scaled  = TH1F('h_mc_scaled','',bins,f,l)
  #  h_mc_scaled.SetTitle(h_mc.GetTitle())
  #  h_data_scaled  = TH1F('h_data_scaled','',bins,f,l)
  #  h_data_scaled.SetTitle(h_data.GetTitle())
  #  
  #  for idx, bx in enumerate(range(bx_min, bx_max)):
  #    h_mc_scaled.SetBinContent( idx+1, h_mc.GetBinContent(bx+1) )
  #    h_data_scaled.SetBinContent( idx+1, h_data.GetBinContent(bx+1) )

  #  scale=bins/nbins
  #  h_mc_scaled.Rebin(scale)
  #  h_data_scaled.Rebin(scale)
  #  return h_mc_scaled, h_data_scaled
