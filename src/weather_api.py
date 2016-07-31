import json
import urllib2
import pyzipcode

from bucket import PrecipBucket
from master import PrecipMaster
from enums import BucketSize

URI = 'https://api.forecast.io/forecast/%s/%f,%f'
ZIP_DB = pyzipcode.ZipCodeDatabase()

LEVEL_KEYS = {
  BucketSize.MINUTE: 'minutely',
  BucketSize.HOUR: 'hourly',
  BucketSize.DAY: 'daily',
  }

def get_weather_for_zip(zipcode):
  zip_data = ZIP_DB[zipcode]
  return get_weather(zip_data.latitude, zip_data.longitude)

def get_weather(latitude, longitude):
  data = _get_weather_json(latitude, longitude)
  return PrecipMaster(
    _classify_data_level(BucketSize.MINUTE, data),
    _classify_data_level(BucketSize.HOUR, data),
    _classify_data_level(BucketSize.DAY, data),
    )

def _classify_data_level(level, full_data):
  return map(
    lambda item: PrecipBucket(level, item),
    full_data[LEVEL_KEYS[level]]['data'],
    )

def _get_weather_json(latitude, longitude):
  uri = URI % (_get_api_key(), latitude, longitude)
  resp = urllib2.urlopen(uri)
  s = resp.read()
  resp.close()
  return json.loads(s)

def _get_api_key():
  f = open('.api-key.secret')
  key = f.read().strip()
  f.close()
  return key

if __name__ == '__main__':
  import datetime
  def _print_weather(buckets):
    for bucket in buckets:
      print datetime.datetime.fromtimestamp(bucket._start_time),
      print '\t', bucket.get_probability()
  def _print_groups(groups):
    for group in groups:
      print datetime.datetime.fromtimestamp(group._buckets[0]._start_time),
      print '\t', len(group._buckets),
      print '\t', group._mean,
      print '\t', group._away, '\t',
      print ''

  import sys
  zip = 10028 if len(sys.argv) < 2 else int(sys.argv[1])
  result = get_weather_for_zip(zip)

  print '--- MINUTELY ----'
  _print_weather(result._minutely)
  print '--- HOURLY ----'
  _print_weather(result._hourly)
  print '--- DAILY ----'
  _print_weather(result._daily)
  print ''

  buckets = result.get_precip_buckets()
  for level in buckets:
    print '--------------', level, '-------------'
    _print_groups(buckets[level])

  import pdb; pdb.set_trace()
