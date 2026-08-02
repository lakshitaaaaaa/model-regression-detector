from enum import Enum
from pydantic import BaseModel
from src.feature.models import Category

class EvaluationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"

class SummaryEvaluation(BaseModel):
    score: float | None = None
    reasoning: str | None = None

class EvaluationResult(BaseModel):
    test_case_id: str

    expected_category: Category
    predicted_category: Category

    expected_summary: str
    predicted_summary: str

    status: EvaluationStatus

    latency_ms: float

    input_tokens: int | None = None
    output_tokens: int | None = None

    summary_evaluation: SummaryEvaluation | None = None

    error_message: str | None = None

# instead of the runner returning random dictionaries, everything will return an EvaluationResult
# that means, html report, sqlLite, diff engine, dashboard, github action all consume the same object
