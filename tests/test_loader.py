from src.llm.prompt_loader import load_prompt


def test_prompt_loader():
    config = load_prompt("v1_baseline.yaml")

    print(config)

    assert config.version == "v1"