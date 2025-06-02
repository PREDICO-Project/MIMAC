Anti-scatter Grid Parameters 
============================

.. code-block:: python
    :linenos:

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%       ANTI-SCATTER GRID PARAMETERS           %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    :P UseAntiScatterGrid True
    :P GridRatio 5.0
    :P GridFrequency 3.1
    :P GridStripThickness 0.065

An anti-scatter grid can be simulated following the guidelines of Day&Dance(1983) :doc:`[3] <../references>`.


* **UseAntiScatterGrid**: If True, an anti-scatter grid defined as Day&Dance(1983) :doc:`[3] <../references>` will be considered.
* **GridRatio**: 
* **GridFrequency**: 
* **GridStripThickness**: Thickness of the Strips in mm.

.. note:: The attenuation coefficients of the Stip Material and the Inter-Strip Material can be modified at ```plug-ins/resources```.
