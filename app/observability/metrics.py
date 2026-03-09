from dataclasses import dataclass, field
from typing import List

@dataclass
class EvaluationMetrics:
    judge_scores: List[float] = field(default_factory=list)

    def add_judge_score(self, score: float):
        if score is not None:
            self.judge_scores.append(score)

    @property
    def avg_judge_score(self):
        if not self.judge_scores:
            return None
        return sum(self.judge_scores) / len(self.judge_scores)
