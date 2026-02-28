CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS prompt_versions (
  id SERIAL PRIMARY KEY,
  prompt_name VARCHAR(100) NOT NULL,
  version INTEGER NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  metadata JSONB,
  embedding VECTOR(384)
);
