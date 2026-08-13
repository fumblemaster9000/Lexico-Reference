#main.py
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

sys.path.append(str(Path(__file__).parent / "src"))

from src.pipeline import rag_pipeline

# Creates the FastAPI app instance for handling web requests
app = FastAPI()

#Initialize
chain = rag_pipeline(file_path = "data", persist_dir="chroma_db")

# Defines the expected JSON schema with a 'question' field for API requests
class QueryRequest(BaseModel):
    question: str

# Creates an API endpoint that listens for POST requests at /query
@app.post("/query")
def query_pipeline(request: QueryRequest):
    try:
        response = chain.invoke(request.question)
        return {"answer": response}
    except Exception as e:
        # Returns a 500 server error response if an exception occurs
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Checks if the 'serve' argument was passed to run the FastAPI server
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        print("Starting FastAPI server on http://localhost:8000 ...")
        # Runs the FastAPI application using Uvicorn on localhost port 8000
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    else:
        print("Starting LEXICO-REFERENCE RAG Pipeline...")
        
        #Initialize
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
                response = chain.invoke(question)
                print(f"\nAnswer: \n{response}\n" + "-"*50)
                
            except KeyboardInterrupt:
                print("\nGoodbye.")
                break
            except Exception as e:
                print(f"\nError: {e}\n" + "-"*50)