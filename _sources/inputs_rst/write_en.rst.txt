Get Image 
=========

Overview
--------
This input file (**GetImage.in**) is used to run and define the parameters of the plugin :doc:`GmGetImage.cc <../plugins_rst/getenergy>`. The parameters defined in this input file are related with the image formation and detector characteristics. 

Step-by-Step Instructions
-------------------------
Users can modify a lot of parameters in order to obtain the desired output from the simulation.

1. Detector Parameters.
^^^^^^^^^^^^^^^^^^^^^^^

- **GetImage:NumPixels(X/Y)**: Command to set the number of pixels in each direction.
- **GetImage:PixelSizeX**: Command to set the pixel size in each direction (in mm).
- **GetImage:zStop**: Is the distance from the the origin to the detector (in mm).
- **GetImage:DetectorModel**: Users can select between MCD or VD detector models.

    - **MCD (Monte Carlo Detector)**: It uses a Geant4-solid box as a detector. All interactions inside the detector are simulated through the cross sections used by Geant4. The final output is a file with the energy deposited in each pixel by the hits.
    - **VD (Virtual Detector)**: It uses a virtual plane as a detector. The interactions are simulated through an efficiency curve located in **plug-ins/resources/**. The output is the energy deposited in each pixel.
- **GetImage:OutputType**: Users can select between two different outputs, **Energy** or **Charge**. We recommend to select the Energy output and modify the output using the **image formation** GUI's module.
- **GetImage:ResultsFolder**: The folder where the output is saved.
- **GetImage:OutputFilename**: The filename of the output.
- **GetImage:OutputFormat**: The format of the output. The format can be DICOM, MHD/RAW or Text.

2.Anti-scatter grid.
^^^^^^^^^^^^^^^^^^^^
The anti-scatter grid is a focussed grid modeled following the steps of Day and Dance :doc:`[3] <../references>` and tha name of the parameters correspond with the names given in the reference. 

- **Grid:UseGrid**: If Yes, an anti-scatter grid will be used in the simulation. If No, it won't.
- **Grid:Ratio**: It is the ratio between the height of the stips and the thickness of the interspace region.
- **Grid:SourceDetectorDistance**: Distance (in mm) Source-Detector.
- **Grid:Frequency**: The frequency iof the strip bars (in 1/mm).
- **Grid:StripThickness**: Thicknes (in mm) of the lead's strip.
- **Grid:Gap**: It is the position of the source in the X-direction. 

Example:
--------

.. code-block:: python
    :linenos:

    ########################
    # DETECTOR MODEL SETUP #
    ########################

    # Virtual detector segmentation
    #/gamos/setParam SD:VirtSegmBox:NDiv:Absorber 1765.0 1765.0 1.
    #/gamos/setParam SD:VirtSegmBox:Width:Absorber 150.025 150.025 0.2
    #/gamos/SD/assocSD2LogVol GmSDVirtSegmBox Absorber detector
    #/gamos/SD/recHitBuilder GmRecHitBuilderBydose Absorber

    /gamos/setParam GetImage:NumPixelsX 1765.0
    /gamos/setParam GetImage:NumPixelsY 1765.0
    /gamos/setParam GetImage:PixelSizeX 0.085
    /gamos/setParam GetImage:PixelSizeY 0.085
    /gamos/setParam GetImage:zStop 648.9
    #/gamos/setParam GetImage:PairCreationEnergy 50.0

    ################
    # OUTPUT SETUP #
    ################

    /gamos/setParam GetImage:DetectorModel VD
    /gamos/setParam GetImage:OutputType Charge
    /gamos/setParam GetImage:ResultsFolder output/
    /gamos/setParam GetImage:OutputFilename test
    /gamos/setParam GetImage:OutputFormat MHD/RAW

    #####################
    # ANTI-SCATTER GRID #
    #####################

    /gamos/setParam Grid:UseGrid Yes
    /gamos/setParam Grid:Ratio 5.0
    /gamos/setParam Grid:SourceDetectorDistance 648.9
    /gamos/setParam Grid:Frequency 3.1
    /gamos/setParam Grid:StripThickness 0.065
    /gamos/setParam Grid:Gap -75.0125

    ####################
    # USER ACTION CALL #
    ####################

    /gamos/userAction GmGetImage