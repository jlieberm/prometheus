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
           'expandPath',
           'Holder',
           'checkExtension',
           'ensureExtension',
           'changeExtension',
           'mkdir_p',
           'measureLoopTime',
           'measureCallTime',

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
#def progressbar(it, prefix="", size=60):
#    count = len(it)
#    def _show(_i):
#        x = int(size*_i/count)
#        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "█"*x, "."*(size-x), _i, count))
#        sys.stdout.flush()
#    _show(0)
#    for i, item in enumerate(it):
#        yield item
#        _show(i+1)
#    sys.stdout.write("\n")
#    sys.stdout.flush()




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
  #from RingerCore import progressbar, traverse
  pathList = list(traverse([glob(path) if '*' in path else path for path in traverse(pathList,simple_ret=True)],simple_ret=True))
  for path in progressbar( pathList, len(pathList), 'Expanding folders: ', 60, 50,
                           True if logger is not None else False, logger = logger,
                           level = level):
    path = expandPath( path )
    if not os.path.exists( path ):
      raise ValueError("Cannot reach path '%s'" % path )
    if os.path.isdir(path):
      for idx, filt in enumerate(filters):
        cList = filter(lambda x: not(os.path.isdir(x)), [ f for f in glob( os.path.join(path,filt) ) ])
        if cList:
          retList[idx].extend(cList)
      folders = [ os.path.join(path,f) for f in os.listdir( path ) if os.path.isdir( os.path.join(path,f) ) ]
      if folders:
        recList = expandFolders( folders, filters )
        if len(filters) is 1:
          recList = [recList]
        for l in recList:
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


class Holder( object ):
  """
  A simple object holder
  """
  def __init__(self, obj = None, replaceable = True):
    self._obj = obj
    self._replaceable = replaceable
  def __call__(self):
    return self._obj
  def isValid(self):
    return self._obj not in (None, NotSet)
  def set(self, value):
    if self._replaceable or not self.isValid():
      self._obj = value
    else:
      raise RuntimeError("Cannot replace held object.")


def checkExtension( filename, ext, ignoreNumbersAfterExtension = True):
  """
    Check if file matches extension(s) ext. If checking for multiple
    extensions, use | to separate the extensions.
  """
  return bool(__extRE(ext, ignoreNumbersAfterExtension).match( filename ))


def __extRE(ext, ignoreNumbersAfterExtension = True):
  """
  Returns a regular expression compiled object that will search for
  extension ext
  """
  import re
  if not isinstance( ext, (list,tuple,)): ext = ext.split('|')
  ext = [e[1:] if e[0] == '.' else e for e in ext]
  # remove all first dots
  return re.compile(r'(.*)\.(' + r'|'.join(ext) + r')' + \
                    (r'(\.[0-9]*|)' if ignoreNumbersAfterExtension else '()') + r'$')


def ensureExtension( filename, extL, ignoreNumbersAfterExtension = True ):
  """
  Ensure that filename extension is extL, else adds its extension.
  Extension extL may start with '.' or not. In case it does not, a dot will be
  added.
  A '|' may be specified to treat multiple extensions. In case either one of
  the extensions specified is found, nothing will be changed in the output,
  else the first extension will be added to the file.
  """
  if isinstance(extL, basestring) and '|' in extL:
    extL = extL.split('|')
  if not isinstance(extL, (list,tuple)):
    extL = [extL]
  extL = ['.' + e if e[0] != '.' else e for e in extL]

  # FIXME: This can be returned earlier by using filter
  if any([checkExtension(filename, ext, ignoreNumbersAfterExtension) for ext in extL]):
    return filename

  # FIXME We should check every extension and see how many composed matches we had before doing this
  ext = extL[0]
  composed = ext.split('.')
  if not composed[0]: composed = composed[1:]
  lComposed = len(composed)
  if lComposed > 1:
    for idx in range(lComposed):
      if filename.endswith( '.'.join(composed[0:idx+1]) ):
        filename += '.' + '.'.join(composed[idx+1:])
        break
    else:
      filename += ext
  else:
    filename += ext
  return filename

def changeExtension( filename, newExtension, knownFileExtensions = ['tgz', 'tar.gz', 'tar.xz','tar',
                                                                    'pic.gz', 'pic.xz', 'pic',
                                                                    'npz', 'npy', 'root'],
                      retryExtensions = ['gz', 'xz'],
                      moreFileExtensions = [],
                      moreRetryExtensions = [],
                      ignoreNumbersAfterExtension = True,
                    ):
  """
  Append string to end of file name but keeping file extension in the end.
  Inputs:
    -> filename: the filename path;
    -> newExtension: the extension to be used by the file;
    -> knownFileExtensions: the known file extensions, use to override all file extensions;
    -> retryExtensions: some extensions are inside other extensions, e.g.
    tar.gz and .gz. This makes regexp operator | to match the smaller
    extension, so the easiest solution is to retry the smaller extensions after
    checking the larger ones.
    -> moreFileExtensions: add more file extensions to consider without overriding all file extensions;
    -> moreRetryExtensions: add more extensions to consider while retrying without overriding the retryExtensions;
    -> ignoreNumbersAfterExtension: whether to ignore numbers after the file extensions or not.
  Output:
    -> the filename with the string appended.
  """
  knownFileExtensions.extend( moreFileExtensions )
  def repStr( newExt ):
    return r'\g<1>' + ( newExt if newExt.startswith('.') else ( '.' + newExt ) )
  str_ = __extRE( knownFileExtensions )
  m = str_.match( filename )
  if m:
    return str_.sub( repStr(newExtension), filename )
  str_ = __extRE( retryExtensions )
  m = str_.match( filename )
  if m:
    return str_.sub( repStr(newExtension), filename )
  else:
    return filename + newExtension


def mkdir_p(path):
  import errno
  path = os.path.expandvars( path )
  try:
    if not os.path.exists( path ):
      os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise IOError










def progressbar(it, count ,prefix="", size=60, step=1, disp=True, logger = None, level = None,
                no_bl = int(os.environ.get('RCM_GRID_ENV',0)) or sys.stdout.isatty(), 
                measureTime = True):
  """
    Display progressbar.
    Input arguments:
    -> it: the iterations collection;
    -> count: total number of iterations on collection;
    -> prefix: the strings preceding the progressbar;
    -> size: number of chars to use on the progressbar;
    -> step: the number of iterations needed for updating;
    -> disp: whether to display progressbar or not;
    -> logger: use this logger object instead o sys.stdout;
    -> level: the output level used on logger;
    -> no_bl: whether to show messages without breaking lines;
    -> measureTime: display time measurement when completing progressbar task.
  """
  from Gaugi.messenger.Logger import LoggingLevel
  from logging import StreamHandler
  from Gaugi.messenger.Logger import nlStatus, resetNlStatus
  import sys
  if level is None: level = LoggingLevel.INFO
  def _show(_i):
    x = int(size*_i/count) if count else 0
    if _i % (step if step else 1): return
    if logger:
      if logger.isEnabledFor(level):
        fn, lno, func = logger.findCaller() 
        record = logger.makeRecord(logger.name, level, fn, lno, 
                                   "%s|%s%s| %i/%i\r",
                                   (prefix, "█"*x, "-"*(size-x), _i, count,), 
                                   None, 
                                   func=func)
        record.nl = False
        # emit message
        logger.handle(record)
    else:
      sys.stdout.write("%s|%s%s| %i/%i\r" % (prefix, "█"*x, "-"*(size-x), _i, count))
      sys.stdout.flush()
  # end of (_show)
  # prepare for looping:
  try:
    if disp:
      if measureTime:
        from time import time
        start = time()
      # override emit to emit_no_nl
      if logger:
        if not nlStatus(): 
          sys.stdout.write("\n")
          sys.stdout.flush()
        if no_bl:
          from Gaugi.messenger.Logger import StreamHandler2
          prev_emit = []
          # TODO On python3, all we need to do is to change the Handler.terminator
          for handler in logger.handlers:
            if type(handler) is StreamHandler:
              stream = StreamHandler2( handler )
              prev_emit.append( handler.emit )
              setattr(handler, StreamHandler.emit.__name__, stream.emit_no_nl)
      _show(0)
    # end of (looping preparation)
    # loop
    try:
      for i, item in enumerate(it):
        yield item
        if disp: _show(i+1)
    except GeneratorExit:
      pass
    # end of (looping)
    # final treatments
    step = 1 # Make sure we always display last printing
    if disp:
      if measureTime:
        end = time()
      if logger:
        if no_bl:
          # override back
          for handler in logger.handlers:
            if type(handler) is StreamHandler:
              setattr( handler, StreamHandler.emit.__name__, prev_emit.pop() )
          _show(i+1)
        if measureTime:
          logger.log( level, "%s... finished task in %3fs.", prefix, end - start )
        if no_bl:
          resetNlStatus()
      else:
        if measureTime:
          sys.stdout.write("\n%s... finished task in %3fs.\n" % ( prefix, end - start) )
        else:
          sys.stdout.write("\n" )
        sys.stdout.flush()
  except (BaseException) as e:
    import traceback
    print traceback.format_exc()
    step = 1 # Make sure we always display last printing
    if disp:
      if logger:
        # override back
        if no_bl:
          for handler in logger.handlers:
            if type(handler) is StreamHandler:
              try:
                setattr( handler, StreamHandler.emit.__name__, prev_emit.pop() )
              except IndexError:
                pass
        try:
          _show(i+1)
        except NameError:
          _show(0)
        for handler in logger.handlers:
          if type(handler) is StreamHandler:
            handler.stream.flush()
      else:
        sys.stdout.write("\n")
        sys.stdout.flush()
    # re-raise:
    raise e
  # end of (final treatments)


def measureCallTime(f, *args, **kw):
  from logging import StreamHandler
  from Gaugi.messenger.Logger import nlStatus, resetNlStatus
  import sys
  msg = kw.pop('__msg', '' )
  logger = kw.pop('__logger', None )
  no_bl = kw.pop('__no_bl', True )
  if logger:
    if not nlStatus(): 
      sys.stdout.write("\n")
      sys.stdout.flush()
    if no_bl:
      from Gaugi.messenger.Logger import StreamHandler2
      prev_emit = []
      # TODO On python3, all we need to do is to change the Handler.terminator
      for handler in logger.handlers:
        if type(handler) is StreamHandler:
          stream = StreamHandler2( handler )
          prev_emit.append( handler.emit )
          setattr(handler, StreamHandler.emit.__name__, stream.emit_no_nl)
  level = kw.pop('__level', None )
  from time import time
  if level is None:
    from Gaugi.messenger.Logger import LoggingLevel
    level = LoggingLevel.DEBUG
  if not msg:
    msg = 'Executing ' + f.__name__ + '(' + ','.join(args) + ','.join([(str(key) + '=' + str(val)) for key, val in kw.iteritems()]) + ')'
  if not msg.endswith('...') and not msg.endswith('... '): msg += '...'
  if not msg.endswith(' '): msg += ' '
  if logger:
    fn, lno, func = logger.findCaller() 
    record = logger.makeRecord(logger.name, level, fn, lno, 
                               "%s\r",
                               (msg), 
                               None, 
                               func=func)
    record.nl = False
    # emit message
    logger.handle(record)
  start = time()
  ret = f(*args, **kw)
  end = time()
  if logger:
    if no_bl:
      # override back
      for handler in logger.handlers:
        if type(handler) is StreamHandler:
          try:
            setattr( handler, StreamHandler.emit.__name__, prev_emit.pop() )
          except IndexError:
            pass
    record.msg = record.msg[:-1] + 'done!'
    logger.handle(record)
    logger.log( level, '%s execution took %.2fs.', f.__name__, end - start)
    if no_bl:
      resetNlStatus()
  return ret

def measureLoopTime(it, prefix = 'Iteration', prefix_end = '', 
                    logger = None, level = None, showLoopBenchmarks = True):
  from time import time
  if level is None:
    from Gaugi.messenger.Logger import LoggingLevel
    level = LoggingLevel.DEBUG
  start = time()
  for i, item in enumerate(it):
    lStart = time()
    yield item
    end = time()
    if showLoopBenchmarks:
      if logger:
        logger.log( level, '%s %d took %.2fs.', prefix, i, end - lStart)
      else:
        sys.stdout.write( level, '%s %d took %.2fs.\n' % ( prefix, i, end - lStart ) )
        sys.stdout.flush()
  if logger:
    logger.log( level, 'Finished looping (%s) in %.2fs.', prefix_end, end - start)
  else:
    sys.stdout.write( level, 'Finished looping (%s) in %.2fs.\n' % ( prefix_end, end - start) )
    sys.stdout.flush()



