"""
FastAPI route handlers.

Defines the API endpoints:
- POST /api/ingest - Upload PDF
- POST /api/query - Ask question
- GET /api/documents - List documents
- DELETE /api/documents/{filename} - Delete document
"""

from math import exp

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from langsmith import expect
from sqlalchemy import exists
from sympy import content
from app.utils.helpers import validate_pdf_file
from app.schemas.models import QueryRequest, QueryResponse, IngestResponse, ErrorResponse
from app.services.rag_service import RAGService
import os

router = APIRouter(prefix="/api", tags=["rag"]) 

def get_rag_service() -> RAGService:
    """Dependency injection for RAGService."""
    return RAGService()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_pdf(file: UploadFile = File(...), rag_service: RAGService = Depends(get_rag_service)):
    """
    Ingest a PDF document.
    - **file**: PDF file to upload
    
    Returns IngestResponse with file path and chunks created.
    """
    #1.Validate file is PDF
    if not validate_pdf_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. only pdf are expected"
        )
    
    #2.Save file
    file_path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)

    # Write uploaded file to disk
    with open(file_path,"wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
         # 3. Process with RAG service
        result = rag_service.ingest_pdf(file_path)
        return result
    except Exception as e:
         # 4. Cleanup on error - remove file if processing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing pdf: {str(e)}")

    

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, rag_service: RAGService = Depends(get_rag_service)):
    """
    Query the vector store with a natural language question.
    
    - **request**: QueryRequest with question
    
    Returns QueryResponse with answer and sources.
    """
    # TODO: Validate 
    try:
        result = rag_service.query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Error processing query: {str(e)}")

@router.get("/documents")
async def list_documents(rag_service: RAGService = Depends(get_rag_service)):
    """List all ingested documents with metadata."""
    # TODO: Implement document listing
    pass

@router.delete("/documents/{filename}")
async def delete_document(filename: str, rag_service: RAGService = Depends(get_rag_service)):
    """Delete a document from the vector store."""
    # TODO: Implement document deletion
    pass