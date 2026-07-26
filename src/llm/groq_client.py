"""
Thin wrapper around the Groq API client: chat completion calls,
retries, and token/latency tracking for a single request.
"""

# this file will read our groq api key from .env
# will connect to the groq api and send the prompt and emailand will return an EmailClassification object

import json
import os
from typing import Type, TypeVar

from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from src.llm.base import BaseLLMClient
from src.utils.json_parser import extract_json
from src.llm.exceptions import LLMRequestError, LLMOutputError

load_dotenv()
# we are hiding groq, because our classifier should not know which provider we are using
# in this way, our code is not dependent on which model we are using. 
# later, if we change our model to gemini(for eg), it will work fabously in the exact same interface.
# so when we use classifier.classify(email), internally our system will do EmailClassifier()->GroqClient.generate()->Groq API
# later if model changed -> classifier will remain same

T = TypeVar("T", bound=BaseModel)

class GroqClient(BaseLLMClient):

    def __init__(self):
        super().__init__()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("Groq API key not found")
        
        self.client = Groq(api_key= api_key)

    # generate(...) should receive prompt -> call groq -> receive json -> validate using pydantic -> return EmailClassification
    def generate(
            self,
            *,
            system_prompt: str,
            user_prompt: str,
            response_model: Type[T],
            model: str,
            temperature: float,
            max_tokens: int | None = None,
    ) -> T:
        # api call will go here
        try:
            response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )    
        except Exception as e:
            raise LLMRequestError(f"Groq request failed: {e}") from e

        content = response.choices[0].message.content
        
        try:
            data = extract_json(content)
            return response_model.model_validate(data)
        except (ValueError, ValidationError) as e:
            raise LLMOutputError(
                f"Failed to parse/validate LLM output: {e}", raw_content=content
            ) from e

    
    """
        response_model (Pydantic)
                │
                ▼
        Generate JSON Schema
                │
                ▼
        Send schema to Groq
                │
                ▼
        Receive JSON string
                │
                ▼
        Validate with Pydantic
                │
                ▼
        Return EmailClassification

        The client will never know what EmailClassification is. It simply receives a Pydantic class
"""