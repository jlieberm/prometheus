import ROOT,cppyy
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
cppyy.loadDict("RingerSelectorTools")
from ROOT import prometheus

alg = prometheus.AsgElectronRingerSelector("teste")
