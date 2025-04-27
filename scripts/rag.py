from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, MultiVectorComparator, MultiVectorConfig
from langchain.text_splitter import NLTKTextSplitter
import os
from pathlib import Path
from pydantic import BaseModel
import ollama
from tqdm import tqdm
import uuid


BASE_DOWNLOAD_PATH = os.path.join(os.getcwd(), ".downloads")

qc = QdrantClient(host="localhost", port=6333)

class MarkdownFile(BaseModel):
    name: str
    path: str
    
    def content(self):
        with open(self.path, 'r') as file:
            content = file.read()
        return content


class MarkdownDocuments:
    def __init__(self) -> None:
        self.file_list = self.__list_files()

    def __list_files(self):
        folder_path = Path(BASE_DOWNLOAD_PATH)
        files = [f.name for f in folder_path.iterdir() if f.is_file()]

        file_list = [
            MarkdownFile(name=f, path=os.path.join(BASE_DOWNLOAD_PATH, f))
            for f in files
        ]

        return file_list
    
    def list(self) -> list[MarkdownFile]:
        return self.file_list

class Rag:
    """
    open each document split them and then create embeddings and then store them in qdrant database
    """
    def __init__(self, documents: MarkdownDocuments) -> None:
        self.qc = QdrantClient(host="localhost", port=6333)
        self.documents = documents

    def chunk_file(self, content: str):
        text_splitter = NLTKTextSplitter()

        chunks = text_splitter.split_text(content)
        return chunks
    
    def generate_embeddings(self, chunks: str | list[str]):
        total_chunks = len(chunks)
        embedding_list = []
        with tqdm(total=total_chunks, desc="Creating embedding") as bar:
            for chunk in chunks:
                embeddings = ollama.embed(model="nomic-embed-text", input=chunk)
                embedding_list.append({
                    "id": str(uuid.uuid4()),
                    "chunk": chunk,
                    "embeddings": embeddings.embeddings[0]
                })
                bar.update(1)
        
        return embedding_list


        
    def start(self):
        docs = self.documents.list()
        embed_list = []
        for doc in docs:
            chunks = self.chunk_file(doc.content())
            embeds = self.generate_embeddings(chunks)
            embed_list.append({
                "id": str(doc.name.split(".")[0]),
                "embed": embeds
            })
        for embed in embed_list:

            self.qc.recreate_collection(
                collection_name=embed["id"],
                vectors_config={
                    "vectors": VectorParams(size=768, distance=Distance.COSINE, multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM))
                }
            )

            self.qc.upsert(
                collection_name=embed["id"],
                points=[
                    PointStruct(
                        id=idx,
                        vector={"vectors": em["embeddings"]},
                        payload={"text": em["chunk"]}
                    ) for idx, em in enumerate(embed["embed"])
                ]
            )

            print(f"Embeddings Saved in qdrant client for {embed["id"]}")


if __name__ == "__main__":
    markdown_doc = MarkdownDocuments()
    rag = Rag(documents=markdown_doc)
    rag.start()

