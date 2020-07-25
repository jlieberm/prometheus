
__all__ = ['norm1']


#
# Normalize all rings by the abs total energy
#
def norm1( data ):
  return (data/abs(sum(data))).reshape((1,100))









