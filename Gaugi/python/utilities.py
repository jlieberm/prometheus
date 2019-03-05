#coding: utf-8
__all__ = [
           'retrieve_kw',
           'checkForUnusedVars',
           'str_to_class',
           'csvStr2List',
           'get_attributes',
           'printArgs',
           'list_to_stdvector',
           'stdvector_to_list',
           'progressbar',
           'appendToOutput',
           'traverse',
           'expandFolders',
           'expandPath'
           ]


import re, os, __main__
import sys
import code
import types
import cPickle
import gzip
import inspect
import numpy as np
from Gaugi.types import NotSet

def retrieve_kw( kw, key, default = NotSet ):
  """
  Use together with NotSet to have only one default value for your job
  properties.
  """
  if not key in kw or kw[key] is NotSet:
    kw[key] = default
  return kw.pop(key)


 
def checkForUnusedVars(d, fcn = None):
  """
    Checks if dict @d has unused properties and print them as warnings
  """
  for key in d.keys():
    if d[key] is NotSet: continue
    msg = 'Obtained not needed parameter: %s' % key
    if fcn:
      fcn(msg)
    else:
      print 'WARNING:%s' % msg


def str_to_class(module_name, class_name):
  try:
    import importlib
  except ImportError:
    # load the module, will raise ImportError if module cannot be loaded
    m = __import__(module_name, globals(), locals(), class_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c
  # load the module, will raise ImportError if module cannot be loaded
  m = importlib.import_module(module_name)
  # get the class, will raise AttributeError if class cannot be found
  c = getattr(m, class_name)
  return c


def csvStr2List( csvStr ):
  # Return a list from the comma separated values
  # If input string starts with @, then it is assumed that the leading string
  # an actual path and the content from the file is parsed.
  # Treat comma separated lists:
  if type(csvStr) is str:
    # Treat files which start with @ as a comma separated list of files
    if csvStr.startswith('@'):
      with open( os.path.expandvars( csvStr[1:] ), 'r') as content_file:
        csvStr = content_file.read()
        csvStr = csvStr.replace('\n','')
        if csvStr.endswith(' '): csvStr = csvStr[:-1]
    csvStr = csvStr.split(',')
  # Make sure our confFileList is a list (just to be compatible for 
  if not type(csvStr) is list:
    csvStr = [csvStr]
  return csvStr


def get_attributes(o, **kw):
  """
    Return attributes from a class or object.
  """
  onlyVars = kw.pop('onlyVars', False)
  getProtected = kw.pop('getProtected', True)
  checkForUnusedVars(kw)
  return [(a[0] if onlyVars else a) for a in inspect.getmembers(o, lambda a:not(inspect.isroutine(a))) \
             if not(a[0].startswith('__') and a[0].endswith('__')) \
                and (getProtected or not( a[0].startswith('_') or a[0].startswith('__') ) ) ]


def printArgs(args, fcn = None):
  try:
    import pprint as pp
    if args:
      if not isinstance(args,dict):
        args_dict = vars(args)
      else:
        args_dict = args
      msg = 'Retrieved the following configuration:\n%s' % pp.pformat([(key, args_dict[key]) for key in sorted(args_dict.keys())])
    else:
      msg = 'Retrieved empty configuration!'
    if fcn:
      fcn(msg)
    else:
      print 'INFO:%s' % msg
  except ImportError:
    logger.info('Retrieved the following configuration: \n %r', vars(args))



# helper function to display a progress bar
def progressbar(it, prefix="", size=60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "█"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()




def list_to_stdvector(vecType,l):
  from ROOT.std import vector
  vec = vector(vecType)()
  for v in l:
    vec.push_back(v)
  return vec

def stdvector_to_list(vec, size=None):
  if size:
    l=size*[0]
  else:
    l = vec.size()*[0]
  for i in range(vec.size()):
    l[i] = vec[i]
  return l


def floatFromStr(str_):
  "Return float from string, checking if float is percentage"
  if '%' in str_:
    return float(str_.strip('%'))*100.
  return float(str_)



def appendToOutput( o, cond, what):
  """
  When multiple outputs are configurable, use this method to append to output in case some option is True.
  """
  if cond:
    if type(o) is tuple: o = o + (what,)
    else: o = o, what
  return o

def traverse(o, tree_types=(list, tuple),
    max_depth_dist=0, max_depth=np.iinfo(np.uint64).max, 
    level=0, parent_idx=0, parent=None,
    simple_ret=False, length_ret=False):
  """
  Loop over each holden element. 
  Can also be used to change the holden values, e.g.:
  a = [[[1,2,3],[2,3],[3,4,5,6]],[[[4,7],[]],[6]],7]
  for obj, idx, parent in traverse(a): parent[idx] = 3
  [[[3, 3, 3], [3, 3], [3, 3, 3, 3]], [[[3, 3], []], [3]], 3]
  Examples printing using max_depth_dist:
  In [0]: for obj in traverse(a,(list, tuple),0,simple_ret=False): print obj
  (1, 0, [1, 2, 3], 0, 3)
  (2, 1, [1, 2, 3], 0, 3)
  (3, 2, [1, 2, 3], 0, 3)
  (2, 0, [2, 3], 0, 3)
  (3, 1, [2, 3], 0, 3)
  (3, 0, [3, 4, 5, 6], 0, 3)
  (4, 1, [3, 4, 5, 6], 0, 3)
  (5, 2, [3, 4, 5, 6], 0, 3)
  (6, 3, [3, 4, 5, 6], 0, 3)
  (4, 0, [4, 7], 0, 4)
  (7, 1, [4, 7], 0, 4)
  (6, 0, [6], 0, 3)
  (7, 2, [[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 0, 1) 
  In [1]: for obj in traverse(a,(list, tuple),1): print obj
  ([1, 2, 3], 0, [[1, 2, 3], [2, 3], [3, 4, 5, 6]], 1, 3)
  ([2, 3], 0, [[1, 2, 3], [2, 3], [3, 4, 5, 6]], 1, 3)
  ([3, 4, 5, 6], 0, [[1, 2, 3], [2, 3], [3, 4, 5, 6]], 1, 3)
  ([4, 7], 0, [[4, 7], []], 1, 4)
  ([6], 0, [[[4, 7], []], [6]], 1, 3)
  ([[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 2, None, 1, 1)
  In [2]: for obj in traverse(a,(list, tuple),2,simple_ret=False): print obj
  ([[1, 2, 3], [2, 3], [3, 4, 5, 6]], 0, [[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 2, 2)
  ([[4, 7], []], 0, [[[4, 7], []], [6]], 2, 3)
  ([[[4, 7], []], [6]], 1, [[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 2, 2)
  In [3]: for obj in traverse(a,(list, tuple),3): print obj
  ([[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 0, None, 3, 1)
  In [4]: for obj in traverse(a,(list, tuple),4): print obj
  ([[[1, 2, 3], [2, 3], [3, 4, 5, 6]], [[[4, 7], []], [6]], 7], 1, None, 4, 1)
  In [5]: for obj in traverse(a,(list, tuple),5): print obj
  <NO OUTPUT>
  """
  if isinstance(o, tree_types):
    level += 1
    # FIXME Still need to test max_depth
    if level > max_depth:
      if simple_ret:
        yield o
      elif length_ret:
        yield level
      else:
        yield o, parent_idx, parent, 0, level
      return
    skipped = False
    isDict = isinstance(o, dict)
    if isDict:
      loopingObj = o.iteritems()
    else:
      loopingObj = enumerate(o)
    for idx, value in loopingObj:
      try:
        for subvalue, subidx, subparent, subdepth_dist, sublevel in traverse(value 
                                                                            , tree_types     = tree_types
                                                                            , max_depth_dist = max_depth_dist
                                                                            , max_depth      = max_depth
                                                                            , level          = level
                                                                            , parent_idx     = idx
                                                                            , parent         = o ):
          if subdepth_dist == max_depth_dist:
            if skipped:
              subdepth_dist += 1
              break
            else:
              if simple_ret:
                yield subvalue
              elif length_ret:
                yield sublevel
              else:
                yield subvalue, subidx, subparent, subdepth_dist, sublevel 
          else:
            subdepth_dist += 1
            break
        else: 
          continue
      except SetDepth, e:
        if simple_ret:
          yield o
        elif length_ret:
          yield level
        else:
          yield o, parent_idx, parent, e.depth, level
        break
      if subdepth_dist == max_depth_dist:
        if skipped:
          subdepth_dist += 1
          break
        else:
          if simple_ret:
            yield o
          elif length_ret:
            yield level
          else:
            yield o, parent_idx, parent, subdepth_dist, level
          break
      else:
        if level > (max_depth_dist - subdepth_dist):
          raise SetDepth(subdepth_dist+1)
  else:
    if simple_ret:
      yield o
    elif length_ret:
      yield level
    else:
      yield o, parent_idx, parent, 0, level



def expandFolders( pathList, filters = None, logger = None, level = None):
  """
    Expand all folders to the contained files using the filters on pathList
    Input arguments:
    -> pathList: a list containing paths to files and folders;
    filters;
    -> filters: return a list for each filter with the files contained on the
    list matching the filter glob.
    -> logger: whether to print progress using logger;
    -> level: logging level to print messages with logger;
    WARNING: This function is extremely slow and will severely decrease
    performance if used to expand base paths with several folders in it.
  """
  if not isinstance( pathList, (list,tuple,) ):
    pathList = [pathList]
  from glob import glob
  if filters is None:
    filters = ['*']
  if not( type( filters ) in (list,tuple,) ):
    filters = [ filters ]
  retList = [[] for idx in range(len(filters))]
  pathList = list(traverse([glob(path) if '*' in path else path for path in traverse(pathList,simple_ret=True)],simple_ret=True))
  for path in progressbar( pathList,  'Expanding folders: ', 60):
    path = expandPath( path )
    if not os.path.exists( path ):
      raise ValueError("Cannot reach path '%s'" % path )
    if os.path.isdir(path):
      for idx, filt in enumerate(filters):
        cList = [ f for f in glob( os.path.join(path,filt) ) ]
        if cList: 
          retList[idx].extend(cList)
      folders = [ os.path.join(path,f) for f in os.listdir( path ) if os.path.isdir( os.path.join(path,f) ) ]
      if folders:
        recList = expandFolders( folders, filters )
        if len(filters) is 1:
          recList = [recList]
        for idx, l in enumerate(recList):
          retList[idx].extend(l)
    else:
      for idx, filt in enumerate(filters):
        if path in glob( os.path.join( os.path.dirname( path ) , filt ) ):
          retList[idx].append( path )
  if len(filters) is 1:
    retList = retList[0]
  return retList


class BadFilePath(ValueError): pass

def expandPath(path):
  " Returns absolutePath path expanding variables and user symbols "
  if not isinstance( path, basestring):
    raise BadFilePath(path)
  return os.path.abspath( os.path.expanduser( os.path.expandvars( path ) ) )


