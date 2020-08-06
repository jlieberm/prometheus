

import json
from ROOT import TFile, TTree
import numpy as np


def stdvector_to_list(vec, size=None):
  if size:
    l=size*[0]
  else:
    l = vec.size()*[0]
  for i in range(vec.size()):
    l[i] = vec[i]
  return l


#
# Convert the Tuning tool's format to keras model
#
def convert2keras( neuron, W, B ):
  # Build the standard model
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Dropout, Activation
  model  = Sequential()
  model.add( Dense( neuron , input_shape= (100,), activation = 'tanh') )
  model.add( Dense( 1, activation='linear' ) )
  model.add( Activation('tanh') )
  w0 = []; b0 = []
  for l in range(neuron):
    w0X=[]
    for i in range(100):
      w0X.append( W.pop(0) )
    w0.append(w0X)
    b0.append( B.pop(0) )
  w1 = W; b1 = B
  ww = np.array([ np.array(w0).T, np.array(b0), np.array(w1), np.array(b1) ] )
  ww[2]=ww[2].reshape((ww[2].shape[0],1))
  model.set_weights(ww)
  
  model.pop()
  model.summary()
  return model



def keras_weights_to_list( weights ):
  for i, w in enumerate(weights):
    weights[i]=w.tolist()
  return weights


def weights_list_to_keras( weights ):
  for i, w in enumerate(weights):
    weights[i]=np.array(w,dtype='float32')
  return weights




#
# Convert the root to dict
#
def get_discriminators( fname ):

  f = TFile( fname , 'read' )
  t = f.Get("tuning/discriminators")
  models = []
  for entry in t:      
    nodes = stdvector_to_list(t.nodes)
    w = stdvector_to_list(t.weights)
    b = stdvector_to_list(t.bias)
    model = convert2keras( nodes[1], w, b )
    d = {
         #'sequence' : model.to_json(),
         #'weights'  : keras_weights_to_list(model.get_weights()),
         'model'    : model,
         'etBin'    : stdvector_to_list(t.etBin),
         'etaBin'   : stdvector_to_list(t.etaBin),
         }
    models.append(d)
  return models


#
# Conver root to dict
#
def get_thresholds( fname ):

  f = TFile( fname , 'read' )
  t = f.Get("tuning/thresholds")
  cuts = []
  for entry in t:      
    thresholds = stdvector_to_list(t.thresholds)
    d = {
          'threshold' : thresholds,
          'etBin'     : stdvector_to_list(t.etBin),
          'etaBin'    : stdvector_to_list(t.etaBin),
          'muBin'     : [0,100],
         }
    cuts.append( d )
  return cuts

    
 


#
# Import all models from json to keras
#
def import_all_models( path ):
  
  import json
  from tensorflow.keras.models import model_from_json
  archieve = json.load(open(path,'r'))
  models = []
  for d in archieve['models']:
    #model = model_from_json( json.dumps(d['sequence'], separators=(',', ':')) )
    model = model_from_json( d['sequence'] )
    weights = weights_list_to_keras(d['weights'])
    model.set_weights(weights)
    model.summary()
    models.append( {'etBin' : d['etBin'],
                    'etaBin': d['etaBin'],
                    'muBin' : [0,100],
                    'model' : model
                    })
  return models


#
# Import all thresholds from json to dict
#
def import_all_thresholds( path ):
 
  import json
  archieve = json.load(open(path,'r'))
  return archieve['thresholds']






#
# Dump the root file into the new json format
#
def convert_and_dump_models( path, outname, version='', name='', operation_point=''):

  discrs = get_discriminators(path)
  archieve = {
                'models'          : discrs,
                '__version__'     : version,
                '__name__'        : name,
                '__description__' : "",
                '__type__'        : 'Model',
                '__operation__'   : operation_point,
             }
  
  with open(outname,"w") as f:
    json.dump(archieve,f)



#
# Dump the root file into the new json format
#
def convert_and_dump_thresholds( path, outname, version='', name='', operation_point=''):

  thr = get_thresholds(path)
  archieve = {
                'thresholds'      : thr,
                '__version__'     : version,
                '__name__'        : name,
                '__description__' : "",
                '__type__'        : 'Threshold',
                '__operation__'   : operation_point,
             }
  
  with open(outname,"w") as f:
    json.dump(archieve,f)



def convert_to_onnx( cpath, tpath, version, name, operation_point, maxAvgmu, tname, output, netas ):


  models = get_discriminators(cpath)
  thresholds = get_thresholds(tpath)

  import onnx
  import keras2onnx


  from ROOT import TEnv
  file = TEnv( 'ringer' )

  model_et_lower_edges = []
  model_et_high_edges = []
  model_eta_lower_edges = []
  model_eta_high_edges = []

  thr_et_lower_edges = []
  thr_et_high_edges = []
  thr_eta_lower_edges = []
  thr_eta_high_edges = []

  slopes = []
  offsets = []

  model_paths = []


  et=0; eta=0

  for idx, model in enumerate(models):

    model_et_lower_edges.append( model['etBin'][0] )
    model_et_high_edges.append( model['etBin'][1] )

    model_eta_lower_edges.append( model['etaBin'][0] )
    model_eta_high_edges.append( model['etaBin'][1] )

    onnx_model_name = tname%( et, eta )
    onnx_model = keras2onnx.convert_keras(model['model'], model['model'].name)
    onnx.save_model(onnx_model, 'models/'+onnx_model_name+'.onnx')

    model_paths.append( onnx_model_name + '.onnx')


    # serialize model to JSON
    model_json = model['model'].to_json()
    with open("models/%s.json"%onnx_model_name, "w") as json_file:
      json_file.write(model_json)
    # serialize weights to HDF5
    model['model'].save_weights("models/%s.h5"%onnx_model_name)


    eta+=1
    if eta==netas:
      eta=0
      et+=1


  for idx, thr in enumerate( thresholds ):

    thr_et_lower_edges.append( thr['etBin'][0] )
    thr_et_high_edges.append( thr['etBin'][1] )

    thr_eta_lower_edges.append( thr['etaBin'][0] )
    thr_eta_high_edges.append( thr['etaBin'][1] )

    slopes.append( thr['threshold'][0] )
    offsets.append( thr['threshold'][1] )


  def list_to_str( l ):
    s = str()
    for ll in l:
      s+=str(ll)+'; '
    #s[-1]='' # remove last ;
    return s[:-2]



  
  file.SetValue( "__name__", name )
  file.SetValue( "__version__", version )
  file.SetValue( "__operation__", operation_point )
  file.SetValue( "__signature__", 'electron' )


  file.SetValue( "Model__size"  , str(len(models)) )
  file.SetValue( "Model__etmin" , list_to_str(model_et_lower_edges) )
  file.SetValue( "Model__etmax" , list_to_str(model_et_high_edges) )
  file.SetValue( "Model__etamin", list_to_str(model_eta_lower_edges) )
  file.SetValue( "Model__etamax", list_to_str(model_eta_high_edges) )
  file.SetValue( "Model__path"  , list_to_str( model_paths ) )


  file.SetValue( "Threshold__size"  , str(len(thresholds)) )
  file.SetValue( "Threshold__etmin" , list_to_str(thr_et_lower_edges) )
  file.SetValue( "Threshold__etmax" , list_to_str(thr_et_high_edges) )
  file.SetValue( "Threshold__etamin", list_to_str(thr_eta_lower_edges) )
  file.SetValue( "Threshold__etamax", list_to_str(thr_eta_high_edges) )
  file.SetValue( "Threshold__slope" , list_to_str(slopes) )
  file.SetValue( "Threshold__offset", list_to_str(offsets) )
  file.SetValue( "Threshold__MaxAverageMu", str(maxAvgmu) )
  
  
  
  file.WriteFile(output)










for op in ['Tight','Medium','Loose','VeryLoose']:

  cpath = "TrigL2_20180125_v8/TrigL2CaloRingerElectron"+op+"Constants.root"
  tpath = "TrigL2_20180125_v8/TrigL2CaloRingerElectron"+op+"Thresholds.root"
  convert_to_onnx( cpath, tpath , 'v8', 'TrigL2_20180125_v8', op, 100, 
      'data17_13TeV_EGAM1_probes_lhmedium_EGAM7_vetolhvloose.model_v8.electron'+op+'.et%d_eta%d',
      "ElectronRinger%sTriggerConfig.conf"%op, 5)



#for op in ['Tight','Medium','Loose','VeryLoose']:
#
#  cpath = "TrigL2_20170505_v6/TrigL2CaloRingerElectron"+op+"Constants.root"
#  tpath = "TrigL2_20170505_v6/TrigL2CaloRingerElectron"+op+"Thresholds.root"
#  convert_to_onnx( cpath, tpath , 'v6', 'TrigL2_20170505_v6', op, 40, 
#      'mc15_13TeV.423300.Zee_probes_lhmedium.423300.JF17_Truth.model_v6.electron'+op+'.et%d_eta%d',
#      "ElectronRinger%sTriggerConfig.conf"%op, 4)








