#retriever.py
import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

def retriever(chunks, persist_dir="./chroma_db", k=3):
    #Initialize Chroma Retriever
    
    #Clear the old database directory if it exists to keep data fresh
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
        
    embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    #Set up vector store and retrieval
    db = Chroma.from_documents(
        documents = chunks,
        embedding = embed,
        persist_directory = persist_dir
    )
    vector = db.as_retriever(search_kwargs={"k": k})
    
    #BM25 set up for keyword matching
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = k
    
    #Combine both methods 50/50 using rank fusion
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector],
        weights=[0.5,0.5]
    )
    
    return ensemble_retriever