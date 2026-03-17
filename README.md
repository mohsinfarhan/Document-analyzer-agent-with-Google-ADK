# Financial Document Analyzer Agent with Google ADK

A multi-document financial Retrieval-Augmented Generation (RAG) agent built with **FastAPI** and Google Cloud's **Agent Development Kit (ADK)**. This agent processes financial reports (PDFs), indexes them in a vector store, and provides intelligent answers using **Gemini 2.5 Flash**. It also features real-time stock price retrieval using the Alpha Vantage API.

## 🚀 Features

- **Multi-Document Indexing**: Automatically processes all PDF reports in the `data/reports/` directory on startup.
- **Intelligent Extraction**: Uses **Google Cloud Document AI** for high-accuracy text extraction from complex financial documents.
- **Semantic Search**: Implements a RAG pipeline with `sentence-transformers` for embeddings and `FAISS` for efficient similarity search.
- **Dynamic Tools**: 
    - `query_rag_document`: Search through indexed financial reports.
    - `get_any_stock_price`: Fetch real-time stock data (via Alpha Vantage).
- **Modern LLM**: Powered by `gemini-2.5-flash` for synthesizing complex financial insights.

## 🛠️ Project Structure

```text
finance-rag-agent/
├── app/
│   ├── retrieval/          # RAG logic (Embeddings, Vector Store, PDF Processor)
│   ├── tools/              # Agent tools (Stock API)
│   ├── agent.py            # ADK Agent definition and tool mapping
│   ├── main.py             # FastAPI entry point & startup indexing
│   └── schemas.py          # Pydantic request/response models
├── data/
│   └── reports/            # Place your PDF financial reports here
├── test/                   # API test scripts
├── .env                    # Configuration and API keys
├── pyproject.toml          # Dependencies and project metadata
└── README.md               # You are here
```

## ⚙️ Setup

### Prerequisites

1. **Python 3.11+**
2. **Google Cloud Project**:
    - Enable **Document AI API**.
    - Create a **Processor** (e.g., OCR or Document OCR).
3. **API Keys**:
    - [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)
    - [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Installation

1. Clone the repository and navigate to the project directory.
2. Install dependencies (using `uv` or `pip`):
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If using `uv`, run `uv sync`.*

3. Create a `.env` file in the root directory:
   ```env
   ALPHA_VANTAGE_KEY=your_alpha_vantage_key
   GEMINI_API_KEY=your_gemini_api_key
   GCP_PROJECT_ID=your_gcp_project_id
   GCP_LOCATION=us
   GCP_PROCESSOR_ID=your_document_ai_processor_id
   ```

### Running the Application

1. Place your financial PDF reports in `data/reports/`.
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The application will index all documents in the `data/reports/` folder on startup.

## 📖 Usage

### Query the Agent

Send a POST request to `/query`:

**Endpoint**: `POST http://localhost:8000/query`

**Payload**:
```json
{
  "query": "What was the revenue growth for Google in the latest report, and what is its current stock price?"
}
```

**Response**:
The agent will retrieve context from the indexed PDFs and fetch the real-time stock price to provide a synthesized answer.

## 🧪 Testing

Run the provided test script to verify the API:
```bash
python test/test_api.py
```
