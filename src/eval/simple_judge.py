# just for architecture evaluation purposes

from src.eval.judge import BaseSummaryJudge
from src.eval.models import SummaryEvaluation

class SimpleEvaluationJudge(BaseSummaryJudge):

    def evaluate(
            self, 
            expected: str, 
            predicted: str,
        ) -> SummaryEvaluation:

        if expected.strip().lower() == predicted.strip().lower():
            return SummaryEvaluation(
                score=5.0,
                reasoning="Exact match"
            )
        
        return SummaryEvaluation(
            score=3.0,
            reasoning="Placeholder implementation"
        )