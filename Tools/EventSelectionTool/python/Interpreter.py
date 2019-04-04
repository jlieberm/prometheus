__all__ = ['Interpreter']

from prometheus import Algorithm
from Gaugi import StatusCode
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger.macros import *


class Interpreter( Algorithm ):

  def __init__(self,name):
    Algorithm.__init__(self,name)

  def make_expression( self, items ):
    # fix into the string
    expression = items
    expression = expression.replace('&&',' and ')
    expression = expression.replace('!' ,' not ')
    expression = expression.replace('||',' or ' )
    expression = expression.replace('(' ,' ( '  )
    expression = expression.replace(')' ,' ) '  )
    expression = expression.replace('>' ,' > '  )
    expression = expression.replace('<' ,' < '  )
    expression = expression.replace('<' ,' < '  )
    expression = expression.replace('<=',' <= ' )
    expression = expression.replace('>=',' >= ' )
    expression = expression.replace('==',' == ' )
    return expression

  def compile( self, pidname ):
    #NOTE: This method will get the bool accept answer give an logical expression like:
    #  TDT__HLT__e28_lhtight_nod0_ivarloose
    #  TDT__EFCalo__e28_lhtight_nod0_ivarloose
    #  EMU__HLT__e28_lhtight_nod0_ivarloose
    #  pyEMU__HLT__e17_lhvloose_nod0
    #  IsRingerTight_v6
    #  TDT__HLT_e5_etcut&&(IsLHTight||!IsRingerTight)
    #  el_lhtight&&TDT__HLT_e5_etcut&&(IsLHTight||!IsRingerTight)&&(Et>15GeV)&&(eta>1.37)
    #  IsRingerTight_v6&&IsLHTight_CaloOnly
    # We can get the information from the trigger metadata (TDT) or selector decorations
    # installed at the rDev stack.
    from EventAtlas import DecisionCore, AcceptType
    # all information will be storaged here.
    if self.dataframe is DataframeEnum.PhysVal_v2:
      # information storage from TDT athena/emulation core (metadata)
      tdt = self.getContext().getHandler("HLT__TDT")
    
    el      = self.getContext().getHandler("HLT__ElectronContainer")
    off_el  = self.getContext().getHandler("ElectronContainer")
    fc      = self.getContext().getHandler("HLT__FastCaloContainer")

    # make the expression 
    expression = self.make_expression(pidname)
    expression = expression.replace('GeV' ,'*1000')

    def _contain(s,_s_):
      for ss in _s_:
        if s in ss: return True
      return False

    # helper function to loop over a set of string and check if contains inside of 's'
    strs  = expression.split(' ')
    for idx, s in enumerate(strs):
      # check and skip if in
      if _contain(s, ['and','or','not','(',')','>','<','>=','<=','==']):  continue
      # boolean 
      passed = False
      # get the accept decision from the TDT metadata
      if self._dataframe is DataframeEnum.PhysVal_v2 and 'TDT' in s:
        trigInfo = s.split('__')
        tdt.core(DecisionCore.TriggerDecisionTool) # athena core
        # TDT__AcceptType__trigItem
        passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      elif self._dataframe is DataframeEnum.PhysVal_v2 and 'EMU' in s:
        trigInfo = s.split('__')
        tdt.core(DecisionCore.TrigEgammaEmulationTool) # athena emulation e/g core
        # EMU__AcceptType__trigItem
        passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      else:  
        try: # s is not a pure branch
          number = eval(s) # is a number
          expression=expression.replace(s,str(number))
          continue
        except: # s is a branch or decorations
          # need to extract some number inside of this branch
          if (s == 'Et') or (s == 'eta') or  (s== 'phi'):
            number = getattr(off_el,'%s'%s.lower())()
            expression=expression.replace(s,str(number))
            continue
          else: # is a PID
            if el.checkBody(s): # the s allow to HLT electron
              self._logger.debug('(%s) is in of online electron', s)
              passed = el.accept(s)
            elif off_el.checkBody(s):
              self._logger.debug('(%s) is in of offline electron', s)
              passed = off_el.accept(s)
            elif fc.checkBody(s):
              self._logger.debug('(%s) is in of fastcalo electron', s)
              passed = fc.accept(s) 
            else:
              MSG_WARNING( self, 'There is no interpretation for this item (%s)',s)
              
      # add answer to the expression
      expression=expression.replace(s,str(passed))
    self._logger.debug('Expression: %s',expression)
    return expression


  def apply(self, expression):
    return eval(self.compile(expression))


  #NOTE: Search for Et cut into the items
  # el_lhtight && Et>15GeV && HLT__isElectronRingerTight 
  def search_et(self, items):
    strs = self.make_expression(items).split(' ')
    for s in strs:
      if 'GeV' in s:  return float(s.replace('GeV',''))
    return 0.0

  #NOTE: Search for offline branches into items
  # el_lhtight && Et>15GeV && HLT__isElectronRingerTight 
  def search_pid(self, items):
    off_el = self.getContext().getHandler("ElectronContainer")
    strs = self.make_expression(items).split(' ')
    for s in strs:
      if off_el.checkBody(s):  return s
    return 'el_lhvloose' # default very loose offline selection
    


