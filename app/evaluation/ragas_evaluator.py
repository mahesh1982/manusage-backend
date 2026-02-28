from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_precision,
    context_recall
)

class RAGASEvaluator:
    def __init__(self):
        self.metrics = [
            faithfulness,
            answer_relevance,
            context_precision,
            context_recall
        ]

    async def run(self, dataset):
        return evaluate(dataset, metrics=self.metrics)
