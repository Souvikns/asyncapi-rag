from langchain_text_splitters import MarkdownTextSplitter 
from qdrant import QdrantHandler
from sentence_transformers import SentenceTransformer
from spec_v3 import SPEC_V3
import uuid


class RagWorker():
    def __init__(self, spec_docment: str, qdrant: QdrantHandler=None):
        self._spec_document = spec_docment
        self._qdrant = qdrant
        self._inference = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1",
            trust_remote_code=True,
            cache_folder="./cache"
        )
    
    def _split_text(self):
        splitter = MarkdownTextSplitter()
        splitter._chunk_size = 500
        splitter._chunk_overlap = 50

        documents = splitter.split_text(self._spec_document)
        return documents
    
    def generate_emeddings(self, content: str) -> list:
        embeddings = self._inference.encode([content])
        return embeddings

    def build_rag(self):
        chunks = self._split_text()
        sd = []
        for chunk in chunks:
            sd.append({
                "id": str(uuid.uuid4()),
                "chunk": chunk,
                "embedding": self.generate_emeddings(content=chunk)
            })

        self._qdrant.save(embeddings=sd)

    


