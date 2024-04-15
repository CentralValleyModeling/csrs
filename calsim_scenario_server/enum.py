import enum


# Define the assumption types as a Python enumeration
class AssumptionEnum(enum.StrEnum):
    hydrology = "hydrology"
    sea_level_rise = "sea_level_rise"
    land_use = "land_use"
    tucp = "tucp"
    dcp = "dcp"
    va = "va"
    south_of_delta = "south_of_delta"


class DimensionalityEnum(enum.StrEnum):
    volume = "[length] ** 3"
    area = "[length] ** 2"
    length = "[length]"
    flow = "[length] ** 3 / [time]"
    flux = "[length] ** 2 / [time]"
    mass = "[mass]"
    mass_flow = "[mass] / [time]"
    temperature = "[temperature]"


class PathCategoryEnum(enum.StrEnum):
    delivery = "delivery"
    delta = "delta"
    other = "other"
    salinity = "salinity"
    storage = "storage"
    upstream_flows = "upstream_flows"
    water_year_type = "wyt"
