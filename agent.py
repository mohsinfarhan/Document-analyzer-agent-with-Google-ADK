import os
from google.adk.agents.llm_agent import LlmAgent
from app.retrieval.pdf_retriever import PDFRetriever
from app.retrieval.embeddings import Embedder
from app.retrieval.vector_store import VectorStore
from app.tools.stock_api import get_stock_price

# Components remain the same
pdf_retriever = PDFRetriever(
    project_id=os.getenv("GCP_PROJECT_ID"),
    location=os.getenv("GCP_LOCATION", "us"),
    processor_id=os.getenv("GCP_PROCESSOR_ID")
)
embedder = Embedder()
vector_store = VectorStore(dimension=384)

def index_document(pdf_path: str) -> list[str]:
    """Processes a single document and adds it to the shared vector store."""
    text = pdf_retriever.extract_text(pdf_path)
    chunks = pdf_retriever.create_chunks(text)
    embeddings = embedder.get_embeddings(chunks)
    vector_store.add_to_index(chunks, embeddings)
    return chunks

# NEW: Dynamic Stock Tool
def get_any_stock_price(symbol: str) -> str:
    """
    Fetches the real-time stock price for ANY given ticker symbol.
    The agent will automatically identify the symbol from the user's query.
    """
    return get_stock_price(symbol)

def query_rag_document(query: str) -> str:
    """Queries the global vector index containing data from all uploaded reports."""
    query_embedding = embedder.get_embeddings([query])
    retrieved_chunks = vector_store.search(query_embedding, k=5) # Increased k for multi-doc
    return "\n\n".join([f"Source Context:\n{chunk}" for chunk in retrieved_chunks])

root_agent = LlmAgent(
    name="general_finance_agent",
    instruction="""
    You are a versatile financial AI. Use your tools to query the provided document 
    context (which may contain multiple company reports) and fetch real-time stock 
    data for any company mentioned. Synthesize answers based strictly on tools.
    """,
    tools=[get_any_stock_price, query_rag_document],
    model="gemini-2.5-flash"
)