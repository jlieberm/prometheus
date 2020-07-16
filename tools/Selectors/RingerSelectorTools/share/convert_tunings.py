

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
         'sequence' : model.to_json(),
         'weights'  : keras_weights_to_list(model.get_weights()),
         #'model'    : model,
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





for op in ['Tight','Medium','Loose','VeryLoose']:

  #cpath = "TrigL2_20170505_v6/TrigL2CaloRingerElectron"+op+"Constants.root"
  cpath = "TrigL2_20180125_v8/TrigL2CaloRingerElectron"+op+"Constants.root"
  #tpath = "TrigL2_20170505_v6/TrigL2CaloRingerElectron"+op+"Thresholds.root"
  tpath = "TrigL2_20180125_v8/TrigL2CaloRingerElectron"+op+"Thresholds.root"
  coutput = "TrigL2CaloRingerElectron"+op+"Constants.json"
  toutput = "TrigL2CaloRingerElectron"+op+"Thresholds.json"

  #convert_and_dump_models( cpath, coutput, 'v6', 'TrigL2_20170505_v6', op)
  convert_and_dump_models( cpath, coutput, 'v8', 'TrigL2_20180125_v8', op)
  #convert_and_dump_thresholds( tpath, toutput, 'v6', 'TrigL2_20170505_v6', op)
  convert_and_dump_thresholds( tpath, toutput, 'v8', 'TrigL2_20180125_v8', op)
  










