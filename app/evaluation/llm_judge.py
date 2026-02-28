from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class LLMJudge:
    def __init__(self, model="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, temperature=0)

        self.prompt = PromptTemplate(
            input_variables=["question", "answer", "context"],
            template=(
                "You are an impartial evaluator.\n"
                "Question: {question}\n"
                "Answer: {answer}\n"
                "Context: {context}\n\n"
                "Evaluate the answer on correctness, groundedness, and completeness.\n"
                "Return a score from 1 to 10 and a short justification."
            )
        )

    async def score(self, question, answer, context):
        prompt = self.prompt.format(
            question=question,
            answer=answer,
            context=context
        )
        result = self.llm.invoke(prompt)
        return result.content
