import random

import pandas as pd
import numpy as np
from random import *

# Values to be used for busses
MAX_SPEED_SHORT_DISTANCE = "9.72"
MAX_SPEED_LONG_DISTANCE = "12.5"
bus_max_speed_other = "12.5"
SIGMA = "0.7"
test_dict = {"Sigma": 0.7}

def create_bus_route_df(random_seed):
    seed(random_seed)

    # stops
    stops = ["01_cross_junction", "02_mendis_tower", "03_rawatawatta", "04_lakshapathiya", "05_commercial_bank_rw",
             "06_katubedda_junc", "07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
             "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc", "15_dhramarama_temp",
             "16_mount_lavinia_police", "17_ratmalana_depot", "18_mount_lavinia_junc", "19_mount_lavinia_court",
             "20_hotel_road", "21_odeon_cinema", "22_dehiwala_junc", "23_waydya_rd", "24_william_junc",
             "25_roxi_cinema",
             "26_wellawatta_arpico", "27_wellawatta_police", "28_wellawatta_mosque", "29_savoy_cinema", "30_st_peters",
             "31_bambalapitiya_flats", "32_milagiriya", "33_majestic_city", "34_cagills_bank", "35_marino_mall",
             "36_vogue_jewel", "37_pan_asia", "38_kollupitiya_junc"]

    stops_long_distance = ["01_cross_junction", "03_rawatawatta",
                           "05_commercial_bank_rw",
                           "06_katubedda_junc", "08_german_tec", "10_golumadama",
                           "12_belek_kade", "14_maliban_junc",
                           "16_mount_lavinia_police", "17_ratmalana_depot", "18_mount_lavinia_junc",
                           "22_dehiwala_junc", "24_william_junc",
                           "27_wellawatta_police", "28_wellawatta_mosque", "29_savoy_cinema",
                           "32_milagiriya", "33_majestic_city", "34_cagills_bank",
                           "35_marino_mall",
                           "36_vogue_jewel", "37_pan_asia", "38_kollupitiya_junc"]

    other_bus_stops = ["06_katubedda_junc", "09_soyza_flat", "14_maliban_junc", "18_mount_lavinia_junc",
                       "22_dehiwala_junc", "24_william_junc", "27_wellawatta_police",
                       "30_st_peters", "32_milagiriya", "33_majestic_city", "34_cagills_bank",
                       "35_marino_mall", "36_vogue_jewel", "37_pan_asia", "38_kollupitiya_junc"]

    stops_255 = ["07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
                 "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc", "15_dhramarama_temp",
                 "16_mount_lavinia_police", "17_ratmalana_depot"]

    stops_183 = ["01_cross_junction", "02_mendis_tower", "03_rawatawatta", "04_lakshapathiya", "05_commercial_bank_rw",
                 "06_katubedda_junc", "07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
                 "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc", "15_dhramarama_temp",
                 "16_mount_lavinia_police", "17_ratmalana_depot", "18_mount_lavinia_junc", "19_mount_lavinia_court",
                 "20_hotel_road", "21_odeon_cinema", "22_dehiwala_junc", "23_waydya_rd", "24_william_junc"]

    stops_154 = ["08_german_tec", "09_soyza_flat", "10_golumadama",
                 "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc", "15_dhramarama_temp",
                 "16_mount_lavinia_police", "17_ratmalana_depot", "18_mount_lavinia_junc", "19_mount_lavinia_court",
                 "20_hotel_road", "21_odeon_cinema", "22_dehiwala_junc", "23_waydya_rd", "24_william_junc",
                 "25_roxi_cinema",
                 "26_wellawatta_arpico", "27_wellawatta_police", "28_wellawatta_mosque", "29_savoy_cinema",
                 "30_st_peters",
                 "31_bambalapitiya_flats", "32_milagiriya", "33_majestic_city", "34_cagills_bank"]

    stops_192 = ["01_cross_junction", "02_mendis_tower", "03_rawatawatta", "04_lakshapathiya", "05_commercial_bank_rw",
                 "06_katubedda_junc", "07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
                 "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall"]

    # main dataframe that holds information about all bus flows
    all_bus_route_df = pd.DataFrame(columns=['trip_id', 'depart'])

    route_100 = {"route": "bus_100", "headways": [180, 150, 150], "bus_type": "short_distance",
                 "start_edge": "112446385#5", "end_edge": "455043449",
                 "start_time": 3600, "end_time": 18000, "bus_stops": stops}

    route_101 = {"route": "bus_101", "headways": [300, 360, 360], "bus_type": "short_distance",
                 "start_edge": "51086283#3", "end_edge": "194099559#0",
                 "start_time": 3900, "end_time": 18000, "bus_stops": stops}

    route_255 = {"route": "bus_255", "headways": [900, 900, 900], "bus_type": "short_distance",
                 "start_edge": "gneE5", "end_edge": "15242148#0",
                 "start_time": 4200, "end_time": 18000, "bus_stops": stops_255}

    route_183 = {"route": "bus_183", "headways": [800, 600, 600], "bus_type": "short_distance",
                 "start_edge": "51086283#3", "end_edge": "23323086",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_183}

    route_154 = {"route": "bus_154", "headways": [900, 1200, 1200], "bus_type": "short_distance",
                 "start_edge": "376601738#2", "end_edge": "18598988",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_154}

    route_155 = {"route": "bus_154", "headways": [1800, 1800, 900], "bus_type": "short_distance",
                 "start_edge": "376601738#2", "end_edge": "18598988",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_154}

    route_192 = {"route": "bus_192", "headways": [1200, 480, 600], "bus_type": "short_distance",
                 "start_edge": "112446385#5", "end_edge": "19811337#1",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_192}

    route_400 = {"route": "bus_400", "headways": [600, 360, 360], "bus_type": "long_distance",
                 "start_edge": "112446385#5", "end_edge": "455043449",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_400_1 = {"route": "bus_400/1", "headways": [900, 900, 900], "bus_type": "long_distance",
                   "start_edge": "112446385#5", "end_edge": "455043449",
                   "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_401 = {"route": "bus_401", "headways": [3600, 3600, 1200], "bus_type": "long_distance",
                 "start_edge": "112446385#5", "end_edge": "455043449",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_430 = {"route": "bus_430", "headways": [720, 400, 300], "bus_type": "long_distance",
                 "start_edge": "112446385#5", "end_edge": "455043449",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_433_s = {"route": "bus_433_s", "headways": [1800, 1200, 900], "bus_type": "long_distance",
                   "start_edge": "112446385#5", "end_edge": "455043449",
                   "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_434 = {"route": "bus_434", "headways": [3600, 3600, 3600], "bus_type": "long_distance",
                 "start_edge": "112446385#5", "end_edge": "455043449",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_437 = {"route": "bus_437", "headways": [3600, 3600], "bus_type": "long_distance",
                 "start_edge": "112446385#5", "end_edge": "455043449",
                 "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_02 = {"route": "bus_02", "headways": [720, 360, 300], "bus_type": "long_distance",
                "start_edge": "112446385#5", "end_edge": "455043449",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    # changed based on the bus count made from the video - Jeberson
    route_17 = {"route": "bus_17", "headways": [1800, 1800, 1800], "bus_type": "long_distance",
                "start_edge": "51086283#3", "end_edge": "155990909#1",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_183}

    route_24 = {"route": "bus_24", "headways": [3600, 1800, 1800], "bus_type": "long_distance",
                "start_edge": "112446385#5", "end_edge": "455043449",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance}

    route_26 = {"route": "bus_26", "headways": [1800, 3600], "bus_type": "long_distance",
                "start_edge": "112446385#5", "end_edge": "455043449",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance,
                "route_name": "Hakmana-Colombo"}

    route_32 = {"route": "bus_32", "headways": [720, 3600, 900], "bus_type": "long_distance",
                "start_edge": "112446385#5", "end_edge": "455043449",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance,
                "route_name": "Kataragama-Colombo"}

    route_42 = {"route": "bus_42", "headways": [1800, 1800, 1800], "bus_type": "long_distance",
                "start_edge": "112446385#5", "end_edge": "455043449",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance,
                "route_name": "Udugama-Colombo"}

    route_60 = {"route": "bus_60", "headways": [2400], "bus_type": "long_distance",
                "start_edge": "112446385#5", "end_edge": "455043449",
                "start_time": 4500, "end_time": 18000, "bus_stops": stops_long_distance,
                "route_name": "Deniyaya-Colombo"}

    other_busses = {"route": "other_bus", "headways": [180, 90, 360], "bus_type": "long_distance",
                    "start_edge": "112446385#5", "end_edge": "455043449",
                    "start_time": 4500, "end_time": 18000, "bus_stops": other_bus_stops,
                    "route_name": "Other-(office, school)"}

    all_routes = {"route_100": route_100,
                  "route_101": route_101,
                  "route_255": route_255,
                  "route_183": route_183,
                  "route_154": route_154,
                  "route_155": route_155,
                  "route_192": route_192,
                  "route_400": route_400,
                  "route_401": route_401,
                  "route_400/1": route_400_1,
                  "route_430": route_430,
                  "route_433_s": route_433_s,
                  "route_437": route_437,
                  "route_434": route_434,
                  "route_02": route_02,
                  "route_17": route_17,
                  "route_24": route_24,
                  "route_26": route_26,
                  "route_32": route_32,
                  "route_42": route_42,
                  "route_60": route_60,
                  "other_bus": other_busses}

    # loop over the routes and create a dataframe

    for route in all_routes.values():
        start_times = [3600, 7200, 10800]
        end_times = [7199, 10799, 14399]

        route_depart_all = []
        route_veh_id_all = []

        for i, headway in enumerate(route["headways"]):
            rand_num = randint(0, 100)
            route_depart = np.arange(start=start_times[i] + rand_num, stop=end_times[i],
                                     step=headway).tolist()
            # print(route_depart)
            route_depart_all.extend(route_depart)

            route_veh_id = list(map(lambda dep_time: route["route"] + "_" + str(dep_time), route_depart))
            route_veh_id_all.extend(route_veh_id)

        route_df = pd.DataFrame(list(zip(route_veh_id_all, route_depart_all)), columns=['trip_id', 'depart'])
        route_df['bus_type'] = route["bus_type"]
        route_df['start_edge'] = route['start_edge']
        route_df['end_edge'] = route['end_edge']
        route_df["bus_stops"] = [route["bus_stops"] for i in route_df.index]

        all_bus_route_df = all_bus_route_df.append(route_df)

    # Sorting the data frame so that the vehicles can be inserted in to the simulation orderly
    all_bus_route_df.sort_values(by="depart", ascending=True, inplace=True)

    return all_bus_route_df


# Define a stopping time distribution
def stopping_duration(type_of_bus, list_long_dist, list_short_dist, rand_seed):
    seed(rand_seed)
    rand_int = np.random.randint(0, 99)
    if type_of_bus == "short_distance":
        return list_short_dist[rand_int]

    elif type_of_bus == "long_distance":
        return list_long_dist[rand_int]
    elif type_of_bus == "other":
        return "0"


def create_random_stop_times(rndm_seed):
    rng = np.random.RandomState(rndm_seed)
    seed(rndm_seed)

    _ld_mean = 15
    _ld_std = 5
    _sd_mean = 25
    _sd_std = 10

    _ld_stop_time = rng.normal(_ld_mean, _ld_std, 100).tolist()
    _sd_stop_time = rng.normal(_sd_mean, _sd_std, 100).tolist()

    _ld_stop_time_format = [0 if x < 0 else x for x in _ld_stop_time]
    _sd_stop_time_format = [0 if x < 0 else x for x in _sd_stop_time]

    _ld_stop_time_format = ['%.0f' % elem for elem in _ld_stop_time_format]
    _sd_stop_time_format = ['%.0f' % elem for elem in _sd_stop_time_format]

    return _ld_stop_time_format, _sd_stop_time_format


def create_bus_xml(_file_path, _sigma, rnd_seed=55):
    short_distance_max_speed = "9.72"
    long_distance_max_speed = "12.5"

    seed(rnd_seed)

    all_bus_routes_df = create_bus_route_df(rnd_seed)

    with open(_file_path, 'w') as fh_1:
        fh_1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh_1.write(
            '<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n')
        fh_1.write('\n')

        # short distance bus type
        fh_1.write(
            '\t<vType id="short_distance" vClass="bus" accel="2.6" decel="4.5" sigma="{}" length="12" minGap="3" '
            'maxSpeed="{}" color="red" '
            'guiShape="bus"/>\n'.format(_sigma, short_distance_max_speed))

        # long distance bus type
        fh_1.write(
            '\t<vType id="long_distance" vClass="bus" accel="2.6" decel="4.5" sigma="{}" length="12" minGap="3" '
            'maxSpeed="{}" color="red" '
            'guiShape="bus"/>\n'.format(_sigma, long_distance_max_speed))

        # writing xml lines
        for _, _row in all_bus_routes_df.iterrows():
            _trip_id = _row['trip_id']
            _bus_type = _row['bus_type']
            _vehicle_depart = _row['depart']
            _start_edge = _row['start_edge']
            _end_edge = _row['end_edge']
            _bus_stops = _row['bus_stops']

            fh_1.write('\t<trip id="{}" type="{}" depart="{}" from="{}" to="{}">\n'.format(
                _trip_id, _bus_type, _vehicle_depart, _start_edge, _end_edge))

            _ld_stop_time_format, _sd_stop_time_format = create_random_stop_times(rnd_seed)

            for _stop_time_id, _stop in enumerate(_bus_stops):
                if _bus_type == "short_distance":
                    _stop_duration = _sd_stop_time_format[_stop_time_id]
                    fh_1.write('\t\t<stop busStop="{}" duration="{}"/>\n'.format(_stop, _stop_duration))

                elif _bus_type == "long_distance":
                    _stop_duration = _ld_stop_time_format[_stop_time_id]
                    fh_1.write('\t\t<stop busStop="{}" duration="{}"/>\n'.format(_stop, _stop_duration))

            fh_1.write('\t</trip>\n')
        fh_1.write('</additional>\n')
        fh_1.close()


def create_bus_xml_test_network(_file_path, _sigma, rnd_seed=55):
    short_distance_max_speed = "9.72"
    long_distance_max_speed = "12.5"

    seed(rnd_seed)

    all_bus_routes_df = create_bus_route_df(rnd_seed)

    with open(_file_path, 'w') as fh_1:
        fh_1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh_1.write(
            '<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n')
        fh_1.write('\n')

        # short distance bus type
        fh_1.write(
            '\t<vType id="short_distance" vClass="bus" accel="2.6" decel="4.5" sigma="{}" length="12" minGap="3" '
            'maxSpeed="{}" color="red" '
            'guiShape="bus"/>\n'.format(_sigma, short_distance_max_speed))

        # long distance bus type
        fh_1.write(
            '\t<vType id="long_distance" vClass="bus" accel="2.6" decel="4.5" sigma="{}" length="12" minGap="3" '
            'maxSpeed="{}" color="red" '
            'guiShape="bus"/>\n'.format(_sigma, long_distance_max_speed))

        # writing xml lines
        for _, _row in all_bus_routes_df.iterrows():
            _trip_id = _row['trip_id']
            _bus_type = _row['bus_type']
            _vehicle_depart = _row['depart']
            _start_edge = _row['start_edge']
            _end_edge = _row['end_edge']
            _bus_stops = _row['bus_stops']

            fh_1.write('\t<trip id="{}" type="{}" depart="{}" from="{}" to="{}">\n'.format(
                _trip_id, _bus_type, _vehicle_depart, _start_edge, _end_edge))

            _ld_stop_time_format, _sd_stop_time_format = create_random_stop_times(rnd_seed)

            for _stop_time_id, _stop in enumerate(_bus_stops):
                if _bus_type == "short_distance":
                    _stop_duration = _sd_stop_time_format[_stop_time_id]
                    fh_1.write('\t\t<stop busStop="{}" duration="{}"/>\n'.format(_stop, _stop_duration))

                elif _bus_type == "long_distance":
                    _stop_duration = _ld_stop_time_format[_stop_time_id]
                    fh_1.write('\t\t<stop busStop="{}" duration="{}"/>\n'.format(_stop, _stop_duration))

            fh_1.write('\t</trip>\n')
        fh_1.write('</additional>\n')
        fh_1.close()
