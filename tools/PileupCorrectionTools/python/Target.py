
__all__ = ["Target"]

from Gaugi.messenger import Logger
from Gaugi.messenger.macros import *


class ExpertAndExperimentalMethods(object):
  
  def __init__(self):
    self._doSP = False
    self._scaleParameter = None

  @property
  def doSP(self):
    return self._doSP

  @doSP.setter
  def doSP(self, v):
    self._doSP = v

  @property
  def scaleParameter(self):
    return self._scaleParameter

  @scaleParameter.setter
  def scaleParameter(self, v):
    self._scaleParameter = v



# Target class used as interface to configure the 
# pileup correction tool.
class Target( Logger ):

  def __init__( self, name, algname, reference, outputfile=None ):
    Logger.__init__(self)
    # Target name will be used as the root directory
    self._name = name
    # Algorithm name will be used to store the discr histograms
    self._algname = algname
    # Reference can ve a float, list of lists or the name of the target
    # directory. The target dir will be used to extract the ref values
    self._refname = reference
    # Relax parameter will be used to relax the ref value
    self._outputfile = outputfile # The name of the threshold file config that will be produced in the end.
    # expert methods
    self._expertAndExperimentalMethods = ExpertAndExperimentalMethods()

  # get the internal menu used for experts
  def expertAndExperimentalMethods(self):
    return self._expertAndExperimentalMethods

  def name(self):
    return self._name

  def algname(self):
    return self._algname

  def refname(self):
    return self._refname

  def outputfile(self):
    return self._outputfile


  # Retrive the reference value from the target
  def reference( self, storegate, basepath, etbinidx=None, etabinidx=None, mumin=0.0, mumax=100.0, useFalseAlarm=False ):
    
    # The refrence is a str and need to access the histogram directory
    if type(self._refname) is str:
      # etbin and etabin is mandatory in this case
      if (etbinidx is None) or (etabinidx is None):
        MSG_FATAL( self,"Can not access the reference. You must pass et/eta bin index as argument.")
      binningname = ('et%d_eta%d') % (etbinidx,etabinidx)
      
      if self.expertAndExperimentalMethods().doSP:
        det, fa, sp = CalculateMaxSP(
        storegate.histogram('{}/{}/{}/{}/{}/discriminantVsMu'.format(basepath,'probes',self.name(),self.algname(),binningname)).ProjectionX(),
        storegate.histogram('{}/{}/{}/{}/{}/discriminantVsMu'.format(basepath,'fakes',self.name(),self.algname(),binningname)).ProjectionX()
        )
        
        passed = int(total * fa) if useFalseAlarm else int(total * det)
        eff     = passed/float(total) if total>0 else 0
      else:
        # integrate all entries along x axis
        def _integrate(hist, xmin, xmax):
          total=0
          xhighidx = hist.GetXaxis().FindBin(xmax)
          xlowidx = hist.GetXaxis().FindBin(xmin) - 1
          xhighidx = min(hist.GetNbinsX(),xhighidx)
          for bx in range(int(xlowidx),int(xhighidx)):
            total+= hist.GetBinContent(bx)  
          return total

        path = '{}/{}/{}/{}/{}'.format(basepath,'fakes' if useFalseAlarm else 'probes',self.name(),self.refname(),binningname)
        total   = _integrate( storegate.histogram(path+'/mu'), mumin, mumax )
        passed  = _integrate( storegate.histogram(path+'/match_mu'), mumin, mumax )
        eff     = passed/float(total) if total>0 else 0
    else:
      MSG_FATAL( self,"Impossible to retrive the reference value. Abort!")
    
    # Appling the scale parameter (relax) into the calculated efficiency
    if self.expertAndExperimentalMethods().scaleParameter:
      factor = self.expertAndExperimentalMethods().scaleParameter; diff = (1-eff)*abs(factor) 
      eff = eff+diff if factor > 0.0 else eff-diff
      passed = eff*total

    # return the calculated reference values
    return eff, passed, total





