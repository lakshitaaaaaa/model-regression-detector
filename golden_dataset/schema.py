from enum import Enum

from pydantic import BaseModel

from src.feature.models import Category


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GoldenTestCase(BaseModel):
    id: str
    email: str
    expected_category: Category
    expected_summary: str
    difficulty: Difficulty
    notes: str
    # later add priority 