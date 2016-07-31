import numpy

MIN_DIST = 0.1
MAX_DIST = 0.2

class BucketAggregater:
  def __init__(self, bucket):
    self._buckets = [bucket]
    self._mean = bucket.get_probability()
    self._away = MIN_DIST

  def belongs_in_group(self, bucket):
    if not bucket.can_aggregate_with(self._buckets[0]):
      return False
    return (self._mean - self._away) < bucket.get_probability() < (self._mean + self._away)

  def add_to_group(self, bucket):
    self._buckets.append(bucket)
    probs = map(lambda x:x.get_probability(), self._buckets)
    self._mean = numpy.mean(probs)
    self._away = min(MAX_DIST, max(MIN_DIST, 2 * numpy.std(probs)))
