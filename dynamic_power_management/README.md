# Classes
## `State` [server.py](server.py)
* `rate` as consumption rate r{i, j}
* `power_up_energy` as power-up energy \Delta{i, j}

## `ServerType` [server.py](server.py)
An object of this class contains `State` objects and other properties. It can be created with the number of servers and a list of tuples (r{i, j}, \Delta{i, j}). We require that a deeper sleep state has smaller consumption rate and requires higher power-up energy.
```python
>>> ServerType(127, [(15, 0), (5, 3), (3, 4), (0, 5)])
127 * <states(4):
    <rate: 15.000000, power_up: 0.000000>
    <rate: 5.000000, power_up: 3.000000>
    <rate: 3.000000, power_up: 4.000000>
    <rate: 0.000000, power_up: 5.000000>
>
```

## `DemandProfile` [demand.py](demand.py)
An object is created by passing a list of points in time `T` and a list of demands `D`. We requires that the `len(T) == len(D) + 1` and `T[k + 1] > T[k]` for all `k`. The index of DemandProfile's properties `t` and `d` start from 1.

```python
>>> demand_profile = DemandProfile([1, 2, 5], [1, 2])
>>> demand_profile.t[3]
5
```

## `Schedule` [schedule.py](schedule.py)
Provide class for schedule with functionalities and verification.

# Functions
## `generate_server_types(number_of_types, m, sigma)` [generate.py](generate.py)
Generate `number_of_types` server types in which each type has `m` servers and the same number of sleep states `sigma`.

## `generate_demand_profile(n, maximum_demands, max_length=1000)` [generate.py](generate.py)
Generate `DemandProfile` of `n` time steps each of length between 1 to `max_length`.
