#include "SemiCone_Dist.hh"
#include "Pyr_Dist_Isotropic.hh"

#ifdef ROOT5
#include "Reflex/PluginService.h"

PLUGINSVC_FACTORY(GmGenerDistDirectionCone,GmVGenerDistDirection*())

#include "GmGenerVerbosity.hh"
PLUGINSVC_FACTORY(GmGenerVerbosity,GmVVerbosity*())

#else 

//#include "GmGeneratorFactory.hh"
#include "GamosCore/GamosGenerator/include/GmGeneratorDistributionFactories.hh"
#include "SEAL_Foundation/PluginManager/PluginManager/ModuleDef.h"

DEFINE_SEAL_MODULE ();
DEFINE_GAMOS_GENER_DIST_DIRECTION(SemiCone_Dist);
DEFINE_GAMOS_GENER_DIST_DIRECTION(Pyr_Dist_Isotropic);

//#include "GamosCore/GamosBase/Base/include/GmVerbosityFactory.hh"
//#include "GmGenerVerbosity.hh"

//DEFINE_SEAL_PLUGIN(GmVerbosityFactory, GmGenerVerbosity, "GmGenerVerbosity");

#endif
