import os
import psycopg2

#MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")
MIGRATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")


def run_migrations():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "maheswarareddyp"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    for filename in sorted(os.listdir(MIGRATIONS_DIR)):
        if filename.endswith(".sql"):
            path = os.path.join(MIGRATIONS_DIR, filename)
            print(f"Running migration: {filename}")
            with open(path, "r") as f:
                sql = f.read()
                cur.execute(sql)

    cur.close()
    conn.close()

if __name__ == "__main__":
    run_migrations()
