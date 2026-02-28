from .summarizer_agent import SummarizerAgent
from app.evaluation.llm_judge import LLMJudge

class EvaluatorAgent:
    def __init__(self):
        self.judge = LLMJudge()

    async def evaluate(self, question, answer, context):
        return await self.judge.score(question, answer, context)
