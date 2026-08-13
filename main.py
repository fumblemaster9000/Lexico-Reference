#main.py
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uvicorn

sys.path.append(str(Path(__file__).parent / "src"))

from src.pipeline import rag_pipeline

app = FastAPI()

# Initialize your pipeline chain
chain = rag_pipeline(file_path="data", persist_dir="chroma_db")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_pipeline(request: QueryRequest):
    try:
        def generate():
            for chunk in chain.stream(request.question):
                if hasattr(chunk, "content"):
                    yield chunk.content
                else:
                    yield str(chunk)
                    
        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        print("Starting FastAPI server on http://localhost:8000 ...")
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    else:
        print("Starting LEXICO-REFERENCE RAG Pipeline...")
        print("\nPipeline Ready, type 'exit' or 'quit' to stop. \n")
        
        while True:
            try:
                question = input("USER: ").strip()
                if not question:
                    continue
                if question.lower() in ["exit", "quit"]:
                    print("Exiting pipeline.")
                    break
                
                print("\nThinking...")
                print("\nAnswer: ", end="", flush=True)
                
                for chunk in chain.stream(question):
                    if hasattr(chunk, "content"):
                        print(chunk.content, end="", flush=True)
                    else:
                        print(str(chunk), end="", flush=True)
                        
                print("\n" + "-"*50)
                
            except KeyboardInterrupt:
                print("\nGoodbye.")
                break
            except Exception as e:
                print(f"\nError: {e}\n" + "-"*50)