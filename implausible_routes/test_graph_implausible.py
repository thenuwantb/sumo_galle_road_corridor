import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

os.chdir(
    'E:\\OneDrive\\SUMO\\Coding\\Coding\\bpm_shared_05102021\\2_real_network_simulations\\2_2_galle_road_routeSampler_6_to_10\\implausible_routes')

test_data = pd.read_xml('imp_routes_test_03022022.xml')
# print(test_data.tail())
# #
# sns.boxplot(data=test_data, x='score')
# plt.show()

print(test_data['score'].describe())
print(test_data['score'].quantile(0.9))

print(sum(test_data['score'] >= 8.43875))
print(sum(test_data['score'] <= 8.43875))

# plot
test_data[test_data['score'] < 2.159178]['score'].hist()
plt.show()
