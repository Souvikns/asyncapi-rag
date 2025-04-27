from fastapi import FastAPI, Response
from app import Application


app = FastAPI()
asyncapi_rag = Application()


@app.get("/")
def root():
    return Response(content="AsyncAPI RAG API.")

@app.post("/chat")
def chat(message: str):
    # Chat endpoint to chat with AsyncAPI spec and tool docs context
    res = asyncapi_rag.ask(query=message)
    return {"response": res}
