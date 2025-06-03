########################
##   SPHERE phantom   ##
########################

#Params definition
#:P SpherePosition 1800.
:P SphereRadius 5
:P BoxSide 20.
:ROTM RM1 0. 0. 0.

########################
##   VOL definition   ##
########################

#Solid water sphere filled with a teflon box
#:VOLU test ORB $SphereRadius G4_Ca
:VOLU test ORB $SphereRadius "AAPM_PMMA"
:PLACE test 1 world RM1 0. 0. $SOD


