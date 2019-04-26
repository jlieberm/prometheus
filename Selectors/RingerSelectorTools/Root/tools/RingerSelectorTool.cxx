
/*
  Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
*/


// Use this tool as base to asg or alg mt
#include "RingerSelectorTools/tools/RingerSelectorTool.h"
#include "RingerSelectorTools/tools/procedures/Norm1.h"
#include "RingerSelectorTools/tools/procedures/MultiLayerPerceptron.h"

using namespace Ringer;

RingerSelectorTool::RingerSelectorTool():
  IMsgService("RingerSelectorTool"),
  MsgService(MSG::INFO),
  m_reader("RingerReader"),
  m_useTrack(false),
  m_useCaloRings(true),
  m_useShowerShape(false),
  m_useTileCal(true)
{;}


RingerSelectorTool::~RingerSelectorTool()
{
  MSG_INFO("Finalizing this tool....");
}


bool  RingerSelectorTool::initialize()
{
  if(!m_thresholdsCalibPath.empty()){
    if(!m_reader.retrieve(m_thresholdsCalibPath, m_cutDefs)){
      MSG_ERROR("Can not retrieve the information from " << m_thresholdsCalibPath );
      return false;
    }
    // retrieve metadata
    m_doPileupCorrection = m_reader.doPileupCorrection();
    m_lumiCut  = m_reader.lumiCut();
  }

  // Retrieve the NeuralNetwork list
  if(!m_constantsCalibPath.empty()){
    if(!m_reader.retrieve(m_constantsCalibPath, m_discriminators)){
      MSG_ERROR("Can not retrieve all information from " << m_constantsCalibPath );
      return false;
    }

    m_useShowerShape=m_reader.useShowerShape();
    m_useTrack=m_reader.useTrack();
    m_useCaloRings=m_reader.useCaloRings();
    m_useTileCal=m_reader.useTileCal();
    m_removeOutputTansigTF=m_reader.removeOutputTansigTF();

  }
  

  // Use Norm1 as default for rings normalization only!
  for(unsigned i=0; i<m_discriminators.size();++i)  m_preprocs.push_back( std::make_shared< Ringer::Norm1 > (-999.,999.,-999.,999.,-999.,999.,true));
  
  

  MSG_INFO("Using the activation function in the last layer? " <<  (m_removeOutputTansigTF ? "No":"Yes") );
  MSG_INFO("Using the Correction?                            " <<  (m_doPileupCorrection ? "Yes":"No") );
  MSG_INFO("Using lumi threshold equal: "  <<  m_lumiCut );
  MSG_INFO("Initialization completed successfully." );
  return true;

}


bool  RingerSelectorTool::finalize(){
  return true;
}


double  RingerSelectorTool::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double eratio, double reta, double rphi, double rhad, double weta2,
                                              double f1, double f3 ) 
{

  float output = -999;
  // It's ready to select the correct eta/et bin
  std::shared_ptr<Ringer::IModel>         discr;
  std::shared_ptr<Ringer::INormalization> preproc;

  // Apply the discriminator
  if(retrieve(et,eta,mu,discr,preproc)){
    
    //MSG_DEBUG(( "ringer->rings().size() is: " <<rings.size());
    std::vector<float> refRings(rings.size());
    refRings.assign(rings.begin(), rings.end());
 
    // norm1 calo rings
    if(preproc)  preproc->execute(refRings);

    // standards calo variables
    refRings.push_back(eratio/1.0);
    refRings.push_back(reta/1.0);
    refRings.push_back(rphi/1.0);
    refRings.push_back(rhad/0.1);
    refRings.push_back(weta2/0.02);
    refRings.push_back(f1/0.6);
    refRings.push_back(f3/0.04);
    auto answer = discr->propagate(refRings);
    m_outputBeforeTheActivationFunction = answer.outputBeforeTheActivationFunction;
    m_output = answer.output;


    if(m_removeOutputTansigTF){
      output = answer.outputBeforeTheActivationFunction;
    }else{
      output = answer.output;
    }


  }else{
    MSG_DEBUG("There is no discriminator into this Fex." );
  }//
  return output;
}





double  RingerSelectorTool::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double eratio, double reta, double rphi, double rhad, double weta2,
                                              double f1, double f3, double deltaeta1, double deltaPoverP, 
                                              double deltaPhiReescaled, double d0significance, double d0pvunbiased, 
                                              double eProbabilityHT)
{

  float  output = -999;
  ///It's ready to select the correct eta/et bin
  std::shared_ptr<Ringer::IModel>         discr;
  std::shared_ptr<Ringer::INormalization> preproc;


 ///Apply the discriminator
  if(retrieve(et,eta,mu,discr,preproc)){
    
    //MSG_DEBUG(( "ringer->rings().size() is: " <<rings.size());
    std::vector<float> refRings(rings.size());
    refRings.assign(rings.begin(), rings.end());
 
    // norm1 calo rings
    if(preproc)  preproc->execute(refRings);
    // standards calo variables
    refRings.push_back(eratio/1.0);
    refRings.push_back(reta/1.0);
    refRings.push_back(rphi/1.0);
    refRings.push_back(rhad/0.1);
    refRings.push_back(weta2/0.02);
    refRings.push_back(f1/0.6);
    refRings.push_back(f3/0.04);
    // track variables
    refRings.push_back(deltaeta1/0.05);
    refRings.push_back(deltaPoverP/1.0);
    refRings.push_back(deltaPhiReescaled/0.05);
    refRings.push_back(d0significance/6.0);
    refRings.push_back(d0pvunbiased/0.2);
    refRings.push_back(eProbabilityHT/1.0);
    // Add extra variables in this order! Do not change this!!!
 
    auto answer = discr->propagate(refRings);
    m_outputBeforeTheActivationFunction = answer.outputBeforeTheActivationFunction;
    m_output = answer.output;

   
    if(m_removeOutputTansigTF){
      output = answer.outputBeforeTheActivationFunction;
    }else{
      output = answer.output;
    }


  }else{
    MSG_DEBUG( "There is no discriminator into this Fex." );
  }//
  return output;
}




double  RingerSelectorTool::calculate( std::vector<float>& rings, double et, double eta, double mu,
                                              double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                                              double d0significance, double d0pvunbiased, double eProbabilityHT)

{
  
  float output=-999.;

  // It's ready to select the correct eta/et bin
  std::shared_ptr<Ringer::IModel>         discr;
  std::shared_ptr<Ringer::INormalization> preproc;


  // Apply the discriminator
  if(retrieve(et,eta,mu,discr,preproc)){
    
    //MSG_DEBUG(( "ringer->rings().size() is: " <<rings.size());
    std::vector<float> refRings(rings.size());
    refRings.assign(rings.begin(), rings.end());
    if(preproc)  preproc->execute(refRings);
    refRings.push_back(deltaeta1/0.05);
    refRings.push_back(deltaPoverP/1.0);
    refRings.push_back(deltaPhiReescaled/0.05);
    refRings.push_back(d0significance/6.0);
    refRings.push_back(d0pvunbiased/0.2);
    refRings.push_back(eProbabilityHT/1.0);
    // Add extra variables in this order! Do not change this!!!
    
    auto answer = discr->propagate(refRings);
    m_outputBeforeTheActivationFunction = answer.outputBeforeTheActivationFunction;
    m_output = answer.output;

   
    if(m_removeOutputTansigTF){
      output = answer.outputBeforeTheActivationFunction;
    }else{
      output = answer.output;
    }



  }else{
    MSG_DEBUG( "There is no discriminator into this Fex." );
  }//
  return output;
}

double  RingerSelectorTool::calculate( std::vector<float>& rings, double et, double eta, double mu)

{
  
  float output = -999;
  ///It's ready to select the correct eta/et bin
  std::shared_ptr<Ringer::IModel>         discr;
  std::shared_ptr<Ringer::INormalization> preproc;


  ///Apply the discriminator
  if(retrieve(et,eta,mu,discr,preproc)){
    //MSG_DEBUG(( "ringer->rings().size() is: " <<rings.size());
    std::vector<float> refRings(rings.size());
    refRings.assign(rings.begin(), rings.end());
    // Apply preprocessor
    if(preproc)  preproc->execute(refRings);
    auto answer = discr->propagate(refRings);
    m_outputBeforeTheActivationFunction = answer.outputBeforeTheActivationFunction;
    m_output = answer.output;

   
    if(m_removeOutputTansigTF){
      output = answer.outputBeforeTheActivationFunction;
    }else{
      output = answer.output;
    }



  }else{
    MSG_DEBUG( "There is no discriminator into this Fex." );
  }//

  return output;
}




double  RingerSelectorTool::calculate( double et, double eta, double mu,
                                              double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                                              double d0significance, double d0pvunbiased, double eProbabilityHT)
{

  ///It's ready to select the correct eta/et bin
  std::shared_ptr<Ringer::IModel>         discr;
  std::shared_ptr<Ringer::INormalization> preproc;

  float output = -999;
  ///Apply the discriminator
  if(retrieve(et,eta,mu,discr,preproc)){
    std::vector<float> refRings;
    refRings.push_back(deltaeta1/0.05);
    refRings.push_back(deltaPoverP/1.0);
    refRings.push_back(deltaPhiReescaled/0.05);
    refRings.push_back(d0significance/6.0);
    refRings.push_back(d0pvunbiased/0.2);
    refRings.push_back(eProbabilityHT/1.0);
    // Add extra variables in this order! Do not change this!!!
    auto answer = discr->propagate(refRings);
    m_outputBeforeTheActivationFunction = answer.outputBeforeTheActivationFunction;
    m_output = answer.output;

   
    if(m_removeOutputTansigTF){
      output = answer.outputBeforeTheActivationFunction;
    }else{
      output = answer.output;
    }

  }else{
    MSG_DEBUG( "There is no discriminator into this Fex." );
  }//
  return output;
}


bool  RingerSelectorTool::accept( double discriminant, double et, double eta, double mu) 
  
const {

  eta = std::fabs(eta);
  if(eta>2.50) eta=2.50;///fix for events out of the ranger
  et  = et*1e-3; ///in GeV
  double threshold = 0.0;
  double avgmu = mu;
  //m_doPileupCorrection=false; 
  //Apply cut
  for(unsigned i=0; i < m_cutDefs.size(); ++i){
    if((avgmu  > m_cutDefs[i]->mumin()) && (avgmu  <= m_cutDefs[i]->mumax())){
      if((et  > m_cutDefs[i]->etmin()) && (et  <= m_cutDefs[i]->etmax())){
        if((eta > m_cutDefs[i]->etamin()) && (eta <= m_cutDefs[i]->etamax())){
          
          if(m_doPileupCorrection){
            // Limited Pileup
            if(avgmu>m_lumiCut)
              avgmu=m_lumiCut;
            //MSG_DEBUG(("Apply avgmu == " << avgmu);
            threshold = m_cutDefs[i]->threshold(avgmu);
            //MSG_DEBUG(("With correction, thr = "<<threshold);
          }else{
            threshold = m_cutDefs[i]->threshold();
            //MSG_DEBUG( "Without correction, thr = "<<threshold );
          }
        }
      }
    }
  }// Loop over cutDefs

  if(discriminant >= threshold){
    //MSG_DEBUG( "Event approved by discriminator." );
    return true;
    //m_accept.setCutResult("NeuralCut", true);
  }

  //return m_accept;
  return false;
}




bool RingerSelectorTool::retrieve(double et, double eta, double mu, std::shared_ptr<Ringer::IModel> &discr, std::shared_ptr<Ringer::INormalization> &preproc)

const {

  eta = std::fabs(eta);
  if(eta>2.50) eta=2.50;///fix for events out of the ranger
  //et  = et*1e-3; ///in GeV
  
  if(m_discriminators.size() > 0){
    for(unsigned i=0; i<m_discriminators.size(); ++i){
      //MSG_INFO(m_discriminators[i]->etmin()<<"<Et(" <<et<< ")<="<<m_discriminators[i]->etmax());
      //MSG_INFO(m_discriminators[i]->etamin()<<"<Eta(" <<eta<< ")<="<<m_discriminators[i]->etamax());
      if(mu > m_discriminators[i]->mumin() && mu <= m_discriminators[i]->mumax()){
        if(et > m_discriminators[i]->etmin() && et <= m_discriminators[i]->etmax()){
          if(eta > m_discriminators[i]->etamin() && eta <= m_discriminators[i]->etamax()){
            discr   = m_discriminators[i];
            preproc = m_preprocs[i];
            return true;
          }///eta conditions
        }///Et conditions
      }///Mu conditions
    }///Loop over discriminators
  }
  return false;
}



