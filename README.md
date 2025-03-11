# AsyncAPI RAG

### Setup
To run this project you would need ollama running on your computer on port :11434 I wouold use docker for it also install "mistral" model. 

**SETUP OLLAMA**

```bash
docker compose up -d 
```

This should get your ollama server running on port :11434

**SETUP PYTHON DEPENDENCIES**

First create a python enviornment this has been built using python 3.11.9 so that is recommended. 

```bash
python -m venv .env

./.venv/scripts/activate # on windows
```

Then install the dependencies 

```bash
pip install -r requirements.txt
```

**TO RUN**

To run the project just run the main.py file using 

```bash
python main.py
```
