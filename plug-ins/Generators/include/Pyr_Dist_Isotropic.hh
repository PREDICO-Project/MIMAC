#ifndef Pyr_Dist_Isotropic_HH
#define Pyr_Dist_Isotropic_HH

#include "GamosCore/GamosGenerator/include/GmVGenerDistDirection.hh"
#include "G4ThreeVector.hh"
class GmParticleSource;

class Pyr_Dist_Isotropic : public GmVGenerDistDirection
{
public:
  Pyr_Dist_Isotropic();
  virtual ~Pyr_Dist_Isotropic(){};

  virtual G4ThreeVector GenerateDirection( GmParticleSource* source );

  virtual void SetParams( const std::vector<G4String>& params );
  void SetDirection( G4ThreeVector dir );

private:
  G4ThreeVector theInitialDir;
  G4ThreeVector dirPP;
  G4double theOpeningAngle;
  G4double max_costheta;
  G4double theSDD;
  G4double theWidthX;
  G4double theWidthY;
  G4double theDetecX;
  G4double theDetecY;

};

#endif
