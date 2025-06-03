Filters Parameters
==================

.. code-block:: python
    :linenos:

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%           FILTERS PARAMETERS                 %%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    :P Filters True
    # Apply Filter1, Kill all electrons
    :P ApplyF1 True
    # Apply Filter2, Kill secondary tracks
    :P ApplyF2 False
    # Apply Filter3, Kill scattered photons
    :P ApplyF3 False
    # Apply Filter4, Kill photons at the jaws
    :P ApplyF4 False
    # Apply Filter5, Kill photons at detectorEND
    :P ApplyF5 False


* **ApplyF1**: If Yes Kill all electrons when they are generated (**highly recommended**).
* **ApplyF2**: If Yes Kill all secondary tracks.
* **ApplyF3**: If Yes Kill all scatered photons.
* **ApplyF4**: If Yes Kill all non-scattered photons (**not recommended**).
* **ApplyF5**: If Yes Kill all photons that goes through the jaws (**recommended** if Jaws are defined).
* **ApplyF6**: If Yes Kill all photons at the end of the detector.

.. note:: The Filter 2 and 3 are recommended if you want a faster simulation. However, using this Filters and the anti scatter grid could be redundant.