from conversation.abstract_conversation import Role
from conversation.base_conversation_factory import BaseConversationFactory
from rl.agents.semantic_units import BaseSemanticSubunit


class GoalIdentifier(BaseSemanticSubunit):
    def __init__(self, conversation_factory: BaseConversationFactory):
        self.conversation_factory = conversation_factory

    def process_information(self, information: dict) -> dict:
        prompt = information["prompt"]

        conversation = self.conversation_factory.get_conversation()

        conversation.begin_transaction(Role.USER)
        conversation.add_text_message(
            "Your task is to read the prompt for an agentic system and identify the goal of the agent that it would be useful to detect. Please, provide the goal in text using only A CLASS NAME, as if you were defining labels in imagenet, without any additional information. The name will be used as a label for a detection model.")
        conversation.add_text_message(prompt)
        conversation.commit_transaction(send_to_vlm=True)
        _, goal = conversation.get_latest_message()

        information["target"] = goal
        return information

    def get_goal(self, information: dict) -> str:
        """
        Get the goal from the information dictionary.
        :param information: Dictionary with the information to be processed.
        :return: Goal as a string.
        """
        return self.process_information(information)["target"]
