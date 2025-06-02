Detector Parameters 
===================

.. code-block:: python
    :linenos:
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%           DETECTOR PARAMETERS                %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    :P Realistic True
    :P SDD 635.0
    :P DetectorDepth 0.2
    :P NPixelX 1647
    :P NPixelY 3059
    :P PixelSizeX 0.085
    :P PixelSizeY 0.085
    :P Material aSe

* **Realistic**: If Realistic detector is selected, a physical detector is built and the interactions inside it will be considered. If it is False, then a virtual detector will be built, the output will be a matrix with the incident energy of the particles through each pixel weighted by an efficiency factor.
* **SDD**: Source-Detector Distance (mm)
* **DetectorDepth**: Detector Depth (mm)
* **NPixelX**: Number of Pixels of the detector in X direction
* **NPixelY**: Number of Pixels of the detector in Y direction
* **PixelSizeX**: Detector's Pixel Size in X direction (mm)
* **PixelSizeY**: Detector's Pixel Size in X direction (mm)
* **Material**: Detector's Material