from dynamic_power_management import generate_server_types
from dynamic_power_management import generate_demand_profile
from solver import DPMSolver
from algorithm import flow_based_algorithm


def main():
    number_of_types = 4
    number_of_servers_for_each_type = 100
    sigma = 10

    number_of_time_steps = 20
    maximum_demands = number_of_types * number_of_servers_for_each_type

    server_types = generate_server_types(
        number_of_types,
        number_of_servers_for_each_type,
        sigma
    )
    demand_profile = generate_demand_profile(
        number_of_time_steps,
        maximum_demands
    )

    solver = DPMSolver(server_types, demand_profile, variable_type='C')
    solver.silent()
    fractional = solver.solve()
    solver.verify_feasibility()
    print(f'Fractional optimum: {fractional:.6f}')

    solver = DPMSolver(server_types, demand_profile, variable_type='I')
    solver.silent()
    integral = solver.solve()
    solver.verify_feasibility()
    print(f'Integral optimum:   {integral:.6f}')

    schedule, flow_cost = flow_based_algorithm(server_types, demand_profile)
    print(f'Flow cost:          {flow_cost}')
    print(f'Approximation:      {schedule.total_energy}')


if __name__ == '__main__':
    main()
