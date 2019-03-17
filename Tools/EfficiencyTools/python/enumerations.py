
__all__ = ['EfficiencyMode']

from Gaugi import EnumStringification


class EfficiencyMode(EnumStringification):
  # @brief: Use to apply the same athena trigger approch
  Athena   = 0
  # @brief: Use for selector/cut combinations
  Selector = 1


