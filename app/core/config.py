"""
Configuration loader for DocuVector.

Loads environment variables from .env and provides default values.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration from .env or environment."""
    
    # Groq API Configuration
    groq_api_key: str  # Required - must be in .env
    groq_model: str = "mixtral-8x7b-32768"  # LLM model name
    
    # RAG Pipeline Configuration
    chunk_size: int = 500  # PDF chunk size
    chunk_overlap: int = 100  # Overlap between chunks
    retrieval_k: int = 3  # Number of documents to retrieve
    embeddings_model: str = "sentence-transformers/multi-qa-mpnet-base-cos-v1"
    faiss_index_path: str = "embeddings/index"  # Where to store FAISS index
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()