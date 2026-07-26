"""
Customer support email classifier — the LLM feature under test.

Takes an email (subject + body) and returns a structured classification:
category (billing, technical, account, general) + a one-sentence summary.
"""

# this class should not know anything about :
#   groq, openAI, json, api calls, parsing
# its job is email->prompt->llm->emailclassification
## this is called an ORCHESTRATOR

from src.feature.config import PromptConfig
from src.feature.models import EmailClassification
from src.llm.base import BaseLLMClient

class EmailClassifier:

    def __init__(
        self,
        llm: BaseLLMClient,
        prompt_config: PromptConfig,
    ):
        self.llm = llm
        self.prompt_config = prompt_config

    def classify(self, email: str) -> EmailClassification:

        return self.llm.generate(
            system_prompt=self.prompt_config.system_prompt,
            user_prompt=email,
            response_model=EmailClassification,
            model=self.prompt_config.model,
            temperature=self.prompt_config.temperature,
            max_tokens=self.prompt_config.max_tokens,
        )

        