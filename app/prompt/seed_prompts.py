import os
import psycopg2

def seed_initial_prompt():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "maheswarareddyp"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    prompt_name = "rag_system_prompt"
    version = 1
    content = """
                    You are ManusAge, an expert system for ink age estimation and document analysis.
                    Use retrieved context strictly. If context is missing, say No.
                    Provide concise, factual answers.
            """

    cur.execute(
        """
        INSERT INTO prompt_versions (prompt_name, version, content, is_active)
        VALUES (%s, %s, %s, TRUE)
        ON CONFLICT DO NOTHING;
        """,
        (prompt_name, version, content),
    )

    cur.close()
    conn.close()
    print("Seeded rag_system_prompt.")

if __name__ == "__main__":
    seed_initial_prompt()
