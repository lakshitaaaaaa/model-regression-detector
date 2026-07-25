"""
Thin wrapper around the Groq API client: chat completion calls,
retries, and token/latency tracking for a single request.
"""

# this file will read our groq api key from .env
# will connect to the groq api and send the prompt and emailand will return an EmailClassification object

from groq import Groq
from dotenv import load_dotenv
import os

from src.llm.base import BaseLLMClient

load_dotenv()
# we are hiding groq, because our classifier should not know which provider we are using
# in this way, our code is not dependent on which model we are using. 
# later, if we change our model to gemini(for eg), it will work fabously in the exact same interface.
# so when we use classifier.classify(email), internally our system will do EmailClassifier()->GroqClient.generate()->Groq API
# later if model changed -> classifier will remain same

class GroqClient:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("Groq API key not found")
        
        self.client = Groq(api_key= api_key)

    # generate(...) should receive prompt -> call groq -> receive json -> validate using pydantic -> return EmailClassification
    def generate(self, **kwargs):
        pass