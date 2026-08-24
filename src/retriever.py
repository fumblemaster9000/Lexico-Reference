#retriever.py
import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document

def retriever(chunks=None, persist_dir="./chroma_db", k=3):
    #Initialize Chroma Retriever
    
    embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") #initialize vector model in langchain wrapper
    
    if chunks is None:
        #set up vector store and retrieval
        db = Chroma(
            persist_directory=persist_dir,
            embedding_function=embed
        )
        stored_data = db.get() #load local database into stored data
        chunks = [
            Document(page_content=text, metadata=meta)
            for text, meta in zip(stored_data["documents"], stored_data["metadatas"])
        ] #loop through paired metadata and text items and wrap in langchain doc for chunks
    else:
        #Clear the old database directory if it exists to keep data fresh
        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)
            
        #Set up vector store and retrieval
        db = Chroma.from_documents(
            documents = chunks,
            embedding = embed,
            persist_directory = persist_dir
        )
        
    vector = db.as_retriever(search_kwargs={"k": k}) #turns data base into search tool, "meaning"
    #cut off search results at top k items (search_kwargs={"k": k}), 3 in this case
    
    #BM25 set up for keyword matching, "exact words"
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = k
    
    #Combine both methods 50/50 using rank fusion, "both meaning and exactness"
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector],
        weights=[0.5, 0.5]
    )
    
    return ensemble_retriever #return useable hybrid search engine