from google.transit import gtfs_realtime_pb2
# import gtfs_realtime_pb2
import requests

# get API key from MTA
api_key = 'api_key'

# data for BDFM line
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=16')
feed.ParseFromString(response.content)

print str(feed)



