from rl.evaluation.validators.base_validator import BaseValidator


class BaseValidatorFactory:
    def get_validator(self) -> BaseValidator:
        raise NotImplementedError()
