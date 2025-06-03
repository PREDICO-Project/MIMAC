Energy to DCM
=============

The output of the simulation is a text file with the energy deposited in each pixel. This function convert the text file into an
image in DICOM or tiff formats. The processes to generate the image are:

- First, the .out files (text files) from the path that serves as input of the ``SimulationProcessor.generate_image(energy_file_path)`` method are uploaded and are added.

- Second, the final array with the total energy deposited in each pixel is converted into electric charge. 

- Third ...

.. literalinclude:: ../../pysrc/energyTodcm.py