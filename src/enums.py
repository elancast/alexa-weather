def enum(**enums):
    return type('Enum', (), enums)

PrecipProbSummary = enum(
  NONE = 0,
  SMALL = 1,
  MEDIUM = 2,
  HIGH = 3,
  GUARANTEED = 4,
  )

BucketSize = enum(
  MINUTE = 1,
  HOUR = 2,
  DAY = 3,
  )

def get_prob_summary(probability):
  if probability <= 0.05:
    return PrecipProbSummary.NONE
  elif probability <= 0.35:
    return PrecipProbSummary.SMALL
  elif probability <= 0.65:
    return PrecipProbSummary.MEDIUM
  elif probability <= 0.95:
    return PrecipProbSummary.HIGH
  else:
    return PrecipProbSummary.GUARANTEED
