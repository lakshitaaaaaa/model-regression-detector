from src.feature.classifier import EmailClassifier
from src.llm.groq_client import GroqClient
from src.llm.prompt_loader import load_prompt

def main():
    config = load_prompt("v1_baseline.yaml")

    llm = GroqClient()

    classifier= EmailClassifier(
        llm=llm,
        prompt_config=config,
    )

    email = """
    Hey,

    My credit card has been charged twice this month.
    Please refund the duplicate payment.

    Thanks.
    """

    result = classifier.classify(email)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()