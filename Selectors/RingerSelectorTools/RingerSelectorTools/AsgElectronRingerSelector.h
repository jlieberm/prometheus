#ifndef RingerSelectorTools_AsgElectronRingerSelector
#define RingerSelectorTools_AsgElectronRingerSelector



// Atlas includes
#include "AsgTools/AsgTool.h"
#include <string>
#include <vector>
#include "RingerSelectorTools/IAsgElectronRingerSelector.h"
#include "RingerSelectorTools/tools/RingerSelectorTool.h"


namespace prometheus{



class AsgElectronRingerSelector : public asg::AsgTool,
                                  virtual public IAsgElectronRingerSelector
{

  ASG_TOOL_CLASS2(AsgElectronRingerSelector, IAsgElectronRingerSelector, IAsgSelectionTool)

  public:
    /// Standard constructor
    AsgElectronRingerSelector(std::string name);

    /// Standard destructor
    virtual ~AsgElectronRingerSelector();

    virtual StatusCode initialize();

    virtual StatusCode finalize();

    bool useCaloRings() const {return m_selectorTool.useCaloRings();};
    bool useTrack() const {return m_selectorTool.useTrack();};
    bool useShowerShape() const {return m_selectorTool.useShowerShape();};
    bool useTileCal() const {return m_selectorTool.useTileCal();};




  public:

     /** The main accept method: using the generic interface */
    virtual const Root::TAccept&  accept( const xAOD::IParticle* /*part*/ );

    virtual const Root::TAccept&  accept( double discriminant, double et, double eta, double mu);

    /** The main accept method: in case mu not in EventInfo online */
    //virtual bool accept( const xAOD::Electron* /*part*/, double /*mu*/ ) const;

    /** The main accept method: in case mu not in EventInfo online */
    //virtual bool accept( const xAOD::Egamma* /*part*/, double /*mu*/ ) const;





    double  calculate( double et, double eta, double mu,
                       double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                       double d0significance, double d0pvunbiased, double eProbabilityHT);

    double  calculate( std::vector<float>& rings, double et, double eta, double mu);

    double  calculate( std::vector<float>& rings, double et, double eta, double mu,
                       double deltaeta1, double deltaPoverP, double deltaPhiReescaled,
                       double d0significance, double d0pvunbiased, double eProbabilityHT);

    double  calculate( std::vector<float>& rings, double et, double eta, double mu,
                       double eratio, double reta, double rphi, double rhad, double weta2,
                       double f1, double f3);

    double  calculate( std::vector<float>& rings, double et, double eta, double mu,
                       double eratio, double reta, double rphi, double rhad, double weta2,
                       double f1, double f3, double deltaeta1, double deltaPoverP,
                       double deltaPhiReescaled, double d0significance, double d0pvunbiased,
                       double eProbabilityHT);

    virtual const Root::TAccept& getTAccept( ) const { // in base
      return m_accept;
    }


  private:


    //Discriminator configuration
    std::string m_constantsCalibPath, m_thresholdsCalibPath;
    // Ringer selector tool 
    Ringer::RingerSelectorTool m_selectorTool;
    /** A dummy return TAccept object */
    Root::TAccept m_acceptDummy;
    /** A  return TAccept object */
    Root::TAccept m_accept;

    
};// end class

}


#endif // rDev_AsgElectronRingerSelector
