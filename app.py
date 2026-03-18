import shutil
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

from main import load_documents, split_text, query_rag_system
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings


app = FastAPI(title = "Simko Custom RAG")


UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
INDEX_NAME = "simkoyragy"

class QueryRequest(BaseModel):
    prompt: str

@app.post("/upload")
async def uploadfile(file: UploadFile = File(...)):
    """Receives a PDF, saves it temporarily, and indexes it into Pinecone."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail = "Only PDF files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:

        with open(file_path, "wb") as bufffer:
            content = await file.read() # Read the stream
            bufffer.write(content)
        
        docs = load_documents(UPLOAD_DIR)
        chunks = split_text(docs)


        embedding = OpenAIEmbeddings()

        PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embedding, 
            index_name = INDEX_NAME
        )

        os.remove(file_path)

        return {"messages": f"Successfully indexed {file.filename}", "chunks": len(chunks)}
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail = str(e))

@app.post("/ask")
async def ask_question(request: QueryRequest):
    """Answers questions based on the uploaded documents."""
    try:
        # 1. Initialize Embeddings and Vector Store connection
        embeddings = OpenAIEmbeddings()
        vector_store = PineconeVectorStore(
            index_name=INDEX_NAME, 
            embedding=embeddings
        )

        # 2. Pass both the prompt AND the vector_store to your function
        response = query_rag_system(request.prompt, vector_store)
        
        return {'answer': response}
    except Exception as e:
        print(f"Error in /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Changing to 8080 or another common port can help avoid conflicts
    uvicorn.run(app, host="0.0.0.0", port=8001)