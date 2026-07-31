#pipeline.py
import os
from pathlib import Path
from parser import read_file
from splitter import split_text
from retriever import retriever

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate #Prompt container
from langchain_core.output_parsers import StrOutputParser #Final output in simple string
from langchain_core.runnables import RunnablePassthrough #Passes user raw input, and keeps it for later context

def rag_pipeline(file_path: str = "data", persist_dir: str = "./chroma_db", model_name: str = "deepseek-r1"):
    print(f"Processing pipeline for: {file_path}")
    
    #Check if the Chroma database already exists
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
    #Vector store retriever
    db_retriever = retriever(all_chunks if all_chunks else None, persist_dir=persist_dir)
    
    #LLM
    llm = ChatOllama(model=model_name, temperature = 0)
    
    #Cookie Cut Template
    template = """Answer the question based strictly on the following context:
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)
    
    rag_chain = (
        {"context": db_retriever | format_docs, "question" : RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
    
    