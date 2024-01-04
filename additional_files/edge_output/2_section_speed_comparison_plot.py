# created by Thenuwan
# This script helps to compare bus speeds in BPL (proposed) sections

import pandas as pd
import os
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. xml to csv conversion

xml_2_csv_1 = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
               corridor_output_300_agg_bus_lane_test.xml -s , \
            """

xml_2_csv_2 = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
               corridor_output_300_agg_as_is.xml -s , \
            """

subprocess.run(xml_2_csv_1, shell=True)
subprocess.run(xml_2_csv_2, shell=True)

plt.rcParams["font.family"] = "Times New Roman"

# read the edge_data_output
with_bus_lane = pd.read_csv('corridor_output_300_agg_bus_lane_test.csv')
with_bus_lane['scenario'] = 'Bus lane'
no_bus_lane = pd.read_csv('corridor_output_300_agg_as_is.csv')
no_bus_lane['scenario'] = 'As is'

# preprocess bus related data
# add random seed column if required
with_bus_lane = with_bus_lane[['interval_begin', 'interval_end', 'interval_id', 'edge_speed','edge_timeLoss',
                                       'edge_waitingTime','scenario']]
no_bus_lane = no_bus_lane[['interval_begin', 'interval_end', 'interval_id', 'edge_speed','edge_timeLoss',
                                       'edge_waitingTime','scenario']]

scenarios = pd.concat([with_bus_lane, no_bus_lane])

### all sc

scenarios['speed_kmph'] = scenarios['edge_speed'] * 3.6
scenarios['section'] = scenarios['interval_id'].str.split(r'_probe|_bus|_general').str[0]
scenarios['veh_type'] = scenarios['interval_id'].str.split(r'lana_|tiya_').str[1]
print(scenarios.tail())

warm_up = 3600

conditions = [(scenarios['interval_begin'] < 1800 + warm_up),
              (scenarios['interval_begin'] >= 1800 + warm_up) & (
                      scenarios['interval_begin'] < 3600 + warm_up),
              (scenarios['interval_begin'] >= 3600 + warm_up) & (
                      scenarios['interval_begin'] < 5400 + warm_up),
              (scenarios['interval_begin'] >= 5400 + warm_up) & (
                      scenarios['interval_begin'] < 7200 + warm_up),
              (scenarios['interval_begin'] >= 7200 + warm_up) & (
                      scenarios['interval_begin'] < 9000 + warm_up),
              (scenarios['interval_begin'] >= 9000 + warm_up) & (
                      scenarios['interval_begin'] < 10800 + warm_up)]

# values = ['6.00-6.30am', '6.30-7.00am', '7.00-7.30am', '7.30-8.00am', '8:00-8:30', '8:30-9:00']
values = [1800+warm_up, 3600+warm_up, 5400+warm_up, 7200+warm_up, 9000+warm_up, 10800+warm_up]
scenarios['depart_period'] = np.select(conditions, values)
# edge_bus_probe_df.to_csv('test_2_19102022.csv')

bus_data = scenarios[(scenarios['veh_type'] == 'bus') | (scenarios['veh_type'] == 'probe')]

# Bus travel times and speeds at different sections
#
# bus_speed_summary = corridor_out.groupby('section')['speed_kmph'].mean()
# print(bus_speed_summary)

cross_rathmalana = bus_data[bus_data['section'] == 'cross_junction_ratmalana']
# cross_rathmalana_bus_groupby = cross_rathmalana.groupby(['rand_seed', 'depart_period']).mean().reset_index()

# print(cross_rathmalana_bus_groupby.mean())
savoy_colpity = bus_data[bus_data['section'] == 'wellawatta_kollupitiya']
# savoy_colpity_bus_groupby = savoy_colpity.groupby(['rand_seed', 'depart_period']).mean().reset_index()
# print("results---")
# print(savoy_colpity_bus_groupby['speed_kmph'].std())

xlim = np.arange(1800+warm_up, 12600+warm_up, 1800)
time_labels = ['06:30 a.m.', '07:00 a.m.', '07:30 a.m.', '08:00 a.m.', '08:30 a.m.', '09:00 a.m' ]

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False, figsize=(6, 4), constrained_layout=True)

sns.lineplot(data=cross_rathmalana, x='depart_period', y='edge_timeLoss', ax=axs[0],
             color='royalblue', hue='veh_type', style='scenario',
             ci=None, markers=False, dashes = True, hue_order = ['probe', 'bus'],
             style_order = ['Bus lane', 'As is'],markersize=10)
# sns.lineplot(data=cross_ground_truth, x='depart_period', y='bus_mean_speed', ax=axs[0], label='Ground Truth')
axs[0].set_xticks(xlim, labels=time_labels)


sns.lineplot(data=savoy_colpity, x='depart_period', y='edge_timeLoss', ax=axs[1],
             color='forestgreen', hue = 'veh_type', style='scenario',
             ci=None, markers=False, dashes = True,
             hue_order=['probe', 'bus'],
             style_order=['Bus lane', 'As is'], markersize=10)
axs[1].set_xticks(xlim, labels=time_labels)
# axs[].set_ylim(0, 35)
# axs.set_xlabel("Time", fontsize=10)
# axs.set_ylabel("Simulated Speed (kmph)", fontsize=10)
plt.legend(frameon=False)
plt.legend(fontsize=10)
plt.savefig('scenario_comparison_time_loss_test_14112022.svg', dpi=300)
plt.show()
