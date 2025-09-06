from conversation.base_conversation_factory import BaseConversationFactory
from rl.agents.base_agent_factory import BaseAgentFactory
from rl.agents.simple_llm_agent import SimpleLLMAgent


class SimpleLLMAgentFactory(BaseAgentFactory):
    def __init__(self, conversation_factory: BaseConversationFactory):
        self.conversation_factory = conversation_factory

    def create_agent(self, prompt: str, **kwargs) -> SimpleLLMAgent:
        return SimpleLLMAgent(
            conversation=self.conversation_factory.get_conversation(),
            prompt=prompt
        )
