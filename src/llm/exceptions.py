class LLMError(Exception):
    """Base for all LLM-pipeline failures."""


class LLMRequestError(LLMError):
    """The API call itself failed (network, auth, rate limit, etc.)"""


class LLMOutputError(LLMError):
    """The API responded, but output was malformed or failed schema validation."""

    def __init__(self, message: str, raw_content: str | None = None):
        super().__init__(message)
        self.raw_content = raw_content