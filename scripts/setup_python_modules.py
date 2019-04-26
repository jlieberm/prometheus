
import sys, os
import numpy as np


class BadFilePath(ValueError): pass


def traverse(o, tree_types=(list, tuple),
    max_depth_dist=0, max_depth=np.iinfo(np.uint64).max, 
    level=0, parent_idx=0, parent=None,
    simple_ret=False, length_ret=False):
  
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


def expandPath(path):
  " Returns absolutePath path expanding variables and user symbols "
  if not isinstance( path, basestring):
    raise BadFilePath(path)
  try:
    return os.path.abspath( os.path.join(os.path.dirname(path), os.readlink( os.path.expanduser( os.path.expandvars( path ) ) ) ) )
  except OSError:
    return os.path.abspath( os.path.expanduser( os.path.expandvars( path ) ) )


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
  for path in pathList:
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



import argparse

parser = argparse.ArgumentParser(description = 'pycmake', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-b','--basepath', action='store', 
        dest='basepath', required = True,help = "The cmake project path")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()

print expandFolders(args.basepath)
#import glob
#import os
#CURRENT_PATH = os.environ["CMAKE_PROJECT_PATH"]
#stage1 = glob.glob(CURRENT_PATH+'/*/python')
#stage2 = glob.glob(CURRENT_PATH+'/*/*/python')
#python_paths = stage1+stage2
#
#
#for pypath  in python_paths:
#  if 'build' in pypath: continue
#  PATH =  pypath
#  TARGET = pypath.split('/')
#  TARGET = TARGET[len(TARGET)-2]
#  command = 'ln -sf {PATH} {TARGET}'.format(PATH=PATH, TARGET=TARGET)
#  print command
#  os.system(command)
