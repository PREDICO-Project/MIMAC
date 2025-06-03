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
    

Once GAMOS is compiled, user should install all python requirements and clone the github repository:

.. code-block:: python
    :linenos:

    pip install -r requirements.txt

    git clone https://github.com/PREDICO-Project/MIMAC.git
    cd MIMAC/

You can test if the repository has been cloned fine just running the by default simulation with:

.. code-block:: python
    :linenos:

    gamos main.in

The output should be the image of a sphere saved as a MHD/RAW in the output folder.

Once the test have been performed, users can set up the simulation using the GUI. To run the GUI type in the terminal:

.. code-block:: python
    :linenos:

    cd GUI/
    python3 mainWindow.py

Users must press **Apply cfg** button to modify all input files to set up correctly the simulation. Execute your simulation with:

.. code-block:: python
    :linenos:

    gamos main.in

We have prepared a simple bash script , :doc:`sendrun.sh <bash_script>`,  to run several runs at the same time (based on `GAMOS/tutorials/RTTutorials/exercise2 <https://github.com/arceciemat/GAMOS/blob/master/tutorials/RTTutorial/exercise2/sendjobs>`_ credits to Pedro Arce). It only accepts 2 parameters, the number of runs and the initial SEED. 

From the main path of the project you should type in the terminal:

.. code-block:: python
    :linenos:

    bash sendrun.sh 10 11111


.. warning:: The runs are independent, they do not share the geometry, each run builds the geometry. If you don´t have too much RAM memory there could be a memory leak.


