import os
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class DocumentLoader:
    def __init__(self, data_dir: str = "data/documents"):
        self.data_dir = data_dir

    def load(self) -> List[Document]:
        documents = []

        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        for file_name in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file_name)

            if file_name.endswith(".txt"):
                loader = TextLoader(file_path)
                documents.extend(loader.load())

            elif file_name.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

            else:
                # Skip unsupported formats for now
                continue

        return documents
