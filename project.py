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
print routes

# station stops data
stops_file = open('mta-data/stops.txt', 'r')
stops = stops_file.read()
stops_file.close()

# trips data
trips_file = open('mta-data/trips.txt', 'r')
trips = trips_file.read()
trips_file.close()



# print dict_BDFM.get("entity")[0]
# print dict_BDFM.get("entity")[1]
# print dict_BDFM.get("entity")[2]
# print dict_BDFM.get("entity")[3]
# print dict_BDFM.get("entity")[4]

# --------- RETRIEVING DATA (END) --------- #


# --------- DOING THINGS --------- #
# NEED:
# - subway letter
# - station name
# - time enter/leave station

def organize_route_data(data):
    new_data = data.split()[1:]
    return new_data

# {trainLetter: [{stationName : (time enter, time leave)}, {stationName : (time enter, time leave)}], trainLetter: [{stationName : (time enter, time leave)}]}


# for entity in feed_BDFM.entity:
#     if entity.hasField('trip_update'):
#         print entity.trip_update.trip.

# --------- DOING THINGS (END) --------- #


# --------- TESTS --------#
# print str(feed_BDFM)



