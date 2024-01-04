import subprocess
from xml.etree import ElementTree as et
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import additional_files.bus.generate_bus_flows as gen_bus_flow


np.random.seed(55)
random_seeds = np.random.randint(10000, 99999, 10).tolist()
print(random_seeds)

run_sumo_no_gui = "sumo -c 4_2_section_simulation_outputs_bus_flow_random_seed.sumocfg "
sumo_config_file = "4_2_section_simulation_outputs_bus_flow_random_seed.sumocfg"


edge_output_agg_300 = pd.DataFrame()
edge_output_agg_3600 = pd.DataFrame()

# Main loop

for seed in random_seeds:
    print(seed)
    gen_bus_flow.create_bus_xml(_file_path='./additional_files/bus/bus_flows_rand_seed.xml',
                                _sigma=0.23424849961615712, rnd_seed=seed)
    subprocess.run(run_sumo_no_gui, shell=True)

    # Reading the outputfiles at current random seed
    # reading bus only data aggregated for 1 hour as a csv
    xml2csv_bus_3600 = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
                          additional_files/edge_output/edge_route_busses_3600.xml -s , \
                      """
    subprocess.run(xml2csv_bus_3600, shell=True)
    edge_busses_3600_temp = pd.read_csv('additional_files/edge_output/edge_route_busses_3600.csv')

    # reading bus only data aggregated for 5 mins as a csv
    xml2csv_bus_300 = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
                          additional_files/edge_output/edge_route_busses_300.xml -s , \
                      """
    subprocess.run(xml2csv_bus_300, shell=True)
    edge_busses_300_temp = pd.read_csv('additional_files/edge_output/edge_route_busses_300.csv')

    # setting the seed
    edge_busses_300_temp['rand_seed'] = seed
    edge_busses_3600_temp['rand_seed'] = seed

    edge_output_agg_300 = edge_output_agg_300.append(edge_busses_300_temp)
    edge_output_agg_3600 = edge_output_agg_3600.append(edge_busses_3600_temp)


edge_output_agg_300.to_csv('additional_files/edge_output/bus_rand_seed_edge_output_agg_300.csv')
