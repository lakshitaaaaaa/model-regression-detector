"""
Utility for loading and validating the golden evaluation dataset.
"""

import json
from pathlib import Path

from golden_dataset.schema import GoldenTestCase

DATASET_DIR = Path(__file__).parent


def load_dataset(filename: str | Path) -> list[GoldenTestCase]:
    """
    Load and validate a golden dataset.

    Args:
        filename: Either a bare filename resolved against the default
                  golden_dataset/ directory (e.g. "test_cases_v1.json"),
                  or a full/absolute Path pointing anywhere else
                  (e.g. a test fixture path).

    Returns:
        A list of validated GoldenTestCase objects.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If the JSON is malformed or not a list.
        ValidationError: If any test case does not match the schema.
    """
    dataset_path = DATASET_DIR / filename

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    try:
        with dataset_path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

            if not isinstance(raw_data, list):
                raise ValueError("Dataset JSON must contain a list of test cases.")
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in dataset: {dataset_path}") from e

    validated_cases = [
        GoldenTestCase.model_validate(case)
        for case in raw_data
    ]

    return validated_cases