from PIL import Image
from pathlib import Path

from scenarios.city_scenario_mapper import CityScenarioMapper

CLASS_IMAGES_DIR = (
    Path(__file__).resolve().parent.parent / "web" / "client" / "public" / "targets"
)

classes_to_images = {
    CityScenarioMapper.ObjectType.FIRE: Image.open(
        CLASS_IMAGES_DIR / "fire.png.jpg"
    ),
    CityScenarioMapper.ObjectType.CROWD: Image.open(
        CLASS_IMAGES_DIR / "crowd.png.jpg"
    ),
    CityScenarioMapper.ObjectType.POLICE_CAR: Image.open(
        CLASS_IMAGES_DIR / "police_car.png.jpg"
    ),
    CityScenarioMapper.ObjectType.WHITE_SPORT_CAR: Image.open(
        CLASS_IMAGES_DIR / "white_sport_car.png.jpg"
    ),
    CityScenarioMapper.ObjectType.RED_SPORT_CAR: Image.open(
        CLASS_IMAGES_DIR / "red_sport_car.png.jpg"
    ),
    CityScenarioMapper.ObjectType.BLUE_SPORT_CAR: Image.open(
        CLASS_IMAGES_DIR / "blue_sport_car.png.jpg"
    ),
    CityScenarioMapper.ObjectType.BEIGE_SPORT_CAR: Image.open(
        CLASS_IMAGES_DIR / "beige_sport_car.png.jpg"
    ),
    CityScenarioMapper.ObjectType.BLACK_TRUCK: Image.open(
        CLASS_IMAGES_DIR / "black_truck.png.jpg"
    ),
    CityScenarioMapper.ObjectType.WHITE_TRUCK: Image.open(
        CLASS_IMAGES_DIR / "white_truck.png.jpg"
    ),
    CityScenarioMapper.ObjectType.RED_PICKUP_TRUCK: Image.open(
        CLASS_IMAGES_DIR / "red_pickup_truck.png.jpg"
    ),
    CityScenarioMapper.ObjectType.GREEN_PICKUP_TRUCK: Image.open(
        CLASS_IMAGES_DIR / "green_pickup_truck.png.jpg"
    ),
    CityScenarioMapper.ObjectType.BLACK_PICKUP_TRUCK: Image.open(
        CLASS_IMAGES_DIR / "black_pickup_truck.png.jpg"
    ),
    CityScenarioMapper.ObjectType.WHITE_PICKUP_TRUCK: Image.open(
        CLASS_IMAGES_DIR / "white_pickup_truck.png.jpg"
    ),
    CityScenarioMapper.ObjectType.ROAD_CONSTRUCTION_SITE: Image.open(
        CLASS_IMAGES_DIR / "road_construction_site.png.jpg"
    ),
    CityScenarioMapper.ObjectType.LARGE_TRASH_PILE: Image.open(
        CLASS_IMAGES_DIR / "large_trash_pile.png.jpg"
    ),
}
