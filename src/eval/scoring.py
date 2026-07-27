from src.eval.models import EvaluationStatus
from src.feature.models import EmailClassification
from golden_dataset.schema import GoldenTestCase
from src.eval.models import EvaluationResult, EvaluationStatus

def evaluate_category(
        prediction: EmailClassification,
        test_case: GoldenTestCase,
) -> EvaluationStatus:
    
    if prediction.category == test_case.expected_category:
        return EvaluationStatus.PASS
    
    return EvaluationStatus.FAIL

def calculate_accuracy(results: list[EvaluationResult]) -> float:

    if not results:
        return 0.0
    
    passed = sum(
        r.status == EvaluationStatus.PASS
        for r in results
    )

    return (passed/len(results)) * 100

def count_results(results: list[EvaluationResult]) -> tuple[int, int, int]:

    passed = sum(
        r.status == EvaluationStatus.PASS
        for r in results
    )

    failed = sum(
        r.status == EvaluationStatus.FAIL
        for r in results
    )

    errors = sum(
        r.status == EvaluationStatus.ERROR
        for r in results
    )

    return passed, failed, errors