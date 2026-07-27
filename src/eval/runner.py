# its job is to run classifier.classify(email) for each testcase in the dataset, measure latency and return EvaluationResult
import time

from golden_dataset.loader import load_dataset
from src.eval.models import EvaluationResult, EvaluationStatus
from src.feature.classifier import EmailClassifier
from src.eval.scoring import evaluate_category

class EvaluationRunner:
    # this will run the email classifier against the golden data

    def __init__(
            self,
            classifier: EmailClassifier,
            dataset_file: str = "test_cases_v1.json",
        ):
        self.classifier = classifier
        self.dataset_file = dataset_file

    def run(self) -> list[EvaluationResult]:
        # this will evaluate every testcase in the dataset
        dataset = load_dataset(self.dataset_file)
        results: list[EvaluationResult] = []

        for test_case in dataset:

            try:
                start = time.perf_counter()
                prediction = self.classifier.classify(test_case.email)

                latency_ms = (time.perf_counter() - start) * 100

                status = evaluate_category(
                    prediction,
                    test_case,
                )

                results.append(
                    EvaluationResult(
                        test_case_id=test_case.id,

                        expected_category=test_case.expected_category,
                        predicted_category=prediction.category,

                        expected_summary=test_case.expected_summary,
                        predicted_summary=prediction.summary,

                        status=status,

                        latency_ms=latency_ms,
                    )
                )

            except Exception as e:

                results.append(
                    EvaluationResult(
                        test_case_id=test_case.id,

                        expected_category=test_case.expected_category,
                        predicted_category=test_case.expected_category,

                        expected_summary=test_case.expected_summary,
                        predicted_summary=test_case.expected_summary,

                        status=EvaluationStatus.ERROR,

                        latency_ms=0,

                        error_message=str(e)
                    )
                )


        return results
    
# it doesn't know anything about sqlLite, HTML, Slack, Accuracy, Reports. it only has a single responsibility
        