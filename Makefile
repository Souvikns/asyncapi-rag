start:
	uv run fastapi dev server.py

scrape:
	uv run scripts/scrapper.py

rag:
	uv run scripts/scrapper.py
	uv run scripts/nltks.py
	uv run scripts/rag.py

setup-ollama:
	curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d '{"name": "mistral"}'
	curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d '{"name": "nomic-embed-text"}'
