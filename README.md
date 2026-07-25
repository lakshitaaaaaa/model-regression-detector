# Model Regression Detection System

CI/CD-style pipeline that tests an LLM feature against a golden dataset on
every prompt change, detects quality regressions, and alerts the team via
Slack before bad outputs reach users.

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in GROQ_API_KEY, SLACK_WEBHOOK_URL
3. `python scripts/run_eval.py`

## Adding test cases
Use `scripts/add_test_case.py` or edit `golden_dataset/` directly — see
`golden_dataset/CHANGELOG.md` for versioning convention.

## Adjusting thresholds
Configured in `src/eval/significance.py` (warning: 3% delta, critical: 8%).

## Architecture decisions
See inline docstrings in each module for rationale.
