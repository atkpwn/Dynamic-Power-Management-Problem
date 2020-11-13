from random import randint, sample

from .demand import DemandProfile
from .server import ServerType


def generate_server_types(number_of_types, m, sigma):
    server_types = {}
    powers = [2**j for j in range(1, 2 * sigma)]
    for i in range(1, number_of_types + 1):
        rates = sorted(sample(powers, k=sigma), reverse=True) + [0]
        power_ups = [0] + sorted(sample(powers, k=sigma))
        server_types[i] = ServerType(
            m,
            list(zip(rates, power_ups))
        )
    return server_types


def generate_demand_profile(n, maximum_demands):
    D = [randint(0, maximum_demands) for _ in range(n)]
    T = [randint(1, 100) for _ in range(n)]
    T = [0] + [randint(1, 1000) for _ in range(n)]
    for k in range(2, len(T)):
        T[k] += T[k - 1]
    return DemandProfile(T, D)
