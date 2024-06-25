import os
import argparse

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.config import EmbeddingConfig, OpenAIConfig


class Embedding:
    def __init__(self) -> None:
        self.config = EmbeddingConfig()
        self.openai_config = OpenAIConfig()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        self.embedder = OpenAIEmbeddings(
            model=self.openai_config.embedding_model,
            api_key=self.openai_config.api_key,
        )
        
        self.pdf_files = [os.path.join(self.config.pdf_dir, p) for p in os.listdir(self.config.pdf_dir) if p.endswith('.pdf')]
        assert len(self.pdf_files) > 0, "No PDF files found in the directory."
        
    @staticmethod
    def load_pdfs(pdf_files: list[str]):
        pdf_docs = [PyPDFLoader(pdf).load() for pdf in pdf_files]
        
        return [d for docs in pdf_docs for d in docs]
    
    def embed_and_save(self):
        pdf_docs = self.load_pdfs(self.pdf_files)
        documents = self.splitter.split_documents(pdf_docs)
        
        faiss_db = FAISS.from_documents(documents, self.embedder)
        faiss_db.save_local(self.config.faiss_index)
        
    def embed(self, query: str) -> list[float]:
        embedding_vector = self.embedder.embed_query(query)
        
        return embedding_vector

    
    def load_faiss(self):
        faiss_db = FAISS.load_local(self.config.faiss_index, self.embedder, allow_dangerous_deserialization=True)
        
        return faiss_db
    

if __name__ == "__main__":
    pass