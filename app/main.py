"""
FastAPI application entry point.

This module initializes the FastAPI app, sets up CORS middleware,
configures startup/shutdown events, and includes all API routes.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ application lifespan manager for startup and shutdown events"""
    #startup code- runs when app starts
    print("application starting up...")
    yield
    #shutdown code - runs when app shuts down
    print("application shutting down...")

app = FastAPI(
    title="DocuVector",
    description="RAG API for PDF document retrieval and question answering",
    version="1.0.0",
    lifespan=lifespan
)

#Add CORS middleware
app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"], 
     allow_credentials= True,
     allow_methods=["*"],
     allow_headers=["*"])

# Include routes from app.api.routes
app.include_router(router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)