# this will become the single object every reporting backend will consume

from pydantic import BaseModel

from src.eval.diff import RunDiff
from src.eval.models import EvaluationResult

class EvaluationReport(BaseModel):
    results: list[EvaluationResult]
    diff: RunDiff | None

    accuracy: float
    passed: int
    failed: int
    errors: int