import subprocess
import os
from xml.etree import ElementTree as et

import pandas as pd

os.chdir("E:\\OneDrive\\SUMO\\Coding\\Coding\\bpm_shared_05102021\\2_real_network_simulations\\2_2_galle_road_routeSampler_6_to_10")


implausible_score_df = pd.read_xml("implausible_routes\imp_routes_output.xml")
print("Distribution before removal")
print(implausible_score_df['score'].describe())
removing_routes_df = implausible_score_df[implausible_score_df['score'] > 4.15] # 4.15 is the threshold
print(removing_routes_df.tail())
print("Distribution after removal")
print(implausible_score_df[implausible_score_df['score'] <= 4.15]['score'].describe())
route_list_to_remove = removing_routes_df['id'].to_list()
