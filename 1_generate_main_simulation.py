# Import necessary modules
import subprocess
import os
from xml.etree import ElementTree as et
import yaml
import pandas as pd

# Read the configuration file to retrieve settings
with open("_config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Change the current working directory based on the folder_path specified in the configuration
os.chdir(config['folder_path'])

# 1. Random trips call
random_trips_call = "randomTrips.py " \
                    "--net-file network/colombo_galleroad_edges_renamed_60kmph_01082022.net.xml " \
                    "--end 7200 " \
                    "--fringe-factor 40 " \
                    "--min-distance 250 " \
                    "--max-distance 2750 " \
                    "--period 0.2 " \
                    "--lanes " \
                    "--seed 12345 " \
                    "--speed-exponent 2.75 " \
                    "--route-file intermediate_outputs/1_random_trips_routes.rou.xml " \
                    "--trip-attributes=\" departLane=\"'best'\" \"departSpeed=\"'max'\"  " \
                    "--remove-loops "

subprocess.run(random_trips_call, shell=True)

# 2. Cleaning the routes
get_implausible_routes = """python "%SUMO_HOME%\\tools\\route\\implausibleRoutes.py "\
            network/colombo_galleroad_edges_renamed_60kmph_01082022.net.xml \
            intermediate_outputs/1_random_trips_routes.rou.xml \
            --verbose \
            --threshold 0.0 \
            --min-dist 100.0 \
            --min-air-dist 50 \
            --xml-output implausible_routes/imp_routes_output.xml \
            """

subprocess.run(get_implausible_routes, shell=True)

implausible_score_df = pd.read_xml("implausible_routes\imp_routes_output.xml")
print("Distribution before removal")
print(implausible_score_df['score'].describe())
print(type(implausible_score_df['score'][0]))
removing_routes_df = implausible_score_df[implausible_score_df['score'] > 100.0]  # 4.15 is the threshold
print("Distribution after removal")
print(removing_routes_df['score'].describe())
route_list_to_remove = removing_routes_df['id'].to_list()

# load current route xml
current_route_whitelist_tree = et.parse(r"intermediate_outputs\1_random_trips_routes.rou.xml")
current_route_whitelist_root = current_route_whitelist_tree.getroot()
all_routes = current_route_whitelist_root.findall("./vehicle")

before_list = []
removed_list = []

for child in current_route_whitelist_root:
    before_list.append(child.attrib['id'])

    if int(child.attrib['id']) in route_list_to_remove:
        removed_list.append(child.attrib['id'])
        current_route_whitelist_root.remove(child)
        route_list_to_remove.remove(int(child.attrib['id']))

print("Routes before Clean: ", len(before_list))
print("Routes removed: ", len(removed_list))
print("Routes exists: ", len(before_list) - len(removed_list))

current_route_whitelist_tree.write(r'intermediate_outputs\2_route_whitelist.rou.xml')

# 3. Route sampler call
route_sampler_call = "routeSampler.py " \
                     "--route-files intermediate_outputs/2_route_whitelist.rou.xml " \
                     "--turn-files inputs/turn_counts/turn_counts_v6_warmup_counts_added.xml " \
                     "--min-count 1 " \
                     "--verbose " \
                     "--output-file demand/route_sampler_calibrated.rou.xml " \
                     "--attributes=\"type=\"'typedist1'\" departLane=\"'free'\" \"departSpeed=\"'max'\" "
subprocess.run(route_sampler_call, shell=True)

# 4. Run SUMO

run_sumo_no_gui = "sumo -c 4_1_section_simulation_outputs.sumocfg " \
                  "--tripinfo-output outputs/ti_09092022.xml "

# If you want to run SUMO with no-gui, uncomment and run below
# subprocess.run(run_sumo_no_gui, shell=True)
