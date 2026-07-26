from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class BaseLLMClient(ABC):
    
    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        model: str,
        temperature: float,
        max_tokens: int | None = None,
    ) -> T:
            #Send a prompt to an LLM and returns a validated Pydantic model.
        raise NotImplementedError 

# ABC stands for Abstract Base Class
# it means that any LLM client must implement generate()

# now our architecture is
#                 BaseLLMClient
#                       ▲
#        ┌───────────────┼───────────────┐
#        │                               │
#        │                               │
#   GroqClient                    GeminiClient
#
# thus, our classifier now depends on BaseLLMClient, and not on GroqClient.
# this is called programming to an interface.