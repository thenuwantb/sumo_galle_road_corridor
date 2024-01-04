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
    mape = np.mean(np.abs((observed - simulated) / observed))
    return mape


def results_to_dataframe(current_estimate, error):
    df_columns = ['sigma']  # tau removed
    return_df = pd.DataFrame(columns=df_columns)
    temp_dict = {'sigma': current_estimate[0], 'error': error}
    # temp_dict['min_gap'] = current_estimate[0]

    temp_df = pd.DataFrame(temp_dict, index=[0])
    return_df = return_df.append(temp_df)
    return return_df


def run_simulation_output_hourly_speeds(sigma):
    # Generate files that includes sigma
    gen_bus_flow.create_bus_xml(_file_path='./additional_files/bus/bus_flows.xml', _sigma=sigma[0])
    gen_probe_flow.create_probe_flows(file_path='./additional_files/general_traffic/probe_vehicle_flow.xml',
                                      sigma=sigma[0])
    vtype_dist.create_vtype_dist(file_path='./additional_files/general_traffic/general_vtype_dist.xml', sigma=sigma[0])

    # Run SUMO and collect traffic data
    run_sumo_no_gui = "sumo -c 5_1_change_sim_parameters_automated.sumocfg " \
                      "--tripinfo-output outputs/ti_sigma_changed.xml "

    subprocess.run(run_sumo_no_gui, shell=True)

    probe_travel_speeds = probe_analysis.probe_vehicle_speeds('./outputs/ti_sigma_changed.xml')

    return probe_travel_speeds


if __name__ == '__main__':
    #0.10302464290633022
    # 0.103024642906330 = 0.27
    # 0.10302464290633 = 0.30256159026605434
    #0.34889605742600693
    #0.23424849961615712
    hourly_speeds = run_simulation_output_hourly_speeds([0.23424849961615712])
    print(hourly_speeds)

    # obs = np.array([26.73333, 19.09524, 17.69118])
    # sim = np.array([46.34374262, 15.97624771, 10.8139561 ])

    print(mape(observed_speeds, hourly_speeds))