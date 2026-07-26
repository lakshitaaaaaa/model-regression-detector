"""
PromptConfig — typed contract between prompt versions and the eval pipeline.

Defines the Pydantic model that describes a prompt version: id, timestamp,
system prompt, few-shot examples, and the model it targets.
"""

from pydantic import BaseModel

class PromptConfig(BaseModel):
    version: str
    model: str
    temperature: float
    max_tokens: int = 256
    system_prompt: str

# in this, we are not including everything, such as top_k, max_tokens, frequency_penalty, response_penalty, etc because these are
# the information details of the LLM provider. Our project only needs the information that defines the prompt version.

