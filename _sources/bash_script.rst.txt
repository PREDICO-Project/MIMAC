Bash script
===========


There is a .sh script to perform several runs at the same time with the same simulation configuration. It is based on a script developed by Pedro Arce (author of GAMOS) :doc:`[1] <references>` but with modifications based on our simulation.

Ther are some important notes about this script.

- The variable ``NCORES`` must be changed based on your computer. It is the number of cores used on the simulation, if your computer have 30 cores, NCORES must not be 30 or more.

- The path where the .out files will be saved must be rewritten on each run usign the variable ``OUTPUT_PATH``. 

- Once the script has been modified, you can run it as follows:

.. code-block:: console
    :linenos:

    bash sendrun.sh NRUNS SEED

Where ``NRUNS`` is the number of runs we want to perform and ``SEED`` will be the initial seed of the main_0 generated file.

.. note:: Important!!! Modify the output path and make sure the folder exists.

.. literalinclude:: ../sendrun.sh