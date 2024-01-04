import subprocess
from xml.etree import ElementTree as et
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

random_seeds = np.random.randint(10000, 99999, 30).tolist()

run_sumo_no_gui = "sumo -c 4_1_section_simulation_outputs.sumocfg "
sumo_config_file = "4_1_section_simulation_outputs.sumocfg"

tree = et.parse(sumo_config_file)
root = tree.getroot()
random_num_tag = root.find("./random_number/seed")

edge_output_agg_300 = pd.DataFrame()
edge_output_agg_3600 = pd.DataFrame()

#### Main loop

for seed in random_seeds:
    print(seed)
    random_num_tag.attrib["value"] = str(seed)
    tree.write('config_temp.sumocfg')

    run_sumo = "sumo -c config_temp.sumocfg "
    subprocess.run(run_sumo, shell=True)

    # Reading the outputfiles at current random seed
    ### reading bus only data aggregated for 1 hour as a csv
    xml2csv_bus_3600 = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
                          additional_files/edge_output/edge_route_busses_3600.xml -s , \
                      """
    subprocess.run(xml2csv_bus_3600, shell=True)
    edge_busses_3600_temp = pd.read_csv('additional_files/edge_output/edge_route_busses_3600.csv')

    ### reading bus only data aggregated for 5 mins as a csv
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


edge_output_agg_300.to_csv('outputs/edge_output/edge_output_agg_300.csv')
edge_output_agg_3600.to_csv('outputs/edge_output/edge_output_agg_3600.csv')
