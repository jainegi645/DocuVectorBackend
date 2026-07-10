"""
RAG Service using LangChain.

Orchestrates the Retrieval-Augmented Generation pipeline:
- PDF ingestion and chunking
- Embedding generation with sentence-transformers
- Vector storage with FAISS
- Query retrieval and response generation with Groq API
"""

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings

import os
from typing import Dict, List
import logging


class RAGService:
    """
    Service for RAG pipeline operations.

    Responsibilities:
    - Load and initialize LangChain components (LLM, embeddings, vector store)
    - Ingest PDF documents and create embeddings
    - Retrieve relevant documents and generate responses
    """

    def __init__(self):
        """Initialize RAG service with LLM, embeddings, and vector store."""
        # Initialize ChatGroq LLM
        self.llm = ChatGroq(api_key=settings.groq_api_key, model=settings.groq_model)
        # Initialize HuggingFaceEmbeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.embeddings_model)
        #  Load or create FAISS index
        self.vector_store = self._load_or_create_vector_store()

    def _load_or_create_vector_store(self):
        """Load existing FAISS index or create new one"""
        try:
            # try to load existing index
            if os.path.exists(settings.faiss_index_path):
                return FAISS.load_local(
                    settings.faiss_index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
            else:
                # return new empty vector store
                return FAISS.from_texts([], self.embeddings)
        except Exception as e:
            # if loading fails,create new empty store
            logging.error(f"failed to load FAISS index: {e}")
            return FAISS.from_texts([], self.embeddings)

    def _save_vector_store(self):
        """Save the current vector store to disk."""
        try:
            self.vector_store.save_local(settings.faiss_index_path)
            logging.info("Vector store saved successfully")
        except Exception as e:
            logging.error(f"Failed to save vector store: {e}")

    def ingest_pdf(self, file_path: str):
        try:
            # Load the pdf document
            loader = PyPDFLoader(file_path)
            documents = loader.load()

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
            )
            docs = text_splitter.split_documents(documents)

            # Add documents to vector store
            self.vector_store.add_documents(docs)

            # Save the updated vector store
            self._save_vector_store()

            return {
                "status": "success",
                "file_path": file_path,
                "chunks_created": len(docs),
            }

        except Exception as e:
            logging.error(f"Error ingesting PDF {file_path}: {e}")
            return {"status": "error", "file_path": file_path, "error": str(e)}

    def query(self, query: str):
        """
        query the vector store with natural language

        """
        try:
            # Retrieve relevant documents from vector store
            relevant_docs = self.vector_store.similarity_search(
                query, k=settings.retrieval_k
            )
            if not relevant_docs:
                return {
                    "response": "I could not find any relevant information to anser your question",
                    "source": [],
                }
            
             # Build context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
             
            #Create prompt with context and question
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            {context}
            
            Question: {question}
            Helpful Answer:"""

            #Format the Prompt
            prompt = prompt_template.format(context=context, question=query)

            #Generate response using LLM
            response = self.llm.invoke(prompt)

            #extract just the text response (remove any metadata)
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)

                
            # TODO: Format and return response

            return {"response": "", "source": []}
        except Exception as e:
            logging.error(f"Error querying: {e}")
            return {
                "response": "An error ouccured with procdssing your query",
                "source": [],
                "error": str(e),
            }
