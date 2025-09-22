import os

from openai import OpenAI, _types

from conversation.base_conversation_factory import BaseConversationFactory
from conversation.openai_conversation import OpenAIConversation


class GeminiFactory(BaseConversationFactory):
    def __init__(self, model_name: str):
        self.client = OpenAI(api_key=os.environ["GEMINI_AI_KEY"],
                             base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
                             max_retries=100)

        self.model_name = model_name

    def get_conversation(self):
        return OpenAIConversation(
            self.client,
            model_name=self.model_name,
            max_tokens=_types.NotGiven()
        )  # Without this, Gemini 2.5 Flash will give out Nones. Probably due to reasoning tokens. TODO: Pro still fails (sometimes (!)) for some reason.
