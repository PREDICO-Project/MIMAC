#############################
##     Ion Chamber Setup   ##
#############################


# Rotation Matrix
:ROTM RMIOC 0. 0. 0.

# Ion Chamber Dimensions
:P IOCx 20.0
:P IOCy 20.0
:P IOCz 5.0

# Ion Chamber Position
:P IOCSD 750.0
:P IOCCW -0.012500000000002842
:P IOCLR 0.0

###########################
##     Vol Definition    ##
###########################

# Ion Chamber VOLUME
:VOLU ionchamber BOX 0.5*$IOCx 0.5*$IOCy 0.5*$IOCz G4_AIR
:PLACE ionchamber 1 world RMIOC $IOCCW $IOCLR $IOCSD
:COLOUR ionchamber 0.5 0. 0.5
