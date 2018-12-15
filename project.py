from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
import csv
import requests
import urllib2

# --------- RETRIEVING DATA --------- #

# get API key from MTA
api_key = 'api_key'

# data for BDFM lines
# feed_BDFM = gtfs_realtime_pb2.FeedMessage()
# response_BDFM = requests.get('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=21')
# feed_BDFM.ParseFromString(response_BDFM.content)
# dict_BDFM = protobuf_to_dict(feed_BDFM)

# data for NQRW lines
# feed_NQRW = gtfs_realtime_pb2.FeedMessage()
# response_NQRW = requests.get('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=16')
# feed_NQRW.ParseFromString(response_NQRW.content)
# dict_NQRW = protobuf_to_dict(feed_NQRW)

# routes data - DONE
# route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color
# H = S line
routes_file = open('mta-data/routes.txt', 'r')
routes = routes_file.read()
routes_file.close()
# print routes

# station stops data - DONE
# stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station
stops_file = open('mta-data/stops.txt', 'r')
stops = stops_file.read()
stops_file.close()

# stop_times data
# trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled
stop_times_file = open('mta-data/stop_times.txt', 'r') # !!!!!!!!!!!!!!!!!!! remember to change this to not be the shorter, test file
stop_times = stop_times_file.read()
stop_times_file.close()

# trips data
# route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id
trips_file = open('mta-data/trips.txt', 'r')
trips = trips_file.read()
trips_file.close()

# station locations data
# Station ID,Complex ID,GTFS Stop ID,Division,Line,Stop Name,Borough,Daytime Routes,Structure,GTFS Latitude,GTFS Longitude
# csv_url = 'http://web.mta.info/developers/data/nyct/subway/Stations.csv'
# response = urllib2.urlopen(csv_url)
# cr = csv.reader(response)
# locations_file = []
# for row in cr:
#     locations_file.append(row)

# --------- RETRIEVING DATA (END) --------- #



# --------- ORGANIZING DATA --------- #
# NEED:
# - subway letter
# - station name
# - time enter/leave station

# preps the data to be parsed through after we get them from the txt files
def prep_data(data, idx1, idx2, isValList):
    new_data = data.split("\n")[1:-1]
    data_len = len(new_data)

    for idx in range(data_len):
        new_data[idx] = new_data[idx].split(",")

    my_keys = map(lambda x: x[idx1], new_data)
    my_values = map(lambda x: x[idx2], new_data)

    ret_dict = {}
    if isValList:
        for idx in range(data_len):
            if my_keys[idx] in ret_dict.keys():
                ret_dict[my_keys[idx]].append(my_values[idx])
            else:
                ret_dict[my_keys[idx]] = [my_values[idx]]
    else:
        for idx in range(data_len):
            ret_dict[my_keys[idx]] = my_values[idx]

    return ret_dict


# uses stops.txt
def generate_stopsNameToID(data): # --------- FIX BC SOME NAMES ARE DIFF BUT SAME STOP --------
    return prep_data(data, 2, 0, True)

    # new_data = data.split("\n")[1:-1]
    # data_len = len(new_data)
    #
    # for idx in range(data_len):
    #     new_data[idx] = new_data[idx].split(",")
    # stops_id = map(lambda x: x[0], new_data)
    # stops_name = map(lambda x: x[2], new_data)
    #
    # ret_dict = {}
    # for idx in range(data_len):
    #     ret_dict[stops_name[idx]] = stops_id[idx]
    # return ret_dict

# {trainLetter: [{stationName : (time enter, time leave)}, {stationName : (time enter, time leave)}], trainLetter: [{stationName : (time enter, time leave)}]}


# for entity in feed_BDFM.entity:
#     if entity.hasField('trip_update'):
#         print entity.trip_update.trip.

# uses routes.txt
def generate_linesToTrains(data):
    new_data = data.split("\n")[1:-1]
    ret_dict = {}
    for line in new_data:
        line = line.split(",")

        line_fixed = line[3].replace(" Local", "").replace(" Express", "") # combine the local and express lines
        # some line name formats not centralized
        if "6 Av" in line_fixed or "6th AVE" in line_fixed:
            line_fixed = "6 Avenue"
        if "7 Avenue" in line_fixed:
            line_fixed = "7 Avenue"

        if line_fixed not in ret_dict.keys():
            ret_dict[line_fixed] = [line[0]]
        else:
            ret_dict[line_fixed].append(line[0])

    return ret_dict

# uses trips.txt
def generate_tripIDtoTrain(data): # TODO CHECK IF THIS IS REALLY JUST A ONE-TO-ONE RELATIONSHIP
    return prep_data(data, 2, 0, False)

    # new_data = data.split("\n")[1:-1]
    # data_len = len(new_data)
    #
    # for idx in range(data_len):
    #     new_data[idx] = new_data[idx].split(",")
    #
    # trip_id = map(lambda x: x[2], new_data)
    # train = map(lambda x: x[0], new_data)
    #
    # ret_dict = {}
    # for idx in range(data_len):
    #     ret_dict[trip_id[idx]] = train[idx]
    #
    # return ret_dict

# uses stop_times.txt
def generate_tripIDtoStops(data):
    return prep_data(data, 0, 3, True)

    # new_data = data.split("\n")[1:-1]
    # data_len = len(new_data)
    #
    # for idx in range(data_len):
    #     new_data[idx] = new_data[idx].split(",")
    #
    # trip_id = map(lambda x: x[0], new_data)
    # stop_id = map(lambda x: x[3], new_data)
    #
    # ret_dict = {}
    # for idx in range(data_len):
    #     if trip_id[idx] in ret_dict.keys():
    #         ret_dict[trip_id[idx]].append(stop_id[idx])
    #     else:
    #         ret_dict[trip_id[idx]] = [stop_id[idx]]
    #
    # return ret_dict


def generate_trainsToStops(trip2train, trip2stops): # TODO: does N/S stops matter bc trains will go both ways anyways? or maybe take into account the construction changes?
    trips = trip2train.keys() # doesn't matter which you get from bc they are the same trip_id's
    ret_dict = {}
    for trip in trips:
        ret_dict[trip2train[trip]] = trip2stops[trip]
    return ret_dict

# --------- ORGANIZING DATA (END) --------- #



# --------- DATA TO USE --------- #

stops_name_to_id = generate_stopsNameToID(stops) # mapping from stop_name (string) -> stop_id(s) (list of strings)

lines_to_trains = generate_linesToTrains(routes) # mapping from line names (string) -> trains (list of strings)

tripID_to_train = generate_tripIDtoTrain(trips) # mapping from trip_id (string) -> train (string)
tripID_to_stops = generate_tripIDtoStops(stop_times) # mapping from trip_id (string) -> stops (list of strings)
trains_to_stops = generate_trainsToStops(tripID_to_train, tripID_to_stops) # mapping from trains (string) -> stop names (list of strings)

# --------- DATA TO USE (END) --------- #



# --------- USING THE DATA -------- #


# --------- USING THE DATA (END) -------- #





# --------- TESTS --------#
# print trains_to_stops
# print tripID_to_train

# print dict_BDFM
# print dict_BDFM.get("entity")[0]
# print dict_BDFM.get("entity")[1]
# print dict_BDFM.get("entity")[2]
# print dict_BDFM.get("entity")[3]
# print dict_BDFM.get("entity")[4]
