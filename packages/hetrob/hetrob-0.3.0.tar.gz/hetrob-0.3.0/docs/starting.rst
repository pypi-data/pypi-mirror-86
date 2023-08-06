===============
Getting started
===============

The best way of getting started with the hetrob documentation is to first read the all the example python modules in
the intended order. After that, the additional chapters of this documentation can be used to potentially read up
on topics which were not mentioned within these examples.

Example scripts
---------------

The following listing provides an overview of all the example files, which will serve as a 'guided tour' through the
functionality of the hetrob library. Each script contains example code as well as extensive comments which explain,
as well as the additional underlying principles for most of the operations.

This list of examples is sorted in the order in which the information will make the most sense.

- `basic_vrp.py`_. This file contains the most stripped down version of steps, which are required to essentially
  solve a vehicle routing problem using a genetic algorithm. The vehicle routing problem which is considered in this
  file is one of the easiest imaginable variants, which simply considers some spatially distributed task locations and
  a number of available vehicles. There are no additional constraints and every other aspect such as task duration and
  vehicle speed are entirely constant and homogeneous. This file will not touch on any of the details, but rather
  provide an overview of steps required to operate the library.
- `hsvrsp.py`_. This script contains a more realistic VRP variant abbreviated "HSVRSP". This variant included additional
  constraints such as heterogeneity, cooperation and precedence, which make it much harder to solve. This example still
  follows the same overall pattern as the previous one, but goes into a little bit more details for each step. For
  example it introduces the possibility of loading problem instances from JSON files, modifying the solution
  representations objective function, changing the selection operator and the specifics of solution visualization.

.. _basic_vrp.py: https://github.com/the16thpythonist/hetrob/blob/master/hetrob/examples/basic_vrp.py
.. _hsvrsp.py: https://github.com/the16thpythonist/hetrob/blob/master/hetrob/examples/hsvrsp.py
