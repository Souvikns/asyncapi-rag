from qdrant_client import QdrantClient
import ollama

class Application:
    def __init__(self) -> None:
        self.qc = QdrantClient(host="localhost", port=6333)


    def search(self, query: str):
        embedding = ollama.embed(model="nomic-embed-text", input=query)
        query_embed = embedding.embeddings[0]

        search_result = self.qc.search(
            collection_name="specv3",
            query_vector=("vectors", query_embed),
            limit=5
        )

        return search_result
    
    def ask(self, query: str):
        search_result = self.search(query)
        doc = ""
        for s in search_result:
            doc += s.payload["text"] + "\n\n"
        response = ollama.generate(model="mistral", prompt=f"Read this document and answer the query: \n DOCUMENT: f{doc} \n\n QUERY: f{query}")
        return response.response


# if __name__ == "__main__":
#     app = Application()
#     # res = app.search("How to write server in spec")
#     res = app.ask("How to write server in spec")
#     print(res)
