"""
Docstring for src.eval.judge

only checking expected_category == actual_category for evaluation is wrong.
two completely different summaries can still generate same category.
for eg) summary1> Customer disputes a transaction on their account statement and requests an investigation.
summary2> Customer wants to open a savings account.
both will give category : billing

thus, we should check summary quality as well.

what we can do?
1) prediction.summary == expected.summary is completely WRONG
2) embedding similarity (cosine similarity)
3) ROUGE/ BLEU -> traditional nlp metrics
4) LLM-as-a-Judge

LLM-as-a-Judge
example prompt :
You are evaluating two summaries.

Reference:
Customer disputes unauthorized charge...

Candidate:
Customer disputes duplicate transaction...

Score from 1-5.

Explain briefly.

this is how tools like LangSmith, OpenAI Evals, and many internal evaluation pipelines assess open-ended text


WHAT DO WE WANT?
something like this-
Accuracy

92.31%

Summary Quality

4.72 / 5

Average Latency

36 ms
"""

from abc import ABC, abstractmethod
from src.eval.models import SummaryEvaluation

class BaseSummaryJudge(ABC):

    @abstractmethod
    def evaluate(
            self,
            expected: str,
            predicted: str,
    ) -> SummaryEvaluation:
        
        raise NotImplementedError