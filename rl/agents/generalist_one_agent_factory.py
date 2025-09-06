from rl.agents.base_agent_factory import BaseAgentFactory
from rl.agents.generalist_one import GeneralistOne


class GeneralistOneAgentFactory(BaseAgentFactory):
    def __init__(self, conversation_factory):
        self.conversation_factory = conversation_factory

    def create_agent(self, prompt: str, **kwargs) -> GeneralistOne:
        return GeneralistOne(conversation_factory=self.conversation_factory, prompt=prompt)
