Phantom Generation Script
=========================


This script enables to run the VICTRE Pipeline. There is a ``Generator`` class with the attributes and methods necessary to run the desired parts of the VICTRE Pipeline. It can be used to just generate the phantoms, introduce lesions to pregenerated phantoms and even run the MCGPU simulation to a pregenerated phantom.


.. warning:: The ``phantom_generation.py`` file must be located and run on VICTRE folder.

Code:

.. literalinclude:: ../../phantom_generation.py