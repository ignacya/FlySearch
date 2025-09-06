from rl.environment import EnvironmentType
from rl.environment.city_fly_search_env import CityFlySearchEnv
from rl.environment.forest_fly_search_env import ForestFlySearchEnv

ENVIRONMENTS = {
    EnvironmentType.CITY: CityFlySearchEnv,
    EnvironmentType.FOREST: ForestFlySearchEnv,
}
