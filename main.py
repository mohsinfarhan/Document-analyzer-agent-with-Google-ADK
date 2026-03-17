import os
import glob
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.schemas import QueryRequest, QueryResponse
from app.agent import root_agent, index_document

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Initializing Multi-Document Financial Index...")
    
    # Path to your reports directory
    reports_dir = "data/reports"
    pdf_files = glob.glob(os.path.join(reports_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"Warning: No PDF files found in {reports_dir}")
    
    for pdf_path in pdf_files:
        try:
            print(f"Processing: {os.path.basename(pdf_path)}...")
            chunks = index_document(pdf_path)
            print(f"Successfully indexed {len(chunks)} chunks from {os.path.basename(pdf_path)}.")
        except Exception as e:
            print(f"Failed to index {pdf_path}: {e}")
            
    print("Multi-Document Indexing Complete.")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    try:
        # The agent now handles dynamic tickers and multi-doc retrieval automatically
        response = root_agent.run(request.query)
        
        return QueryResponse(
            query=request.query,
            answer=response.text,
            sources=["Context retrieved from global multi-document vector store"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")