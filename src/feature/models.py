"""
Pydantic models for the feature layer: input email schema and the
structured output schema (category, summary) the classifier must return.
"""

from enum import Enum
from pydantic import BaseModel

class Category(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    GENERAL = "general"

class EmailClassification(BaseModel):
    category : Category
    summary : str

# keeping category as Enum -> using Enum or Literal prevents the LLM from creating extra 5th category other than the 4 mentioned by us.
# summary -> str is fine. we will enforce it to a max length so it stays one sentence. Pydantic supports Field(max_length=...)

