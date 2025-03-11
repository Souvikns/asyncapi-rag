from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, MultiVectorConfig, MultiVectorComparator



class QdrantHandler():
    def __init__(self):
        self._qdrant_instance = None
        self.collection_name = "asyncapi_v3"

    def instantiate_client(self):
        if self._qdrant_instance == None:
            self._qdrant_instance = QdrantClient(path="./qdb")
    
    def save(self, embeddings: list):
        if self._qdrant_instance == None:
            return
        
        self._qdrant_instance.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={"vectors": VectorParams(size=768, distance=Distance.COSINE, multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM))},
            
        )

        self._qdrant_instance.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=idx,
                    vector={"vectors": em["embedding"]},
                    payload={"text": em["chunk"]}
                ) for idx, em in enumerate(embeddings)
            ]
        )

        print("Embeddings saved in qdrant client")

    def get_search_results(self, query):
        if self._qdrant_instance == None:
            return 
        
        # print(type(query), len(query[0].tolist()))
        
        search_results = self._qdrant_instance.search(
            collection_name=self.collection_name,
            query_vector=("vectors", query),
            limit=5
        )
        results = []
        for search_result in search_results:
            results.append(
                search_result.payload["text"]
            )
        return results
    
    def collecton_exists(self):
        if self._qdrant_instance == None:
            return
        
        return self._qdrant_instance.collection_exists(self.collection_name)
    
        