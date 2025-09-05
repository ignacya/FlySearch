from datetime import datetime
import logging
from enum import Enum
import pathlib
from typing import Optional

import typer
from dotenv import load_dotenv

from conversation.conversations import LLM_BACKEND_FACTORIES, LLMBackends
from rl.agents.agents import AGENT_FACTORIES, Agents
from rl.evaluation.loggers.local_fs_logger_factory import LocalFSLoggerFactory

app = typer.Typer(
    help="FlySearch benchmark", add_completion=False, no_args_is_help=True
)

load_dotenv(verbose=True)


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


context = {
    "conversation_factory": None,
    "logger_factories": None,
}


@app.callback()
def main(
    model_backend: LLMBackends = typer.Option(help="The backend of the model to use"),
    model_name: str = typer.Option(
        help="The name of the model to use (passed to the model backend)"
    ),
    run_name: Optional[str] = typer.Option(
        help="The name of the benchmark run (default to date and time)", default=None
    ),
    results_directory: str = typer.Option(
        help="The directory to store the experiment results", default="all_logs"
    ),
    agent: Agents = typer.Option(
        help="The type of agent to use (use default for oryginal FlySearch)",
        default=Agents.SIMPLE_LLM,
    ),
    skip_sanity_check: bool = typer.Option(False,
        "--skip-sanity-check",
        help="Whether to skip running a sanity check before the benchmark (not recommended)",
    ),
    continue_from_idx: int = typer.Option(
        help="The index of the scenario to continue running from (e.g. if execution was interrupted)",
        default=0,
    ),
    log_level: LogLevel = typer.Option(
        help="The level of logging to use",
        default=LogLevel.INFO,
    ),
):
    logging.basicConfig(level=getattr(logging, log_level.value))

    if not run_name:
        run_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    context["conversation_factory"] = LLM_BACKEND_FACTORIES[model_backend](model_name)
    context["logger_factories"] = [
        LocalFSLoggerFactory(
            pathlib.Path(results_directory) / run_name,
            initial_iteration=continue_from_idx,
        )
    ]
    context["agent_factory"] = AGENT_FACTORIES[agent](context["conversation_factory"])
    context["continue_from_idx"] = continue_from_idx
    context["sanity_check"] = not skip_sanity_check


@app.command()
def benchmark(
    scenario_directory: str = typer.Argument(
        help="The directory containing the scenarios to run the benchmark on"
    ),
):
    """
    Run a predefined benchmark set.
    """
    pass


@app.command()
def random_scenarios(
    scenario_type: str = typer.Argument(help="The type of scenario to generate"),
    difficulty: str = typer.Argument(help="The difficulty of the scenario"),
):
    """
    Run FlySearch with random scenario generation.
    """
    pass


@app.command()
def custom_scenarios(
    scenario_type: str = typer.Option(help="The type of scenario to generate"),
    height_min: int = typer.Option(help="The minimum height of the scenario"),
    height_max: int = typer.Option(help="The maximum height of the scenario"),
    alpha: float = typer.Option(help="The alpha value for the scenario"),
    random_sun: bool = typer.Option(
        help="Whether to generate scenarios with random sun positions"
    ),
    number_of_runs: int = typer.Option(help="The number of scenarios to generate"),
    glimpses: int = typer.Option(
        help="The number of glimpses (or images) the agent is allowed to see in the trajectory, 10 for FS-1 and 20 for FS-2"
    ),
    prompt_type: str = typer.Option(help="The type of prompt to use (fs1 or fs2)"),
    show_class_image: bool = typer.Option(
        help="Whether to show the class image in the scenario (true for FS-2, false for FS-1 and FS-Anomaly-1)"
    ),
    forgiveness: int = typer.Option(
        help="The number of model retries in case of action parsing error before terminating the trajectory",
        default=5,
    ),
):
    """
    Run FlySearch with custom random scenario generation.
    """
    pass


if __name__ == "__main__":
    app()
