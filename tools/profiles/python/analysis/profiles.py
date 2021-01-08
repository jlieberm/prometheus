

__all__ = ['profiles']

from Gaugi.messenger import Logger, LoggingLevel
from Gaugi.messenger.macros import *
from Gaugi.monet.AtlasStyle import *
from Gaugi.monet.PlotFunctions import *
from Gaugi.monet.TAxisFunctions import *
from Gaugi.tex import *
from Gaugi import progressbar
from copy import copy
from itertools import product
import numpy as np
import array
import os



from ROOT import gROOT, kTRUE
gROOT.SetBatch(kTRUE)
import ROOT
ROOT.gErrorIgnoreLevel=ROOT.kFatal


# Create default color definitions
from ROOT import TCanvas, TLatex, TH1F,  kRed, kBlue, kBlack,TLine,kBird, kOrange,kGray, kYellow, kViolet, kGreen, kAzure
from Gaugi.monet.utils import getColor, NormHist
fill_colors = [ getColor(color, 0.5) for color in [kYellow-9, kOrange+6, kViolet-4, kGreen-2, kAzure-8] ]
line_colors = [kYellow, kOrange+7, kViolet-5, kGreen-8, kAzure+4]


#
# profiles
#
class profiles(Logger):


    #
    # Constructor
    #
    def __init__(self, etbins, etabins, fill_colors=fill_colors, line_colors=line_colors):

        Logger.__init__(self)
        self.__etbins = etbins
        self.__etabins = etabins
        self.__these_fill_colors=fill_colors
        self.__these_line_colors=line_colors
        self.__hist = {}


    #
    # Add new histogram
    #
    def add_hist(self, branch, bins, xmin, xmax, xlabel=''):
        self.__hist[branch] = {'xmin':xmin, 'xmax':xmax, 'xlabel':xlabel, 'bins':bins} 

    
    def get_etbins(self):
        return self.__etbins


    def get_etabins(self):
        return self.__etabins


    def get_etbin_edges(self, et_bin):
        return (self.__etbins[et_bin], self.__etbins[et_bin+1])


    def get_etabin_edges(self, eta_bin):
        return (self.__etabins[eta_bin], self.__etabins[eta_bin+1])


    #
    # Fill all histograms
    #
    def fill(self, generator , paths):

        hists = { branch:[[None for _ in range(len(self.__etabins)-1)] for __ in range(len(self.__etbins)-1)] for branch in self.__hist.keys()}

        # Prepare all histograms
        for et_bin, eta_bin in progressbar(product(range(len(self.__etbins)-1),range(len(self.__etabins)-1)),
                                           (len(self.__etbins)-1)*(len(self.__etabins)-1), prefix = "Reading... " ):

            data, features = generator(paths[et_bin][eta_bin])
            for branch, hist in self.__hist.items(): 
                th1 = TH1F( branch+'_et'+str(et_bin)+'_eta'+str(eta_bin), "",  hist['bins'], hist['xmin'], hist['xmax'] )
                values = data[:, features.index(branch)] 
                w = array.array( 'd', np.ones_like(values) )
                th1.FillN( len(values), array.array('d',  values.tolist()),  w)
                hists[branch][et_bin][eta_bin] = th1

        return hists


    def get_str_etbin(self, etidx):
        
        etlist=copy(self.__etbins)
        if etlist[-1]>9999:  etlist[-1]='#infty'
        binEt = (str(etlist[etidx]) + ' < E_{T} [GeV] < ' + str(etlist[etidx+1]) if etidx+1 < len(etlist) else 'E_{T} > ' + str(etlist[etidx]) + ' GeV')
        return binEt
 

    def get_str_etabin(self, etaidx):
        binEta = (str(self.__etabins[etaidx]) + ' < |#eta| < ' + str(self.__etabins[etaidx+1]) if etaidx+1 < len(self.__etabins) else \
                  str(self.__etabins[etaidx]) + ' <|#eta| < 2.47')
        return binEta



    #
    # plot and create the beamer report
    #
    def dump_beamer_report(self, hists, output_pdf, output_dir, title=''):

        SetAtlasStyle()

        # create directory
        localpath = os.getcwd()+'/'+output_dir
        try:
            if not os.path.exists(localpath): os.makedirs(localpath)
        except:
            MSG_WARNING( self,'The director %s exist.', localpath)



        # Slide maker
        with BeamerTexReportTemplate1( theme = 'Berlin'
                                     , _toPDF = True
                                     , title = title
                                     , outputFile = output_pdf
                                     , font = 'structurebold' ):


            for branch in hists.keys():

                with BeamerSection( name = branch.replace('_','\_') ):
                    
                    # prepare figures
                    with BeamerSubSection( name = 'Eta comps'):

                        for et_bin in range(len(self.__etbins)-1):
                            hist_list = [ hists[branch][et_bin][eta_bin] for eta_bin in range(len(self.__etabins)-1) ]
                            legends = [ self.get_str_etabin(idx) for idx in range(len(self.__etabins)-1) ]
                            extratext = self.get_str_etbin(et_bin)
                            outname = localpath + '/%s_et%d_etaComp'%(branch,et_bin)
                            output = self.plot_hist( hist_list, legends, extratext, outname )
                            BeamerMultiFigureSlide( title = branch.replace('_','\_')
                                , paths = [output]
                                , nDivWidth = 1 # x
                                , nDivHeight = 1 # y
                                , texts=None
                                , fortran = False
                                , usedHeight = 0.6
                                , usedWidth = 1.
                                )

                    # prepare figures
                    with BeamerSubSection( name = 'Et comps'):
                    
                        for eta_bin in range(len(self.__etabins)-1):
                            hist_list = [ hists[branch][et_bin][eta_bin] for et_bin in range(len(self.__etbins)-1) ]
                            legends = [ self.get_str_etbin(idx) for idx in range(len(self.__etbins)-1) ]
                            extratext = self.get_str_etabin(eta_bin)
                            outname = localpath + '/%s_eta%d_etComp'%(branch,eta_bin)
                            output = self.plot_hist( hist_list, legends, extratext, outname )
                            BeamerMultiFigureSlide( title = branch.replace('_','\_')
                                , paths = [output]
                                , nDivWidth = 1 # x
                                , nDivHeight = 1 # y
                                , texts=None
                                , fortran = False
                                , usedHeight = 0.6
                                , usedWidth = 1.
                                )


    def plot_hist( self, hists, legends, extratext, outname ): 
            # Create canvas
            canvas = TCanvas('canvas','canvas',500, 500)
            hist_list=[]
            maximum = 0
            for hist in hists:
                h = NormHist(hist)
                if h.GetMaximum() > maximum:
                    maximum = h.GetMaximum()
                hist_list.append(h)
            for idx, hist in enumerate(hist_list):
                hist.SetLineColor(self.__these_line_colors[idx])
                hist.SetFillColor(self.__these_fill_colors[idx])
                hist.SetMaximum(1.4*maximum)
                AddHistogram(canvas,hist, 'same')
            AddATLASLabel(canvas, 0.20,0.88,'Internal')
            AddTexLabel(canvas,0.2, 0.80, extratext, textsize=0.03)
            FormatCanvasAxes(canvas, XLabelSize=16, YLabelSize=16, XTitleOffset=0.87, ZLabelSize=16,ZTitleSize=16, YTitleOffset=1.30, ZTitleOffset=1.1)
            SetAxisLabels(canvas,hist_list[0].GetXaxis().GetTitle(), 'counts/bin (norm by counts)')
            MakeLegend(canvas,.60,.75,.98,.95,option='F',textsize=14, names=legends, ncolumns=1, squarebox=True, doFixLength=False)
            canvas.SaveAs(outname+'.pdf')
            return outname+'.pdf'






#
# Quick test to dev.
#
if __name__ == "__main__":


    path = '/Volumes/castor/cern_data/files/Zee/mc15_13TeV.sgn.probes_lhmedium_Zee.bkg.Truth.JF17/'
    path+= 'mc15_13TeV.sgn.probes_lhmedium_Zee.bkg.Truth.JF17_et{ET}_eta{ETA}.npz'
    paths = [[ path.format(ET=et,ETA=eta) for eta in range(5)] for et in range(5)]  

    etbins = [15, 20, 30, 40, 50, 1000000]
    etabins = [0.0, 0.8, 1.37, 1.54, 2.37, 2.50]

    from profiles import profiles
    profile = profiles(etbins, etabins)
    profile.add_hist('L2Calo_reta', 50, 0.7, 1.1 , xlabel='R_{#eta}')
    profile.add_hist('L2Calo_eratio', 30, 0.7, 1.05, xlabel='E_{ratio}')
    profile.add_hist('L2Calo_ring_9', 100, -2000, 15000, xlabel='Ring_{EM1,1;9} [MeV]')


    def generator_for_signal(path):
        from Gaugi import load
        raw = load(path)
        features = raw['features'].tolist()
        data = raw['data']
        target =  raw['target']
        return data[target==1,:], features

    hists = profile.fill( generator_for_signal, paths )
    profile.dump_beamer_report(hists, 'test.pdf', 'test_dir', 'this is a test')

    


