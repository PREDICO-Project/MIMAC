Source Parameters
=================

.. code-block:: python
    :linenos:
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%           SOURCE PARAMETERS                  %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    :P Particle gamma
    :P Energy 0.85
    :P PosDistribution Gaussian_disc
    :P FocusSize 0.3
    :P Spectra RQAM2.txt
    :P Distribution Pyramid
    :P AlignSource True
    # If "AlignSource" is Yes next parameters will be ignored
    :P SourcePosX 0.0
    :P SourcePosY 0.0
    :P AutoSizeSource True
    # If "AutoSize Source" is Yes next parameters will be ignored whichever source distribution chosen
    :P ConeAngle 5.77
    :P PyramidX 150.0
    :P PyramidY 150.0


* **Particle**: Primary Particles generated (always gamma).
* **Energy**: The energy to initialize the gamma particles, in case of using a Spectra it will be replaced.
* **PosDistribution**: Position distribution of the source, can be Gaussian_disc or Single_point.
* **FocusSize**: The size of the Focus in mm (only if Gaussian_disc as position distribution).
* **Spectra**: In case of using a Spectra, write the name of the text file used. The file must be located on the spectra folder.
* **Distribution**: Direction Distribution of the particles. Can be Pyramid, Pyramid_Isotropic, SemiCone or Cone.
* **AlignSource**: If Yes, the source is aligned with the phantom. It will be located above the chest.
* **SourcePosX**: Source Position on X-direction (ignored if AlignSource is True).
* **SourcePosY**: Source Position on Y-direction (ignored if AlignSource is True).
* **AutoSizeConeAngle**: If Yes, the source angle will be calculated to maximize the number of photons that will be contributing to the image formation.
* **ConeAngle**: If AutoSizeConeAngle is No, the Angle must be written (in degrees).
* **PyramidX**: Size on X-direction of the Pyramid distribution in mm (ignored if AutoSizeSource is True).
* **PyramidY**: Size on Y-direction of the Pyramid distribution in mm (ignored if AutoSizeSource is True).