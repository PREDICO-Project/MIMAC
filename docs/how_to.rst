How to run
==========

First `install GAMOS <http://fismed.ciemat.es/GAMOS/gamos_download.php>`_ , then you have to type in the terminal:

.. code-block:: python
    :linenos:

    cd path_to_gamos/GAMOS.ver/
    source config/confgamos.sh

Or alternatively (see `Primer Tutorial <http://fismed.ciemat.es/GAMOS/download/GAMOS.6.2.0/uncompiled/GAMOS.6.2.0/tutorials/Primer/GAMOS.Primer.ppt>`_)

.. code-block:: python
    :linenos:

    cd
    source path_to_gamos/GAMOS.ver/config/confgamos.sh
    
Next, modify the :doc:`Configuration File <configuration_rst/index>` with the parameters you want. Then you should run the :doc:`SimRun.py <python_scripts_rst/simrun>` python script which writes all the Gamos files needed to run the simulation with the parameters written in the :doc:`Configuration File <configuration_rst/index>`. 

From the main path of the project you should type in the terminal:

.. code-block:: python
    :linenos:

    python3 pysrc/SimRun.py

We have prepared a simple bash script , :doc:`sendrun.sh <bash_script>`,  to run several runs at the same time (based on `GAMOS/tutorials/RTTutorials/exercise2 <https://github.com/arceciemat/GAMOS/blob/master/tutorials/RTTutorial/exercise2/sendjobs>`_ credits to Pedro Arce). It only accepts 2 paramters, the number of runs and the initial SEED. 

From the main path of the project you should type in the terminal:

.. code-block:: python
    :linenos:

    bash sendrun.sh 10 11111


.. warning:: The runs are independent, they do not share the geometry, each run builds the geometry. If you don´t have too much RAM memory there could be a memory leak.

If you just want to run one job just type in the terminal:

.. code-block:: python
    :linenos:

    gamos main.in
