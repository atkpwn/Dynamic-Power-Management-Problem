import cplex

from .solver import BaseSolver


def x(i, j, k):
    return f'x({i},{j},{k})'


def y(i, j, k):
    return f'y({i},{j},{k})'


def _create_objective_and_variables(server_types, demand_profile):
    objective = []
    variables = []
    for i in server_types:
        for j in range(server_types[i].sigma + 1):
            for k in demand_profile:
                objective.append(
                    server_types[i][j].rate *
                    (demand_profile.t[k + 1] - demand_profile.t[k])
                )
                variables.append(x(i, j, k))
    for i in server_types:
        for j in range(1, server_types[i].sigma + 1):
            for k in demand_profile:
                objective.append(server_types[i][j].power_up_energy)
                variables.append(y(i, j, k))
    upper_bounds = [cplex.infinity] * len(variables)
    return objective, variables, upper_bounds


def _create_constraints(server_types, demand_profile):
    row_names = []
    rows = []
    rhs = []
    senses = []

    # state constraints
    for k in demand_profile:
        for i in server_types:
            row_names.append(f'state ({i}, {k})')
            row = [
                [x(i, j, k) for j in range(server_types[i].sigma + 1)],
                [1] * (server_types[i].sigma + 1)
            ]
            rows.append(row)
            rhs.append(server_types[i].m)
            senses.append('E')

    # demand constraints
    for k in demand_profile:
        row_names.append(f'demand {k}')
        row = [[x(i, 0, k) for i in server_types],
               [1] * len(server_types)]
        rows.append(row)
        rhs.append(demand_profile.d[k])
        senses.append('G')

    # power-up constraints
    for k in demand_profile:
        if k == 1:
            # the first time step
            for i in server_types:
                row_names.append(
                    f'initial ({i}, {server_types[i].sigma}, {k})'
                )
                # W.l.o.g. set x(i, sigma_i, 0) = m_i so that every server is
                # inactive before the first time step. Then,
                # y(i, sigma_i, 1) >= m_i - x(i, sigma_i, 1)
                row = [[y(i, server_types[i].sigma, 1), x(i, server_types[i].sigma, 1)],
                       [1, 1]]
                rows.append(row)
                rhs.append(server_types[i].m)
                senses.append('G')
        else:
            for i in server_types:
                for j in range(1, server_types[i].sigma + 1):
                    row_names.append(f'powerup ({i}, {j}, {k})')
                    # y(i, j, k) >= x(i, j, k - 1) - x(i, j, k)
                    row = [[y(i, j, k), x(i, j, k - 1), x(i, j, k)],
                           [1, -1, 1]]
                    rows.append(row)
                    rhs.append(0)
                    senses.append('G')
    return rows, senses, rhs, row_names


class DPMSolver(BaseSolver):
    def __init__(self, server_types, demand_profile, variable_type='I'):
        super().__init__()
        self.server_types = server_types
        self.demand_profile = demand_profile

        if variable_type not in {'I', 'C'}:
            variable_type = 'I'

        self.set_objective(
            *_create_objective_and_variables(server_types, demand_profile),
            variable_type
        )
        self.set_constraints(
            *_create_constraints(server_types, demand_profile)
        )

    def solve(self, write=False, filename='dpm_instance.lp'):
        return super().solve(write, filename=filename)

    def verify_feasibility(self, error=1e-12):
        assert all(sum(self.solution[x(i, 0, k)] for i in self.server_types)
                   >= self.demand_profile.d[k] - error
                   for k in self.demand_profile)
