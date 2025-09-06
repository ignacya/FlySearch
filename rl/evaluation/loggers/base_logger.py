from typing import Dict

from rl.evaluation.evaluation_state import EvaluationState


class BaseLogger:
    def log(self, evaluation_state: EvaluationState):
        raise NotImplementedError

    def log_termination(self, termination_info: Dict):
        raise NotImplementedError

    def nuke(self):
        raise NotImplementedError