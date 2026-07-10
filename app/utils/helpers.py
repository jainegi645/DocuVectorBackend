"""
Utility helper functions.

Pure functions for validation, formatting, and other utilities
that don't depend on the RAG service state.
"""

def validate_pdf_file(filename: str) -> bool:
    """Validate that file is a PDF."""
    return filename.lower().endswith('.pdf')

def format_response_text(text: str, max_length: int = None) -> str:
    """Format response text (truncate if needed)."""
    if max_length and len(text) > max_length:
        return text[:max_length] + "..."
    return text

# TODO: Add more utility functions as needed