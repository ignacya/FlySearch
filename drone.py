import logging
from argparse import ArgumentParser

from dotenv import load_dotenv

from arg_resolvers import (
    AgentFactoryResolver,
    Bus,
    ConversationFactoryResolver,
    LoggerFactoryResolver,
    RunnerResolver,
    ScenarioArgResolver,
)

load_dotenv(verbose=True)


logging.basicConfig(level=logging.INFO)


def main():
    parser = ArgumentParser()

    bus = Bus(
        [
            ScenarioArgResolver(),
            ConversationFactoryResolver(),
            LoggerFactoryResolver(),
            AgentFactoryResolver(),
            RunnerResolver(),
        ]
    )

    bus.register_args(parser)
    args = parser.parse_args()
    config = bus.resolve_args(args, {})

    config["experiment_runner"].run()


if __name__ == "__main__":
    main()
