from enum import Enum

from scenarios.default_city_anomaly_scenario_mapper import (
    DefaultCityAnomalyScenarioMapper,
)
from scenarios.default_city_scenario_mapper import DefaultCityScenarioMapper
from scenarios.default_forest_anomaly_scenario_mapper import (
    DefaultForestAnomalyScenarioMapper,
)
from scenarios.default_forest_scenario_mapper import DefaultForestScenarioMapper


class Scenarios(str, Enum):
    CITY = "city"
    FOREST = "forest"
    CITY_ANOMALY = "city_anomaly"
    FOREST_ANOMALY = "forest_anomaly"


SCENARIO_CLASSES = {
    Scenarios.CITY: DefaultCityScenarioMapper,
    Scenarios.FOREST: DefaultForestScenarioMapper,
    Scenarios.CITY_ANOMALY: DefaultCityAnomalyScenarioMapper,
    Scenarios.FOREST_ANOMALY: DefaultForestAnomalyScenarioMapper,
}
