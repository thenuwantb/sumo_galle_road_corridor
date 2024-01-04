import pandas as pd
import os
from xml.etree import ElementTree as et

os.chdir('E:\\OneDrive\\SUMO\\Coding\\Coding\\bpm_shared_05102021\\2_real_network_simulations\\2_2_galle_road_routeSampler_6_to_10\\implausible_routes')

grt_5000_df = pd.read_xml('imp_routes_grt_5000.xml')
print(grt_5000_df.head())

route_list_to_remove = grt_5000_df['id'].to_list()
print("routes to be removed", len(route_list_to_remove))
print(type(route_list_to_remove[0]))

# load current route xml
current_route_whitelist_tree = et.parse(r"E:\OneDrive\SUMO\Coding\Coding\bpm_shared_05102021\2_real_network_simulations\2_2_galle_road_routeSampler_6_to_10\intermediate_outputs\1_1_random_trips_routes_29122021.rou.xml")
current_route_whitelist_root = current_route_whitelist_tree.getroot()
all_routes = current_route_whitelist_root.findall("./vehicle")
print(all_routes[0].attrib)
# grt_5000_df.to_xml('test_out.xml')

before_list = []
after_list = []

for child in current_route_whitelist_root:
    # print(child.attrib['id'])
    before_list.append(child.attrib['id'])
    if int(child.attrib['id']) in route_list_to_remove:
        after_list.append(child.attrib['id'])
        # print('entered')
        # print(child.attrib['id'])
        current_route_whitelist_root.remove(child)
        route_list_to_remove.remove(int(child.attrib['id']))




current_route_whitelist_tree.write('implausible_removed_26012022.xml')
print(len(before_list))
print(len(after_list))




# tree = et.parse('imp_routes_grt_5000.xml')
# root = tree.getroot()
#
# all_routes = root.findall("./route")
# print(type(all_routes))
# print(all_routes[0].attrib)

# for child in root:
#     # print(child.attrib)
#     if child.attrib['id'] == '15222':
#         root.remove(child)

# tree.write('15222_removed.xml')

# this works. Now the next step is to get all the routes to be deleted as a list
# load the route whitelist file
# use the above method to delete them
# source : https://stackoverflow.com/questions/6847263/search-and-remove-element-with-elementtree-in-python



# print(type(tree))
# root = tree.getroot()
# print(root)

