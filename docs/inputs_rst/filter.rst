Filters
=======

Overview
--------
This input file (**Filters.in**) set up the GAMOS's filters used in the simulation.

Step-by-Step Instructions
-------------------------
Users can modified some parameters of the voxelized phantom generation.

- **GmElectronFilter (Filter 1)** kills all electrons.
- **GmSecondaryFilter (Filter 2)** kills secondary particles.
- **ScTT (Filter 3)** filter kills all photons that have suffered a Rayleight or Compton interaction.
- **killJaws (Filter 4)** filter kills all photons that reach the jaws, with this filter we assure that the photons will go through the phantom and eventually will be detected at the detector.

.. note::
    If Filter 3 is used, make sure to define the jaws as a Geant4-solid.

Example:
--------

.. code-block:: python
    :linenos:

    #################
    # FILTERS SETUP #
    #################

    # Photons affected by Rayleigh scattering
    /gamos/filter RL GmProcessFilter Rayl
    # Photons affected by Compton scattering
    /gamos/filter Cmp GmProcessFilter compt
    # Scattered photons filter
    /gamos/filter ScTT GmORFilter RL Cmp

    # kill photons at the jaws
    #/gamos/filter KillJawsx1 GmEnterPhysicalVolumeFilter x1jaw
    #/gamos/filter KillJawsx2 GmEnterPhysicalVolumeFilter x2jaw
    #/gamos/filter KillJawsy1 GmEnterPhysicalVolumeFilter y1jaw
    #/gamos/filter KillJawsy2 GmEnterPhysicalVolumeFilter y2jaw
    #/gamos/filter killJaws GmORFilter KillJawsx1 KillJawsx2 KillJawsy1 KillJawsy2

    #################
    # APPLY FILTERS #
    #################

    #Apply Filter1, Kill all electrons
    /gamos/userAction GmKillAtStackingActionUA GmElectronFilter

    #Apply Filter2, Kill secondary tracks
    #/gamos/userAction GmKillAtSteppingActionUA GmSecondaryFilter

    #Apply Filter3, Kill scattered photons
    #/gamos/userAction GmKillAtSteppingActionUA ScTT

    #Apply Filter4, Kill photons at the jaws
    #/gamos/userAction GmKillAtSteppingActionUA killJaws

