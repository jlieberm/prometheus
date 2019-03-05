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
           'measureCallTime',
           'measureLoopTime',
           'appendToOutput'
           ]


import re, os, __main__
import sys
import code
import types
import cPickle
import gzip
import inspect
import numpy as np

from RingerCore.Configure import NotSet, RCM_NO_COLOR, RCM_GRID_ENV

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
  from RingerCore.Configure import checkForUnusedVars
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



def progressbar(it, count ,prefix="", size=60, step=1, disp=True, logger = None, level = None,
                nRCM_GRID_ENV or sys.stdout.isatty(), 
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
  from Gaugi.messenger import LoggingLevel, nlStatus, resetNlStatus
  from logging import StreamHandler
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
          from Gaugi.messenger import StreamHandler2
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
  from Gaugi.messenger import nlStatus, resetNlStatus
  import sys
  msg = kw.pop('__msg', '' )
  logger = kw.pop('__logger', None )
  no_bl = kw.pop('__no_bl', True )
  if logger:
    if not nlStatus(): 
      sys.stdout.write("\n")
      sys.stdout.flush()
    if no_bl:
      from Gaugi.messenger import StreamHandler2
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
    from Gaugi.messenger import LoggingLevel
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
    from Gaugi.messenger import LoggingLevel
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


