import re
from Gaugi import expandFolders

paths = expandFolders('JF17/')
pat = re.compile(r'.+(?P<binID>et(?P<etBinIdx>\d+).eta(?P<etaBinIdx>\d+))\..+$')
jobIDs = sorted(list(set([pat.match(f).group('binID')  for f in paths if pat.match(f) is not None]))) 


print jobIDs
