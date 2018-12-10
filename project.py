from google.transit import gtfs_realtime_pb2
import requests

api_key = 'API_Key'

mta_info = requests.get('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=16')

print feed.ParseFromString(mta_info.content)