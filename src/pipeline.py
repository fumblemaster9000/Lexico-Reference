#pipeline.py
import os
from pathlib import Path
from parser import read_file
from splitter import split_text
from retriever import retriever

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def rag_pipeline(file_path: str = "data", persist_dir: str = "./chroma_db", model_name: str = "deepseek-r1"):
    print(f"Processing pipeline for: {file_path}")
    
    # check if database exists physically
    db_exists = os.path.exists(persist_dir) and os.listdir(persist_dir)
    force_rechunk = False
    
    # If it exists, ask the user what they want to do
    if db_exists:
        user_choice = input("Database already exists. Re-chunk data? (yes/no): ").strip().lower()
        if user_choice in ['yes', 'y']:
            print("Force re-chunking requested. Existing database will be overwritten.")
            force_rechunk = True
    
    all_chunks = []
    data_path = Path(file_path)
    
    if not data_path.exists():
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    
    #parse if db doesn't exist or if user wants to rechunk
    if not db_exists or force_rechunk:
        print("Parsing and chunking files...")
        
        for file in data_path.iterdir():
            if file.is_file() and not file.name.startswith('.'):
                print(f"Parsing: {file.name}")
                try:
                    docs = read_file(str(file))
                    chunks = split_text(docs)
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Skipping {file.name}: {e}")
                    
        print(f"Total chunks collected: {len(all_chunks)}")
    else:
        print("Reusing existing database, skipping parsing and chunking.")
         
    # if all_chunks is provided while a database already exists.
    db_retriever = retriever(all_chunks if all_chunks else None, persist_dir=persist_dir)
    #returns runnable hybrid search engine
    
    llm = ChatOllama(model=model_name, temperature=0)
    
    template = """You are an expert research assistant. Answer the user's question accurately using ONLY the provided context blocks below.

    ### Instructions:
    1. Base your answer strictly on the facts present in the context. Do not extrapolate, assume, or bring in outside knowledge.
    2. Include an inline citation immediately following every factual statement or claim you make.
    3. Use the exact filename provided in the context header (e.g., [document.pdf]) for your citations.
    4. If the context does not contain the answer, state clearly that the information is not available in the provided documents.
    5.Each piece of context is separated by a retrieval boundary ('---') and includes its source file name.

    ### Context:
    {context}

    ### Question:
    {question}

    ### Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs_with_sources(retrieved_docs): #helper function to clean inline citations
        formatted = [] #list for formatted text string
        for doc in retrieved_docs: #loop through each doc
            source = doc.metadata.get("source", "Unknown Source") #extract 'source' metadata and default to unknown
            source_name = Path(source).name #strip away path
            formatted.append(f"[Source: {source_name}]\n{doc.page_content}") #format chunk
        return "\n\n---\n\n".join(formatted) #join all formatted chunks
    
    rag_chain = (
        {"context": db_retriever | format_docs_with_sources, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    ) #function chain
    #basically a runnable
    #query -> db_rertriever -> resulting chunkobject -> format_docs_with_sources -> clean formatted chunks...-> {context}
    #query -> {question}
    #{question} + {context} -> prompt -> llm -> stroutparse()
    
    return rag_chain
