#retriever.py
import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def retriever(chunks, persist_dir="./chroma_db", k=3):
    #Initialize Chroma Retriever
    
    #Clear the old database directory if it exists to keep data fresh
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
        
    embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db = Chroma.from_documents(
        documents = chunks,
        embedding = embed,
        persist_directory = persist_dir
    )
    
    return db.as_retriever(search_kwargs = {"k": k})