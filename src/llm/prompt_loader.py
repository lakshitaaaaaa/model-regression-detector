"""
Loads and parses versioned prompt YAML files from /prompts into
PromptConfig objects for use by the classifier and eval runner.
"""

# its responsibility: v1_baseline.yaml ->read yaml -> promptConfig
# this keeps our EmailClassifier independent of how prompts are stored
# this file reads a YAML prompt file and converts it into a PromptConfig object

from pathlib import Path

import yaml

from src.feature.config import PromptConfig

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"

def load_prompt(filename: str) -> PromptConfig:
    prompt_path = PROMPTS_DIR/filename

    with open(prompt_path,"r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return PromptConfig(**data)