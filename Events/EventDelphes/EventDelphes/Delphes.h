//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Nov 21 21:54:34 2018 by ROOT version 6.14/00
// from TTree Delphes/Analysis tree
// found on file: delphes_output.root
//////////////////////////////////////////////////////////

#ifndef Delphes_h
#define Delphes_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "TClonesArray.h"
#include "TObject.h"

namespace edm{

class Delphes {
public :
   //UInt_t          Tower_fUniqueID[kMaxTower];   //[Tower_]
   //#UInt_t          Tower_fBits[kMaxTower];   //[Tower_]
   //Float_t         Tower_ET[kMaxTower];   //[Tower_]
   //Float_t         Tower_Eta[kMaxTower];   //[Tower_]
   //Float_t         Tower_Phi[kMaxTower];   //[Tower_]
   //Float_t         Tower_E[kMaxTower];   //[Tower_]
   //Float_t         Tower_T[kMaxTower];   //[Tower_]
   //Int_t           Tower_NTimeHits[kMaxTower];   //[Tower_]
   Float_t         *Tower_Eem;   //[Tower_]
   //Float_t         Tower_Ehad[kMaxTower];   //[Tower_] 
   Float_t         **Tower_Edges;   //[Tower_]
   //TRefArray       Tower_Particles[kMaxTower];
   Int_t           Tower_size;

};


}
#endif // #ifdef Delphes_cxx

