# Dynamic Power Management Problem
Implementation of algorithms for DPM problem based on [this paper](https://dl.acm.org/doi/10.1145/3087556.3087560).

## Requirement
* Python 3.6
* [IBM ILOG CPLEX Optimization Studio](https://www.ibm.com/products/ilog-cplex-optimization-studio)

## Files and Folders
### Algorithm Implementation
* [algorithm.py](algorithm.py): A main file of the implementation of the approximation algorithm
* [network.py](network.py): Network construction step
* [solver](solver): Linear program solvers of the min-cost flow problem and DPM problem.
* [utility](utility): Implementation of graph and other utility functions.

### Examples
* [generate_test.py](generate_test.py): Example of random generated test cases.
* [set_cover_reduction.py](set_cover_reduction.py): Example of a reduction from set cover instance. This module provides `construct_server_types(number_of_elements, sets)` and `construct_demand_profile(number_of_elements)` which are used to create an DPM instance of a given set cover instance.

#### Usage
```shell
$ python set_cover_reduction.py
n    : 3
Sets : [[1, 2], [1, 3], [2, 3]]
========================================
Fractional objective value :  83.502261
Integral objective value   :  84.002205
Difference                 :   0.499944
Ratio                      :   0.994048
```

```shell
$ python generate_test.py
Fractional optimum: 1373369579632.000000
Integral optimum:   1373369579632.000000
Flow cost:          1373369579632.0
Approximation:      1786438111584
```
