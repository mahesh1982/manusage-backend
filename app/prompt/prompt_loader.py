from .prompt_repository import PromptRepository

class PromptLoader:
    def __init__(self, dsn: str):
        self.repo = PromptRepository(dsn)

    async def load(self, prompt_name: str) -> str:
        return await self.repo.get_active_prompt(prompt_name)
