


def reshape_to_square_array( array ):
  import numpy as np
  size = array.shape
  array_copy = np.zeros( (max(size),max(size)) )
  def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
      yield l[i:i + n]
  # duplicate the column
  if size[0] > size[1]:
    for x in range(size[0]):
      gy = chunks( range(size[0]), int(size[0]/float(size[1])))
      for y, gy_ in enumerate(gy):
        for y_ in gy_:
          array_copy[x][y_] = array[x][y]
  else:
    for y in range(size[1]):
      gx = chunks( range(size[1]), int(size[1]/float(size[0])))
      for x, gx_ in enumerate(gx):
        for x_ in gx_:
          array_copy[x_][y] = array[x][y]
  return array_copy





