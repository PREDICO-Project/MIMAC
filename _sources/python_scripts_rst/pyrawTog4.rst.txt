pyrawTog4
=========


The ``pyrawTog4.py`` scripts contains the ``DCM2G4`` class with the methods used to generate the .g4dcm format file interpreted by Geant4 to read the voxelized phantom.

There are some important notes to use correctly this script.

- The mhd/raw files with the voxelized phantoms must be in ``data/original_mhd/`` folder. 

- Must be a ``materials.txt`` file with the Voxel Value - Density (g/cm²) - material - ID inside ``data/materials/`` folder.

- The mhd/raw filename must be specified in the ``DCM2G4._filein_name`` attribute, the output filename will be the same as the input filename. 

- The attribute ``DCM2G4.remove_chest_wall`` if True, removes the chest wall.

- The attribute ``DCM2G4.in_or_out`` if 0 includes the compression paddle, if 1 the compression paddle is not included.

- The attribute ``DCM2G4.cut_only_air`` if True removes slices that contains just air (recommended).

- The attribute ``DCM2G4.free_cut`` if True, cuts the slices as you desire with the attributes ``DCM2G4.slice_ini``, ``DCM2G4.slice_end``, ``DCM2G4.colum_ini``, ``DCM2G4.colum_end``, ``DCM2G4.row_ini`` and ``DCM2G4.row_end``.

- The attribute ``DCM2G4.dcm`` if True, a DICOM set of images inside ``data/dcm/`` folder will be generated. It is useful to check if the applied cuts have been perform as desired.

- The attribute ``DCM2G4.raw`` if True, a raw/mhd images inside ``data/new_mhd/`` folder will be generated. It is useful to check if the applied cuts have been perform as desired. This file will be used in SimRun.py to calculate the number of pixels of the detector and the displacement of the phantom to be aligned with the source.

- The method ``DCM2G4.create_phantom_file()`` will run all the methods to generate the .g4dcm file.

.. literalinclude:: ../../pysrc/pyrawTog4.py