import pathlib

from prompts.drone_prompt_generation import fs1_prompt
from rl.agents.simple_llm_agent_factory import SimpleLLMAgentFactory
from rl.environment.base_fly_search_env import BaseFlySearchEnv
from rl.evaluation.configs.experiment_config import ExperimentConfig
from rl.evaluation.loggers.local_fs_logger_factory import LocalFSLoggerFactory
from rl.evaluation.validators.altitude_validator_factory import AltitudeValidatorFactory
from rl.evaluation.validators.out_of_bounds_flight_validator_factory import OutOfBoundsFlightValidatorFactory
from rl.evaluation.validators.reckless_flying_validator_factory import RecklessFlyingValidatorFactory
from scenarios.base_scenario_mapper import BaseScenarioMapper


class BasicConfig(ExperimentConfig):
    def __init__(self, conversation_factory, environment: BaseFlySearchEnv, scenario_mapper: BaseScenarioMapper,
                 number_of_runs: int, run_name: str):
        super().__init__(
            agent_factory=SimpleLLMAgentFactory(conversation_factory),
            environment=environment,
            scenario_mapper=scenario_mapper,
            logger_factories=[LocalFSLoggerFactory(log_dir_prefix=pathlib.Path(f"all_logs/{run_name}"))],
            validator_factories=[RecklessFlyingValidatorFactory(),
                                 OutOfBoundsFlightValidatorFactory(search_diameter=200),
                                 AltitudeValidatorFactory(max_altitude=120)],
            forgiveness=5,
            number_of_runs=number_of_runs,
            number_of_glimpses=10,
            prompt_factory=fs1_prompt
        )
