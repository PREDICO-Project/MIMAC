GmGetImage
===========

This plugin is used to store the energy (or charge) deposited for each photon into the pixel where it interacts. 

For now, there are two different detector models:
1. a-Se detector with a virtual detector (VD) and anti-scatter grid.
2. a-Se detector with a virtual detector (VD) and no anti-scatter grid.
3. Realistic detector (MCD) and no anti-scatter grid.
4. Realistic detector (MCD) and anti-scatter grid.

MCD detector must be defined as a geometry in the simulation. The geometry must be defined in the macro file. The geometry is defined as a box with a certain size and a certain number of pixels. The number of pixels is defined by the user. The size of the box is defined by the user. The size of the box is defined by the user. The size of the box is defined by the user. The size of the box is defined by the user.

The detector is located at zStop (the distance from the source plane to the detector). The size of the box is defined by the user through the following commands:

.. code-block:: python
    :linenos:

    /gamos/setParam GetImage:NumPixelsX NumPixelsX
    /gamos/setParam GetImage:NumPixelsY NumPixelsY
    /gamos/setParam GetImage:PixelSizeX PixelSizeX(mm)
    /gamos/setParam GetImage:PixelSizeY PixelSizeY(mm)
    /gamos/setParam GetImage:zStop zStop(mm)


- Evaluate at each step of the particle if has reached the "virtual" detector (VD) or the real detector (MCD).

- When the particle go through the detector we apply a function that simulates an anti-scatter grid. 

- The anti-scatter grid is defined as :doc:`[3] <../references>`. 
- If the photon is absorbed in the anti-scatter grid, it is not counted.
- If the photon is absorbed in the detector and the VD model is selected, the absorption is evaluated using the efficiency curve defined for the virtual detector. The efficiency curve determines the probability of photon absorption based on its energy.
- If the output selected is **Energy**, a image with the energy in eV is created.
- If the output selected is **Charge**, a image with the charge in pairs e-hole is created.
- Finally, a file is written with the total deposited energy on the run in each pixel.
- By default, the format of the file is MHD/RAW, but it can be changed using the command:

.. code-block:: python
    :linenos:
    
    /gamos/setParam GetImage:OutputFormat DCM
    /gamos/setParam GetImage:OutputFormat Text
    /gamos/setParam GetImage:OutputFormat MHD/RAW


Source Code:

.. literalinclude:: ../../plug-ins/UserActions/src/GmGetImage.cc


Header File:

.. literalinclude:: ../../plug-ins/UserActions/include/GmGetImage.hh