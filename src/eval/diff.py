from pydantic import BaseModel

from src.eval.models import EvaluationResult, EvaluationStatus
from src.eval.scoring import calculate_accuracy

class RunDiff(BaseModel):
    previous_accuracy: float
    current_accuracy: float
    accuracy_delta: float

    regressions: list[str]
    improvements: list[str]

def compare_runs(
        previous: list[EvaluationResult],
        current: list[EvaluationResult],
) -> RunDiff:
    
    previous_map = {
        r.test_case_id: r 
        for r in previous
    }

    regressions = []
    improvements = []

    for result in current:

        old = previous_map.get(result.test_case_id)

        if old is None:
            continue

        if (
            old.status == EvaluationStatus.PASS
            and result.status == EvaluationStatus.FAIL
        ):
            regressions.append(result.test_case_id)
        
        elif (
            old.status == EvaluationStatus.FAIL
            and result.status == EvaluationStatus.PASS
        ):
            improvements.append(result.test_case_id)

    previous_accuracy = calculate_accuracy(previous)
    current_accuracy = calculate_accuracy(current)


    return RunDiff(
        previous_accuracy=previous_accuracy,
        current_accuracy=current_accuracy,
        accuracy_delta=current_accuracy-previous_accuracy,
        regressions=regressions,
        improvements=improvements
    )

        

