Geometry
========

Overview
--------
- The geometry is defined in **geom/** folder. In this folder there two main folders and an importan text file. 

- The **worlds/** folder contains **.geom** files that defines the world where the simulation is performed. 
- The folder **elementsInWorld/** contains **.geom** files defining Geant4's solids which can be positioned in the world.
- The file **MyMaterials.txt** defines the materials that can be used in the simulation.

.. warning::
    Make sure to define your materials in **MyMaterials.txt** or check if it exists by default as a Geant4 material.

.. figure:: images/setup.jpeg
    :align: center
    
    Setup of the simulation.