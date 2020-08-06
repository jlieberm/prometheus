





def convert_to_onnx_with_dummy_thresholds( models, name, version, signature, model_output_format ):


  import onnx
  import keras2onnx
  from ROOT import TEnv


  model_etmin_vec = []
  model_etmax_vec = []
  model_etamin_vec = []
  model_etamax_vec = []
  model_paths = []

  thr_etmin_vec = []
  thr_etmax_vec = []
  thr_etamin_vec = []
  thr_etamax_vec = []

  slopes = []
  offsets = []

  for model in models:

    model_etmin_vec.append( model['etBin'][0] )
    model_emax_vec.append( model['etBin'][1] )
    model_etamin_vec.append( model['etaBin'][0] )
    model_etamax_vec.append( model['etaBin'][1] )

    etBinIdx = model['etBinIdx']
    etaBinIdx = model['etaBinIdx']

    # Conver keras to Onnx
    onnx_model = keras2onnx.convert_keras(model['model'], model['model'].name)
    
    onnx_model_name = model_output_format%( etBinIdx, etaBinIdx )
    model_paths.append( onnx_model_name )
    
    # Save onnx mode!
    onnx.save_model(onnx_model, 'models/'+onnx_model_name)

    slopes.append( 0.0 )
    offsets.append( 0.0 )


  def list_to_str( l ):
    s = str()
    for ll in l:
      s+=str(ll)+'; '
    #s[-1]='' # remove last ;
    return s[:-2]



  # Write the config file 
  file = TEnv( 'ringer' )
  file.SetValue( "__name__", name )
  file.SetValue( "__version__", version )
  file.SetValue( "__operation__", operation )
  file.SetValue( "__signature__", signature )
  file.SetValue( "Model__size"  , str(len(models)) )
  file.SetValue( "Model__etmin" , list_to_str(model_etmin_vec) )
  file.SetValue( "Model__etmax" , list_to_str(model_etmax_vec) )
  file.SetValue( "Model__etamin", list_to_str(model_etamin_vec) )
  file.SetValue( "Model__etamax", list_to_str(model_etamax_vec) )
  file.SetValue( "Model__path"  , list_to_str( model_paths ) )
  file.SetValue( "Threshold__size"  , str(len(models)) )
  file.SetValue( "Threshold__etmin" , list_to_str(model_etmin_vec) )
  file.SetValue( "Threshold__etmax" , list_to_str(model_etmax_vec) )
  file.SetValue( "Threshold__etamin", list_to_str(model_etamin_vec) )
  file.SetValue( "Threshold__etamax", list_to_str(model_etamax_vec) )
  file.SetValue( "Threshold__slope" , list_to_str(slopes) )
  file.SetValue( "Threshold__offset", list_to_str(offsets) )
  file.SetValue( "Threshold__MaxAverageMu", 100)  
  file.WriteFile(output)









