from rl.evaluation.loggers.base_logger import BaseLogger


class BaseLoggerFactory:

    def get_logger(self) -> BaseLogger:
        raise NotImplementedError()
