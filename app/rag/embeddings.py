from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str):
        return self.model.encode(text).tolist()

    def embed_documents(self, docs: list[str]):
        return [self.model.encode(d).tolist() for d in docs]
