#define _USE_MATH_DEFINES
#include <cmath>
#include "SemiCone_Dist.hh"
#include "GamosCore/GamosGenerator/include/GmParticleSource.hh"
#include "GamosCore/GamosUtils/include/GmGenUtils.hh"
#include "CLHEP/Random/RandFlat.h"
#include "CLHEP/Units/SystemOfUnits.h"

//---------------------------------------------------------------------
SemiCone_Dist::SemiCone_Dist()
{
}

//---------------------------------------------------------------------
G4ThreeVector SemiCone_Dist::GenerateDirection( GmParticleSource* )
{


	//---- Get theta angle around theInitialDir
	G4double theta = (sqrt(CLHEP::RandFlat::shoot())*theOpeningAngle);

	G4ThreeVector newDir = theInitialDir; 
	newDir.rotate( theta, thePerpDir );

	//---- Get phi angle around newDir
	G4double phi = CLHEP::RandFlat::shoot()*M_PI-0.5*M_PI;
	newDir.rotate( phi , theInitialDir );

  	return newDir;

}

//---------------------------------------------------------------------
void SemiCone_Dist::SetParams( const std::vector<G4String>& params )
{
  if( params.size() != 7 ) {
    G4Exception(" SemiCone_Dist::SetParam",
		"Wrong argument",
		FatalErrorInArgument,
		"To set direction you have to add 7 parameters: DIR_X DIR_Y DIR_Z OPENING_ANGLE SDD WIDTH_X WIDTH_Y");  
  }

  theInitialDir = G4ThreeVector(GmGenUtils::GetValue( params[0] ), GmGenUtils::GetValue( params[1] ), GmGenUtils::GetValue( params[2] ) );

  theOpeningAngle = GmGenUtils::GetValue(params[3]);
  
  //----- Get the Source-Detector Distance (mm)
  theSDD = GmGenUtils::GetValue(params[4]);
  
  //----- Get the Width of the Detector on X (mm)
  theWidthX = GmGenUtils::GetValue(params[5]);
  
  //----- Get the Width of the Detector on Y (mm)
  theWidthY = GmGenUtils::GetValue(params[6]);

  //----- Get one perpendicular direction
  G4ThreeVector dir(1.,0.,0.);
  if( fabs(fabs(theInitialDir*dir) - 1.) < 1.E-9 ){
    dir = G4ThreeVector(0.,1.,0.);
  }
  thePerpDir = theInitialDir.cross(dir);

}

//---------------------------------------------------------------------
void SemiCone_Dist::SetDirection( G4ThreeVector dirIni )
{
  theInitialDir = dirIni;
  G4ThreeVector dirPP(1.,0.,0.);
  if( fabs(fabs(theInitialDir*dirPP) - 1.) < 1.E-9 ){
    dirPP = G4ThreeVector(0.,1.,0.);
  }
  thePerpDir = theInitialDir.cross(dirPP);

}
