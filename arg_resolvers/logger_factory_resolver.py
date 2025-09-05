import pathlib
from argparse import ArgumentParser, Namespace
from typing import Dict, List

from arg_resolvers import BaseArgResolver
from rl.evaluation.loggers import LocalFSLoggerFactory


class LoggerFactoryResolver(BaseArgResolver):
    def register_args(self, parser: ArgumentParser):
        parser.add_argument("--log_directory", type=str, required=True)
        parser.add_argument("--run_name", type=str, required=True)

    def get_local_logger_factory(self, args: Namespace) -> List:
        continue_from = args.continue_from if args.continue_from is not None else 0
        return [LocalFSLoggerFactory(pathlib.Path(args.log_directory) / args.run_name, initial_iteration=continue_from)]

    def resolve_args(self, args: Namespace, accumulator: Dict):
        accumulator["logger_factories"] = self.get_local_logger_factory(args)

        return accumulator
