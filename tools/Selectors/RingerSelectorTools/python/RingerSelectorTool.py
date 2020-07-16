
__all__ = ['RingerSelectorTool']


from Gaugi import Algorithm
from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from Gaugi.gtypes import NotSet
import numpy as np
from EventAtlas import *


def norm1( data ):
  return (data/abs(sum(data))).reshape((1,100))


class RingerSelectorTool(Algorithm):

  def __init__(self, name, models_path, thresholds_path, preproc_callback=norm1, remove_last_activation=True ):

    Algorithm.__init__(self, name)
    self.models_path = models_path
    self.thresholds_path = thresholds_path
    self.__preproc_callback = preproc_callback
    self.remove_last_activation=remove_last_activation


  #
  # Apply the data transformation
  #
  def preproc( self, data ):
    return self.__preproc_callback(data)


  #
  # Inialize the selector
  #
  def initialize(self):

    # retrieve the keras model
    self.__models = self.import_all_models( self.models_path )
    # retrieve the thresholds
    self.__thresholds = self.import_all_thresholds( self.thresholds_path )

    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS


  #
  # Import all models from json to keras
  #
  def import_all_models( self, path ):

    # Discriminant model class
    class Model(object):
      def __init__( self, model, etmin, etmax, etamin, etamax):
        self.model=model; self._etmin=etmin; self._etmax=etmax; self._etamin=etamin; self._etamax=etamax
      def etmin(self):
        return self._etmin
      def etmax(self):
        return self._etmax
      def etamin(self):
        return self._etamin
      def etamax(self):
        return self._etamax
      def __call__(self):
        return self.model

    def _treat_weights( weights ):
      for i, w in enumerate(weights):
        weights[i] = np.array(w, dtype='float32')
      return weights

    import json
    from tensorflow.keras.models import model_from_json
    archieve = json.load(open(path,'r'))
    models = []
    for d in archieve['models']:
      #model = model_from_json( json.dumps(d['sequence'], separators=(',', ':')) )
      model = model_from_json( d['sequence'] )
      weights = _treat_weights(d['weights'])
      model.set_weights(weights)
      if self.remove_last_activation:
        model.pop()
      #model.summary()
      models.append( Model( model, d['etBin'][0], d['etBin'][1], d['etaBin'][0], d['etaBin'][1] ) )
    return models
  
  
  #
  # Import all thresholds from json to dict
  #
  def import_all_thresholds( self,path ):
   
    # Threshold model class
    class Threshold(object):
      def __init__( self, thresholds, etmin, etmax, etamin, etamax):
        self.thresholds=thresholds; self._etmin=etmin; self._etmax=etmax; self._etamin=etamin; self._etamax=etamax
      def etmin(self):
        return self._etmin
      def etmax(self):
        return self._etmax
      def etamin(self):
        return self._etamin
      def etamax(self):
        return self._etamax
      def __call__(self, avgmu):
        return avgmu*self.alpha() + self.beta()
      def alpha(self):
        return self.thresholds[0]
      def beta(self):
        return self.thresholds[1]
    
    import json
    thresholds = []
    archieve = json.load(open(path,'r'))
    for d in  archieve['thresholds']:
      thresholds.append( Threshold( d['threshold'], d['etBin'][0], d['etBin'][1], d['etaBin'][0], d['etaBin'][1] ) )
    # Return all phase spaces    
    return thresholds



  def accept( self, fc, avgmu):

    self.output=-999

    eta = abs(fc.eta())
    if eta>2.5: eta=2.5
    et = fc.et()*1e-3 # in GeV
  
    model = self.getModel(et,eta)
    
    # If not fount, return false
    if not model:
      return False
    
    # normalize the inpur data
    data = self.preproc( fc.ringsE() )
    # compute the output
    self.output = model().predict( data )[0][0]
    # get the threshold 
    threshold = self.getThreshold( et, eta )


    # If not fount, return false
    if not threshold:
      return False

    # If the output is below of the cut, reprove it
    if self.output <= threshold(avgmu):
      return False

    # If arrive until here, so the event was passed by the ringer
    return True



  def getDiscriminant(self):
    return self.output

  #
  # Get the corret model given all the phase spaces
  #
  def getModel( self, et, eta ):
    model = None
    for obj in self.__models:
      if et > obj.etmin() and et <= obj.etmax():
        if eta > obj.etamin() and eta <= obj.etamax():
          model=obj; break
    return model

  
   
  #
  # Get the correct threshold given all phase spaces
  #
  def getThreshold( self, et, eta ):
    threshold = None
    for obj in self.__thresholds:
      if et > obj.etmin() and et <= obj.etmax():
        if eta > obj.etamin() and eta <= obj.etamax():
          threshold=obj; break
    return threshold

  






