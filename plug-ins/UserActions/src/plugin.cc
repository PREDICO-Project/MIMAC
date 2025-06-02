#include "GmGetImage.hh"

#ifdef ROOT5
#include "Reflex/PluginService.h"

PLUGINSVC_FACTORY(GmGetImage,GmUserAction*())

#else 

#include "PluginManager/ModuleDef.h"
#include "GamosCore/GamosUserActionMgr/include/GmUserActionFactory.hh"
#include "GamosCore/GamosBase/Base/include/GmFilterFactory.hh"

DEFINE_SEAL_MODULE ();

DEFINE_GAMOS_USER_ACTION(GmGetImage);

#endif
