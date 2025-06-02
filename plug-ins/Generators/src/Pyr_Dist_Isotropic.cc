#define _USE_MATH_DEFINES
#include <cmath>
#include "Pyr_Dist_Isotropic.hh"
//#include "GmGenerVerbosity.hh"
#include "GamosCore/GamosGenerator/include/GmParticleSource.hh"
#include "GamosCore/GamosUtils/include/GmGenUtils.hh"
#include "CLHEP/Random/RandFlat.h"
#include "CLHEP/Units/SystemOfUnits.h"

//---------------------------------------------------------------------
Pyr_Dist_Isotropic::Pyr_Dist_Isotropic()
{
}

//---------------------------------------------------------------------
G4ThreeVector Pyr_Dist_Isotropic::GenerateDirection(GmParticleSource* source)
{
    G4ThreeVector sourcePosition = source->GetPosition();
    
    //G4cout << max_costheta << G4endl;
    //const int maxAttempts = 10; // Número máximo de intentos
    //int attempts = 0;

    while (true) {
        //---- Get theta angle around theInitialDir
        
        double costheta = CLHEP::RandFlat::shoot() * (1-max_costheta) + max_costheta;
        double sintheta = sqrt(1.-costheta*costheta);
		//G4cout << costheta << G4endl;
        //G4ThreeVector newDir = theInitialDir; 
        //newDir.rotate(theta, thePerpDir);

        //---- Get phi angle around newDir
        //G4double phi = CLHEP::RandFlat::shoot() * M_PI - 0.5 * M_PI;
        G4double phi = CLHEP::RandFlat::shoot() * 2* M_PI - M_PI;
        //newDir.rotate(phi, theInitialDir);

        // Normalizar la dirección
        G4ThreeVector newDir = G4ThreeVector( sintheta*cos(phi), sintheta*sin(phi), costheta );
        newDir = newDir.unit();

        // Proyectar newDir desde la posición de la fuente hasta la posición del plano del detector
        G4double t = (theSDD - sourcePosition.z()) / newDir.z();
        G4double x_intersect = sourcePosition.x() + t * newDir.x();
        G4double y_intersect = sourcePosition.y() + t * newDir.y();
        
        

        // Print de las intersecciones
        //G4cout << "x_intersection: " << x_intersect << G4endl;
        //G4cout << "y_intersection: " << y_intersect << G4endl;

        // Verificar si la intersección cae dentro de los límites del detector
        if (x_intersect >= (theDetecX - theWidthX / 2) && x_intersect <= (theDetecX + theWidthX / 2) &&
            y_intersect >= (theDetecY - theWidthY / 2) && y_intersect <= (theDetecY + theWidthY / 2)) {
            return newDir;
        }

        //attempts++;
    }

    // Si no se encontró una dirección válida, lanzar una excepción o retornar un valor por defecto
    //G4Exception("Pyr_Dist_Isotropic::GenerateDirection",
               // "No valid direction found",
                //FatalException,
               // "Could not find a direction that intersects the detector after maximum attempts.");
    //return G4ThreeVector(); // Retornar un vector nulo o manejar el error como prefieras
}

//---------------------------------------------------------------------
void Pyr_Dist_Isotropic::SetParams(const std::vector<G4String>& params)
{
    if (params.size() != 8) {
        G4Exception("Pyr_Dist_Isotropic_sin_centered::SetParam",
                    "Wrong argument",
                    FatalErrorInArgument,
                    "To set direction you have to add 8 parameters: DIR_X DIR_Y DIR_Z SDD WIDTH_X WIDTH_Y DETC_X DETC_Y");
    }

    theInitialDir = G4ThreeVector(GmGenUtils::GetValue(params[0]), GmGenUtils::GetValue(params[1]), GmGenUtils::GetValue(params[2]));

    //----- Get the Source-Detector Distance (mm)
    theSDD = GmGenUtils::GetValue(params[3]);

    //----- Get the Width and X coordinate of the Detector on X (mm)
    theWidthX = GmGenUtils::GetValue(params[4]);
    theDetecX = GmGenUtils::GetValue(params[6]);

    //----- Get the Width and Y coordinate of the Detector on Y (mm)
    theWidthY = GmGenUtils::GetValue(params[5]);
    theDetecY = GmGenUtils::GetValue(params[7]);

    //----- Get the opening angle (Calculate from detector dimensions)
    G4double auxY = (theWidthY) * (theWidthY);
    G4double auxX = (theWidthX) * ( theWidthX);
   
    G4double r = sqrt(auxX+auxY);
    theOpeningAngle = atan(r / theSDD); // radianes
    max_costheta = cos(theOpeningAngle);

    //----- Get one perpendicular direction
    G4ThreeVector dir(1., 0., 0.);
    if (fabs(fabs(theInitialDir * dir) - 1.) < 1.E-9) {
        dir = G4ThreeVector(0., 1., 0.);
    }
    G4ThreeVector thePerpDir = theInitialDir.cross(dir);
}

//---------------------------------------------------------------------
void Pyr_Dist_Isotropic::SetDirection(G4ThreeVector dirIni)
{
    theInitialDir = dirIni;
    G4ThreeVector dirPP(1., 0., 0.);
    if (fabs(fabs(theInitialDir * dirPP) - 1.) < 1.E-9) {
        dirPP = G4ThreeVector(0., 1., 0.);
    }
    G4ThreeVector thePerpDir = theInitialDir.cross(dirPP);
}
