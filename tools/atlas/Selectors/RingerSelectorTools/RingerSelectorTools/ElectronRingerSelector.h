#ifndef RingerSelectorTools_ElectronRingerSelector
#define RingerSelectorTools_ElectronRingerSelector



// Atlas includes
#include <string>
#include <vector>
//#include "RingerSelectorTools/IAsgElectronRingerSelector.h"
#include "RingerSelectorTools/tools/RingerSelectorTool.h"

namespace prometheus{



class ElectronRingerSelector
{


  public:
    /// Standard constructor
    ElectronRingerSelector(std::string name);

    /// Standard destructor
    ~ElectronRingerSelector();

    bool initialize();
    bool finalize();

    bool useCaloRings() const {return m_selectorTool.useCaloRings();};
    bool useTrack() const {return m_selectorTool.useTrack();};
    bool useShowerShape() const {return m_selectorTool.useShowerShape();};
    bool useTileCal() const {return m_selectorTool.useTileCal();};

    void setConstantsCalibPath(std::string s){m_constantsCalibPath=s;};
    void setThresholdsCalibPath(std::string s){m_thresholdsCalibPath=s;};
 

    bool accept( double discriminant, double et, double eta, double mu);




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


    float output();
    float outputBeforeTheActivationFunction();




  private:


    //Discriminator configuration
    std::string m_constantsCalibPath, m_thresholdsCalibPath;
    // Ringer selector tool 
    Ringer::RingerSelectorTool m_selectorTool;
    
};// end class

}


#endif // rDev_AsgElectronRingerSelector
