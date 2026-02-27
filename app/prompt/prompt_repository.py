import asyncpg

class PromptRepository:
    def __init__(self, dsn: str):
        self.dsn = dsn

    async def get_active_prompt(self, prompt_name: str) -> str:
        conn = await asyncpg.connect(self.dsn)

        row = await conn.fetchrow(
            """
            SELECT content 
            FROM prompt_versions
            WHERE prompt_name = $1 AND is_active = TRUE
            ORDER BY version DESC
            LIMIT 1;
            """,
            prompt_name
        )

        await conn.close()

        if row:
            return row["content"]
        return None

    async def add_prompt(self, prompt_name: str, version: int, content: str):
        conn = await asyncpg.connect(self.dsn)

        await conn.execute(
            """
            INSERT INTO prompt_versions (prompt_name, version, content)
            VALUES ($1, $2, $3)
            """,
            prompt_name, version, content
        )

        await conn.close()
