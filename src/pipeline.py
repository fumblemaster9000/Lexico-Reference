#pipeline.py
import os
from pathlib import Path
from parser import read_file
from splitter import split_text
from retriever import retriever

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

def rag_pipeline(file_path: str = "data", persist_dir: str = "./chroma_db", model_name: str = "deepseek-r1"):
    print(f"Processing pipeline for: {file_path}")
    
    db_exists = os.path.exists(persist_dir) and os.listdir(persist_dir)
    
    all_chunks = []
    data_path = Path(file_path)
    
    if not data_path.exists():
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    
    if not db_exists:
        print("Database not found. Parsing and chunking files...")
        
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
        print("Database already exists, skipping parsing and chunking.")

    db_retriever = retriever(all_chunks if all_chunks else None, persist_dir=persist_dir)
    
    llm = ChatOllama(model=model_name, temperature=0)
    
    template = """You are an expert research assistant. Answer the user's question accurately using ONLY the provided context blocks below.

    ### Instructions:
    1. Base your answer strictly on the facts present in the context. Do not extrapolate, assume, or bring in outside knowledge.
    2. Include an inline citation immediately following every factual statement or claim you make.
    3. Use the exact filename provided in the context header (e.g., [document.pdf]) for your citations.
    4. If the context does not contain the answer, state clearly that the information is not available in the provided documents.

    ### Context:
    {context}

    ### Question:
    {question}

    ### Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs_with_sources(retrieved_docs):
        formatted = []
        for doc in retrieved_docs:
            source = doc.metadata.get("source", "Unknown Source")
            # Clean path to just the filename if it's a full path
            source_name = Path(source).name
            formatted.append(f"[Source: {source_name}]\n{doc.page_content}")
        return "\n\n".join(formatted)
    
    # Use RunnableParallel to pass both the formatted text string to the prompt 
    # and retain the raw retrieved documents for reference if needed
    rag_chain = (
        {"context": db_retriever | format_docs_with_sources, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain