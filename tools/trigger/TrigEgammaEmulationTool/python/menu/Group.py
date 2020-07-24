
__all__ = ['Group']


#
# Group
#
class Group( object ):

  #
  # Constructor
  #
  def __init__( self, chain, pidname, etthr ):
    self.__chain = chain
    self.__pidname = pidname
    self.__etthr = etthr

    
  #
  # Get the chain object
  #
  def chain(self):
    return self._chain


  #
  # Get the offline pid name
  #
  def pidname(self):
    return self._pidname


  #
  # Get the offline Et thrshold
  #
  def etthr(self):
    return self._etthr

