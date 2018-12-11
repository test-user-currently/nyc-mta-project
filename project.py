from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
import requests

# --------- RETRIEVING DATA --------- #

# get API key from MTA
api_key = 'api_key'

# data for BDFM lines
feed_BDFM = gtfs_realtime_pb2.FeedMessage()
response_BDFM = requests.get('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=21')
feed_BDFM.ParseFromString(response_BDFM.content)
dict_BDFM = protobuf_to_dict(feed_BDFM)

# data for NQRW lines
feed_NQRW = gtfs_realtime_pb2.FeedMessage()
response_NQRW = requests.get('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=16')
feed_NQRW.ParseFromString(response_NQRW.content)
dict_NQRW = protobuf_to_dict(feed_NQRW)

# routes data
routes_file = open('mta-data/routes.txt', 'r')
routes = routes_file.read()
routes_file.close()


# station stops data
# stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station
stops_file = open('mta-data/stops.txt', 'r')
stops = stops_file.read()
stops_file.close()

# trips data
trips_file = open('mta-data/trips.txt', 'r')
trips = trips_file.read()
trips_file.close()

# --------- RETRIEVING DATA (END) --------- #



# --------- ORGANIZING DATA --------- #
# NEED:
# - subway letter
# - station name
# - time enter/leave station

# def organize_route_data(data):
#     new_data = data.split("\n")[1:]
#     for ()
#     return new_data[0]

# does not return anything; populates stops_to_name dictionary
def organize_stops_data(data):
    new_data = data.split("\n")[1:-1]
    data_len = len(new_data)

    for idx in range(data_len):
        new_data[idx] = new_data[idx].split(",")
    stops_id = map(lambda x: x[0], new_data)
    stops_name = map(lambda x: x[2], new_data)

    ret_dict = {}
    for idx in range(data_len):
        ret_dict[stops_id[idx]] = stops_name[idx]
    return ret_dict

# {trainLetter: [{stationName : (time enter, time leave)}, {stationName : (time enter, time leave)}], trainLetter: [{stationName : (time enter, time leave)}]}


# for entity in feed_BDFM.entity:
#     if entity.hasField('trip_update'):
#         print entity.trip_update.trip.

# --------- ORGANIZING DATA (END) --------- #



# --------- DATA TO USE --------- #

stops_id_to_name = organize_stops_data(stops) # mapping from stop_id (string) -> stop_name (string)

# --------- DATA TO USE (END) --------- #



# --------- TESTS --------#
# print stops_id_to_name

# print organize_stops_data(stops)

# print dict_BDFM.get("entity")[0]
# print dict_BDFM.get("entity")[1]
# print dict_BDFM.get("entity")[2]
# print dict_BDFM.get("entity")[3]
# print dict_BDFM.get("entity")[4]



