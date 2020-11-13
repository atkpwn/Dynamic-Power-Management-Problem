from dynamic_power_management import ServerType, DemandProfile
from solver import DPMSolver, x
from utility import ok, fail

EPS = 0.0001


def r(n, i):
    if i == n + 1:
        return EPS / (6*n**3)
    elif i >= n + 2:
        return 0
    return (n + 1 - i)


def Delta(n, i):
    if i >= n + 2:
        return Delta(n, n + 1) + (1 - EPS)
    return i**2


def inactive_period(n, i):
    return 2 * i


def construct_server_types(number_of_elements, sets):
    server_types = {}
    for i, C in enumerate(sets):
        elements = [0] + C + \
            [number_of_elements + 1, number_of_elements + 2]
        server_types[i + 1] = ServerType(
            1,  # The number of servers of this type
            [(r(number_of_elements, k), Delta(number_of_elements, k))
             for k in elements]
        )
    return server_types


def construct_demand_profile(number_of_elements):
    active_period = EPS
    section_gap = inactive_period(
        number_of_elements, number_of_elements + 1
    )
    T = [0]
    D = []
    for i in range(1, number_of_elements + 1):
        T.append(active_period)
        D.append(1)
        T.append(inactive_period(number_of_elements, i))
        D.append(0)
        T.append(active_period)
        D.append(1)
        if i < number_of_elements:
            T.append(section_gap)
            D.append(0)
    for k in range(2, len(T)):
        T[k] += T[k - 1]
    return DemandProfile(T, D)


def show_used_servers(solver):
    if not solver.solution:
        print(f'{fail("The problem has not been solved!")}')
        return
    m = len(solver.server_types)
    n = len(solver.demand_profile)
    for i in range(1, m + 1):
        vals = [solver.solution[x(i, 0, k)] for k in range(1, n + 1)]
        if any(v > 0 for v in vals):
            print(
                f'{ok(f"S{i}")} : ', end=''
            )
            for v in vals:
                if v > 0:
                    print(ok(f'{v:6.2f}'), end=' ')
                else:
                    print(f'{v:6.2f}', end=' ')
            print()


def main():
    '''
    >>> number_of_elements = 3
    >>> sets = [[1, 2], [1, 3], [2, 3]]
    >>> server_types = construct_server_types(number_of_elements, sets)
    >>> demand_profile = construct_demand_profile(number_of_elements)
    >>> lp = DPMSolver(server_types, demand_profile, variable_type='C')
    >>> lp.silent()
    >>> lp.solve()
    83.50226111117283
    '''
    number_of_elements = 3
    sets = [[1, 2], [1, 3], [2, 3]]

    server_types = construct_server_types(number_of_elements, sets)
    demand_profile = construct_demand_profile(number_of_elements)

    print(f'n    : {number_of_elements}')
    print(f'Sets : {sets}')
    print('=' * 40)
    lp = DPMSolver(server_types, demand_profile, variable_type='C')
    lp.silent()
    res_c = lp.solve()
    # print(f'LP:')
    # show_used_servers(lp)

    ip = DPMSolver(server_types, demand_profile, variable_type='I')
    ip.silent()
    res_i = ip.solve()
    # print(f'IP:')
    # show_used_servers(ip)

    print(f'Fractional objective value : {res_c:10.6f}')
    print(f'Integral objective value   : {res_i:10.6f}')
    print(f'Difference                 : {res_i - res_c:10.6f}')
    print(f'Ratio                      : {res_c / res_i:10.6f}')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
