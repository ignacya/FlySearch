from enum import Enum

from .description_llm_agent_factory import DescriptionLLMAgentFactory
from .detection_cheater_factory import DetectionCheaterFactory
from .detection_driven_description_llm_agent_factory import DetectionDrivenDescriptionLLMAgentFactory
from .generalist_one_agent_factory import GeneralistOneAgentFactory
from .parsing_error_agent_factory import ParsingErrorAgentFactory
from .simple_llm_agent_factory import SimpleLLMAgentFactory


class Agents(str, Enum):
    SIMPLE_LLM = "simple_llm"
    DESCRIPTION_LLM = "description_llm"
    GENERALIST_ONE = "generalist_one"
    DETECTION_DRIVEN_DESCRIPTION_LLM = "detection_driven_description_llm"
    DETECTION_CHEATER = "detection_cheater_factory"
    PARSING_ERROR = "parsing_error"

AGENT_FACTORIES = {
    Agents.SIMPLE_LLM: SimpleLLMAgentFactory,
    Agents.DESCRIPTION_LLM: DescriptionLLMAgentFactory,
    Agents.GENERALIST_ONE: GeneralistOneAgentFactory,
    Agents.DETECTION_DRIVEN_DESCRIPTION_LLM: DetectionDrivenDescriptionLLMAgentFactory,
    Agents.DETECTION_CHEATER: DetectionCheaterFactory,
    Agents.PARSING_ERROR: ParsingErrorAgentFactory,
}