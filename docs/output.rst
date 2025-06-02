Output
======

Overview
--------

- The output of the simulation consist on one or more files where the value at each [row, column] represents the energy (or charge) deposited (generated) inside the pixel with coordinates [row,column]. 
- Output files will be created on the folder defined in the **ResultsFolder** parameter of **GetImage.in**, :doc:`GmGetEnergy <plugins_rst/getenergy>` plugin will be used.
- Running the bash script will generate as many output files as the number of NRUNS specified.
- The format of the output file can be DICOM, MHD/RAW or Text.
- Output files need to be processed to add electronic noise and convert the units of the pixel into gray scale (through a Sensitivity Curve). It can be done using the GUI.