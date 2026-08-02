"""
CLI entrypoint: runs the full eval pipeline end to end
(load prompt -> run golden dataset -> score -> diff -> report -> alert).
"""

from src.eval.runner import EvaluationRunner
from src.feature.classifier import EmailClassifier
from src.llm.groq_client import GroqClient
from src.llm.prompt_loader import load_prompt
from src.eval.scoring import calculate_accuracy, count_results
from src.storage.run_history import (
    latest_run,
    load_run,
    save_run
)

from src.eval.diff import compare_runs
from src.eval.scoring import (
    calculate_accuracy,
    count_results
)

from src.eval.simple_judge import SimpleEvaluationJudge


def main():
    config = load_prompt("v1_baseline.yaml")

    llm = GroqClient()

    classifier = EmailClassifier(
        llm=llm,
        prompt_config=config,
    )

    judge = SimpleEvaluationJudge()

    runner = EvaluationRunner(
        classifier=classifier,
        summary_judge=judge
    )

    previos_file = latest_run()
    previous_results = None

    if previos_file is not None:
        previous_results = load_run(previos_file)

    results = runner.run()

    passed, failed, errors = count_results(results)
    accuracy = calculate_accuracy(results)


    print("-"*60)

    print(f"Total test cases : {len(results)}")

    print(f"\nPassed           : {passed}")
    print(f"Failed           : {failed}")
    print(f"Error.           : {errors}")

    print(f"\nAccuracy         : {accuracy:.2f}%")

    if previous_results is not None:

        diff = compare_runs(previous_results, results)

        print("\nRegression Summary")
        print("-" * 60)

        print(
            f"Previous Accuracy : "
            f"{diff.previous_accuracy:.2f}%"
        )

        print(
            f"Current Accuracy : "
            f"{diff.current_accuracy:.2f}%"
        )

        print(
            f"Accuracy Delta :"
            f"{diff.accuracy_delta:.2f}%"
        )

        print()

        print(f"New Regressions : {len(diff.regressions)}")

        if diff.regressions:
            for tc in diff.regressions:
                print(f"  - {tc}")

        print()

        print(f"Improvements : {len(diff.improvements)}")

        if diff.improvements:
            for tc in diff.improvements:
                print(f"  + {tc}")


        print("-"*60)

        filepath = save_run(results)
        print(f"\nSaved run to: {filepath}")


if __name__ == "__main__":
    main()


"""
so as of now, we have json dataset-> pydantic validation-> evaluation runner -> email classifier -> groq api -> structured output -> evaluation result
"""