from bucketer import BucketAggregater
from enums import BucketSize

class PrecipMaster:
  def __init__(self, minutely, hourly, daily):
    self._minutely = minutely
    self._hourly = hourly
    self._daily = daily

  def get_precip_buckets(self):
    #if not self._hourly[0].has_precip() and not self._minutely[0].has_precip():
    #return []
    return {
      BucketSize.MINUTE: self._get_aggregated(self._minutely),
      BucketSize.HOUR: self._get_aggregated(self._hourly),
      BucketSize.DAY: self._get_aggregated(self._daily),
      }

  def _get_aggregated(self, array):
    group = BucketAggregater(array[0])
    groups = [group]
    i = 1
    while i < len(array):
      if group.belongs_in_group(array[i]):
        group.add_to_group(array[i])
      else:
        group = BucketAggregater(array[i])
        groups.append(group)
      i += 1
    return groups
