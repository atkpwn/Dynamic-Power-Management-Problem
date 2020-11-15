from random import randint, sample

from .demand import DemandProfile
from .server import ServerType


def generate_server_types(number_of_types, m, sigma, max_power_two=32):
    server_types = {}
    powers = [2**j for j in range(1, max_power_two)]
    for i in range(1, number_of_types + 1):
        rates = sorted(sample(powers, k=sigma), reverse=True) + [0]
        power_ups = [0] + sorted(sample(powers, k=sigma))
        server_types[i] = ServerType(
            m,
            list(zip(rates, power_ups))
        )
    return server_types


def generate_demand_profile(n, max_demand, max_length=1000):
    D = [randint(0, max_demand) for _ in range(n)]
    T = [0] + [randint(1, max_length) for _ in range(n)]
    for k in range(2, len(T)):
        T[k] += T[k - 1]
    return DemandProfile(T, D)
