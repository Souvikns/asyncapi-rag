scrape:
	python scripts/scrapper.py

rag:
	python scripts/scrapper.py
	python scripts/nltks.py
	python scripts/rag.py

setup-ollama:
	curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d '{"name": "mistral"}'
	curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d '{"name": "nomic-embed-text"}'