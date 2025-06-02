#ifndef SemiCone_Dist_HH
#define SemiCone_Dist_HH

#include "GamosCore/GamosGenerator/include/GmVGenerDistDirection.hh"
#include "G4ThreeVector.hh"
class GmParticleSource;

class SemiCone_Dist : public GmVGenerDistDirection
{
public:
  SemiCone_Dist();
  virtual ~SemiCone_Dist(){};

  virtual G4ThreeVector GenerateDirection( GmParticleSource* source );

  virtual void SetParams( const std::vector<G4String>& params );
  void SetDirection( G4ThreeVector dir );

private:
  G4ThreeVector theInitialDir;
  G4double theOpeningAngle;
  G4ThreeVector thePerpDir;
  G4double theSDD;
  G4double theWidthX;
  G4double theWidthY;


};

#endif
