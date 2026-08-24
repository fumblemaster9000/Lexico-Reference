#main.py
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uvicorn

sys.path.append(str(Path(__file__).parent / "src")) #add source directory to python's path

from src.pipeline import rag_pipeline

app = FastAPI() #instantiation of web server

#Initialize pipeline chain and build runnable
chain = rag_pipeline(file_path="data", persist_dir="chroma_db")

#enforces the api input type and handles type validation
#ensures invalid requests are discarded before reaching pipeline
class QueryRequest(BaseModel):
    question: str #validates the input must contain a key {question} with a string

#hosts http app streaming endpoint
@app.post("/query")
def query_pipeline(request: QueryRequest): #send queries into pipeline
    try:
        def generate(): #function to spit out word by word
            for chunk in chain.stream(request.question): #assigns chunk whatever the working chunk is
                if hasattr(chunk, "content"): #if the chunk object has .content attribute
                    yield chunk.content #push out the chunk contents
                else:
                    yield str(chunk) #spits out the chunk string
                    
        return StreamingResponse(generate(), media_type="text/plain") #keep the HTTP connection open and stream the plain text
    except Exception as e: #throw exception if something dies
        raise HTTPException(status_code=500, detail=str(e)) #catches any runtime error and ends stream

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve": #check if more than one arguement variable exists
        print("Starting FastAPI server on http://localhost:8000 ...")
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    else:
        print("Starting LEXICO-REFERENCE RAG Pipeline...")
        print("\nPipeline Ready, type 'exit' or 'quit' to stop. \n")
        
        while True: #chat loop
            try:
                question = input("USER: ").strip()
                if not question:
                    continue
                if question.lower() in ["exit", "quit"]:
                    print("Exiting pipeline.")
                    break
                
                print("\nThinking...")
                print("\nAnswer: ", end="", flush=True)
                
                for chunk in chain.stream(question): #live streaming for local running, no http
                    if hasattr(chunk, "content"):
                        print(chunk.content, end="", flush=True)
                    else:
                        print(str(chunk), end="", flush=True)
                        
                print("\n" + "-"*50) #text separator
                
            except KeyboardInterrupt: #catch manual interruption (Ctrl + C)
                print("\nGoodbye.")
                break
            except Exception as e: #catch unexpected runtime errors
                print(f"\nError: {e}\n" + "-"*50)