Testing Instructions
====================
Note that the project has been written for Python 2.x (specifically 2.7.8, the default on the lab clients). It is likely to work with other versions in the 2.x series, and perhaps also within the 3.x series, but it is NOT guaranteed to.

To run the tests, you will need to be in an environment where you can install new python packages (normally this requires either root privileges, or running within a python virtualenvironment (virtualenv). Within whatever environment you are using, you should install the `virtualenv` package (`pip install virtualenv`).

Following this, the entire test suite can be run by simply executing `python setup.py test`. This will automatically download the test-suite runner (tox), and execute the tests in the `test_life.py` file.
