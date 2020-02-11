/*
  Copyright (C) 2002-2019 CERN for the benefit of the ATLAS collaboration
*/


#ifndef RINGERSELECTORTOOLS_NORM1_H     
#define RINGERSELECTORTOOLS_NORM1_H

#include <vector>
#include "RingerSelectorTools/tools/procedures/INormalization.h"

namespace Ringer{

  class Norm1 : public INormalization{
    
    public:
      Norm1(double etmin, double etmax, double etamin, double etamax, double mumin, double mumax, bool usetilecal);
      ~Norm1(){;};
      void execute( std::vector<float> &rings ) const;
  
    private:
      bool m_useTileCal;
  };

}

#endif /* TrigRingerPreproc */

