import subprocess
import copy
import timeit

import numpy as np
import pandas as pd
from scipy.optimize import dual_annealing

import additional_files.bus.generate_bus_flows as gen_bus_flow
import additional_files.general_traffic.generate_probe_flows as gen_probe_flow
import additional_files.general_traffic.vehicle_type_distribution as vtype_dist
import analysis.travel_time.probe_vehicle_travel_time as probe_analysis

# sigma = 0.1

observed_speeds = np.array([26.73333, 19.09524, 17.69118])


def mape(observed, simulated):
    """
        Calculate the Mean Absolute Percentage Error (MAPE) between observed and simulated values.

        Parameters:
        - observed (array-like): Array or list of observed values.
        - simulated (array-like): Array or list of simulated values.

        Returns:
        float: The Mean Absolute Percentage Error (MAPE) between observed and simulated values.
        """
    _mape = np.mean(np.abs((observed - simulated) / observed))
    return _mape


def results_to_dataframe(current_estimate, error):
    """
        Convert current estimation results and error into a pandas DataFrame.

        Parameters:
        - current_estimate (array-like): Array or list containing the current estimation results.
        - error (float): The error associated with the current estimation.

        Returns:
        pd.DataFrame: A DataFrame containing the current estimation results and error.

        Example:
        >>> current_estimate = [0.5]
        >>> error = 0.02
        >>> df = results_to_dataframe(current_estimate, error)
        >>> print(df)
             sigma  error
        0     0.5   0.02
        """
    df_columns = ['sigma']
    return_df = pd.DataFrame(columns=df_columns)
    temp_dict = {'sigma': current_estimate[0], 'error': error}

    temp_df = pd.DataFrame(temp_dict, index=[0])
    return_df = return_df.append(temp_df)
    return return_df


def run_simulation_evaluate_objective_func(sigma):
    # Generate files that includes sigma
    gen_bus_flow.create_bus_xml(_file_path='./additional_files/bus/bus_flows.xml', _sigma=sigma[0])
    gen_probe_flow.create_probe_flows(file_path='./additional_files/general_traffic/probe_vehicle_flow.xml',
                                      sigma=sigma[0])
    vtype_dist.create_vtype_dist(file_path='./additional_files/general_traffic/general_vtype_dist.xml', sigma=sigma[0])

    # Run SUMO and collect traffic data
    run_sumo_no_gui = "sumo -c 5_1_change_sim_parameters_automated.sumocfg " \
                      "--no-warnings " \
                      "--tripinfo-output outputs/ti_sigma_changed.xml "

    subprocess.run(run_sumo_no_gui, shell=True)

    probe_travel_speeds = probe_analysis.probe_vehicle_speeds('./outputs/ti_sigma_changed.xml')

    objective_evaluation = mape(observed_speeds, probe_travel_speeds)

    return objective_evaluation


def run_spsa_sigma(start_guess, max_iter=30):
    alpha = 0.602
    gamma = 0.101
    c = 0.49
    a = 2.4
    A = 5

    ck_manipulate = [1.00]

    initial_guess = copy.copy([start_guess])
    best_estimate = copy.copy(initial_guess)
    current_estimate = copy.copy(initial_guess)

    print(f"Type initial Guess {type(initial_guess)}")

    initial_cost = run_simulation_evaluate_objective_func(initial_guess)
    print(initial_cost)
    best_mape = copy.copy(initial_cost)

    # saving results
    results_columns = ['sigma']
    results_df = pd.DataFrame(columns=results_columns)

    # set random seed
    np.random.seed(55)

    # main SPSA algorithm
    t_start = timeit.default_timer()

    for k in range(max_iter):
        ak = a / (A + k + 1) ** alpha
        ck = c / (k + 1) ** gamma

        print(f"--Iteration{k} ak = {ak}")
        print(f"--Iteration{k} ck = {ck}")

        delta_k = np.random.choice([-1, 1], size=len(current_estimate), p=[0.5, 0.5])  # delta_k = np.array([1,-1])
        print(f"--Iteration{k} delta_k{delta_k}")

        increase_u = copy.copy(current_estimate)
        decrease_u = copy.copy(current_estimate)

        # 2. Perturbate sigma [between 0, 1]
        if 0.0 < (current_estimate[0] + ck * ck_manipulate[0] * delta_k[0]) < 1.0:
            increase_u[0] = current_estimate[0] + ck * ck_manipulate[0] * delta_k[0]
            print(f"-- Iteration {k} perturbed + {ck * ck_manipulate[0] * delta_k[0]}")
            print(f"--Iteration {k} : Increase {increase_u}")
        else:
            increase_u[0] = best_estimate[0]
            print(f"--Iteration {k} : Increase {increase_u}")

        # 2. Perturbate sigma [between 0, 1]
        if 0.0 < (current_estimate[0] - ck * ck_manipulate[0] * delta_k[0]) < 1.0:
            decrease_u[0] = current_estimate[0] - ck * ck_manipulate[0] * delta_k[0]
            print(f"-- Iteration {k} perturbed - {ck * ck_manipulate[0] * delta_k[0]}")
            print(f"--Iteration {k} : Decrease {decrease_u}")
        else:
            decrease_u[0] = best_estimate[0]
            print(f"--Iteration {k} : Decrease {decrease_u}")

        # Step 3 - Function evaluation
        cost_increase = run_simulation_evaluate_objective_func(increase_u)
        print(f"--Iteration {k} : Objective function inc. {cost_increase}")
        # if k==9:
        #     print("9th Iteration")
        cost_decrease = run_simulation_evaluate_objective_func(decrease_u)
        print(f"--Iteration {k} : Objective function dec. {cost_decrease}")

        # Step 4 - Gradient approximation
        gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), delta_k)
        gk_step_size = ak * gk
        gk_step_size_list = gk_step_size.tolist()
        # print("gkgkgkgk", gk_step_size_list)

        # Step 5 - Update current_estimate estimate
        previous_estimate = copy.copy(current_estimate)

        # 5.2. Perturbate sigma [between 0, 1]
        if 0.0 < (previous_estimate[0] - gk_step_size_list[0]) < 1.0:
            current_estimate[0] = previous_estimate[0] - gk_step_size_list[0]
            print(f"--Iteration {k} : New estimate. {current_estimate}")
        else:
            current_estimate[0] = best_estimate[0]
            print(f"--Iteration {k} : failed to update replaced from best estimate. {current_estimate}")

        # Step 6 : get new cost and save calculations
        cost_new = run_simulation_evaluate_objective_func(current_estimate)

        results_df = results_df.append(results_to_dataframe(current_estimate=current_estimate, error=cost_new))

        # Step 6 : update best estimate
        if cost_new < best_mape:
            best_mape = cost_new
            best_estimate = copy.copy(current_estimate)

        print("Iteration", k)
        print("New cost", cost_new)
        print("Current Estimate", current_estimate)
        print("Best Estimate", best_estimate)

    t_duration = timeit.default_timer() - t_start
    print("Duration = " + str(t_duration))
    results_df.to_csv('restart_spsa_11102022.csv')


if __name__ == '__main__':
    run_spsa_sigma(0.23424849961615712, 30)
