# Classes
## `BaseSolver` [solver.py](solver.py)
Wrapper class of CPLEX functionalities that will be used in this project.

## `MinimumCostTwoCommodityFlowSolver` [minimum_cost_flow_solver.py](minimum_cost_flow_solver.py)
LP solver for the minimum-cost two-commodity flow problem. The input network is an instance of `Graph` implemented in [utility/graph.py](../utility/graph.py).

## `DPMSolver` [dpm_solver.py](dpm_solver.py)
LP solver for the DPM problem. The LP is described in Section 4.2 of the thesis.
