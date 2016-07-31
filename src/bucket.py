from enums import get_prob_summary

class PrecipBucket:
  def __init__(self, level, data):
    self._level = level
    self._data = data
    self._precip_probability = data['precipProbability']
    self._precip_type = None if not 'precipType' in data else data['precipType']
    self._precip_intensity = data['precipIntensity']
    self._start_time = data['time']

  def get_probability(self):
    return self._precip_probability

  def get_precip_prob_summary(self):
    return get_prob_summary(self._precip_probability)

  def has_precip(self):
    return self._precip_type != 0

  def can_aggregate_with(self, bucket):
    return self._precip_type == bucket._precip_type or \
      self._precip_type == None or \
      bucket._precip_type == None
