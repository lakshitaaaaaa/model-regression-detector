"""Unit tests for src/eval diff/comparison logic."""
import pytest
from src.eval.diff import compare_runs
from src.eval.models import EvaluationResult, EvaluationStatus
from src.feature.models import Category

def make_result(
        case_id: str,
        status: EvaluationStatus,
) -> EvaluationResult:
    
    return EvaluationResult(
        test_case_id=case_id,
        expected_category=Category.BILLING,
        predicted_category=Category.BILLING,
        expected_summary="",
        predicted_summary="",
        status=status,
        latency_ms=10,
    )

def test_compare_runs():

    previous = [
        make_result("TC001", EvaluationStatus.PASS),
        make_result("TC002", EvaluationStatus.PASS),
        make_result("TC003", EvaluationStatus.FAIL),
    ]

    current = [
        make_result("TC001", EvaluationStatus.PASS),
        make_result("TC002", EvaluationStatus.FAIL),
        make_result("TC003", EvaluationStatus.PASS),
    ]

    diff = compare_runs(previous, current)

    assert diff.regressions == ["TC002"]
    assert diff.improvements == ["TC003"]
    assert diff.previous_accuracy == pytest.approx(66.6666666667)
    assert diff.current_accuracy == pytest.approx(66.6666666667)
    assert diff.accuracy_delta == pytest.approx(0.0)