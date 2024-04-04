from enum import Enum, EnumMeta

from . import (
    delta_conveyance_project,
    hydrology,
    land_use,
    sea_level_rise,
    south_of_delta_storage,
    tucp,
    voluntary_agreements,
)


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return item in [v for v in cls.__members__.keys()]
        else:
            return True


class TableNames(Enum, metaclass=MyEnumMeta):
    dcp = delta_conveyance_project
    hydrology = hydrology
    land_use = land_use
    sea_level_rise = sea_level_rise
    sod = south_of_delta_storage
    tucp = tucp
    va = voluntary_agreements
