"""
Pydantic models for request/response validation.

These models validate incoming requests and outgoing responses,
ensuring type safety and providing API documentation.
"""

from pydantic import BaseModel
from typing import List

# Request Models
class QueryRequest(BaseModel):
    """Request body for /api/query endpoint."""
    query: str

# Response Models
class SourceDocument(BaseModel):
    """Source document reference in response."""
    file: str
    page: int

class QueryResponse(BaseModel):
    """Response body for /api/query endpoint."""
    response: str
    sources: List[SourceDocument]

class IngestResponse(BaseModel):
    """Response body for /api/ingest endpoint."""
    status: str
    file_path: str
    chunks_created: int

class DocumentInfo(BaseModel):
    """Document metadata for /api/documents endpoint."""
    file: str
    chunks: int
    ingested_at: str

class ErrorResponse(BaseModel):
    """Standard error response."""
    status: str = "error"
    message: str
    error_code: str