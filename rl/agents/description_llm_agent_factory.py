from conversation.base_conversation_factory import BaseConversationFactory
from rl.agents.base_agent_factory import BaseAgentFactory
from rl.agents.description_llm_agent import DescriptionLLMAgent
from rl.agents.simple_llm_agent import SimpleLLMAgent


class DescriptionLLMAgentFactory(BaseAgentFactory):
    def __init__(self, conversation_factory: BaseConversationFactory):
        self.conversation_factory = conversation_factory

    def create_agent(self, prompt: str, object_desc: str, **kwargs) -> SimpleLLMAgent:
        return DescriptionLLMAgent(
            conversation=self.conversation_factory.get_conversation(),
            prompt=prompt,
            object_desc=object_desc,
            description_conversation_factory=self.conversation_factory
        )
