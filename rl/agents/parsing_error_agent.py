from typing import Dict

from response_parsers.xml_response_parser import ParsingError
from rl.agents.base_agent import BaseAgent


class ParsingErrorAgent(BaseAgent):
    """
    Used for debugging purposes, always throws ParsingErrors.
    """

    def sample_action(self, observation: Dict) -> Dict:
        raise ParsingError()

    def correct_previous_action(self, fail_reason: Dict) -> Dict:
        raise ParsingError()

    def get_agent_info(self) -> Dict:
        return {
            "conversation_history": []
        }
