import os
import sys

from dynamic_power_management import ServerType
from dynamic_power_management import DemandProfile
from dynamic_power_management import generate_server_types
from dynamic_power_management import generate_demand_profile
from solver import DPMSolver
from algorithm import flow_based_algorithm
from utility import fail, ok


def get_subfolder_name(number_of_types,
                       servers_in_each_type,
                       sigma,
                       number_of_time_steps):
    return f'{number_of_types}_{servers_in_each_type}_{sigma}_{number_of_time_steps}'


def get_server_file_name(folder_path, num):
    return os.path.join(folder_path, f'server_{num:03d}.in')


def get_demand_profile_name(folder_path, num):
    return os.path.join(folder_path, f'demand_{num:03d}.in')


def create_test_cases(number_of_types,
                      servers_in_each_type,
                      sigma,
                      number_of_time_steps,
                      max_power_two,
                      max_demand,
                      max_length=1000,
                      number_of_tests=10,
                      folder='input'):
    subfolder = get_subfolder_name(number_of_types,
                                   servers_in_each_type,
                                   sigma,
                                   number_of_time_steps)
    folder_path = os.path.join(folder, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for num in range(1, number_of_tests + 1):
        server_file = get_server_file_name(folder_path, num)
        server_types = generate_server_types(
            number_of_types,
            servers_in_each_type,
            sigma,
            max_power_two=max_power_two
        )
        demand_file = get_demand_profile_name(folder_path, num)
        demand_profile = generate_demand_profile(
            number_of_time_steps,
            max_demand,
            max_length=max_length
        )
        ServerType.write(server_file, server_types)
        DemandProfile.write(demand_file, demand_profile)


def experiment(number_of_types,
               servers_in_each_type,
               sigma,
               number_of_time_steps,
               folder,
               test_num):
    subfolder = get_subfolder_name(number_of_types,
                                   servers_in_each_type,
                                   sigma,
                                   number_of_time_steps)
    folder_path = os.path.join(folder, subfolder)

    server_file = get_server_file_name(folder_path, test_num)
    server_types = ServerType.read(server_file)
    demand_file = get_demand_profile_name(folder_path, test_num)
    demand_profile = DemandProfile.read(demand_file)

    schedule, fractional = flow_based_algorithm(
        server_types, demand_profile, use_flow=False)
    print(server_file)
    print(f'  Fractional optimum: {fractional}')
    print(f'  Approximation:      {schedule.total_energy}')

    isolver = DPMSolver(server_types, demand_profile, variable_type='I')
    isolver.silent()
    integral = isolver.solve()
    isolver.verify_feasibility()
    print(f'  Integral optimum:   {integral}')

    if fractional > integral:
        print(fail('Values exceed the limit!'))
        sys.exit(-1)

    return schedule.total_energy / integral


if __name__ == '__main__':
    max_power_two = 32
    max_length = 1000
    number_of_tests = 100
    folder = 'input'
    res = []
    for number_of_types in [2, 4, 8, 16]:
        for servers_in_each_type in [100, 150, 200, 300]:
            sys.stderr.write(
                f'# {number_of_types} {servers_in_each_type}\n'
            )
            for sigma in [2, 4, 8, 16]:
                for number_of_time_steps in [20, 40, 60, 80, 100]:
                    max_demand = number_of_types * servers_in_each_type
                    create_test_cases(number_of_types,
                                      servers_in_each_type,
                                      sigma,
                                      number_of_time_steps,
                                      max_power_two,
                                      max_demand,
                                      max_length,
                                      number_of_tests,
                                      folder
                                      )

                    for test_num in range(1, number_of_tests + 1):
                        # print(
                        #     f'number_of_types      {number_of_types}\n'
                        #     f'servers_in_each_type {servers_in_each_type}\n'
                        #     f'sigma                {sigma}\n'
                        #     f'number_of_time_steps {number_of_time_steps}'
                        # )
                        r = experiment(
                            number_of_types,
                            servers_in_each_type,
                            sigma,
                            number_of_time_steps,
                            folder,
                            test_num
                        )
                        res.append(r)
                        print(20 * '-')
