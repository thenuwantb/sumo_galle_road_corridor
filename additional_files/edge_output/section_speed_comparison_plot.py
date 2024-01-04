# created by Thenuwan
# This script helps to compare bus speeds in BPL (proposed) sections

import pandas as pd
import os
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Times New Roman"
# read the edge_data_output
edge_bus_probe_df = pd.read_csv('bus_rand_seed_edge_output_agg_300_19102022.csv')

# preprocess bus related data
edge_bus_probe_df = edge_bus_probe_df[['interval_begin', 'interval_end', 'interval_id', 'edge_speed', 'rand_seed']]
# edge_bus_probe_df = edge_bus_probe_df[
#     ~edge_bus_probe_df['interval_begin'].isin([0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400,
#                                                2700, 3000, 3300])]

edge_bus_probe_df['speed_kmph'] = edge_bus_probe_df['edge_speed'] * 3.6
edge_bus_probe_df['section'] = edge_bus_probe_df['interval_id'].str.split(r'_probe|_bus').str[0]
edge_bus_probe_df['veh_type'] = edge_bus_probe_df['interval_id'].str.split(r'lana_|tiya_').str[1]
# print(edge_bus_probe_df.tail())

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

# values = ['6.00-6.30am', '6.30-7.00am', '7.00-7.30am', '7.30-8.00am', '8:00-8:30', '8:30-9:00']
values = [1800+warm_up, 3600+warm_up, 5400+warm_up, 7200+warm_up, 9000+warm_up, 10800+warm_up]
edge_bus_probe_df['depart_period'] = np.select(conditions, values)
# edge_bus_probe_df.to_csv('test_2_19102022.csv')

bus_data = edge_bus_probe_df[edge_bus_probe_df['veh_type'] == 'bus']

# Bus travel times and speeds at different sections

bus_speed_summary = bus_data.groupby('section')['speed_kmph'].mean()
print(bus_speed_summary)

cross_rathmalana_bus = bus_data[bus_data['section'] == 'cross_junction_ratmalana']
cross_rathmalana_bus_groupby = cross_rathmalana_bus.groupby(['rand_seed', 'depart_period']).mean().reset_index()

# print(cross_rathmalana_bus_groupby.mean())
savoy_colpity_bus = bus_data[bus_data['section'] == 'wellawatta_kollupitiya']
savoy_colpity_bus_groupby = savoy_colpity_bus.groupby(['rand_seed', 'depart_period']).mean().reset_index()
print("results---")
print(savoy_colpity_bus_groupby['speed_kmph'].std())

xlim = np.arange(1800+warm_up, 12600+warm_up, 1800)
time_labels = ['06:30 a.m.', '07:00 a.m.', '07:30 a.m.', '08:00 a.m.', '08:30 a.m.', '09:00 a.m' ]

fig, axs = plt.subplots(nrows=1, ncols=1, sharex=False, figsize=(6, 2.5), constrained_layout=True)

sns.lineplot(data=cross_rathmalana_bus_groupby, x='depart_period', y='speed_kmph', ax=axs, label='Section 01',
             color='royalblue', marker='v')
# sns.lineplot(data=cross_ground_truth, x='depart_period', y='bus_mean_speed', ax=axs[0], label='Ground Truth')
axs.set_xticks(xlim, labels=time_labels)


sns.lineplot(data=savoy_colpity_bus_groupby, x='depart_period', y='speed_kmph', ax=axs, label='Section 02',
             color='forestgreen', marker='o')
axs.set_xticks(xlim, labels=time_labels)
axs.set_ylim(0, 35)
axs.set_xlabel("Time", fontsize=10)
axs.set_ylabel("Simulated Speed (kmph)", fontsize=10)
plt.legend(frameon=False)
plt.legend(fontsize=10)
# plt.savefig('bus_speed_variation.svg', dpi=300)
