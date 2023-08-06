Rest API Base
=============

Quickstart
----------

Install Remotely from GitHub:
    
    pip install git+https://github.com/JHibbard/rest-api-base --upgrade


Running Test Matrix
-------------------

note: you can add `-s` flag to print to stderr/stdout during pytest-ing

    tox


Complexity Metrics
------------------

Cyclomatic complexity (cc):

    radon cc ./src/*

Maintainability index:

    radon mi ./src/*


Building Distribution
---------------------

Building Wheel:

    python setup.py bdist_wheel sdist

Installing Wheel:

    pip install /path/to/wheel/..
