"""
CLI entrypoint: runs the full eval pipeline end to end
(load prompt -> run golden dataset -> score -> diff -> report -> alert).
"""

from src.eval.runner import EvaluationRunner
from src.feature.classifier import EmailClassifier
from src.llm.groq_client import GroqClient
from src.llm.prompt_loader import load_prompt
from src.eval.scoring import calculate_accuracy, count_results
from src.storage.run_history import save_run


def main():
    config = load_prompt("v1_baseline.yaml")

    llm = GroqClient()

    classifier = EmailClassifier(
        llm=llm,
        prompt_config=config,
    )

    runner = EvaluationRunner(classifier)

    results = runner.run()

    for result in results:
        print(result)

    accuracy = calculate_accuracy(results)
    count = count_results(results)

    print("-"*60)

    print(f"Total test cases : {len(results)}")

    print(f"\nPassed           : {count[0]}")
    print(f"Failed           : {count[1]}")
    print(f"Error.           : {count[2]}")

    print(f"\nAccuracy         : {accuracy:.2f}%")

    filepath = save_run(results)
    print(f"\nSaved run to: {filepath}")
    
    print("-"*60)


if __name__ == "__main__":
    main()


"""
so as of now, we have json dataset-> pydantic validation-> evaluation runner -> email classifier -> groq api -> structured output -> evaluation result
"""