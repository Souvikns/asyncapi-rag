# AsyncAPI CHATBOT API 🐻

A specialized conversational API that provides contextual support for AsyncAPI documentation through Retrieval-Augmented Generation (RAG) technology. This intelligent interface enables developers to query and navigate AsyncAPI specifications through natural language conversations, enhancing documentation accessibility and developer productivity.


### Installation

#### Prerequisites

- Docker and Docker Compose 
- Make Utility

#### Setup Steps 

1. Start Requried Services:
Launch the Ollama LLM service and Qdrant vector database:

```bash
docker compose up -d 
```

2. Install AI models 
Set up the required models (Mistral LLM and Nomic text embedding model):

```bash 
make setup-ollama
```

3. Build Knowledge Base
Generate the Retrieval-Augmented Generation (RAG) index from AsyncAPI documentation:

```bash
make rag
```

4. Launch the API 
Start the AsyncAPI Documentation Assistant service:

```bash
make
```

