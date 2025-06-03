Voxelized Phantom Input File 
============================

Overview
--------
This input file (**VoxelizedPhantom.in**) is used to load a .g4dcm file into the simulation. The g4dcm file contains the information to generate a voxelized phantom.

Step-by-Step Instructions
-------------------------
Users can modified some parameters of the voxelized phantom generation.

- **GmReadPhantomGeometry:Phantom:FileName**: This command is used to select the path to the g4dcm file.
- **GmReadPhantomGeometry:FileName**: This command is used to select the world where the voxelized phantom is placed.
- **GmReadPhantomGeometry:MotherName**: Name of the world.
- **GmReadPhantomGeometry:Phantom:SkipEqualMaterials**: If 1, SkipEqualMaterials algorithm is applied, if 0 it is not. 
- **GmReadPhantomGeometry:InitialDisplacement**: Displacement (in mm) of the phantom. 

Example:
--------

.. code-block:: python
    :linenos:

    #############################
    # VOXELIZED PHANTOM SETUP #
    ###########################

    # File definition for loading a VOXELIZED PHANTOM
    /P GmReadPhantomGeometry:Phantom:FileName data/g4dcm/Phantom-BCT_16006_015_57.76mm.g4dcm
    /P GmReadPhantomGeometry:FileName geom/worlds/world.geom
    /P GmReadPhantomGeometry:MotherName world
    /P GmReadPhantomGeometry:Phantom:SkipEqualMaterials 1
    /P GmReadPhantomGeometry:InitialDisplacement -21.770000000000003 -83.4375 625.9759998321533

    /gamos/geometry GmReadPhantomG4Geometry


