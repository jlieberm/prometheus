#ifndef RINGERSELECTORTOOLS_IAsgElectronRingerSelector
#define RINGERSELECTORTOOLS_IAsgElectronRingerSelector
/**
   @class IAsgElectronRingerSelector
   @brief Interface to tool to select electrons from HLT
   31-AGO-2017, convert to ASG tool
*/

// Include the interfaces
#include "PATCore/IAsgSelectionTool.h"




namespace prometheus{

class IAsgElectronRingerSelector : 
  virtual public IAsgSelectionTool
{

  ASG_TOOL_INTERFACE(IAsgElectronRingerSelector)

  public:

  /**Virtual Destructor*/
  IAsgElectronRingerSelector() {};
  virtual ~IAsgElectronRingerSelector() {};

  /** The main accept method: using the generic interface */
  virtual const Root::TAccept& accept( const xAOD::IParticle* /*part*/ ) const=0;
  virtual const Root::TAccept& accept( float, float, float, float  ) const=0;

  /** The main accept method: in case mu not in EventInfo online */
  //virtual const Root::TAccept& accept( const xAOD::Electron* /*part*/, double /*mu*/ ) const = 0;

  /** The main accept method: in case mu not in EventInfo online */
  //virtual const Root::TAccept& accept( const xAOD::Egamma* /*part*/, double /*mu*/ ) const = 0;



}; // End: class definition



}
#endif // rDev_IAsgElectronRingerSelector
