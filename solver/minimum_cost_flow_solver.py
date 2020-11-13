import cplex

from solver import BaseSolver


def f(i, e):
    s = str(e).replace("'", '').replace(' ', '')
    return f'f{i}{s}'


def _create_objective_and_variables(network):
    objective = []
    variables = []
    upper_bounds = []
    for e in network.edges:
        objective.append(network.edges[e].cost)
        variables.append(f(1, e))
        upper_bounds.append(network.edges[e].capacity1)
        objective.append(network.edges[e].cost)
        variables.append(f(2, e))
        upper_bounds.append(network.edges[e].capacity2)
    return objective, variables, upper_bounds


def _create_constraints(network):
    row_names = []
    rows = []
    rhs = []
    senses = []

    supplies = {
        1: {v: network.vertices[v].supply1 for v in network},
        2: {v: network.vertices[v].supply2 for v in network},
    }
    for i in [1, 2]:
        for v in network:
            row_names.append(f'f{i};{v.replace(" ", "")}')
            row = [
                [f(i, (v, w)) for w in network.out_edges[v]] +
                [f(i, (w, v)) for w in network.in_edges[v]],
                [1 for _ in network.out_edges[v]] +
                [-1 for _ in network.in_edges[v]]
            ]
            rows.append(row)
            rhs.append(supplies[i][v])
            senses.append('E')

    # total capacity constraints
    for e in network.edges:
        row_names.append(f'{e}')
        row = [
            [f(1, e), f(2, e)],
            [1, 1]
        ]
        rows.append(row)
        rhs.append(network.edges[e].capacity)
        senses.append('L')
    return rows, senses, rhs, row_names


class MinimumCostTwoCommodityFlowSolver(BaseSolver):

    def __init__(self, network, variable_type='C'):
        super().__init__()
        self.network = network
        if variable_type not in {'I', 'C'}:
            variable_type = 'I'

        self.set_objective(
            *_create_objective_and_variables(network),
            variable_type
        )
        self.set_constraints(
            *_create_constraints(network)
        )

    def solve(self, write=False, filename='flow.lp'):
        res = super().solve(write, filename=filename)
        for e in self.network.edges:
            edge = self.network.edges[e]
            edge.flow1 = self.solution[f(1, e)]
            edge.flow2 = self.solution[f(2, e)]
        return res
