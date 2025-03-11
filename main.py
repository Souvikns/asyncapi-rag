from qdrant import QdrantHandler
from spec_v3 import SPEC_V3
from rag import RagWorker
import ollama

qdrant_client = QdrantHandler()
qdrant_client.instantiate_client()

rag = RagWorker(spec_docment=SPEC_V3, qdrant=qdrant_client)

if not qdrant_client.collecton_exists():
    rag.build_rag()


def ask(query: str):
    query_embed = rag.generate_emeddings(query)
    search_results = qdrant_client.get_search_results(query=query_embed)
    print(search_results)
    context = "".join(search_results)
    prompt = f"Using the following information: {context}\n\nAnswer the following query: {query}"
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response["message"]["content"]


print(ask(query="give a example asyncapi spec v3 file for kafka"))
