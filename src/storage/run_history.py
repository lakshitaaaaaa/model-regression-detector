from datetime import datetime
from pathlib import Path
import json

from src.eval.models import EvaluationResult

RUN_HISTORY_DIR = Path("data/run_history")

def save_run(results: list[EvaluationResult]) -> Path:
    # saving one evaluation run as a json snapshot

    RUN_HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = RUN_HISTORY_DIR / f"run_{timestamp}.json"

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(
            [r.model_dump(mode="json") for r in results],
            f,
            indent=4,
        )

    return filepath

#model_dump(mode="json") will personally serialize enums into strings

def load_run(filepath: Path) -> list[EvaluationResult]:

    with filepath.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return [
        EvaluationResult.model_validate(item)
        for item in data
    ]

def latest_run() -> Path | None:

    files = sorted(
        RUN_HISTORY_DIR.glob("run_*.json")
    )

    if not files:
        return None
    
    return files[-1]