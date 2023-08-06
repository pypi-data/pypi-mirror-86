README	
=========

This is the README file for a collection of Python scripts that implement
the Comparison Model Method (CMM, [1]_, [2]_, [3]_ and [4]_).

For more details about the tests and the methodology, please see the
manuscript "Improving the robustness of the Comparison Model Method
for the identification of hydraulic transmissivities" by A.Comunian
and M.Giudici (submitted to `Computers & Geosciences`).

|

Purpose
=====================

This is a python implementation of the Comparison Model Method (CMM),
a direct method to solve inverse problems in hydrogeology, and in
particular to compute the hydraulic conductivity *T* of a confined
aquifer given an initial tentative value of *T* and one or more
interpolated hydraulic head fields *h*.  This implementation of the
CMM heavily relies on the USGS engines of the `Modflow
<https://www.usgs.gov/mission-areas/water-resources/science/modflow-and-related-programs>`_
family (and `Modflow6
<https://www.usgs.gov/software/modflow-6-usgs-modular-hydrologic-model>`_
in particular) to solve the forward problem, facilitated by the use of
the Python module `flopy
<https://www.usgs.gov/software/flopy-python-package-creating-running-and-post-processing-modflow-based-models>`_. Nevertheless,
it can be adapted to make use of other engines for the solution of the
forward problem.

|

Installation
=====================

|

Requirements
--------------------

In addition to the common Python modules ``numpy``, ``scipy`` and
``matplotlib``, this codes requires a recent version of ``flopy``.

.. note::

   You should adapt the name of the ``Modflow6`` executable name
   defined in the JSON configuration file (variable ``exe_name``) provided for the
   corresponding test case. For a general example, have a look at the
   file ``cmmpy/test/template/test.json``.

|

Download and install
-----------------------------

The suggested way is to use ``pip`` (which should be also already
available with `Anaconda`).

``cmmpy`` is available at the `Python Package Index repository
<https://pypi.org/project/cmmpy/>`_. Therefore, in can be easily
installed (together with its dependencies) with the command::

    pip install cmmpy

Alternatively, if you prefer to download the sources from
`https://bitbucket.org/alecomunian/cmmpy
<https://bitbucket.org/alecomunian/cmmpy>`_, you can:

1) Clone or download this repository on your hard drive.
2) If required, unpack it and ``cd cmmpy``.
3) Inside the project directory, from the command line::

     pip install -e .

4) To check if it worked, open a Python terminal and try::

     import cmmpy

|

Run the tests
---------------------------

1) Move into the folder ``ŧest``.
2) Then, from the shell, use the script ``run_cmm.py`` to run the
   corresponding test by providing the name of the JSON parameter file
   as unique input argument, like for example::

     ./run_cmm.py template/test.json

3) This should create (in the folder defined by the ``wdir`` variable in the JSON parameter file)
   all the output of the selected test.

If you want to run multiple test, have a look at the script ``run_all.py``.
   
|

Contacts
----------------------

This code was developed by the `HydroGeophysics
Lab. <https://sites.unimi.it/labidrogeofisica/>`_ of the University of
Milan.  Please do not hesitate to contact us should you require more
information or interested in contributing.

|


References
-------------------

.. [1] Scarascia, S. and Ponzini, G., "An approximate solution of the
       inverse problem in hydraulics" in L'Energia Elettrica (1972),
       pp 518–531, Volume 49

.. [2] Ponzini, G. and Crosta, G., "The comparison model method: A new
       arithmetic approach to the discrete inverse problem of
       groundwater hydrology", Transport in Porous Media, DOI:
       `10.1007/BF00233178 <http://dx.doi.org/10.1007/BF00233178>`_

.. [3] Ponzini, G. and Crosta, G. and Giudici, M. "Identification of
       thermal conductivities by temperature gradient profiles;
       one-dimensional steady flow", Geophysics, DOI:
       `10.1190/1.1442691 <http://dx.doi.org/10.1190/1.1442691>`_

.. [4] Ponzini, G. and Lozej, A., "Identification of aquifer
       transmissivities: The comparison model method", Water Resources
       Research, DOI: `10.1029/WR018i003p00597 <10.1029/WR018i003p00597>`_
