
__all__ = ['RingerSelectorTool']


from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi.messenger.macros import *
from EventAtlas import Accept
import numpy as np



#
# Hypo tool
#
class RingerSelectorTool(Algorithm):

  __property = [
                "ConfigFile",
                "Preproc"
                ]

  #
  # Constructor
  #
  def __init__(self, name, **kw  ):

    Algorithm.__init__(self, name)
   
    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)

    self.__models = []
    self.__thresholds = []
 

  #
  # Inialize the selector
  #
  def initialize(self):


    #
    # Onnx model inference
    #
    class OnnxModel(object):

      def __init__( self, modelPath, etmin, etmax, etamin, etamax):
        self._etmin=etmin; self._etmax=etmax; self._etamin=etamin; self._etamax=etamax
        import onnxruntime as rt
        self._session = rt.InferenceSession(modelPath)
        self._input_name = self._session.get_inputs()[0].name
        self._input_shape = self._session.get_inputs()[0].shape
        self._input_type = self._session.get_inputs()[0].type
        self._output_name = self._session.get_outputs()[0].name

      def predict( self, input ):
        return self._session.run([self._output_name], {self._input_name: input})

      def etmin(self):
        return self._etmin
      def etmax(self):
        return self._etmax
      def etamin(self):
        return self._etamin
      def etamax(self):
        return self._etamax

    # 
    # Threshold model class
    #
    class Threshold(object):
      def __init__( self, slope, offset, etmin, etmax, etamin, etamax):
        self.slope=slope; self.offset=offset; self._etmin=etmin; self._etmax=etmax; self._etamin=etamin; self._etamax=etamax
      def etmin(self):
        return self._etmin
      def etmax(self):
        return self._etmax
      def etamin(self):
        return self._etamin
      def etamax(self):
        return self._etamax
      def __call__(self, avgmu):
        return avgmu*self.slope + self.offset
    

    def treat_float( env, key ):
      return [float(value) for value in  env.GetValue(key, '').split('; ')]
    
    def treat_string( env, key ):
      return [str(value) for value in  env.GetValue(key, '').split('; ')]

    configPath = self.getProperty( "ConfigFile" )

    MSG_INFO( self, "Reading tuning from: %s", configPath )
    basepath = '/'.join(configPath.split('/')[:-1])

    from ROOT import TEnv



    env = TEnv( configPath )

    version = env.GetValue("__version__", '')
    number_of_models = env.GetValue("Model__size", 0)
    etmin_list = treat_float( env, 'Model__etmin' )
    etmax_list = treat_float( env, 'Model__etmax' )
    etamin_list = treat_float( env, 'Model__etamin' )
    etamax_list = treat_float( env, 'Model__etamax' )
    paths = treat_string( env, 'Model__path' )
    
    for idx, path in enumerate( paths ):
      model = OnnxModel( basepath+'/models/'+path, etmin_list[idx], etmax_list[idx], etamin_list[idx], etamax_list[idx] ) 
      self.__models.append(model)

    number_of_thresholds = env.GetValue("Threshold__size", 0)
    self.__maxAverageMu = env.GetValue("Threshold__MaxAverageMu", 0)
    etmin_list = treat_float( env, 'Threshold__etmin' )
    etmax_list = treat_float( env, 'Threshold__etmax' )
    etamin_list = treat_float( env, 'Threshold__etamin' )
    etamax_list = treat_float( env, 'Threshold__etamax' )
    slopes = treat_float( env, 'Threshold__slope' )
    offsets = treat_float( env, 'Threshold__offset' )
 
    for idx, slope in enumerate(slopes):
      threshold = Threshold( slope, offsets[idx], etmin_list[idx], etmax_list[idx], etamin_list[idx], etamax_list[idx] ) 
      self.__thresholds.append(threshold)

    MSG_INFO( self, "Tuning version: %s" , version )
    MSG_INFO( self, "Loaded %d models using onnx runtime for inference." , number_of_models)
    MSG_INFO( self, "Loaded %d threshold for decision" , number_of_thresholds)
    MSG_INFO( self, "Max Average mu equal %1.2f", self.__maxAverageMu )


    return StatusCode.SUCCESS



  def accept( self, context):

    accept = self.__getAcceptInfo()
    fc = context.getHandler("HLT__FastCaloContainer")
    eventInfo = context.getHandler( "EventInfoContainer" )
    avgmu = eventInfo.avgmu()

    eta = abs(fc.eta())
    if eta>2.5: eta=2.5
    et = fc.et()*1e-3 # in GeV
    if avgmu > self.__maxAverageMu: avgmu = self.__maxAverageMu

    # get the model for inference
    model = self.__getModel(et,eta)
    
    # If not fount, return false
    if not model:
      return accept
    
    
    # get the threshold 
    threshold = self.__getThreshold( et, eta )

    # If not fount, return false
    if not threshold:
      return accept

    # Until here, we have all to run it!

    # apply the normalization step
    preproc = self.getProperty("Preproc")
    # normalize the inpur data
    data = preproc( fc.ringsE() )
    # compute the output
    output = model.predict( data )[0][0][0]
    
    accept.setDecor("discriminant", output)

    # If the output is below of the cut, reprove it
    if output <= threshold(avgmu):
      return accept

    # If arrive until here, so the event was passed by the ringer
    accept.setCutResult( "Pass", True )
    return accept



  #
  # Get the corret model given all the phase spaces
  #
  def __getModel( self, et, eta ):
    model = None
    for obj in self.__models:
      if et > obj.etmin() and et <= obj.etmax():
        if eta > obj.etamin() and eta <= obj.etamax():
          model=obj; break
    return model
  
   
  #
  # Get the correct threshold given all phase spaces
  #
  def __getThreshold( self, et, eta ):
    threshold = None
    for obj in self.__thresholds:
      if et > obj.etmin() and et <= obj.etmax():
        if eta > obj.etamin() and eta <= obj.etamax():
          threshold=obj; break
    return threshold

  #
  # Get the accept object
  #
  def __getAcceptInfo( self ):
    
    accept = Accept(self.name())
    self.output=-999
    accept.setCutResult( "Pass", False )
    accept.setDecor( "discriminant", self.output )
    return accept


