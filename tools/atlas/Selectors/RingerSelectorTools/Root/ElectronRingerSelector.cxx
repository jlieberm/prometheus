


#include "RingerSelectorTools/ElectronRingerSelector.h"
#include <iostream>


#define MSG_INFO( msg )        \
std::cout << msg << std::endl; \


using namespace prometheus;

ElectronRingerSelector::ElectronRingerSelector(std::string /*name*/):
  m_selectorTool()
{;}


ElectronRingerSelector::~ElectronRingerSelector()
{
  MSG_INFO("Finalizing this tool....");
}


bool ElectronRingerSelector::initialize()
{
  m_selectorTool.setConstantsCalibPath( m_constantsCalibPath ); 
  m_selectorTool.setThresholdsCalibPath( m_thresholdsCalibPath ); 

  if(!m_selectorTool.initialize())
    return false;
  
  MSG_INFO("RingerSelectorTools initialization completed successfully.");
  return true;
}


bool ElectronRingerSelector::finalize(){
  
  if(!m_selectorTool.finalize())
    return false;
  MSG_INFO("RingerSelectorTools finalization completed successfully.");
  return true;
}




double  ElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double eratio, double reta, double rphi, double rhad, double weta2,
                                              double f1, double f3 ) 
{
  return m_selectorTool.calculate(rings,et,eta,mu,eratio,reta,rphi,rhad,weta2,f1,f3);
}





double  ElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu,
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




double  ElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                                              double d0significance, double d0pvunbiased, double eProbabilityHT)
{
  return m_selectorTool.calculate( rings, et,  eta,  mu,
                                   deltaeta1, deltaPoverP, 
                                   deltaPhiReescaled,  d0significance, d0pvunbiased, 
                                   eProbabilityHT);


}


double  ElectronRingerSelector::calculate( std::vector<float>& rings, double et, double eta, double mu) 
{
  return m_selectorTool.calculate(rings,et,eta,mu);
}


double  ElectronRingerSelector::calculate( double et, double eta, double mu,
                                              double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                                              double d0significance, double d0pvunbiased, double eProbabilityHT)
{
  return m_selectorTool.calculate( et,  eta,  mu,
                                   deltaeta1, deltaPoverP, 
                                   deltaPhiReescaled,  d0significance, d0pvunbiased, 
                                   eProbabilityHT);


}


bool ElectronRingerSelector::accept( double discriminant, double et, double eta, double mu)
{
  return m_selectorTool.accept( discriminant, et,eta,mu);
}




float ElectronRingerSelector::output()
{
  return m_selectorTool.output();
}

float ElectronRingerSelector::outputBeforeTheActivationFunction()
{
  return m_selectorTool.outputBeforeTheActivationFunction();
}




