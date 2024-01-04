# created by Thenuwan
# This script helps to compare bus speeds in BPL (proposed) sections

import pandas as pd
import os
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt

# read the edge_data_output

xml_2_csv_bus = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
               edge_route_busses_3600.xml -s , \
            """
xml_2_csv_all = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
               edge_FD_output.xml -s , \
            """

subprocess.run(xml_2_csv_bus, shell=True)
subprocess.run(xml_2_csv_all, shell=True)

edge_bus_probe_df = pd.read_csv('edge_route_busses_3600.csv')
edge_all_df = pd.read_csv('edge_FD_output.csv')

# preprocess bus related data
edge_bus_probe_df = edge_bus_probe_df[['interval_begin', 'interval_end', 'interval_id', 'edge_speed']]
edge_bus_probe_df['speed_kmph'] = edge_bus_probe_df['edge_speed'] * 3.6
edge_bus_probe_df['section'] = edge_bus_probe_df['interval_id'].str.split(r'_probe|_bus').str[0]
edge_bus_probe_df['veh_type'] = edge_bus_probe_df['interval_id'].str.split(r'lana_|tiya_').str[1]

# preprocess all vehicle related data
edge_all_df['speed_kmph'] = edge_all_df['edge_speed']*3.6
edge_all_cro_rat = edge_all_df[edge_all_df['interval_id'] == 'cross_junction_ratmalana_all']
edge_all_wel_kol = edge_all_df[edge_all_df['interval_id'] == 'wellawatta_kollupitiya_all']

# print(edge_bus_probe_df.head())
# print(edge_bus_probe_df.columns)
print(edge_all_df.head())



# sns.catplot(x = 'interval_id', y='speed_kmph', kind='bar', data=edge_agg_df, row='section', col)
# plt.show()

# sns.barplot(x = 'interval_id', y='speed_kmph', hue='interval_begin', data=edge_agg_df)
# plt.show()

# sns.catplot(x = 'section', y='speed_kmph', kind='bar',hue='interval_begin',row='veh_type',data=edge_agg_df)
# plt.show()


# sns.relplot(data=edge_bus_probe_df, x='interval_begin', y='speed_kmph', kind='line', row='section', col='veh_type')
# plt.show()

sns.catplot(data=edge_bus_probe_df, x='interval_begin', y='speed_kmph', kind='bar', row='section', col='veh_type')
plt.show()

# fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
# (ax1, ax2), (ax3, ax4) = axs
# sns.scatterplot(x='edge_density', y='speed_kmph', hue= 'interval_id', data=edge_all_df, ax=ax1)
# sns.scatterplot(x='edge_left', y='speed_kmph', hue= 'interval_id', data=edge_all_df, ax=ax2)
# sns.scatterplot(x='edge_density', y='edge_left', hue= 'interval_id', data=edge_all_df, ax=ax3)
# plt.show()