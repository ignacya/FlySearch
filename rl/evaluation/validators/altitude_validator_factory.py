from rl.evaluation.validators.altitude_validator import AltitudeValidator
from rl.evaluation.validators.base_validator import BaseValidator
from rl.evaluation.validators.base_validator_factory import BaseValidatorFactory


class AltitudeValidatorFactory(BaseValidatorFactory):
    def __init__(self, max_altitude: int):
        self.max_altitude = max_altitude

    def get_validator(self) -> BaseValidator:
        return AltitudeValidator(self.max_altitude)
