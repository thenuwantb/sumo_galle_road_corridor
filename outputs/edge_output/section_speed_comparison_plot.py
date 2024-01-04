# created by Thenuwan
# This script helps to compare bus speeds in BPL (proposed) sections

import pandas as pd
import os
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# os.chdir('E:\\OneDrive\\SUMO\\Coding\\Coding\\bpm_shared_05102021\\2_real_network_simulations\\2_7_galle_road_6_10_simulator_warmup\\additional_files\\edge_output')
# Reading in Ground Truth Data
print(os.getcwd())

# cross_ground_truth = pd.read_csv(
#     'E:\\OneDrive\\SUMO\\Coding\\Coding\\bpm_shared_05102021\\2_real_network_simulations\\2_6_galle_road_6_10_6kmph_network\\ground_truth\\cross_ratmalana_30min_groud_truth.csv')
# savoy_ground_truth = pd.read_csv(
#     'E:\\OneDrive\\SUMO\\Coding\\Coding\\bpm_shared_05102021\\2_real_network_simulations\\2_6_galle_road_6_10_6kmph_network\\ground_truth\\savoy_kollupitiya_30min_groud_truth.csv')

# read the edge_data_output
edge_bus_probe_df = pd.read_csv('bus_rand_seed_edge_output_agg_3600_19102022.csv')

# preprocess bus related data
edge_bus_probe_df = edge_bus_probe_df[['interval_begin', 'interval_end', 'interval_id', 'edge_speed', 'rand_seed']]
# edge_bus_probe_df = edge_bus_probe_df[
#     ~edge_bus_probe_df['interval_begin'].isin([0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400,
#                                                2700, 3000, 3300])]

edge_bus_probe_df['speed_kmph'] = edge_bus_probe_df['edge_speed'] * 3.6
edge_bus_probe_df['section'] = edge_bus_probe_df['interval_id'].str.split(r'_probe|_bus').str[0]
edge_bus_probe_df['veh_type'] = edge_bus_probe_df['interval_id'].str.split(r'lana_|tiya_').str[1]
# print(edge_bus_probe_df.tail())

# preprocess all vehicle related data
# edge_all_df['speed_kmph'] = edge_all_df['edge_speed']*3.6
# edge_all_cro_rat = edge_all_df[edge_all_df['interval_id'] == 'cross_junction_ratmalana_all']
# edge_all_wel_kol = edge_all_df[edge_all_df['interval_id'] == 'wellawatta_kollupitiya_all']

# print(edge_bus_probe_df.head())
# print(edge_bus_probe_df.columns)
# print(edge_all_df.head())


# sns.catplot(x = 'interval_id', y='speed_kmph', kind='bar', data=edge_agg_df, row='section', col)
# plt.show()

# sns.barplot(x = 'interval_id', y='speed_kmph', hue='interval_begin', data=edge_agg_df)
# plt.show()

# sns.catplot(x = 'section', y='speed_kmph', kind='bar',hue='interval_begin',row='veh_type',data=edge_agg_df)
# plt.show()

warm_up = 3600

conditions = [(edge_bus_probe_df['interval_begin'] < 1800 + warm_up),
              (edge_bus_probe_df['interval_begin'] >= 1800 + warm_up) & (
                      edge_bus_probe_df['interval_begin'] < 3600 + warm_up),
              (edge_bus_probe_df['interval_begin'] >= 3600 + warm_up) & (
                      edge_bus_probe_df['interval_begin'] < 5400 + warm_up),
              (edge_bus_probe_df['interval_begin'] >= 5400 + warm_up) & (
                      edge_bus_probe_df['interval_begin'] < 7200 + warm_up),
              (edge_bus_probe_df['interval_begin'] >= 7200 + warm_up) & (
                      edge_bus_probe_df['interval_begin'] < 9000 + warm_up),
              (edge_bus_probe_df['interval_begin'] >= 9000 + warm_up) & (
                      edge_bus_probe_df['interval_begin'] < 10800 + warm_up)]

values = ['6.00-6.30am', '6.30-7.00am', '7.00-7.30am', '7.30-8.00am', '8:00-8:30', '8:30-9:00']
# values = [1800, 3600, 5400, 7200, 9000, 10800]
edge_bus_probe_df['depart_period'] = np.select(conditions, values)
edge_bus_probe_df.to_csv('test_2_19102022.csv')

bus_data = edge_bus_probe_df[edge_bus_probe_df['veh_type'] == 'bus']

# Bus travel times and speeds at different sections

bus_speed_summary = bus_data.groupby('section')['speed_kmph'].mean()
print(bus_speed_summary)

cross_rathmalana_bus = bus_data[bus_data['section'] == 'cross_junction_ratmalana']
savoy_colpity_bus = bus_data[bus_data['section'] == 'wellawatta_kollupitiya']

xlim = np.arange(1800, 12600, 1800)
time_labels = ['6:00 a.m.', '6:30 a.m.', '7:00 a.m.', '7:30 a.m.', '8:00 a.m.', '8:30 a.m.']

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False, figsize=(6, 8), constrained_layout=True)

# sns.lineplot(data=cross_rathmalana_bus, x='depart_period', y='speed_kmph', ax=axs[0], label='Simulated')
sns.lineplot(data=cross_ground_truth, x='depart_period', y='bus_mean_speed', ax=axs[0], label='Ground Truth')
axs[0].set_xticks(xlim, labels=time_labels)
axs[0].set_ylim(0, 40)
axs[0].set_title("Cross Junction to Rathmalana")

sns.lineplot(data=savoy_colpity_bus, x='depart_period', y='speed_kmph', ax=axs[1], label='Simulated')
# sns.lineplot(data=savoy_ground_truth, x='depart_period', y='bus_mean_speed', ax=axs[1], label='Ground Truth')
axs[1].set_xticks(xlim, labels=time_labels)
axs[1].set_ylim(0, 40)
axs[1].set_title("Wellawatta to Kollupitiya")

plt.show()
# plt.savefig('simulated_observed_test_29082022.svg')

# xlim = np.arange(0, 10800, 1800)
# time_labels = ['6:00 a.m.', '6:30 a.m.', '7:00 a.m.', '7:30 a.m.', '8:00 a.m.', '8:30 a.m.']
# g1 = sns.relplot(data=edge_bus_probe_df, x='interval_begin', y='speed_kmph', kind='line', row='section', col='veh_type')
#
# for ax in g1.axes.flat:
#     ax.set_xticks(ticks=xlim)
#     ax.set_xticklabels(labels=time_labels)
#
# plt.show()

# sns.catplot(data=edge_bus_probe_df, x='interval_begin', y='speed_kmph', kind='bar', row='section', col='veh_type')
# plt.show()

# fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
# (ax1, ax2), (ax3, ax4) = axs
# sns.scatterplot(x='edge_density', y='speed_kmph', hue= 'interval_id', data=edge_all_df, ax=ax1)
# sns.scatterplot(x='edge_left', y='speed_kmph', hue= 'interval_id', data=edge_all_df, ax=ax2)
# sns.scatterplot(x='edge_density', y='edge_left', hue= 'interval_id', data=edge_all_df, ax=ax3)
# plt.show()
