BOSS
=========
Bayesian Optimization Structure Search (BOSS) is an active machine learning technique for accelerated global exploration of energy and property phase space. It is designed to facilitate machine learning in computational and experimental natural sciences.

For a more detailed description of the code and tutorials, please consult the `user guide <https://cest-group.gitlab.io/boss>`_.

Installation
------------
BOSS is distributed as a PyPI package and can be installed using pip::

    python3 -m pip install --user aalto-boss

Basic usage
-----------
As an easy example, consider the optimization of a bounded 1D function. BOSS can be run either directly from Python or via a CLI interface, both these approaches are illustrated briefly below. Note that BOSS always minimizes a given function.

Python iterface
^^^^^^^^^^^^^^^^^^^^^
To run BOSS from Python we first define our objective function, by default BOSS expects this function to take a single 2D numpy array as argument (this behaviour can be modified) and return a scalar value, although. Next, we import the ``BOMain`` object and feed it the function plus any number of BOSS keywords, after which the optimization can be started. Once finished, the optimziation results are returned in a ``BOResults`` object.

.. code-block:: python

    """ Using BOSS to solve the minimization problem
    f(x) = sin(x) + 1.5*exp(-(x-4.3)**2) , 0 < x < 7
    """
    import numpy as np
    from boss.bo.bo_main import BOMain

    def func(X):
    """ BOSS-compatible definition of the function. """
        x = X[0, 0]
        return np.sin(x) + 1.5*np.exp(-(x - 4.3)**2)

    if __name__ == '__main__':
        bo = BOMain(
            func, 
            np.array([[0., 7.]]),  # bounds
            yrange=[-1, 1],
            kernel='rbf',
            initpts=5,
            iterpts=15,
            verbosity=2
        )
        res = bo.run()
        print(res.xmin, res.fmin)


Command-line iterface
^^^^^^^^^^^^^^^^^^^^^
The CLI is provided by an executable called ``boss``. The user must provide an input file containing a list of BOSS keywords and a separate Python script that defines a function to be optimized. By default, BOSS expects this function to take a single 2D numpy array as argument (this behaviour can be modified) and return a scalar value. Below we define such a function in a Python script, arbitrarily named ``user_function.py``:

.. code-block:: python

    """ user_function.py
    This script contains the function definition for the minimization problem
    f(x) = sin(x) + 1.5*exp(-(x-4.3)**2) ,  0 < x < 7
    Note that the bounds are specified in the BOSS input file.
    """
    import numpy as np

    def func(X):
    """ BOSS-compatible definition of the function. """
        x = X[0, 0]
        return np.sin(x) + 1.5*np.exp(-(x - 4.3)**2)


To minimize this function subject to the constraint *0 < x < 7*, we define a BOSS input file ``boss.in``:

.. code-block:: python

    # boss.in
    userfn        user_function.py func
    bounds        0 7
    yrange        -1 1
    kernel        rbf
    initpts       5
    iterpts       15
    verbosity     2

The optimization can now be started from the command line:

.. code-block:: bash

    $ boss o boss.in

Credits
-------
BOSS is under active development in the `Computational Electronic Structure Theory (CEST) group <http://cest.aalto.fi/>`_ at Aalto University. Past and current members of development team include

* Ville Parkkinen
* Henri Paulamäki
* Arttu Tolvanen
* Ulpu Remes
* Nuutti Sten
* Joakim Löfgren (maintainer)
* Milica Todorović (team lead)

If you wish to use BOSS in your research, please cite

| Milica Todorovic, Micheal U. Gutmann, Jukka Corander, and Patrick Rinke
| *Bayesian inference of atomistic structure in functional materials*
| npj Comput Mater **5**, 35 (2019)
| `doi: 10.1038/s41524-019-0175-2 <https://doi.org/10.1038/s41524-019-0175-2>`_

Issues and feature requests
---------------------------
It is strongly encouraged to submit bug reports and feature requests via the
`gitlab issue tracker <https://gitlab.com/cest-group/boss/issues>`_.
The BOSS development team can be contacted by email at milica.todorovic@aalto.fi
