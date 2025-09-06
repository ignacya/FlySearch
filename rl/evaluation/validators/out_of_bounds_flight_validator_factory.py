from rl.evaluation.validators.base_validator_factory import BaseValidatorFactory
from rl.evaluation.validators.out_of_bounds_flight_validator import OutOfBoundsFlightValidator


class OutOfBoundsFlightValidatorFactory(BaseValidatorFactory):
    def __init__(self, search_diameter: int = 200, fs2_behavior: bool = False):
        self.search_diameter = search_diameter
        self.fs2_behavior = fs2_behavior

    def get_validator(self):
        return OutOfBoundsFlightValidator(self.search_diameter, self.fs2_behavior)
