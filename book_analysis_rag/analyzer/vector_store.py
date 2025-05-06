from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        
    def embed(self, texts):
        return self.model.encode(texts, show_progress_bar=False).tolist()
    

class ChromaClient:
    def __init__(self, collection_name="article_chunks", persist_dir=".chrome"):
        self.client = chromadb.PersistentClient(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_dir,
            )
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def add_chunks(self, article_id, chunks, embeddings):
        ids = [f"{article_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"article_id": article_id, "chunk_id": i} for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
    def query(self, query_text, embedding_service, n_results=5):
        query_vector = embedding_service.embed([query_text])[0]
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=n_results,
        )
        return results
