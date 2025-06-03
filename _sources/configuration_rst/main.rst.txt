Main Parameters
===============

The next section is for main parameters of the simulation.

.. code-block:: python
    :linenos:

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%              MAIN parameters                 %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # SET CUT-OFF. PARTICLE MINIMUM RANGE AT ANY MATERIAL
    :P Cut 1.0
    # REPLACE SOME PHYSICAL MODELS
    :P ReplacePhysic False
    # ANALYSIS AND HISTOGRAMS
    :P Ana&Hist False
    # GENERATOR OF PRIMARIES
    :P Source True
    # VRML VISUALIZATION FILE
    :P Vis False
    # RUN N EVENTS
    :P NEvents 2000000000


* **Cut**: The Cut-off is defined for all particles and has units of mm.
* **ReplacePhysic**: Defined to modify the standar physics model used by GAMOS, if it is selected as No, the file Physics.in won't run.
* **Ana&Hist**: If Yes runs the Output.infile on the simulation.
* **Source**: If Yes runs the Source.in file on the simulation (it should be Yes always).
* **Vis**: If Yes runs the visVRML2FILE.in file on the simulation. It creates a vrml file. If you are running the simulation with a voxelized phantom the file size can be dozens of GB.
* **NEvents**: Number of events on the simulation. On GAMOS, scientific notation is not interpreted.
