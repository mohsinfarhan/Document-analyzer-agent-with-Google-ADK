import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

class PDFRetriever:
    def __init__(self, project_id: str, location: str, processor_id: str, chunk_size: int = 600, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        self.client = documentai.DocumentProcessorServiceClient(client_options=opts)

    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing PDF at: {file_path}")
            
        name = self.client.processor_path(self.project_id, self.location, self.processor_id)
        
        with open(file_path, "rb") as image:
            image_content = image.read()

        raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        
        result = self.client.process_document(request=request)
        return " ".join(result.document.text.split())

    def create_chunks(self, text: str) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += (self.chunk_size - self.overlap)
        return chunks