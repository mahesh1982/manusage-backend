from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class SummarizerAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, temperature=0)

        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following text:\n\n{text}"
        )

    async def run(self, text):
        prompt = self.prompt.format(text=text)
        result = self.llm.invoke(prompt)
        return result.content
