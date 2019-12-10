//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
// $Id: RunData.hh 69223 2013-04-23 12:36:10Z gcosmo $
// 
/// \file RunData.hh
/// \brief Definition of the RunData class

#ifndef RunData_h
#define RunData_h 1

#include "G4Run.hh"
#include "globals.hh"
#include <vector>


enum {
  kAbs = 0,
  kGap = 1,
  kDim = 2, 
  kNumCells = 504 + 3 // 3 overflow bins for the three calo layers
};  

struct point{
  G4double x;
  G4double y;
  G4double z;
  G4double energy;
};

class RunData : public G4Run
{
public:
  RunData();
  virtual ~RunData();

  void AddPoint( G4double x, G4double y, G4double z, G4double de );
  void AddCell(G4int id, G4double de);
  void FillPerEvent();
  void Reset();

  G4double  GetEdep(G4int id) const;
  G4double GetTotalEnergy(){return TotalEnergy;};
  void SetTotalEnergy(G4double e){TotalEnergy = e;};

private:
  
  G4double  m_cell_energy[kNumCells];
  G4double TotalEnergy;
  std::vector<point> m_points;
  std::vector<G4double> m_point_x;
  std::vector<G4double> m_point_y;
  std::vector<G4double> m_point_z;
  std::vector<G4double> m_point_energy;
};



inline void RunData::AddPoint( G4double x, G4double y, G4double z, G4double de ){
  point p = {x,y,z,de};
  m_points.push_back( p );
}

inline void RunData::AddCell(G4int id, G4double de) {
  m_cell_energy[id] += de; 
}

inline G4double  RunData::GetEdep(G4int id) const {
  return m_cell_energy[id];
}   


#endif

