
__all__ = ['EDM']

from Gaugi.messenger import Logger
from Gaugi import NotSet, EnumStringification, StatusCode
from Gaugi.enumerations import Dataframe as DataframeEnum
from Gaugi.messenger.macros import *


class EDM(Logger):

  # set the default skimmed dataframe
  _dataframe = DataframeEnum.SkimmedNtuple
  
  def __init__(self):
    Logger.__init__(self)
    self._idx = 0
    self._is_hlt = False
    self._decoration = dict()
    self._tree  = NotSet
    self._event = NotSet
    self._context = NotSet
    #from  import ElectronCandidate
    # this is use only for SkimmedNtuple
    self._elCand = NotSet# Default is probe
    # this is used for metadata properties
    self._useMetadataParams = False
    self._metadataParams = {}
    self._branches = list() # hold all branches from the body class


  def setContext( self, context):
    self._context=context

  def getContext(self):
    return self._context

  def initialize(self):
    return StatusCode.SUCCESS

  def execute(self):
    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS

  @property
  def dataframe(self):
    return self._dataframe

  @dataframe.setter
  def dataframe(self, v):
    self._dataframe=v

  @property
  def tree(self):
    self._tree

  @tree.setter
  def tree(self, v):
    self._tree = v

  @property
  def event(self):
    return self._event

  @event.setter 
  def event(self, v):
    self._event = v

  def setDecor(self, key, v):
    self._decoration[key] = v

  def getDecor(self,key):
    try:
      return self._decoration[key]
    except KeyError:
      self._logger.warning('Decoration %s not found',key)

  def clearDecorations(self):
    self._decoration = dict()

  def decorations(self):
    return self._decoration.keys()

  def setBranchAddress( self, tree, varname, holder, pointername=None):
    if not pointername:  pointername=varname
    " Set tree branch varname to holder "
    if not tree.GetBranchStatus(varname):
      tree.SetBranchStatus( varname, True )
      from ROOT import AddressOf
      tree.SetBranchAddress( varname, AddressOf(holder, pointername) )
      MSG_DEBUG( self, "Set %s branch address on %s", varname, tree )
    else:
      MSG_DEBUG( self, "Already set %s branch address on %s", varname, tree)

  def retrieve(self, key):
    try:
      return self._containersSvc[key]
    except KeyError:
      MSG_WARNING( self, 'Container %s not found',key)

  @property
  def candidate(self, v):
    return self._elCand
  
  # Use this only for skimmed ntuple dataframe
  # Default is 2 (probes)
  @candidate.setter
  def candidate(self, v):
    self._elCand = v

  @property
  def is_hlt(self):
    return self._is_hlt

  @is_hlt.setter
  def is_hlt(self, v):
    self._is_hlt=v

  def __iter__(self):
    self.setPos(-1) # force to be -1 
    if self.size()>0:
      while (self.getPos()+1) < self.size():
        self.setPos(self.getPos()+1)
        yield self

  def size(self):
    return 1

  def setPos( self, idx ):
    self._idx = idx

  def getPos( self ):
    return self._idx


  def useMetadataParams(self):
    return self._useMetadataParams

  def setMetadataParams( self, dParam ):
    self._metadataParams = dParam

  def checkBody(self, branch):
    if branch in self._branches:
      return True
    elif branch in self.decorations():
      return True
    else:
      return False


  def accept(self, v):
    return True



