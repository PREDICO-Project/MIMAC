Source
======

Overview
--------

This file (**Source.in**) is used to define all parameters related to the radiation source. This file must be executed always and the type of particle, its energy, spatial and angular
distribution would be defined. 

Step-by-Step Instructions
-------------------------
Users can modified some parameters of the source.

- **/gamos/generator/addSingleParticleSource**: This command initializes the particle source used in the simulation. The name, the type of particle and its energy is defined. The energy is an initialization energy, it is not their final energy if a spectra is used.

- **/gamos/generator/energyDist**: The energy distribution (spectra) is defined with this command. If you are not going to use a spectra, delete or comment this command.
- **/gamos/generator/positionDist**: This command is used to define the position distribution of the source.
- **/gamos/generator/directionDist**: This command defines the direction distribution of the particles generated in the source.

There are three exclusive direction distribution developed as an extension of GAMOS through plugins.

* **Semi Conical distribution**. The distribution follows a semi-conical distribution aligned with the detector edge in the X-direction. To call it:

.. code-block:: python
    :linenos:

    /gamos/generator/directionDist NAME SemiCone_Dist DIR_X DIR_Y DIR_Z OPENING_ANGLE SDD WIDTH_X WIDTH_Y

* **Pyramidal Isotropic distribution**. The distribution is Isotropic but the generation of the photons are constrained to pass through a rectangular plane defined by WIDTH_X and WIDTH_Y (in mm). To call it:

.. code-block:: python
    :linenos:

    /gamos/generator/directionDist NAME Pyr_Dist_Isotropic DIR_X DIR_Y DIR_Z SDD WIDTH_X WIDTH_Y DETC_X DETC_Y

Example:
--------

.. code-block:: python
    :linenos:

    ########################
    ##    SOURCE Setup    ##
    ########################

    #Initialization
    /gamos/generator/addSingleParticleSource source gamma 0.85*MeV

    #Spectra
    /gamos/generator/energyDist source GmGenerDistEnergyFromFile spectra/28Mo-Rh0.05-Be1.in interpolate

    #Position Distribution
    /gamos/generator/positionDist source GmGenerDistPositionDiscGaussian 0.3 -75.0125 0. 0. 0. 0. -1.

    #Distribution Shape
    /gamos/generator/directionDist source Pyr_Dist_Isotropic 0. 0. 1. 650.0 150.025 150.025 0. 0.



