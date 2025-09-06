from rl.agents.base_agent import BaseAgent


class BaseAgentFactory:
    def create_agent(self, prompt: str, **kwargs) -> BaseAgent:
        raise NotImplementedError
