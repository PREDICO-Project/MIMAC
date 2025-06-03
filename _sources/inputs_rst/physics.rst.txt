Physics
=======

Overview
--------

This file (**Physics.in**) is used to modify physics list and the Cut-off of the particles. It is also used to generate the particles and initialize the simulation.

Step-by-Step Instructions
-------------------------
Users can modified some parameters of the voxelized phantom generation.

- **/gamos/physicsList**: This command is used to modify the physics list.
- **/run/setCut**: Users can modify the cut-off (in mm) of the particles using this command.

Example:
--------

.. code-block:: python
    :linenos:
    
    ################
    # PHYSIC SETUP #
    ################

    #Physics EMstandard
    /gamos/physicsList GmEMPhysics

    #Set CUT-OFF. Range
    /run/setCut 1.0

    #Generator
    /gamos/generator GmGenerator

    #INITIALISE GEANT4
    /run/initialize

