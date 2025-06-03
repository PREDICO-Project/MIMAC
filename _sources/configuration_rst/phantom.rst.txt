Phantom Parameters
==================

.. code-block:: python
    :linenos:


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%            PHANTOMS USED (NO-DICOM)          %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    :P DICOMGeom False
    :P SOD 650.0
    :P Phantom AAPM.geom
    :P VoxelPhantom None


* **DICOMGeom**: If True a voxelized phantom will be used. They must be created before running the simulation and stored in ```data/g4dcm```.
* **SOD**: Source-Object Distance in mm.
* **Phantom**: Non-voxelized phantom name. None if not going to use it.
* **VoxelPhantom**: Voxelized phantom name. None if not going to use it.
