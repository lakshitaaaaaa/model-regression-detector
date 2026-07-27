from pathlib import Path

import pytest
from pydantic import ValidationError

from golden_dataset.loader import load_dataset
from golden_dataset.schema import GoldenTestCase, Difficulty
from src.feature.models import Category

FIXTURES_DIR = Path(__file__).parent/"fixtures"

def test_load_dataset_returns_expected_count():
    dataset = load_dataset("test_cases_v1.json")
    assert len(dataset) == 13


def test_load_dataset_returns_valid_type():
    dataset = load_dataset("test_cases_v1.json")
    assert all(isinstance(case, GoldenTestCase) for case in dataset)


def test_specific_case_fields_are_correct():
    dataset = load_dataset("test_cases_v1.json")
    tc001 = next(case for case in dataset if case.id == "TC001")

    assert tc001.expected_category == Category.BILLING
    assert tc001.difficulty == Difficulty.MEDIUM
    assert "unauthorized transaction" in tc001.expected_summary.lower()


def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_dataset("does_not_exist.json")


def test_invalid_dataset_raises_validation_error():
    with pytest.raises(ValidationError):
        load_dataset(FIXTURES_DIR / "invalid_dataset.json")


def test_invalid_json_raises_value_error():
    with pytest.raises(ValueError):
        load_dataset(FIXTURES_DIR / "bad_json.json")