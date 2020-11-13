from dynamic_power_management import Schedule

from network import construct_network, u
from solver.minimum_cost_flow_solver import MinimumCostTwoCommodityFlowSolver


def construct_schedule(server_types, demand_profile, network):

    def find_next_power_up(i, k):
        def energy(s, k, p):
            '''
            Return energy residing in state s from k to p and powers up
            '''
            return s.rate * (demand_profile.t[p] - demand_profile.t[k]) + s.power_up_energy

        for p in range(k + 1, len(demand_profile) + 1):
            if d[i, p] >= mu + 1:
                _, j = min((energy(server_types[i][j], k, p), j)
                           for j in range(1, server_types[i].sigma + 1))
                return p, j
        return k - 1, server_types[i].sigma

    # compute d[i, k]
    tau = len(server_types)
    d = {
        # scale up the flow of commodity 1
        (i, k): min(int(tau * network.edges[(u(i, k), u(i, k + 1))].flow1),
                    server_types[i].m)
        for k in demand_profile for i in server_types
    }

    schedule = Schedule(server_types, demand_profile)
    for i in server_types:
        for k in demand_profile:
            schedule.reside(i, k, 1, d[i, k], 0)
            mu = d[i, k]
            while mu < d.get((i, k - 1), 0):
                # use p = k'
                p, j = find_next_power_up(i, k)
                new_mu = min(d[i, k - 1], d[i, p])
                for q in range(k, p):
                    schedule.reside(i, q, mu + 1, new_mu, j)
                mu = new_mu

    schedule.is_feasible()
    return schedule


def verify_flow(server_types, demand_profile, network, error=1e-12):
    assert all(
        sum(network.edges[(u(i, k), u(i, k + 1))].flow1 for i in server_types)
        >= demand_profile.d[k] - error
        for k in demand_profile
    )


def flow_based_algorithm(server_types, demand_profile):
    '''
    >>> from set_cover_reduction import construct_server_types, construct_demand_profile
    >>> number_of_elements = 3
    >>> sets = [[1, 2], [1, 3], [2, 3]]
    >>> server_types = construct_server_types(number_of_elements, sets)
    >>> demand_profile = construct_demand_profile(number_of_elements)
    >>> schedule = flow_based_algorithm(server_types, demand_profile)
    >>> schedule.total_energy
    167.0045222223457
    '''
    network = construct_network(server_types, demand_profile)
    solver = MinimumCostTwoCommodityFlowSolver(network)
    solver.silent()
    flow_cost = solver.solve()
    verify_flow(server_types, demand_profile, network)
    schedule = construct_schedule(server_types, demand_profile, network)
    return schedule, flow_cost


if __name__ == '__main__':
    import doctest
    doctest.testmod()
