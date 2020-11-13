import cplex
from cplex.exceptions import CplexError


class BaseSolver:

    def __init__(self):
        self._solution = None
        self._status = None
        self._model = cplex.Cplex()

    def set_objective(self, objective, variables, upper_bounds, variable_type='I'):
        self._model.objective.set_sense(
            self._model.objective.sense.minimize
        )
        self._model.variables.add(
            obj=objective,
            ub=upper_bounds,
            names=variables,
            types=variable_type * len(variables)
        )

    def set_constraints(self, rows, senses, rhs, names):
        self._model.linear_constraints.add(
            lin_expr=rows,
            senses=senses,
            rhs=rhs,
            names=names
        )

    def silent(self):
        self._model.set_log_stream(None)
        self._model.set_error_stream(None)
        self._model.set_warning_stream(None)
        self._model.set_results_stream(None)

    def solve(self, write=False, filename='instance.lp'):
        def save_solution():
            variables = self.model.variables.get_names()
            values = self.model.solution.get_values(variables)
            self._solution = dict(zip(variables, values))
            self._status = self.model.solution.status[
                self.model.solution.get_status()
            ]

        try:
            self._model.solve()
        except CplexError as exc:
            print(exc)
            return

        save_solution()
        if write:
            self._model.write(filename)

        return self._model.solution.get_objective_value()

    @property
    def model(self):
        return self._model

    @property
    def solution(self):
        if not self._solution:
            return None
        return self._solution.copy()

    @property
    def status(self):
        return self._status
