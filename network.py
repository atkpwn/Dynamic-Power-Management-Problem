from utility import Graph


def u(i, k):
    return f'u({i}, {k})'


def l(i, j, k):
    return f'l({i}, {j}, {k})'


def la(i, j, k):
    return f'la({i}, {j}, {k})'


def _construct_component(network, server_types, demand_profile, i):
    def add_upper_path_edge(i, k):
        network.add_edge(
            u(i, k), u(i, k + 1),
            capacity=server_types[i].m, capacity1=server_types[i].m, capacity2=0,
            cost=server_types[i][0].rate *
            (demand_profile.t[k + 1] - demand_profile.t[k])
        )

    def add_lower_path_edges(i, j, k):
        network.add_edge(
            l(i, j, k), la(i, j, k),
            capacity=server_types[i].m, capacity1=server_types[i].m, capacity2=0,
            cost=server_types[i][j].rate *
            (demand_profile.t[k + 1] - demand_profile.t[k])
        )
        network.add_edge(
            la(i, j, k), l(i, j, k + 1),
            capacity=server_types[i].m, capacity1=server_types[i].m, capacity2=server_types[i].m,
            cost=0
        )

    def add_state_transition_edges(i, j, k):
        # power-up edge
        network.add_edge(
            l(i, j, k), u(i, k),
            capacity=server_types[i].m, capacity1=server_types[i].m, capacity2=0,
            cost=server_types[i][j].power_up_energy
        )
        # power-down edge
        network.add_edge(
            u(i, k), l(i, j, k),
            capacity=server_types[i].m, capacity1=server_types[i].m, capacity2=0,
            cost=0
        )

    n = len(demand_profile)
    for k in demand_profile:
        add_upper_path_edge(i, k)
    for j in range(1, server_types[i].sigma + 1):
        for k in demand_profile:
            add_lower_path_edges(i, j, k)
            add_state_transition_edges(i, j, k)
        add_state_transition_edges(i, j, n + 1)


def _add_sources_sinks(network, server_types, demand_profile):
    n = len(demand_profile)
    m = sum(s.m for s in server_types.values())
    # Commodity 1
    network.add_vertex('a0', supply1=m)
    network.add_vertex('b0', supply1=-m)
    for i, s in server_types.items():
        network.add_edge(
            'a0', l(i, s.sigma, 1),
            capacity=s.m, capacity1=s.m, capacity2=0,
            cost=0
        )
        network.add_edge(
            l(i, s.sigma, n + 1), 'b0',
            capacity=s.m, capacity1=s.m, capacity2=0,
            cost=0
        )
    # Commodity 2
    M = sum(s.m * (s.sigma - 1) for s in server_types.values())
    for k in demand_profile:
        Dk = M + demand_profile.d[k]
        network.add_vertex(f'a{k}', supply2=Dk)
        network.add_vertex(f'b{k}', supply2=-Dk)
        for i, s in server_types.items():
            for j in range(1, s.sigma + 1):
                network.add_edge(
                    f'a{k}', la(i, j, k),
                    capacity=s.m, capacity1=0, capacity2=s.m,
                    cost=0
                )
                network.add_edge(
                    l(i, j, k + 1), f'b{k}',
                    capacity=s.m, capacity1=0, capacity2=s.m,
                    cost=0
                )


def construct_network(server_types, demand_profile):
    '''
    >>> from set_cover_reduction import construct_server_types, construct_demand_profile
    >>> number_of_elements = 3
    >>> sets = [[1, 2], [1, 3], [2, 3]]
    >>> server_types = construct_server_types(number_of_elements, sets)
    >>> demand_profile = construct_demand_profile(number_of_elements)
    >>> network = construct_network(server_types, demand_profile)
    >>> len(network.vertices)
    336
    >>> len(network.edges)
    855
    '''
    network = Graph()
    for i in server_types:
        _construct_component(network, server_types, demand_profile, i)
    _add_sources_sinks(network, server_types, demand_profile)
    return network


if __name__ == '__main__':
    import doctest
    doctest.testmod()
