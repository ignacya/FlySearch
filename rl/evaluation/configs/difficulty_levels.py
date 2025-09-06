from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from prompts.prompts import Prompts


class SearchAreaBoundsType(str, Enum):  # noqa: F821
    ABSOLUTE = "absolute"
    RELATIVE = "relative"  # relative to starting altitude


@dataclass
class CitySpecificDifficultySettings:
    sun_elevation_angle_range: Optional[
        Tuple[float, float]
    ]  # leave empty for static sun direction
    sun_azimuth_angle_range: Optional[
        Tuple[float, float]
    ]  # leave empty for static sun direction


@dataclass
class ForestSpecificDifficultySettings:
    tree_density_range: Tuple[float, float]
    rock_density_range: Tuple[float, float]
    cliff_density_range: Tuple[float, float]


@dataclass
class DifficultyLevel:
    description: Optional[str]  # description of the difficulty level

    starting_uav_altitude_range: Tuple[int, int]  # range of starting UAV altitude
    starting_uav_position_offset: float  # offset of starting UAV position from the target relative to the starting altitude

    search_area_bounds: int | float  # bounds of the search area in each direction
    search_area_bounds_type: SearchAreaBoundsType  # type of the search area bounds

    max_uav_altitude: int  # max altitude of the UAV
    can_move_beyond_current_view: (
        bool  # whether the UAV can move beyond the current view
    )
    max_steps: int  # max number of steps/glimpses the UAV can take
    max_retries: int  # max number of retries in case of action parsing error or out of bounds action

    target_line_of_sight_assured: (
        bool  # whether the target is guaranteed to be in the line of sight of the UAV
    )
    show_visual_sample: (
        bool  # whether to show a visual sample of the target in the prompt
    )
    prompt_type: Prompts  # type of the prompt

    city_settings: CitySpecificDifficultySettings  # settings for the city environment
    forest_settings: (
        ForestSpecificDifficultySettings  # settings for the forest environment
    )


FS_1 = DifficultyLevel(
    description="The FS-1 and FS-Anomaly-1 benchmark difficulty level",
    starting_uav_altitude_range=(30, 100),
    starting_uav_position_offset=0.5,
    search_area_bounds=200,
    search_area_bounds_type=SearchAreaBoundsType.ABSOLUTE,
    max_uav_altitude=120,
    can_move_beyond_current_view=False,
    max_steps=10,
    max_retries=5,
    target_line_of_sight_assured=True,
    show_visual_sample=False,
    prompt_type=Prompts.FS1,
    city_settings=CitySpecificDifficultySettings(
        sun_elevation_angle_range=None, sun_azimuth_angle_range=None
    ),
    forest_settings=ForestSpecificDifficultySettings(
        tree_density_range=(0.0, 0.3),
        rock_density_range=(0.0, 0.1),
        cliff_density_range=(0.0, 0.0),
    ),
)

FS_2 = DifficultyLevel(
    description="The FS-2 benchmark difficulty level",
    starting_uav_altitude_range=(100, 125),
    starting_uav_position_offset=0.95,
    search_area_bounds=1,
    search_area_bounds_type=SearchAreaBoundsType.RELATIVE,
    max_uav_altitude=300,
    can_move_beyond_current_view=True,
    max_steps=20,
    max_retries=5,
    target_line_of_sight_assured=False,
    show_visual_sample=True,
    prompt_type=Prompts.FS2,
    city_settings=CitySpecificDifficultySettings(
        sun_elevation_angle_range=(10, 90), sun_azimuth_angle_range=(0, 360)
    ),
    forest_settings=ForestSpecificDifficultySettings(
        tree_density_range=(0.0, 0.3),
        rock_density_range=(0.0, 0.1),
        cliff_density_range=(0.0, 0.0),
    ),
)


class DifficultySettings(str, Enum):
    FS_1 = "fs1"
    FS_2 = "fs2"


DIFFICULTY_LEVELS = {
    DifficultySettings.FS_1: FS_1,
    DifficultySettings.FS_2: FS_2,
}
