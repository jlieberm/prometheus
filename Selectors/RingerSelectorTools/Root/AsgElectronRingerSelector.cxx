


#include "RingerSelectorTools/AsgElectronRingerSelector.h"


using namespace prometheus;

AsgElectronRingerSelector::AsgElectronRingerSelector(std::string name):
  asg::AsgTool(name),
  m_selectorTool()
{
  declareProperty("ConstantsCalibPath"  , m_constantsCalibPath=""              );
  declareProperty("ThresholdsCalibPath" , m_thresholdsCalibPath=""             );
}


AsgElectronRingerSelector::~AsgElectronRingerSelector()
{

  ATH_MSG_INFO("Finalizing this tool....");
}


StatusCode AsgElectronRingerSelector::initialize()
{
  m_selectorTool.setConstantsCalibPath( m_constantsCalibPath ); 
  m_selectorTool.setThresholdsCalibPath( m_thresholdsCalibPath ); 

  if(m_selectorTool.initialize().isFailure())
    return StatusCode::FAILURE;
  
  m_accept.addCut("NeuralCut","pass by neural threshold");
  ATH_MSG_INFO("RingerSelectorTools initialization completed successfully.");
  return StatusCode::SUCCESS;
}


StatusCode AsgElectronRingerSelector::finalize(){
  
  if(m_selectorTool.finalize().isFailure())
    return StatusCode::FAILURE;
  ATH_MSG_INFO("RingerSelectorTools finalization completed successfully.");
  return StatusCode::SUCCESS;
}




double  AsgElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double eratio, double reta, double rphi, double rhad, double weta2,
                                              double f1, double f3 ) 
{
  return m_selectorTool.calculate(rings,et,eta,mu,eratio,reta,rphi,rhad,weta2,f1,f3);
}





double  AsgElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double eratio, double reta, double rphi, double rhad, double weta2,
                                              double f1, double f3, double deltaeta1, double deltaPoverP, 
                                              double deltaPhiReescaled, double d0significance, double d0pvunbiased, 
                                              double eProbabilityHT)
{
  return m_selectorTool.calculate( rings, et,  eta,  mu,
                                   eratio, reta, rphi, rhad, weta2,
                                   f1, f3, deltaeta1, deltaPoverP, 
                                   deltaPhiReescaled,  d0significance, d0pvunbiased, 
                                   eProbabilityHT);

}




double  AsgElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                                              double d0significance, double d0pvunbiased, double eProbabilityHT)
{
  return m_selectorTool.calculate( rings, et,  eta,  mu,
                                   deltaeta1, deltaPoverP, 
                                   deltaPhiReescaled,  d0significance, d0pvunbiased, 
                                   eProbabilityHT);


}


double  AsgElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu) 
{
  return m_selectorTool.calculate(rings,et,eta,mu);
}


double  AsgElectronRingerSelector::calculate( double et, double eta, double mu,
                                              double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                                              double d0significance, double d0pvunbiased, double eProbabilityHT)
{
  return m_selectorTool.calculate( et,  eta,  mu,
                                   deltaeta1, deltaPoverP, 
                                   deltaPhiReescaled,  d0significance, d0pvunbiased, 
                                   eProbabilityHT);


}


const Root::TAccept& AsgElectronRingerSelector::accept( double discriminant, double et, double eta, double mu)
{
  bool passed =  m_selectorTool.accept( discriminant, et,eta,mu);
  m_accept.setCutResult("NeuralCut", passed);
  return m_accept;
}




float AsgElectronRingerSelector::output()
{
  return m_selectorTool.output();
}

float AsgElectronRingerSelector::outputBeforeTheActivationFunction()
{
  return m_selectorTool.outputBeforeTheActivationFunction();
}




